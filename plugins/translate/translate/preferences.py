# -*- coding: utf-8 -*-
#
#  Copyrignt (C) 2017 Jordi Mas <jmas@softcatala.org>
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

import os
from gi.repository import Gio, Gtk
from gpdefs import GETTEXT_PACKAGE
from .services.services import Services
from .settings import Settings

try:
    import gettext
    gettext.bindtextdomain('gedit-plugins')
    gettext.textdomain('gedit-plugins')
    _ = gettext.gettext
except:
    _ = lambda s: s

class Preferences(object):

    LANG_NAME = 0
    LANG_CODE = 1

    def __init__(self, datadir, get_languages_names_codes):
        self._get_languages_names_codes = get_languages_names_codes
        self._settings = Settings()
        self._service_id = self._settings.get_service()

        self._load_ui(datadir)
        self._init_radiobuttons()
        self._init_combobox_languages()
        self._init_combobox_services()
        self._init_api_entry()

    def _load_ui(self, datadir):
        self._ui_path = os.path.join(datadir, 'ui', 'preferences.ui')
        self._ui = Gtk.Builder()
        self._ui.set_translation_domain(GETTEXT_PACKAGE)
        self._ui.add_from_file(self._ui_path)

    def _get_default_language(self):
        service = Services.get(self._service_id)
        selected = service.get_default_language_codes()
        return self._get_index(selected)

    def _populate_languages(self):
        self._languages.set_wrap_width(3)
        self._language_names, self._language_codes = self._get_languages_names_codes(self._service_id)
        self._model = self._get_languages_stored_model()
        self._languages.set_model(self._model)
        selected = self._settings.get_language_pair()
        index = self._get_index(selected)
        if index == -1:
            index = self._get_default_language()

        self._languages.set_active(index)

    def _init_api_entry(self):
        service = Services.get(self._service_id)
        if service.has_api_key() is True:
            self._update_api_key_ui(True)

    def _update_api_key_ui(self, show):
        apibox_container = self._ui.get_object('api_box_container')
        apibox = self._ui.get_object('api_box')

        if show is True:
            service = Services.get(self._service_id)
            self._apilabel = Gtk.Label(_("API Key"))
            self._apikey = Gtk.Entry(expand=True)
            self._apikey.connect('changed', self._changed_apikey)
            key = self._settings.get_apikey()
            self._apikey.set_text(key)

            apibox.add(self._apilabel)
            apibox.add(self._apikey)

            self._hint = Gtk.Label()
            self._hint.set_markup(service.get_api_hint())
            self._apilabel.set_margin_right(12)
            apibox_container.add(self._hint)
            apibox_container.show_all()
        else:
            apibox.remove(self._apilabel)
            apibox.remove(self._apikey)
            apibox_container.remove(self._hint)
            self._apilabel = None
            self._apikey = None
            self._hint = None

    def _init_radiobuttons(self):
        self._radio_samedoc = self._ui.get_object('same_document')
        self._output_window = self._ui.get_object('output_window')
        self._radio_samedoc.connect("toggled", self._radio_samedoc_callback)
        active = self._settings.get_output_document()

        if active:
            self._radio_samedoc.set_active(active)
        else:
            self._output_window.set_active(active is False)

    def _init_combobox_services(self):
        self._services = self._ui.get_object('services')

        cell = Gtk.CellRendererText()
        self._services.pack_start(cell, 1)
        self._services.add_attribute(cell, 'text', 0)
        services = Services.get_names_and_ids()

        model = Gtk.ListStore(str, int)
        for service_id in services.keys():
            model.append((services[service_id], service_id))

        self._services.set_model(model)
        service_id = self._settings.get_service()
        self._services.set_active(service_id)
        self._services.connect('changed', self._changed_services)

    def _init_combobox_languages(self):
        self._languages = self._ui.get_object('languages')

        cell = Gtk.CellRendererText()
        self._languages.pack_start(cell, 1)
        self._languages.add_attribute(cell, 'text', 0)
        self._populate_languages()
        self._languages.connect('changed', self._changed_lang_pair)

    def _get_languages_stored_model(self):
        sorted_language_names = set()

        for i in range(len(self._language_names)):
            sorted_language_names.add((self._language_names[i], self._language_codes[i]))

        sorted_language_names = sorted(sorted_language_names,
                                       key=lambda tup: tup[Preferences.LANG_NAME])

        model = Gtk.ListStore(str, str)
        for name_code in sorted_language_names:
            model.append(name_code)

        return model

    def _get_index(self, selected):
        for i in range(len(self._model)):
            if self._model[i][Preferences.LANG_CODE] == selected:
                return i
        return -1

    def _changed_lang_pair(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        if index > -1:
            item = model[index]
            self._settings.set_language_pair(item[Preferences.LANG_CODE])

    def _changed_services(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        if index == -1:
            return

        item = model[index]
        self._service_id = item[1]
        service = Services.get(self._service_id)
        if service.has_api_key() is True:
            key = self._settings.get_apikey()
            service.set_api_key(key)
        else:
            self._settings.set_service(self._service_id)

        service.init()
        self._update_api_key_ui(service.has_api_key())
        self._populate_languages()

    def _changed_apikey(self, text_entry):
        text = text_entry.get_text()
        self._settings.set_apikey(text)
        if len(text) > 0:
            self._settings.set_service(self._service_id)
        else:
            self._settings.set_service(Services.APERTIUM_ID)


    def _radio_samedoc_callback(self, widget, data=None):
        self._settings.set_output_document(widget.get_active())

    def configure_widget(self):
        self._ui.connect_signals(self)
        widget = self._ui.get_object('grid')
        return widget
