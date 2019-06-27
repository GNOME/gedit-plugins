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
        self.n_sessions = 0

        global app_activable
        app_activable = self
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
        n_sessions = len(self.sessions)
        for i, session in enumerate(self.sessions):
            session_id = 'win.session_%u'.format(i)
            item = Gio.MenuItem.new(_("Recover '%s' session") % session.name, session_id)
            self.menu_ext.prepend_menu_item(item)

    def _remove_session_menu(self):
        self.menu_ext.remove_items()
        for i in range(self.n_sessions):
            session_id = 'win.session_%u'.format(i)
            print("_remove_session_menu. remove %s".format(session_id))
            self.app.remove_accelerator(session_id, None)

    def _update_session_menu(self):
        self._remove_session_menu()
        self._insert_session_menu()
    
       
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
            session_id = 'session_%u'.format(i)
            action = Gio.SimpleAction(name=session_id)
            action.connect('activate', self.session_menu_action, session)
            self.window.add_action(action)

    def session_menu_action(self, action, parameter, session):
        print("session_menu_action")
        self._load_session(session)

    def do_deactivate(self):
        return

    def do_update_state(self):
        return

    def on_manage_sessions_action(self):
        print("on_manage_sessions_action\n")
        dialog = SessionManagerDialog(app_activable, self.sessions)
        dialog.run()

    def on_save_session_action(self):
        print("on_save_session_action\n")
        dialog = SaveSessionDialog(self.window, app_activable, self.sessions)
        dialog.run()

    def _load_session(self, session):
        # Note: a session has to stand on its own window.
        tab = self.window.get_active_tab()
        if tab is not None and \
           not (tab.get_document().is_untouched() and \
                tab.get_state() == Gedit.TabState.STATE_NORMAL):
            # Create a new gedit window
            window = Gedit.App.get_default().create_window(None)
            window.show()
        else:
            window = self.window

        Gedit.commands_load_locations(window, session.files, None, 0, 0)


