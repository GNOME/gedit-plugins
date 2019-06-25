# -*- coding: utf-8 -*-
# Copyright (c) 2007 - Steve Frécinaux <code@istique.net>
# Copyright (c) 2010 - Kenny Meyer <knny.myer@gmail.com>
# Licence: GPL2 or later

from gi.repository import GObject, Gtk, Gedit
import os.path
from gpdefs import GETTEXT_PACKAGE
from .store import Session


try:
    import gettext
    gettext.bindtextdomain('gedit-plugins')
    gettext.textdomain('gedit-plugins')
    _ = gettext.gettext
except:
    _ = lambda s: s

class SessionModel(Gtk.ListStore):
    OBJECT_COLUMN = 0
    NAME_COLUMN = 1
    N_COLUMNS = 2

    def __init__(self, store):
        super(SessionModel, self).__init__(GObject.TYPE_PYOBJECT, str)
        self.store = store
        for session in store:
            row = { self.OBJECT_COLUMN : session,
                    self.NAME_COLUMN: session.name }
            self.append(row.values())
        self.store.connect_after('session-added', self.on_session_added)
        self.store.connect('session-removed', self.on_session_removed)

    def on_session_added(self, store, session):
        row = { self.OBJECT_COLUMN : session,
                self.NAME_COLUMN: session.name }
        self.append(row.values())

    def on_session_removed(self, store, session):
        it = self.get_iter_first()
        if it is not None:
            while True:
                stored_session = self.get_value(it, self.OBJECT_COLUMN)
                if stored_session == session:
                    self.remove(it)
                    break
                it = self.iter_next(it)
                if not it:
                    break

class Dialog(object):
    UI_FILE = "sessionsaver.ui"

#    def __new__(cls):
#        if not ('_instance' in cls.__dict__) or cls._instance is None:
#            cls._instance = object.__new__(cls)
#        return cls._instance

    def __init__(self, main_widget, datadir, parent_window = None):
        super(Dialog, self).__init__()

        if parent_window is None:
            parent_window = Gedit.App.get_default().get_active_window()
        self.parent = parent_window

        self.ui = Gtk.Builder()
        self.ui.set_translation_domain(GETTEXT_PACKAGE)

        self.ui.add_from_file(os.path.join(datadir, 'ui', self.UI_FILE))
        self.dialog = self.ui.get_object(main_widget)
        self.dialog.connect('delete-event', self.on_delete_event)

    def __getitem__(self, item):
        return self.ui.get_object(item)

    def on_delete_event(self, dialog, event):
        dialog.hide()
        return True

    def __del__(self):
        self.__class__._instance = None

    def run(self):
        self.dialog.set_transient_for(self.parent)
        self.dialog.show()

    def destroy(self):
        self.dialog.destroy()
        self.__del__()

class SaveSessionDialog(Dialog):
    def __init__(self, window, plugin, sessions):
        super(SaveSessionDialog, self).__init__('save-session-dialog',
                                                plugin.plugin_info.get_data_dir(),
                                                window)
        self.plugin = plugin
        self.sessions = sessions
        self.sessionsaver = plugin

        model = SessionModel(sessions)

        combobox = self['session-name']
        combobox.set_model(model)
        combobox.set_entry_text_column(1)

        self.dialog.connect('response', self.on_response)

    def on_response(self, dialog, response_id):
        if response_id == Gtk.ResponseType.OK:
            files = [doc.get_location()
                        for doc in self.parent.get_documents()
                        if doc.get_location() is not None]
            name = self['session-name'].get_child().get_text()
            self.sessions.add(Session(name, files))
            self.sessions.save()
            self.sessionsaver.sessions = self.sessions
#            self.sessionsaver._update_session_menu()
        self.destroy()

class SessionManagerDialog(Dialog):
    def __init__(self, plugin, sessions):
        super(SessionManagerDialog, self).__init__('session-manager-dialog', plugin.plugin_info.get_data_dir())
        self.plugin = plugin
        self.sessions = sessions

        model = SessionModel(sessions)

        self.view = self['session-view']
        self.view.set_model(model)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(_("Session Name"), renderer, text = model.NAME_COLUMN)
        self.view.append_column(column)

        handlers = {
            'on_close_button_clicked': self.on_close_button_clicked,
            'on_open_button_clicked': self.on_open_button_clicked,
            'on_delete_button_clicked': self.on_delete_button_clicked
        }
        self.ui.connect_signals(handlers)

    def on_delete_event(self, dialog, event):
        dialog.hide()
        self.sessions.save()
        return True

    def get_current_session(self):
        (model, selected) = self.view.get_selection().get_selected()
        if selected is None:
            return None
        return model.get_value(selected, SessionModel.OBJECT_COLUMN)

    def on_open_button_clicked(self, button):
        session = self.get_current_session()
        if session is not None:
            self.plugin._load_session(session)

    def on_delete_button_clicked(self, button):
        session = self.get_current_session()
        self.sessions.remove(session)
#        self.plugin._update_session_menu()

    def on_close_button_clicked(self, button):
        self.sessions.save()
        self.destroy()

# ex:ts=4:et:
