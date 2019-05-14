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

import os
import sys
import collections
import tempfile
from xml.etree import ElementTree as ET

from gi.repository import Gtk, GdkPixbuf, Gdk, GtkSource, Gio, GLib, Pango

from .languages import samples

try:
    import gettext
    gettext.bindtextdomain('gedit-plugins')
    gettext.textdomain('gedit-plugins')
    _ = gettext.gettext
except:
    _ = lambda s: s


# Holds style properties for a GtkSourceStyle element
class Props:

  def __init__(self):
  
    self.background = None  # str
    self.foreground = None  # str
    self.italic = False
    self.bold = False
    self.strikethrough = False
    self.underline = False
    
  def is_clear(self):
    """ Return true if all the attributes are at the defaults/unset """
    
    return (self.foreground == None and 
        self.background == None and 
        self.bold == False and 
        self.italic == False and 
        self.underline == False and 
        self.strikethrough == False)
    
  def from_gtk_source_style(self, gtkStyle):
  
    self.background = gtkStyle.props.background
    self.foreground = gtkStyle.props.foreground
    self.italic = gtkStyle.props.italic
    self.bold = gtkStyle.props.bold
    self.underline = gtkStyle.props.pango_underline == Pango.Underline.NONE
    self.strikethrough = gtkStyle.props.strikethrough
    
    # here we make sure every color starts with a hash
    # maybe this is a workaround for a bug that I should file
    # or maybe this is a false assumption

    # if self.foreground and self.foreground[0] != '#':
    #   self.foreground = '#' + self.foreground
      
    # if self.background and self.background[0] != '#':
    #   self.background = '#' + self.background
    

