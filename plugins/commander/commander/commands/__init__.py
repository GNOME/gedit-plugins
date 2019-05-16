# -*- coding: utf-8 -*-
#
#  __init__.py - commander
#
#  Copyright (C) 2010 - Jesse van den Kieboom
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301, USA.

from gi.repository import GLib, GObject, Gio

import sys, bisect, types, shlex, re, os, traceback

from . import module, method, result, exceptions, metamodule, completion

from commands.accel_group import AccelGroup
from commands.accel_group import Accelerator

__all__ = ['is_commander_module', 'Commands', 'Accelerator']

import commander.modules

def attrs(**kwargs):
    def generator(f):
        for k in kwargs:
            setattr(f, k, kwargs[k])

        return f

    return generator

def autocomplete(d={}, **kwargs):
    ret = {}

    for dic in (d, kwargs):
        for k in dic:
            if type(dic[k]) == types.FunctionType:
                ret[k] = dic[k]

    return attrs(autocomplete=ret)

def accelerator(*args, **kwargs):
    return attrs(accelerator=Accelerator(args, kwargs))

def is_commander_module(mod):
    if type(mod) == types.ModuleType:
        return mod and ('__commander_module__' in mod.__dict__)
    else:
        mod = str(mod)
        return mod.endswith('.py') or (os.path.isdir(mod) and os.path.isfile(os.path.join(mod, '__init__.py')))

class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
            cls._instance.__init_once__()

        return cls._instance

