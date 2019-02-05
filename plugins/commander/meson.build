install_subdir(
  'commander',
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

install_subdir(
  'modules',
  install_dir: join_paths(
    pkgdatadir,
    'plugins',
    'commander',
  )
)

commander_plugin_in = configure_file(
  input: 'commander.plugin.desktop.in.in',
  output: 'commander.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

custom_target(
  'commander.plugin',
  input: commander_plugin_in,
  output: 'commander.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

if install_metainfo
  custom_target(
    'gedit-commander.metainfo.xml',
    input: 'gedit-commander.metainfo.xml.in',
    output: 'gedit-commander.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
