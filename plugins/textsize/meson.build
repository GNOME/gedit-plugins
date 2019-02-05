install_subdir(
  'textsize',
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

textsize_plugin_in = configure_file(
  input: 'textsize.plugin.desktop.in.in',
  output: 'textsize.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

textsize_plugin = custom_target(
  'textsize.plugin',
  input: textsize_plugin_in,
  output: 'textsize.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

textsize_metainfo = i18n.merge_file(
  'gedit-textsize.metainfo.xml',
  input: 'gedit-textsize.metainfo.xml.in',
  output: 'gedit-textsize.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-gedit-textsize.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      textsize_metainfo.full_path(),
    ]
  )
endif
