joinlines_sources = files(
  'joinlines.py',
)

install_data(
  joinlines_sources,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

joinlines_plugin_in = configure_file(
  input: 'joinlines.plugin.desktop.in.in',
  output: 'joinlines.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

joinlines_plugin = custom_target(
  'joinlines.plugin',
  input: joinlines_plugin_in,
  output: 'joinlines.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

joinlines_metainfo = i18n.merge_file(
  'gedit-joinlines.metainfo.xml',
  input: 'gedit-joinlines.metainfo.xml.in',
  output: 'gedit-joinlines.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-gedit-joinlines.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      joinlines_metainfo.full_path(),
    ]
  )
endif
