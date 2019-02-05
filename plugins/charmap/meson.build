install_subdir(
  'charmap',
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

charmap_plugin_in = configure_file(
  input: 'charmap.plugin.desktop.in.in',
  output: 'charmap.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

charmap_plugin = custom_target(
  'charmap.plugin',
  input: charmap_plugin_in,
  output: 'charmap.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

charmap_metainfo = i18n.merge_file(
  'gedit-charmap.metainfo.xml',
  input: 'gedit-charmap.metainfo.xml.in',
  output: 'gedit-charmap.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-gedit-charmap.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      charmap_metainfo.full_path(),
    ]
  )
endif