class GUI:
  
  def __init__(self, geditApp, uiDir):

    # constants

    self.colorBlack = Gdk.color_parse('#000000');
    
    # we set this explicitly since the API does not give us a method for it
    self.guiStyleIds = ['bracket-match', 'bracket-mismatch',
      'current-line', 'cursor', 'line-numbers', 'secondary-cursor',
      'selection', 'selection-unfocused', 'text']

    # set up GUI widgets and signals
    
    GtkSource.View() # hack to get GtkSourceView widget to run from glade file

    self.builder = Gtk.Builder()

    uiFile = os.path.join(uiDir, 'schemer.ui')

    if (os.path.isfile(uiFile)):
      self.builder.add_from_file(uiFile)
    else:
      print('unable to find UI file')
      sys.exit(1)
    
    self.builder.connect_signals(self)
    
    self.window = self.builder.get_object('window')
    self.aboutDialog = self.builder.get_object('aboutdialog')
    
    self.sourceBuffer = GtkSource.Buffer(max_undo_levels=0)
    self.sourceView = self.builder.get_object('gtksourceviewSample')
    self.sourceView.set_buffer(self.sourceBuffer)
    
    self.liststoreStyles = self.builder.get_object('liststoreStyles')
    self.liststoreLanguages = self.builder.get_object('liststoreLanguages')
    self.comboboxLanguages = self.builder.get_object('comboboxLanguages')
    self.treeviewStyles = self.builder.get_object('treeviewStyles')
    
    self.colorbuttonForeground = self.builder.get_object('colorbuttonForeground')
    self.colorbuttonBackground = self.builder.get_object('colorbuttonBackground')
    self.togglebuttonItalic = self.builder.get_object('togglebuttonItalic')
    self.togglebuttonBold = self.builder.get_object('togglebuttonBold')
    self.togglebuttonUnderline = self.builder.get_object('togglebuttonUnderline')
    self.togglebuttonStrikethrough = self.builder.get_object('togglebuttonStrikethrough')
    self.checkbuttonForeground = self.builder.get_object('checkbuttonForeground')
    self.checkbuttonBackground = self.builder.get_object('checkbuttonBackground')
    self.resetButton = self.builder.get_object('resetButton')
    
    self.entryName = self.builder.get_object('entryName')
    self.entryAuthor = self.builder.get_object('entryAuthor')
    self.entryDescription = self.builder.get_object('entryDescription')
    self.entryId = self.builder.get_object('entryId')
    self.labelSample = self.builder.get_object('labelSample')
    
    self.colorbuttonBackground.connect('color-set', self.on_style_changed)
    self.colorbuttonForeground.connect('color-set', self.on_style_changed)

    self.builder.get_object('buttonCancel').connect('clicked', self.on_cancel_clicked)
    self.builder.get_object('buttonSave').connect('clicked', self.on_save_clicked)
    
    self.togglebuttonItalicHandler = self.togglebuttonItalic.connect(
      'toggled', self.on_style_changed)
    self.togglebuttonBoldHandler = self.togglebuttonBold.connect(
      'toggled', self.on_style_changed)
    self.togglebuttonUnderlineHandler = self.togglebuttonUnderline.connect(
      'toggled', self.on_style_changed)
    self.togglebuttonStrikethroughHandler = self.togglebuttonStrikethrough.connect(
      'toggled', self.on_style_changed)
    
    self.checkbuttonBackgroundHandler =  self.checkbuttonBackground.connect(
      'toggled', self.on_background_toggled)
    self.checkbuttonForegroundHandler = self.checkbuttonForeground.connect(
      'toggled', self.on_foreground_toggled)
    
    self.resetButton.connect('clicked', self.on_reset_clicked)
    
    self.schemeManager = GtkSource.StyleSchemeManager().get_default() # requires gedit 3.3.3 or newer
    self.languageManager = GtkSource.LanguageManager()

    self.dictAllStyles = collections.OrderedDict()
    
    languages = self.languageManager.get_language_ids()

    self.geditApp = geditApp
    self.geditView = geditApp.get_default().get_active_window().get_active_view()

    self.defaultLanguageId = 'c'
    self.defaultLanguageName = 'C'
    self.defaultLanguage = self.languageManager.get_language(self.defaultLanguageId)

    self.selectedLanguageId = self.defaultLanguageId
    self.selectedLanguageName = self.defaultLanguageName
    self.selectedLanguage = self.defaultLanguage

    self.bufferLanguageId = self.defaultLanguageId
    self.bufferLanguageName = self.defaultLanguageName
    self.bufferLanguage = self.defaultLanguage

    # guess the language from the current buffer
    if self.geditView:
      bufferLanguage = self.geditView.get_buffer().get_language()

      if bufferLanguage and bufferLanguage.get_id() in languages:
        self.bufferLanguageId = bufferLanguage.get_id()
        self.bufferLanguageName = bufferLanguage.get_name()
        self.bufferLanguage = bufferLanguage

    # watch temp directory to help the sample viewer
    self.schemeManagerOrigSearchPath = self.schemeManager.get_search_path()
    self.schemeManager.append_search_path(tempfile.gettempdir())

    self.origSchemeFile = None

    if self.geditView: # if there is a view open, get the scheme from the buffer
      self.load_scheme(self.geditView.get_buffer().get_style_scheme().get_filename())
    else: # is there is no view, check gsettings
      self.load_scheme(Gio.Settings('org.gnome.gedit.preferences.editor').get_string('scheme'))
    
    for langStyleId in self.guiStyleIds:
      self.liststoreStyles.append([langStyleId])
    
    self.langMapNameToId = {}
    
    # make a special case for Defaults which is moved to the top and includes GUI styles
    self.liststoreLanguages.append(['  Default styles'])
    self.langMapNameToId['  Default styles'] = 'def'
    
    langs = []
    
    for thisLanguage in languages:
      langName = self.languageManager.get_language(thisLanguage).get_name()
      self.langMapNameToId[langName] = thisLanguage
      
      if langName != 'Defaults':
        langs.append(langName)
        
    langs.sort(key=lambda y: y.lower())
    
    for langName in langs:
      self.liststoreLanguages.append([langName]);
        
    renderer_text = Gtk.CellRendererText()
    self.comboboxLanguages.pack_start(renderer_text, True)
    self.comboboxLanguages.connect('changed', self.on_language_selected)
    self.comboboxLanguages.add_attribute(renderer_text, 'text', 0)

    self.treeviewStylesSelection = self.treeviewStyles.get_selection()
    self.treeviewStylesSelection.connect('changed', self.on_style_selected)
    
    # select the first language
    self.comboboxLanguages.set_active(0)
    
    # select the first style
    treeIter = self.treeviewStyles.get_model().get_iter_first()
    self.treeviewStylesSelection.select_iter(treeIter)
    model = self.treeviewStyles.get_model()
    self.selectedStyleId = model[treeIter][0]
  
  def destroy(self, window):
    self.window.destroy()
    
  def on_cancel_clicked(self, param):
    self.schemeManager.set_search_path(self.schemeManagerOrigSearchPath)
    self.window.destroy()

  def on_save_clicked(self, param):

    inFile = self.origSchemeFile

    tempDirectory = tempfile.gettempdir()

    outFile = None

    # check to see if they choose a new ID or Name. Create a new file if they did.
    
    nameOrIdChange = False
    
    if (self.currentScheme.get_name() != self.entryName.get_text() or
        self.currentScheme.get_id()   != self.entryId.get_text()):
      # make sure the new name/id does not conflict with one that exists already
      
      schemeIds = self.schemeManager.get_scheme_ids()

      for thisSchemeId in schemeIds:
        if self.entryId.get_text() == thisSchemeId or self.entryName.get_text() == self.schemeManager.get_scheme(thisSchemeId).get_name():

          text = '<span weight="bold" size="larger">' + _('There was a problem saving the scheme') + '</span>\n\n'
          text += _('You have choosen to create a new scheme' \
            '\nbut the Name or ID you are using is being used already.' \
            '\n\nPlease be sure to choose a Name and ID that are not already in use.\n')
          message_dialog(Gtk.MessageType.ERROR, text, parent=self.window,
            buttons=Gtk.ButtonsType.NONE,
            additional_buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

          return

      nameOrIdChange = True

  
    # attempt to save to ~/.local/share/gedit/styles/
    stylesDir = os.path.join(GLib.get_user_data_dir(), "gedit", "styles")
      
    # if the file name or ID did not change, and they are using a local file, save it there
    if (not nameOrIdChange and
        os.access(inFile, os.W_OK) and
        os.path.dirname(inFile) == stylesDir and
        (str(os.path.dirname(inFile)) != tempDirectory)):

      outFile = inFile
      
    # else, designate a new file
    else:
      
      if not os.path.isdir(stylesDir):
        try:
          os.makedirs(stylesDir)
        except:
          pass

      if (os.access(stylesDir, os.W_OK)):
        outFile = os.path.join(stylesDir, self.entryId.get_text() + '.xml')


    if outFile:

      # make sure the name/ID to not refer to a system scheme that is not writable
      if inFile != outFile:

        schemeIds = self.schemeManager.get_scheme_ids()

        for thisSchemeId in schemeIds:
          if self.entryId.get_text() == thisSchemeId or self.entryName.get_text() == self.schemeManager.get_scheme(thisSchemeId).get_name():

            text = '<span weight="bold" size="larger">' + _('There was a problem saving the scheme') + '</span>\n\n'
            text += _('You do not have permission to overwrite the scheme you have choosen.' \
              '\nInstead a copy will be created.' \
              '\n\nPlease be sure to choose a Name and ID that are not already in use.\n')
            message_dialog(Gtk.MessageType.ERROR, text, parent=self.window,
              buttons=Gtk.ButtonsType.NONE,
              additional_buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

            return

      # write the file. complain if it fails to save
      if not self.write_scheme(outFile, self.entryId.get_text(), self.entryName.get_text()):
        message_dialog(Gtk.MessageType.ERROR, 'Error saving theme',
          parent=self.window, buttons=Gtk.ButtonsType.NONE,
          additional_buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
          
      else:
        self.schemeManager.force_rescan()
        updatedScheme = self.schemeManager.get_scheme(self.entryId.get_text())

        s = Gio.Settings('org.gnome.gedit.preferences.editor')
        s.set_string('scheme', self.entryId.get_text())

        # update the view in all open documents
        for thisDoc in self.geditApp.get_default().get_documents():
          thisDoc.set_style_scheme(updatedScheme)

    else:
      message_dialog(Gtk.MessageType.ERROR, 'Error saving theme',
        buttons=Gtk.ButtonsType.NONE, parent=self.window,
        additional_buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

    self.schemeManager.set_search_path(self.schemeManagerOrigSearchPath)
    self.window.destroy()

  def load_scheme(self, schemeIdOrFile):
    """ Load a scheme from a file or an existing scheme ID """

    if os.path.isfile(schemeIdOrFile):
      
      directory = os.path.dirname(schemeIdOrFile)
    
      if directory not in self.schemeManager.get_search_path():
        self.schemeManager.prepend_search_path(directory)
      
      fp = open(schemeIdOrFile, 'r')
      xmlTree = ET.parse(fp)
      fp.close()

      if xmlTree.getroot().tag == 'style-scheme':
        thisScheme = self.schemeManager.get_scheme(xmlTree.getroot().attrib['id'])
      
      if thisScheme == None:
        return False
        
      testFilename = thisScheme.get_filename()
      
      if testFilename != schemeIdOrFile:
        # there must have been some conflict, since it opened the wrong file

        text = '<span weight="bold" size="larger">' + _('There was a problem opening the file') + '</span>\n\n'
        text += _('You appear to have schemes with the same IDs in different directories\n')
        message_dialog(Gtk.MessageType.ERROR, text,
          parent=self.window, buttons=Gtk.ButtonsType.NONE,
          additional_buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        
        return False
        
      self.origSchemeFile = schemeIdOrFile

    else:

      thisScheme = self.schemeManager.get_scheme(schemeIdOrFile)
    
      if thisScheme == None:
        return False
    
    self.currentScheme = thisScheme
    
    self.entryName.set_text( thisScheme.get_name() )
    self.entryAuthor.set_text(', '.join(thisScheme.get_authors()))
    self.entryDescription.set_text(thisScheme.get_description())
    self.entryId.set_text(thisScheme.get_id())
    
    # get all the style elements
    # since there are no API calls to do this, we parse the XML file for now
    # also works around this https://bugzilla.gnome.org/show_bug.cgi?id=667194
    self.origSchemeFile = self.currentScheme.get_filename()
    
    fp = open(self.origSchemeFile, 'r')
    xmlTree = ET.parse(fp)
    fp.close()
    styleElements = xmlTree.findall('style')
    
    self.dictAllStyles.clear()
    for styleElement in styleElements:
      thisStyle = self.currentScheme.get_style(styleElement.attrib['name'])
      styleProps = Props()
      
      styleProps.from_gtk_source_style(thisStyle)
      
      self.dictAllStyles[styleElement.attrib['name']] = styleProps;
            
    self.sourceBuffer.set_style_scheme(self.currentScheme);
    
    # set up temp file so the sample view can be updated
    self.tempSchemeId = thisScheme.get_id() + '_temp'
    self.tempSchemeName = thisScheme.get_name() + '_temp'
    self.tempSchemeFile = tempfile.gettempdir() + '/' + self.tempSchemeId + '.xml'
    
    return True
    
  def clear_and_disable_style_buttons(self):

    self.colorbuttonForeground.set_color(self.colorBlack)
    self.colorbuttonBackground.set_color(self.colorBlack)
    self.colorbuttonForeground.set_sensitive(False)
    self.checkbuttonForeground.set_active(False)
    self.colorbuttonBackground.set_sensitive(False)
    self.checkbuttonBackground.set_active(False)
    
    self.togglebuttonItalic.set_active(False)
    self.togglebuttonBold.set_active(False)
    self.togglebuttonStrikethrough.set_active(False)
    self.togglebuttonUnderline.set_active(False)
    
    self.resetButton.set_sensitive(False)
    
  def update_sample_view(self):
    """
    Update the sample shown in the GUI.
    To do this we must write the scheme to disk and reload it from there.
    """
    
    # write it to disk
    self.write_scheme(self.tempSchemeFile, self.tempSchemeId, self.tempSchemeName)
    
    # and reload it from disk
    self.schemeManager.force_rescan()
    
    newScheme = self.schemeManager.get_scheme(self.tempSchemeId)
    self.sourceBuffer.set_style_scheme(newScheme);
    
  def write_scheme(self, location, schemeId, schemeName):
    """Write the scheme to disk
    
    location -- the file location to write to
    schemeId -- the ID of the scheme
    """

    output = '<style-scheme name="'+ schemeName + '" id="'+ schemeId +'" version="1.0">\n'
    
    output += '  <author>'+ self.entryAuthor.get_text() +'</author>\n'
    output += '  <description>'+ self.entryDescription.get_text() +'</description>\n\n'
    
    for k, v in list(self.dictAllStyles.items()):
      output += '  <style name="'+k+'"\t'
      
      if (v.foreground): output += 'foreground="'+ v.foreground +'" '
      if (v.background): output += 'background="'+ v.background +'" '
      if (v.italic): output += 'italic="true" '
      if (v.bold): output += 'bold="true" '
      if (v.underline):  output += 'underline="true" '
      if (v.strikethrough):  output += 'strikethrough="true" '
      
      output += '/>\n'
    
    output  += '</style-scheme>\n'
    
    try:
      fp = open(location, 'w')
      fp.write(output)
      fp.close()
    except:
      return False

    return True
    
  def on_reset_clicked(self, param):
    
    if self.selectedStyleId in self.dictAllStyles:
    
      del self.dictAllStyles[self.selectedStyleId]
    
      # reset the GUI
      self.clear_and_disable_style_buttons()
      
      self.update_sample_view()
      
  def on_background_toggled(self, param):
    
    # user is enabling color selection
    if param.get_active():
      self.colorbuttonBackground.set_sensitive(True)
      self.colorbuttonBackground.activate()
      
      self.resetButton.set_sensitive(True)
      
    # user is disabling color selection
    else:
      self.colorbuttonBackground.set_sensitive(False)
      
      try:
        self.dictAllStyles[self.selectedStyleId].background = None;
        
        self.clear_style_if_empty(self.selectedStyleId)
          
      except:
        pass

      self.update_sample_view()
      
  def on_foreground_toggled(self, param):
    
    # user is enabling color selection
    if param.get_active():
      self.colorbuttonForeground.set_sensitive(True)
      self.colorbuttonForeground.activate()

      self.resetButton.set_sensitive(True)
      
    # user is disabling color selection
    else:
      self.colorbuttonForeground.set_sensitive(False)
      
      try:
        self.dictAllStyles[self.selectedStyleId].foreground = None;
        self.clear_style_if_empty(self.selectedStyleId)
      except:
        pass
        
      self.update_sample_view()
  
  def clear_style_if_empty(self, styleId):
    """ Check to see if there are no attribtes set for a style. If so disable the
      "Clear" button and remove the style entry from the schema file.
    """
    
    if styleId not in self.dictAllStyles:
      return

    if (self.dictAllStyles[self.selectedStyleId].is_clear()):
      del self.dictAllStyles[self.selectedStyleId]
      self.clear_and_disable_style_buttons()
  
  
  def on_style_changed(self, data):
    """ Handles button clicks for foreground color, background color, 
      bold, italic, underline, or strikethrough.
    """
        
    if self.selectedStyleId not in self.dictAllStyles:
      self.dictAllStyles[self.selectedStyleId] = Props()
    
    cScale = 255.0/65535.0
    
    if data == self.colorbuttonBackground:
      color = data.get_color()
      self.dictAllStyles[self.selectedStyleId].background = ('#%02x%02x%02x' %
        (int(color.red * cScale), int(color.green * cScale), int(color.blue * cScale)))
    
    elif data == self.colorbuttonForeground:
      color = data.get_color()
      self.dictAllStyles[self.selectedStyleId].foreground = ('#%02x%02x%02x' %
        (int(color.red * cScale), int(color.green * cScale), int(color.blue * cScale)))
    
    elif data == self.togglebuttonBold:
      self.dictAllStyles[self.selectedStyleId].bold = data.get_active()
      
    elif data == self.togglebuttonItalic:
      self.dictAllStyles[self.selectedStyleId].italic = data.get_active()
    
    elif data == self.togglebuttonUnderline:
      self.dictAllStyles[self.selectedStyleId].underline = data.get_active()
    
    elif data == self.togglebuttonStrikethrough:
      self.dictAllStyles[self.selectedStyleId].strikethrough = data.get_active()
    
    # make sure the "Clear" button is enabled if something gets turned on
    try:
      if data.get_active() == True:
        self.resetButton.set_sensitive(True)
    except: pass
    
    self.clear_style_if_empty(self.selectedStyleId)
    
    self.update_sample_view()
    
  def on_style_selected(self, selection):
    model, treeiter = selection.get_selected()

    # handle the special case for when the styles get cleared since the signal activates
    if treeiter == None:
      return
    
    self.selectedStyleId = self.selectedLanguageId + ':' + model[treeiter][0]

    # handle the special case for GUI styles
    if self.selectedStyleId not in self.dictAllStyles and self.selectedLanguageId == 'def':
      self.selectedStyleId = model[treeiter][0]
    
    # block all the toggle handlers so they dont get triggered
    self.togglebuttonItalic.handler_block(self.togglebuttonItalicHandler)
    self.togglebuttonBold.handler_block(self.togglebuttonBoldHandler)
    self.togglebuttonUnderline.handler_block(self.togglebuttonUnderlineHandler)
    self.togglebuttonStrikethrough.handler_block(self.togglebuttonStrikethroughHandler)
    self.checkbuttonBackground.handler_block(self.checkbuttonBackgroundHandler)
    self.checkbuttonForeground.handler_block(self.checkbuttonForegroundHandler)
    
    if self.selectedStyleId in self.dictAllStyles:
      
      thisStyle = self.dictAllStyles[self.selectedStyleId]
      
      # handle foreground and background colors

      if thisStyle.foreground:
        self.colorbuttonForeground.set_color(Gdk.color_parse(thisStyle.foreground))
        self.colorbuttonForeground.set_sensitive(True)
        self.checkbuttonForeground.set_active(True)
      else:
        self.colorbuttonForeground.set_color(self.colorBlack)
        self.colorbuttonForeground.set_sensitive(False)
        self.checkbuttonForeground.set_active(False)

      if thisStyle.background:
        self.colorbuttonBackground.set_color(Gdk.color_parse(thisStyle.background))
        self.colorbuttonBackground.set_sensitive(True)
        self.checkbuttonBackground.set_active(True)
      else:
        self.colorbuttonBackground.set_color(self.colorBlack)
        self.colorbuttonBackground.set_sensitive(False)
        self.checkbuttonBackground.set_active(False)
        
      # handle text styling

      self.togglebuttonItalic.set_active(thisStyle.italic)
      self.togglebuttonBold.set_active(thisStyle.bold)
      self.togglebuttonStrikethrough.set_active(thisStyle.strikethrough)
      self.togglebuttonUnderline.set_active(thisStyle.underline)
      self.resetButton.set_sensitive(True)
      
    # if style does not exist, set to default GUI values
    else:
      self.clear_and_disable_style_buttons()
      
    # unblock toggle handlers so the user can do stuff
    self.togglebuttonItalic.handler_unblock(self.togglebuttonItalicHandler)
    self.togglebuttonBold.handler_unblock(self.togglebuttonBoldHandler)
    self.togglebuttonUnderline.handler_unblock(self.togglebuttonUnderlineHandler)
    self.togglebuttonStrikethrough.handler_unblock(self.togglebuttonStrikethroughHandler)
    self.checkbuttonBackground.handler_unblock(self.checkbuttonBackgroundHandler)
    self.checkbuttonForeground.handler_unblock(self.checkbuttonForegroundHandler)
  
  def on_language_selected(self, combo):

    tree_iter = combo.get_active_iter()
    if tree_iter != None:
      model = combo.get_model()
      self.selectedLanguageName = model[tree_iter][0]
      self.selectedLanguageId = self.langMapNameToId[self.selectedLanguageName]
      
      self.liststoreStyles.clear()
      
      # remove the language namespace thing from the style name
      removeLen = len(self.selectedLanguageId) + 1
      
      thisLanguage = self.languageManager.get_language(self.selectedLanguageId)
      
      if thisLanguage != None:
      
        styleIds = thisLanguage.get_style_ids() # TODO: why is 'gtk-doc.lang' throwing a warning?
        
        styleIds.sort() # make the styles list alphabetical
        
        if self.selectedLanguageId == 'def':
          for styleId in self.guiStyleIds:
            self.liststoreStyles.append([styleId])
        
        for styleId in styleIds:
          self.liststoreStyles.append([styleId[removeLen:]])
      
      # select the first style in the list
      treeIter = self.treeviewStyles.get_model().get_iter_first()
      
      if treeIter != None:  # make sure the list is not empty since some languages have no styles
        self.treeviewStylesSelection.select_iter(treeIter)
        model = self.treeviewStyles.get_model()
        self.selectedStyleId = model[treeIter][0]
      
      # update the sample view
      if self.selectedLanguageId in samples:
        self.sourceBuffer.set_language(thisLanguage);
        self.sourceBuffer.set_text(samples[self.selectedLanguageId])
        self.labelSample.set_text(self.selectedLanguageName + ' sample')
      elif self.bufferLanguageId in samples:
        self.sourceBuffer.set_language(self.bufferLanguage)
        self.sourceBuffer.set_text(samples[self.bufferLanguageId])
        self.labelSample.set_text(self.bufferLanguageName + ' sample')
      else:
        self.sourceBuffer.set_language(self.defaultLanguage);
        self.sourceBuffer.set_text(samples[self.defaultLanguageId])
        self.labelSample.set_text(self.defaultLanguageName + ' sample')



def message_dialog(dialog_type, shortMsg, longMsg=None, parent=None,
                  buttons=Gtk.ButtonsType.OK, additional_buttons=None):

  d = Gtk.MessageDialog(parent=parent, flags=Gtk.DialogFlags.MODAL,
    type=dialog_type, buttons=buttons)

  if additional_buttons:
    d.add_buttons(*additional_buttons)

  d.set_markup(shortMsg)

  if longMsg:
    if isinstance(longMsg, Gtk.Widget):
      widget = longMsg
    elif isinstance(longMsg, str):
      widget = Gtk.Label()
      widget.set_markup(longMsg)
    else:
      raise TypeError('"longMsg" must be a Gtk.Widget or a string')
    
    expander = Gtk.Expander(label = 'Click here for details')
    expander.set_border_width(6)
    expander.add(widget)
    d.vbox.pack_end(expander, True, True, 0)
      
  d.show_all()
  response = d.run()
  d.destroy()
  return response
 
