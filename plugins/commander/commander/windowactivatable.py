# -*- coding: utf-8 -*-
#
#  windowhelper.py - commander
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

from gi.repository import GLib, GObject, Gio, Gtk, Gedit
from entry import Entry
from info import Info

class CommanderWindowActivatable(GObject.Object, Gedit.WindowActivatable):

    window = GObject.Property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        action = Gio.SimpleAction.new_stateful("commander", None, GLib.Variant.new_boolean(False))
        action.connect('activate', self.activate_toggle)
        action.connect('change-state', self.commander_mode)
        self.window.add_action(action)

    def do_deactivate(self):
        self.window.remove_action("commander")

    def do_update_state(self):
        action = self.window.lookup_action("commander")
        state = action.get_state()

        action.change_state(GLib.Variant.new_boolean(state.get_boolean()))

    def activate_toggle(self, action, parameter):
        view = self.window.get_active_view()
        state = action.get_state()

        action.change_state(GLib.Variant.new_boolean(not state.get_boolean()))

        if state.get_boolean() and view._entry:
            view._entry.grab_focus()
            return

    def commander_mode(self, action, state):
        view = self.window.get_active_view()

        if not view:
            return False

        if not hasattr(view, '_entry'):
            view._entry = None

        active = state.get_boolean()
        if active:
            if not view._entry:
                view._entry = Entry(view)
                view._entry.connect('destroy', self.on_entry_destroy, view)

            view._entry._show()
            view._entry.grab_focus()

        elif view._entry:
            view._entry._hide()

        action.set_state(GLib.Variant.new_boolean(active))

        return True

    def on_entry_destroy(self, widget, view):
        view._entry = None

# ex:ts=4:et
