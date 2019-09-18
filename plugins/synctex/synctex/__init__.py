import gi
gi.require_version('Gedit', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Peas', '1.0')
gi.require_version('PeasGtk', '1.0')

from .synctex import SynctexAppActivatable, SynctexWindowActivatable
