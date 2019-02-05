smartspaces_sources = files(
  'smartspaces.py',
)

install_data(
  smartspaces_sources,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

smartspaces_plugin_in = configure_file(
  input: 'smartspaces.plugin.desktop.in.in',
  output: 'smartspaces.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

custom_target(
  'smartspaces.plugin',
  input: smartspaces_plugin_in,
  output: 'smartspaces.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

if install_metainfo
  custom_target(
    'gedit-smartspaces.metainfo.xml',
    input: 'gedit-smartspaces.metainfo.xml.in',
    output: 'gedit-smartspaces.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
