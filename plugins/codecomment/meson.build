codecomment_sources = files(
  'codecomment.py',
)

install_data(
  codecomment_sources,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

codecomment_plugin_in = configure_file(
  input: 'codecomment.plugin.desktop.in.in',
  output: 'codecomment.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

codecomment_plugin = custom_target(
  'codecomment.plugin',
  input: codecomment_plugin_in,
  output: 'codecomment.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

codecomment_metainfo = i18n.merge_file(
  'gedit-codecomment.metainfo.xml',
  input: 'gedit-codecomment.metainfo.xml.in',
  output: 'gedit-codecomment.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-gedit-codecomment.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      codecomment_metainfo.full_path(),
    ]
  )
endif
