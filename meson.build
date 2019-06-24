project(
  'gedit-plugins', 'c',
  version: '3.32.2',
  meson_version: '>=0.49.0',
  license: 'GPL2'
)

gnome = import('gnome')
i18n = import('i18n')
pkg = import('pkgconfig')
python = import('python')

# Versioning
version = meson.project_version()
version_arr = version.split('.')
version_major = version_arr[0]
version_minor = version_arr[1]
version_micro = version_arr[2]

api_version = '3.14'

package_name = meson.project_name()
package_string = '@0@-@1@'.format(package_name, api_version)

# Paths
rootdir = include_directories('.')

srcdir = meson.current_source_dir()
builddir = meson.current_build_dir()

prefix = get_option('prefix')

bindir = join_paths(prefix, get_option('bindir'))
includedir = join_paths(prefix, get_option('includedir'))
libdir = join_paths(prefix, get_option('libdir'))
libexecdir = join_paths(prefix, get_option('libexecdir'))
datadir = join_paths(prefix, get_option('datadir'))

pkglibdir = join_paths(libdir, 'gedit')
pkgdatadir = join_paths(datadir, 'gedit')

appstreamdir = join_paths(datadir, 'metainfo')
dbusdir = join_paths(datadir, 'dbus-1')
glibdir = join_paths(datadir, 'glib-2.0')
localedir = join_paths(datadir, 'locale')

# Dependencies
libpeas_req = '>= 1.14.1'
gedit_req = '>= 3.16'
appstream_req = '>= 0.12.1'
zeitgeist_req = '>= 0.9.12'

libpeas_dep = dependency('libpeas-1.0', version: libpeas_req)
gedit_dep = dependency('gedit', version: gedit_req)

appstream_util = find_program('appstream-util', required: false)

# Configurations
config_h = configuration_data()
config_h.set_quoted('PACKAGE_NAME', package_name)
config_h.set_quoted('PACKAGE_STRING', package_string)
config_h.set_quoted('PACKAGE_VERSION', version)
config_h.set_quoted('GETTEXT_PACKAGE', package_name)
config_h.set_quoted('LOCALEDIR', localedir)
config_h.set_quoted('LIBDIR', libdir)
config_h.set_quoted('DATADIR', datadir)
config_h.set_quoted('VERSION', version)

config_h.set('GEDIT_MAJOR_VERSION', version_major)
config_h.set('GEDIT_MINOR_VERSION', version_minor)
config_h.set('GEDIT_MICRO_VERSION', version_micro)

configure_file(
  output: 'config.h',
  configuration: config_h
)

# Options
active_plugins = []
extra_languages = []
all_plugins = {
  'bookmarks': {'language': 'c'},
  'bracketcompletion': {'language': 'python'},
  'charmap': {'language': 'python'},
  'codecomment': {'language': 'python'},
  'colorpicker': {'language': 'python'},
  'colorschemer': {'language': 'python'},
  'commander': {'language': 'python'},
  'drawspaces': {'language': 'c'},
  'findinfiles': {'language': 'vala'},
  'git': {'language': 'python'},
  'joinlines': {'language': 'python'},
  'multiedit': {'language': 'python'},
  'sessionsaver': {'language': 'python'},
  'smartspaces': {'language': 'python'},
  'terminal': {'language': 'python'},
  'textsize': {'language': 'python'},
  'translate': {'language': 'python'},
  'wordcompletion': {'language': 'c'},
  'zeitgeist': {'language': 'c'},
}

foreach plugin_name, plugin_metadata : all_plugins
  if get_option('plugin_@0@'.format(plugin_name))
    active_plugins += plugin_name

    plugin_language = plugin_metadata.get('language')
    if plugin_language != 'c'
      extra_languages += plugin_language
    endif
  endif
endforeach

zeitgeist_needed = 'zeitgeist' in active_plugins
zeitgeist_dep = dependency('zeitgeist-2.0', version: zeitgeist_req, required: zeitgeist_needed)


if 'python' in extra_languages
  python3 = python.find_installation('python3')
endif

if 'vala' in extra_languages
  add_languages('vala', required: true)
  valac = meson.get_compiler('vala')
endif

install_metainfo = true

subdir('po')
subdir('plugins')
subdir('help')

summary = [
  '',
  '------',
  'gedit-plugins @0@ (@1@)'.format(version, api_version),
  '',
  '  AppData: @0@'.format(install_metainfo),
  '',
  'Plugins:']
foreach plugin_name : active_plugins
  summary += '  ' + plugin_name
endforeach
summary += [
  '',
  'Directories:',
  '   prefix: @0@'.format(prefix),
  '   libdir: @0@'.format(libdir),
  '  datadir: @0@'.format(datadir),
  '',
  '------',
]

meson.add_install_script(
  'build-aux/meson/post_install.py',
  libdir, datadir,
)

message('\n'.join(summary))
