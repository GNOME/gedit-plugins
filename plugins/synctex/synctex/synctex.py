# -*- coding: utf-8 -*-   

#  synctex.py - Synctex support with Gedit and Evince.
#  
#  Copyright (C) 2010 - José Aliste <jose.aliste@gmail.com>
#  Copyright (C) 2015 - Germán Poo-Caamaño <gpoo@gnome.org>
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

from gi.repository import GObject, Pango, Gtk, Gedit, Peas, PeasGtk, Gio, Gdk
from .evince_dbus import EvinceWindowProxy
import dbus.mainloop.glib
import logging
import os
import re

try:
    import gettext
    gettext.bindtextdomain('gedit-plugins')
    gettext.textdomain('gedit-plugins')
    _ = gettext.gettext
except:
    _ = lambda s: s

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

_logger = logging.getLogger("SynctexPlugin")

def apply_style (style, tag):
    def apply_style_prop(tag, style, prop):
        if style.get_property(prop + "-set"):
            tag.set_property(prop, style.get_property(prop))
        else:
            tag.set_property(prop, None)

    def apply_style_prop_bool(tag, style, prop, whentrue, whenfalse):
        if style.get_property(prop + "-set"):
            prop_value = whentrue if style.get_property(prop) else whenfalse
            tag.set_property(prop, prop_value)

    apply_style_prop(tag, style, "foreground")
    apply_style_prop(tag, style, "background")

    apply_style_prop_bool(tag, style, "bold", Pango.Weight.BOLD, Pango.Weight.NORMAL)
    apply_style_prop_bool(tag, style, "italic", Pango.Style.ITALIC, Pango.Style.NORMAL)
    apply_style_prop_bool(tag, style, "underline", Pango.Underline.SINGLE,
                          Pango.Underline.NONE)
    apply_style_prop(tag, style, "strikethrough")

def parse_modeline(text):
    gedit_r = re.search(r'%+\s*mainfile:\s*(.*)$', text,
                        re.IGNORECASE)
    auctex_r = re.search(r'%+\s*TeX-master:\s*"(.*)"$', text,
                         re.IGNORECASE)
    if gedit_r:
        return gedit_r.group(1)
    elif auctex_r:
        return auctex_r.group(1)
    else:
        return None


class SynctexViewHelper:
    def __init__(self, view, window, plugin):
        self._view = view
        self._window = window
        self._plugin = plugin
        self._doc = view.get_buffer()
        self.window_proxy = None

        self._handlers = [
            self._doc.connect('saved', self.on_saved_or_loaded),
            self._doc.connect('loaded', self.on_saved_or_loaded)
        ]

        self._highlight_tag = self._doc.create_tag()
        self.active = False
        self.last_iters = None
        self.gfile = None
        self.update_location()

    def on_notify_style_scheme(self, doc, param_object):
        apply_style (doc.get_style_scheme().get_style('search-match'), self._highlight_tag)

    def on_button_release(self, view, event):
        modifier_mask = Gtk.accelerator_get_default_mod_mask()
        event_state = event.state & modifier_mask

        if event.button == 1 and event_state == Gdk.ModifierType.CONTROL_MASK:
            self.sync_view(event.time)

    def on_saved_or_loaded(self, doc):
        self.update_location()

    def get_output_file(self):
        file_output = None
        line_count = self._doc.get_line_count()

        for i in list(range(min(3,line_count))) + list(range(max(0,line_count - 3), line_count)):
            start = self._doc.get_iter_at_line(i)
            end = start.copy()
            end.forward_to_line_end()
            file_output = parse_modeline(self._doc.get_text(start, end, False))
            if file_output is not None:
                break

        return file_output

    def on_key_press(self, a, b):
        self._unhighlight()

    def on_cursor_moved(self, cur):
        self._unhighlight()

    def deactivate(self):
        self._unhighlight()

        for h in self._handlers:
            self._doc.disconnect(h)

        del self._highlight_tag

    def update_location(self):
        gfile = self._doc.get_file().get_location()

        if gfile is None:
            return

        if self.gfile is None or gfile.get_uri() != self.gfile.get_uri():
            SynctexWindowActivatable.view_dict[gfile.get_uri()] = self
            self.gfile = gfile

        modeline_output_file = self.get_output_file()

        if modeline_output_file is not None:
            filename = modeline_output_file
        else:
            filename = self.gfile.get_basename()

        out_path = self.gfile.get_parent().get_child(filename).get_path()
        out_path = os.path.splitext(out_path)
        out_gfile = Gio.file_new_for_path(out_path[0] + ".pdf")

        if out_gfile.query_exists(None):
            self.out_gfile = out_gfile
        else:
            self.out_gfile = None

        self.update_active()

    def _highlight(self):
        iter = self._doc.get_iter_at_mark(self._doc.get_insert())
        end_iter = iter.copy()
        end_iter.forward_to_line_end()

        self._doc.apply_tag(self._highlight_tag, iter, end_iter)
        self.last_iters = [iter, end_iter];

    def _unhighlight(self):
        if self.last_iters is not None:
            self._doc.remove_tag(self._highlight_tag,
                                 self.last_iters[0], self.last_iters[1])
        self.last_iters = None

    def goto_line (self, line, time):
        self._doc.goto_line(line) 
        self._view.scroll_to_cursor()
        self._window.set_active_tab(Gedit.Tab.get_from_document(self._doc))
        self._highlight()
        self._window.present_with_time (time)

    def goto_line_after_load(self, line, time):
        GObject.idle_add (lambda : self.goto_line(line, time))
        self._doc.disconnect(self._goto_handler)

    def sync_view(self, time):
        if self.active:
            cursor_iter =  self._doc.get_iter_at_mark(self._doc.get_insert())
            line = cursor_iter.get_line() + 1
            col = cursor_iter.get_line_offset()
            self.window_proxy.SyncView(self.gfile.get_path(), (line, col), time)

    def update_active(self):
        # Activate the plugin only if the doc is a LaTeX file.
        lang = self._doc.get_language()
        self.active = (lang is not None and lang.get_id() == 'latex' and
                        self.out_gfile is not None)

        if self.active and self.window_proxy is None:
            self._doc_active_handlers = [
                        self._doc.connect('cursor-moved', self.on_cursor_moved),
                        self._doc.connect('notify::style-scheme', self.on_notify_style_scheme)]
            self._view_active_handlers = [
                        self._view.connect('key-press-event', self.on_key_press),
                        self._view.connect('button-release-event', self.on_button_release)]


            style = self._doc.get_style_scheme().get_style('search-match')
            apply_style(style, self._highlight_tag)
            self._window.lookup_action("synctex").set_enabled(True)
            self.window_proxy = self._plugin.ref_evince_proxy(self.out_gfile, self._window)

        elif not self.active and self.window_proxy is not None:
            #destroy the evince window proxy.
            for handler in self._doc_active_handlers:
                self._doc.disconnect(handler)
            for handler in self._view_active_handlers:
                self._view.disconnect(handler)

            self._window.lookup_action("synctex").set_enabled(False)
            self._plugin.unref_evince_proxy(self.out_gfile)
            self.window_proxy = None


class SynctexWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "SynctexWindowActivatable"

    window = GObject.Property(type=Gedit.Window)
    view_dict = {}
    _proxy_dict = {}

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        action = Gio.SimpleAction(name="synctex")
        action.connect('activate', self.forward_search_cb)
        self.window.add_action(action)

        for view in self.window.get_views():
            self.add_helper(view, self.window)

        self.handlers = [
            self.window.connect("tab-added", lambda window, tab: self.add_helper(tab.get_view(), window)),
            self.window.connect("tab-removed", lambda window, tab: self.remove_helper(tab.get_view())),
        ]

    def do_deactivate(self):
        for h in self.handlers:
            self.window.disconnect(h)

        for view in self.window.get_views():
            self.remove_helper(view)

        self.window.remove_action("synctex")

    def do_update_state(self):
        view_helper = self.get_helper(self.window.get_active_view())

        active = False
        if view_helper is not None:
            active = view_helper.active

        self.window.lookup_action("synctex").set_enabled(active)

    def add_helper(self, view, window):
        helper = SynctexViewHelper(view, window, self)
        location = view.get_buffer().get_file().get_location()

        if location is not None:
            self.view_dict[location.get_uri()] = helper
        view.synctex_view_helper = helper

    def remove_helper(self, view):
        helper = self.get_helper(view)

        if helper.gfile is not None:
            del self.view_dict[helper.gfile.get_uri()]

        helper.deactivate()
        del view.synctex_view_helper

    def get_helper(self, view):
        if not hasattr(view, 'synctex_view_helper'):
            return None
        return view.synctex_view_helper

    def forward_search_cb(self, action, parameter, user_data=None):
        self.get_helper(self.window.get_active_view()).sync_view(Gtk.get_current_event_time())

    def source_view_handler(self, out_gfile, uri_input, source_link, time):

        if uri_input not in self.view_dict:
            window = self._proxy_dict[out_gfile.get_uri()][2]

            tab = window.create_tab_from_location(Gio.file_new_for_uri(uri_input),
                                                  None, source_link[0] - 1, 0, False, True)

            helper = self.get_helper(tab.get_view())
            helper._goto_handler = tab.get_document().connect_object("loaded", 
                                                SynctexViewHelper.goto_line_after_load,
                                                helper, source_link[0] - 1, time)
        else:
            self.view_dict[uri_input].goto_line(source_link[0] - 1, time)

    def ref_evince_proxy(self, gfile, window):
        uri = gfile.get_uri()
        proxy = None

        if uri not in self._proxy_dict:
            proxy = EvinceWindowProxy (uri, True, _logger)
            self._proxy_dict[uri] = [1, proxy, window]
            proxy.set_source_handler (lambda i, s, time: self.source_view_handler(gfile, i, s, time))
        else:
            self._proxy_dict[uri][0]+=1
            proxy = self._proxy_dict[uri][1]

        return proxy

    def unref_evince_proxy(self, gfile):
        uri = gfile.get_uri()

        if uri in self._proxy_dict:
            self._proxy_dict[uri][0] -= 1
            if self._proxy_dict[uri][0] == 0:
                del self._proxy_dict[uri]

class SynctexAppActivatable(GObject.Object, Gedit.AppActivatable):

    app = GObject.Property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.app.add_accelerator("<Primary><Alt>F", "win.synctex", None)

        self.menu_ext = self.extend_menu("tools-section")
        item = Gio.MenuItem.new(_("Forward Search"), "win.synctex")
        self.menu_ext.append_menu_item(item)

    def do_deactivate(self):
        self.app.remove_accelerator("win.synctex", None)
        self.menu_ext = None

# ex:ts=4:et:
