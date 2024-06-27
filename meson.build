project(
  'gedit-plugins', 'c',
  version: '48.alpha',
  meson_version: '>= 0.57'
)

gnome = import('gnome')
i18n = import('i18n')
pkg = import('pkgconfig')
python = import('python')

# Paths

root_include_dir = include_directories('.')
srcdir = meson.current_source_dir()

pkglibdir = get_option('prefix') / get_option('libdir') / 'gedit'
pkgdatadir = get_option('prefix') / get_option('datadir') / 'gedit'
appstreamdir = get_option('prefix') / get_option('datadir') / 'metainfo'
glibdir = get_option('prefix') / get_option('datadir') / 'glib-2.0'

# Dependencies in common for all plugins

libpeas_dep = dependency('libpeas-1.0')
gedit_dep = dependency('gedit', version: '>= 48')

# Find programs

appstream_util = find_program('appstream-util', required: false)

# config.h

config_data = configuration_data()
config_data.set_quoted('GETTEXT_PACKAGE', meson.project_name())

configure_file(
  output: 'config.h',
  configuration: config_data,
)

# Enabled/disabled C/Python plugins

c_plugins = [
  'bookmarks',
  'drawspaces',
  'smartspaces',
  'wordcompletion',
]
python_plugins = [
  'bracketcompletion',
  'charmap',
  'codecomment',
  'colorpicker',
  'git',
  'joinlines',
  'multiedit',
  'sessionsaver',
  'terminal',
  'textsize',
]

enabled_c_plugins = []
disabled_c_plugins = []
enabled_python_plugins = []
disabled_python_plugins = []

foreach plugin_name : c_plugins
  if get_option('plugin_' + plugin_name)
    enabled_c_plugins += plugin_name
  else
    disabled_c_plugins += plugin_name
  endif
endforeach

foreach plugin_name : python_plugins
  if get_option('plugin_' + plugin_name)
    enabled_python_plugins += plugin_name
  else
    disabled_python_plugins += plugin_name
  endif
endforeach

# Enable Python 3

if enabled_python_plugins.length() > 0
  python3 = python.find_installation('python3')
endif

# Go to subdirs

subdir('po')
subdir('plugins')

if get_option('user_documentation')
  subdir('help')
endif

# Post-install

meson.add_install_script(
  'build-aux/meson/post_install.py',
  get_option('prefix') / get_option('libdir'),
  get_option('prefix') / get_option('datadir'),
)

gnome.post_install(
  glib_compile_schemas: true,
)

# Summary message

enabled_c_plugins_description = enabled_c_plugins.length() > 0 ? enabled_c_plugins : '(None)'
disabled_c_plugins_descripiton = disabled_c_plugins.length() > 0 ? disabled_c_plugins : '(None)'
enabled_python_plugins_description = enabled_python_plugins.length() > 0 ? enabled_python_plugins : '(None)'
disabled_python_plugins_description = disabled_python_plugins.length() > 0 ? disabled_python_plugins : '(None)'

summary('Prefix', get_option('prefix'))
summary('User documentation', get_option('user_documentation'))
summary('Enabled', enabled_c_plugins_description, section: 'C plugins')
summary('Disabled', disabled_c_plugins_descripiton, section: 'C plugins')
summary('Enabled', enabled_python_plugins_description, section: 'Python plugins')
summary('Disabled', disabled_python_plugins_description, section: 'Python plugins')
