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

commander_plugin = custom_target(
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

commander_metainfo = i18n.merge_file(
  'gedit-commander.metainfo.xml',
  input: 'gedit-commander.metainfo.xml.in',
  output: 'gedit-commander.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-gedit-commander.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      commander_metainfo.full_path(),
    ]
  )
endif
