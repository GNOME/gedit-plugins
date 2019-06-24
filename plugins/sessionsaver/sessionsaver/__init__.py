# -*- coding: utf-8 -*-
#
#  Copyrignt (C) 2019 Jordi Mas <jmas@softcatala.org>
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

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
gi.require_version('PeasGtk', '1.0')

from gi.repository import GObject, Gio, Gtk, Gedit, PeasGtk
from .dialogs import SaveSessionDialog, SessionManagerDialog
from .store import XMLSessionStore

try:
    import gettext
    gettext.bindtextdomain('gedit-plugins')
    gettext.textdomain('gedit-plugins')
    _ = gettext.gettext
except:
    _ = lambda s: s

class SessionSaverAppActivatable(GObject.Object, Gedit.AppActivatable):

    app = GObject.Property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)
        print("SessionSaverAppActivatable.__init__\n")

    def do_activate(self):
        self.menu_ext = self.extend_menu("tools-section")
        item = Gio.MenuItem.new(_("_Manage saved sessions..."), "win.managedsession")
        self.menu_ext.prepend_menu_item(item)

        item = Gio.MenuItem.new(_("_Save session..."), "win.savesession")
        self.menu_ext.prepend_menu_item(item)
        self._insert_session_menu()


    def do_deactivate(self):
        self.menu_ext = None


    def _insert_session_menu(self):
        print("_insert_session_menu\n")

        self.sessions = XMLSessionStore()
        for i, session in enumerate(self.sessions):
            action_name = 'SessionSaver%X' % i
            session_id = 'win.session_%u'.format(i)
            item = Gio.MenuItem.new(_("Recover '%s' session") % session.name, session_id)
            self.menu_ext.prepend_menu_item(item)
    
       
class SessionSaverWindowActivatable(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):

    __gtype_name__ = "SessionSaverWindowActivatable"
    window = GObject.Property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        print("SessionSaverWindowActivatable.__init__\n")
        self.sessions = XMLSessionStore()

    def do_activate(self):
        action = Gio.SimpleAction(name="managedsession")
        action.connect('activate', lambda a, p: self.on_manage_sessions_action())
        self.window.add_action(action)

        action = Gio.SimpleAction(name="savesession")
        action.connect('activate', lambda a, p: self.on_save_session_action())
        self.window.add_action(action)

        self.sessions = XMLSessionStore()
        for i, session in enumerate(self.sessions):
            action_name = 'SessionSaver%X' % i
            session_id = 'session_%u'.format(i)
            action = Gio.SimpleAction(name=session_id)
            action.connect('activate', self.capture_menu_action, self.window)
            self.window.add_action(action)

    def capture_menu_action(self, action, parameter, window):
        print("capture_menu_action\n")
        return


    def do_deactivate(self):
        return

    def do_update_state(self):
        return

    def on_manage_sessions_action(self):
        print("on_manage_sessions_action\n")
        dialog = SessionManagerDialog(self, self.sessions)
        dialog.run()

    def on_save_session_action(self):
        print("on_save_session_action\n")
        dialog = SaveSessionDialog(self.window, self, self.sessions)
        dialog.run()

