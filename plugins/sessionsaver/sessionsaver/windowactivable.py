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
from gi.repository import GObject, Gio, Gedit
from .dialogs import SaveSessionDialog, SessionManagerDialog
from .store import XMLSessionStore
from .appactivable import SessionSaverAppActivatable

gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
gi.require_version('PeasGtk', '1.0')


try:
    import gettext
    gettext.bindtextdomain('gedit-plugins')
    gettext.textdomain('gedit-plugins')
    _ = gettext.gettext
except:
    _ = lambda s: s


class SessionSaverWindowActivatable(GObject.Object, Gedit.WindowActivatable):

    __gtype_name__ = "SessionSaverWindowActivatable"
    window = GObject.Property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        print("SessionSaverWindowActivatable.__init__\n")
        self.sessions = XMLSessionStore()
        self.n_sessions = 0

    def do_activate(self):
        self._insert_menus()

    def _insert_menus(self):
        print("SessionSaverWindowActivatable._insert_menus")
        action = Gio.SimpleAction(name="managedsession")
        action.connect('activate', lambda a, p: self._on_manage_sessions_action())
        self.window.add_action(action)

        action = Gio.SimpleAction(name="savesession")
        action.connect('activate', lambda a, p: self._on_save_session_action())
        self.window.add_action(action)

        self.sessions = XMLSessionStore()
        self.n_sessions = len(self.sessions)
        for i, session in enumerate(self.sessions):
            session_id = 'session_{0}'.format(i)
            action = Gio.SimpleAction(name=session_id)
            action.connect('activate', self._session_menu_action, session)
            self.window.add_action(action)

    def _remove_menus(self):
        print("SessionSaverWindowActivatable._remove_menus")
        self.window.remove_action("managedsession")
        self.window.remove_action("savesession")

        for i in range(self.n_sessions):
            session_id = 'session_{0}'.format(i)
            print("SessionSaverWindowActivatable._remove_session_menu. remove {0}".format(session_id))
            self.window.remove_action(session_id)

    def _session_menu_action(self, action, parameter, session):
        print("SessionSaverWindowActivatable._session_menu_action {0}".format(session.name))
        self._load_session(session)

    def do_deactivate(self):
        self._remove_menus()
        return

    def do_update_state(self):
        return

    def _on_manage_sessions_action(self):
        print("on_manage_sessions_action\n")
        data_dir = SessionSaverAppActivatable.get_instance().plugin_info.get_data_dir()
        dialog = SessionManagerDialog(self.window, self.on_updated_sessions, self.load_session, self.sessions, data_dir)
        dialog.run()

    def _on_save_session_action(self):
        print("on_save_session_action\n")
        data_dir = SessionSaverAppActivatable.get_instance().plugin_info.get_data_dir()
        dialog = SaveSessionDialog(self.window, self.on_updated_sessions, self.sessions, data_dir)
        dialog.run()

    def on_updated_sessions(self):
        print("on_updated_sessions")
        SessionSaverAppActivatable.get_instance().update_session_menu()
        self._insert_menus()

    def load_session(self, session):
        # Note: a session has to stand on its own window.
        tab = self.window.get_active_tab()
        if tab is not None and \
           not (tab.get_document().is_untouched() and
                tab.get_state() == Gedit.TabState.STATE_NORMAL):
            # Create a new gedit window
            window = Gedit.App.get_default().create_window(None)
            window.show()
        else:
            window = self.window

        Gedit.commands_load_locations(window, session.files, None, 0, 0)
