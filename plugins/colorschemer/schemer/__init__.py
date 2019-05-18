#!/usr/bin/python
#
# Gedit Scheme Editor
# https://github.com/jonocodes/GeditSchemer
#
# Copyright (C) Jono Finger 2013 <jono@foodnotblogs.com>
# 
# The program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# The program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
gi.require_version('Gedit', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gio, Gedit, Gtk
import os
from .schemer import GUI

try:
    import gettext
    gettext.bindtextdomain('gedit-plugins')
    gettext.textdomain('gedit-plugins')
    _ = gettext.gettext
except:
    _ = lambda s: s


class AppActivatable(GObject.Object, Gedit.AppActivatable):

  app = GObject.Property(type=Gedit.App)

  def __init__(self):
    GObject.Object.__init__(self)

  def do_activate(self):
    action = Gio.SimpleAction(name="schemer")
    action.connect('activate', self.open_dialog)
    self.app.add_action(action)

    self.menu_ext = self.extend_menu("preferences-section")
    item = Gio.MenuItem.new(_("Color Scheme Editor"), "app.schemer")
    self.menu_ext.append_menu_item(item)

  def do_deactivate(self):
    self.app.remove_action("schemer")
    self.menu_ext = None

  def open_dialog(self, action, parameter, data=None):
    GUI(Gedit.App, os.path.join(self.plugin_info.get_data_dir(), 'ui'))