class Commands(Singleton):
    class Continuated:
        def __init__(self, generator):
            self.generator = generator
            self.retval = None

        def autocomplete_func(self):
            mod = sys.modules['commander.commands.result']

            if self.retval == mod.Result.PROMPT:
                return self.retval.autocomplete
            else:
                return {}

        def args(self):
            return [], True

    class State:
        def __init__(self):
            self.clear()

        def clear(self):
            self.stack = []

        def top(self):
            return self.stack[0]

        def run(self, ret):
            ct = self.top()

            if ret:
                ct.retval = ct.generator.send(ret)
            else:
                ct.retval = next(ct.generator)

            return ct.retval

        def push(self, gen):
            self.stack.insert(0, Commands.Continuated(gen))

        def pop(self):
            if not self.stack:
                return

            try:
                self.stack[0].generator.close()
            except GeneratorExit:
                pass

            del self.stack[0]

        def __len__(self):
            return len(self.stack)

        def __nonzero__(self):
            return len(self) != 0

    def __init_once__(self):
        self._modules = None
        self._dirs = []
        self._monitors = []
        self._accel_group = None

        self._timeouts = {}

        self._stack = []

    def set_dirs(self, dirs):
        self._dirs = dirs

    def stop(self):
        for mon in self._monitors:
            mon.cancel()

        self._monitors = []
        self._modules = None

        for k in self._timeouts:
            GLib.source_remove(self._timeouts[k])

        self._timeouts = {}

    def accelerator_activated(self, accel, mod, state, entry):
        self.run(state, mod.execute('', [], entry, 0, accel.arguments))

    def scan_accelerators(self, modules=None):
        if modules == None:
            self._accel_group = AccelGroup()
            modules = self.modules()

        recurse_mods = []

        for mod in modules:
            if type(mod) == types.ModuleType:
                recurse_mods.append(mod)
            else:
                accel = mod.accelerator()

                if accel != None:
                    self._accel_group.add(accel, self.accelerator_activated, mod)

        for mod in recurse_mods:
            self.scan_accelerators(mod.commands())

    def accelerator_group(self):
        if not self._accel_group:
            self.scan_accelerators()

        return self._accel_group

    def modules(self):
        self.ensure()
        return list(self._modules)

    def add_monitor(self, d):
        gfile = Gio.file_new_for_path(d)
        monitor = None

        try:
            monitor = gfile.monitor_directory(Gio.FileMonitorFlags.NONE, None)
        except Exception as e:
            # Could not create monitor, this happens on systems where file monitoring is
            # not supported, but we don't really care
            pass

        if monitor:
            monitor.connect('changed', self.on_monitor_changed)
            self._monitors.append(monitor)

    def scan(self, d):
        files = []

        try:
            files = os.listdir(d)
        except OSError:
            pass

        for f in files:
            full = os.path.join(d, f)

            # Test for python files or modules
            if is_commander_module(full):
                if self.add_module(full) and os.path.isdir(full):
                    # Add monitor on the module directory if module was
                    # successfully added. TODO: recursively add monitors
                    self.add_monitor(full)

        # Add a monitor on the scanned directory itself
        self.add_monitor(d)

    def module_name(self, filename):
        # Module name is the basename without the .py
        return os.path.basename(os.path.splitext(filename)[0])

    def add_module(self, filename):
        base = self.module_name(filename)

        # Check if module already exists
        if base in self._modules:
            return

        # Create new 'empty' module
        mod = module.Module(base, os.path.dirname(filename))
        bisect.insort_right(self._modules, mod)

        # Reload the module
        self.reload_module(mod)
        return True

    def ensure(self):
        # Ensure that modules have been scanned
        if self._modules != None:
            return

        self._modules = []

        for d in self._dirs:
            self.scan(d)

    def _run_generator(self, state, ret=None):
        mod = sys.modules['commander.commands.result']

        try:
            # Determine first use
            retval = state.run(ret)

            if not retval or (isinstance(retval, mod.Result) and (retval == mod.DONE or retval == mod.HIDE)):
                state.pop()

                if state:
                    return self._run_generator(state)

            return self.run(state, retval)

        except StopIteration:
            state.pop()

            if state:
                return self.run(state)
        except Exception as e:
            # Something error like, we throw on the parent generator
            state.pop()

            if state:
                state.top().generator.throw(type(e), e, e.__traceback__)
            else:
                # Re raise it for the top most to show the error
                raise

        return None

    def run(self, state, ret=None):
        mod = sys.modules['commander.commands.result']

        if type(ret) == types.GeneratorType:
            # Ok, this is cool stuff, generators can ask and susped execution
            # of commands, for instance to prompt for some more information
            state.push(ret)

            return self._run_generator(state)
        elif not isinstance(ret, mod.Result) and len(state) > 1:
            # Basicly, send it to the previous?
            state.pop()

            return self._run_generator(state, ret)
        else:
            return ret

    def execute(self, state, argstr, words, wordsstr, entry, modifier):
        self.ensure()

        if state:
            return self._run_generator(state, [argstr, words, modifier])

        cmd = completion.single_command(wordsstr, 0)

        if not cmd:
            raise exceptions.Execute('Could not find command: ' + wordsstr[0])

        if len(words) > 1:
            argstr = argstr[words[1].start(0):]
        else:
            argstr = ''

        # Execute command
        return self.run(state, cmd.execute(argstr, wordsstr[1:], entry, modifier))

    def invoke(self, entry, modifier, command, args, argstr=None):
        self.ensure()

        cmd = completion.single_command([command], 0)

        if not cmd:
            raise exceptions.Execute('Could not find command: ' + command)

        if argstr == None:
            argstr = ' '.join(args)

        ret = cmd.execute(argstr, args, entry, modifier)

        if type(ret) == types.GeneratorType:
            raise exceptions.Execute('Cannot invoke commands that yield (yet)')
        else:
            return ret

    def resolve_module(self, path, load=True):
        if not self._modules or not is_commander_module(path):
            return None

        # Strip off __init__.py for module kind of modules
        if path.endswith('__init__.py'):
            path = os.path.dirname(path)

        base = self.module_name(path)

        # Find module
        idx = bisect.bisect_left(self._modules, base)
        mod = None

        if idx < len(self._modules):
            mod = self._modules[idx]

        if not mod or mod.name != base:
            if load:
                self.add_module(path)

            return None

        return mod

    def remove_module_accelerators(self, modules):
        recurse_mods = []

        for mod in modules:
            if type(mod) == types.ModuleType:
                recurse_mods.append(mod)
            else:
                accel = mod.accelerator()

                if accel != None:
                    self._accel_group.remove(accel)

        for mod in recurse_mods:
            self.remove_module_accelerators(mod.commands())

    def remove_module(self, mod):
        # Remove roots
        for r in mod.roots():
            if r in self._modules:
                self._modules.remove(r)

        # Remove accelerators
        if self._accel_group:
            self.remove_module_accelerators([mod])

        if mod.name in commander.modules.__dict__:
            del commander.modules.__dict__[mod.name]

    def reload_module(self, mod):
        if isinstance(mod, str):
            mod = self.resolve_module(mod)

        if not mod or not self._modules:
            return

        # Remove roots
        self.remove_module(mod)

        # Now, try to reload the module
        try:
            mod.reload()
        except Exception as e:
            # Reload failed, we remove the module
            info = traceback.format_tb(sys.exc_info()[2])
            print('Failed to reload module ({0}):\n  {1}'.format(mod.name, info[-1]))

            self._modules.remove(mod)
            return

        # Insert roots
        for r in mod.roots():
            bisect.insort(self._modules, r)

        commander.modules.__dict__[mod.name] = metamodule.MetaModule(mod.mod)

        if self._accel_group:
            self.scan_accelerators([mod])

    def on_timeout_delete(self, path, mod):
        if not path in self._timeouts:
            return False

        # Remove the module
        mod.unload()
        self.remove_module(mod)
        self._modules.remove(mod)

        return False

    def on_monitor_changed(self, monitor, gfile1, gfile2, evnt):
        if evnt == Gio.FileMonitorEvent.CHANGED:
            # Reload the module
            self.reload_module(gfile1.get_path())
        elif evnt == Gio.FileMonitorEvent.DELETED:
            path = gfile1.get_path()
            mod = self.resolve_module(path, False)

            if not mod:
                return

            if path in self._timeouts:
                GLib.source_remove(self._timeouts[path])

            # We add a timeout because a common save strategy causes a
            # DELETE/CREATE event chain
            self._timeouts[path] = GLib.timeout_add(500, self.on_timeout_delete, path, mod)
        elif evnt == Gio.FileMonitorEvent.CREATED:
            path = gfile1.get_path()

            # Check if this CREATE followed a previous DELETE
            if path in self._timeouts:
                GLib.source_remove(self._timeouts[path])
                del self._timeouts[path]

            # Reload the module
            self.reload_module(path)

# ex:ts=4:et
