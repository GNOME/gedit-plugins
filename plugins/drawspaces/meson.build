libdrawspaces_sources = files(
  'gedit-drawspaces-app-activatable.c',
  'gedit-drawspaces-view-activatable.c',
  'gedit-drawspaces-window-activatable.c',
)

libdrawspaces_deps = [
  gedit_dep,
]

libdrawspaces_c_args = [
  '-DHAVE_CONFIG_H',
]

libdrawspaces_res = gnome.compile_resources(
  'gedit-drawspaces-resources',
  'gedit-drawspaces.gresource.xml',
)

libdrawspaces_sources += [
  libdrawspaces_res.get(0),
]

libdrawspaces_sha = shared_module(
  'drawspaces',
  sources: libdrawspaces_sources,
  include_directories: rootdir,
  dependencies: libdrawspaces_deps,
  c_args: libdrawspaces_c_args,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

drawspaces_plugin_in = configure_file(
  input: 'drawspaces.plugin.desktop.in.in',
  output: 'drawspaces.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

custom_target(
  'drawspaces.plugin',
  input: drawspaces_plugin_in,
  output: 'drawspaces.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

install_data(
  'org.gnome.gedit.plugins.drawspaces.gschema.xml',
  install_dir: join_paths(
    glibdir,
    'schemas',
  )
)

if install_metainfo
  custom_target(
    'gedit-drawspaces.metainfo.xml',
    input: 'gedit-drawspaces.metainfo.xml.in',
    output: 'gedit-drawspaces.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif