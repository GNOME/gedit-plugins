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

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
gi.require_version('PeasGtk', '1.0')

from gi.repository import GObject, Gio, Gtk, Gedit, PeasGtk
from .apertium import Apertium
from .translateview import TranslateView
from .preferences import Preferences
import gettext
from gpdefs import *

try:
    gettext.bindtextdomain(GETTEXT_PACKAGE, GP_LOCALEDIR)
    _ = lambda s: gettext.dgettext(GETTEXT_PACKAGE, s);
except:
    _ = lambda s: s

class TranslateAppActivatable(GObject.Object, Gedit.AppActivatable):

    app = GObject.Property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.app.add_accelerator("<Primary>M", "win.translate", None)
       
    def do_deactivate(self):
        self.app.remove_accelerator("win.translate", None)
       
class TranslateWindowActivatable(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):

    __gtype_name__ = "TranslateWindowActivatable"
    window = GObject.Property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        action = Gio.SimpleAction(name="translate")
        action.connect('activate', lambda a, p: self.do_translate())
        self.window.add_action(action)

        global g_console
        g_console = TranslateView(namespace = {'__builtins__' : __builtins__,
                                                   'gedit' : Gedit,
                                                   'window' : self.window})
        g_console.write(_('Welcome!'))
        bottom = self.window.get_bottom_panel()
        g_console.show_all()
        bottom.add_titled(g_console, "GeditTranslateConsolePanel", _('Translate Console'))
     
    def do_deactivate(self):
        self.window.remove_action("translate")

    def do_update_state(self):
        sensitive = False
        view = self.window.get_active_view()
        if view and hasattr(view, "translate_view_activatable"):
            sensitive = True

        self.window.lookup_action('translate').set_enabled(sensitive)

    def do_create_configure_widget(self):
        print("called do_create_configure_widget")
        apertium = Apertium()
        config_widget = Preferences(self.plugin_info.get_data_dir(),
                                    apertium.get_language_names(),
                                    apertium.get_language_codes())
        widget = config_widget.configure_widget()
        print("called do_create_configure_widget return:" + str(type(widget)))
        return widget
       
    '''Entry point when user uses keyboard shortcut'''
    def do_translate(self, unindent=False):
        view = self.window.get_active_view()
        if view and view.translate_view_activatable:
            view.translate_view_activatable.do_translate(view.get_buffer(), unindent)

    
class TranslateViewActivatable(GObject.Object, Gedit.ViewActivatable):

    TRANSLATE_KEY_BASE = 'org.gnome.gedit.plugins.translate'
    OUTPUT_TO_DOCUMENT = 'output-to-document'
    LANGUAGE_PAIR = 'language-pair'

    view = GObject.Property(type=Gedit.View)

    def __init__(self):
        GObject.Object.__init__(self)
        self._settings = Gio.Settings.new(self.TRANSLATE_KEY_BASE)

    def do_activate(self):
        self.view.translate_view_activatable = self
        self.view.connect('populate-popup', self.populate_popup)

    def do_deactivate(self):
        delattr(self.view, "translate_view_activatable")

    def _get_language_pair_name(self):
        language_pair = self._settings.get_string(self.LANGUAGE_PAIR)
        languages = language_pair.split('|')

        apertium = Apertium()
        return apertium.get_language_pair_name(languages[0], languages[1])

    def populate_popup(self, view, popup):
        if not isinstance(popup, Gtk.MenuShell):
            return

        item = Gtk.SeparatorMenuItem()
        item.show()
        popup.append(item)

        language_pair_name = self._get_language_pair_name()
        text = _("Translate selected text [{0}]").format(language_pair_name)

        item = Gtk.MenuItem.new_with_mnemonic(text)
        item.set_sensitive(self.is_enabled())
        item.show()
        item.connect('activate', lambda i: self.do_translate(view.get_buffer()))
        popup.append(item)
  
    def is_enabled(self):
        document = self.view.get_buffer()
        if document is None:
            return False

        start = None
        end = None

        try:
            start, end = document.get_selection_bounds()

        except:
            pass

        return start is not None and end is not None

    def translate_text(self, document, start, end):
        doc = self.view.get_buffer()
        text = doc.get_text(start, end, False)
        language_pair = self._settings.get_string(self.LANGUAGE_PAIR)
      
        apertium = Apertium()
        translated = apertium.translate_text(text, language_pair)

        if self._settings.get_boolean(self.OUTPUT_TO_DOCUMENT):
            doc.insert(start, translated)
        else:
            g_console.write(translated)

    def do_translate(self, document, unindent=False):
        start, end = document.get_selection_bounds()
        self.translate_text(document, start, end)


