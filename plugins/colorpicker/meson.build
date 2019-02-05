colorpicker_sources = files(
  'colorpicker.py',
)

install_data(
  colorpicker_sources,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

colorpicker_plugin_in = configure_file(
  input: 'colorpicker.plugin.desktop.in.in',
  output: 'colorpicker.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

colorpicker_plugin = custom_target(
  'colorpicker.plugin',
  input: colorpicker_plugin_in,
  output: 'colorpicker.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

colorpicker_metainfo = i18n.merge_file(
  'gedit-colorpicker.metainfo.xml',
  input: 'gedit-colorpicker.metainfo.xml.in',
  output: 'gedit-colorpicker.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-gedit-colorpicker.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      colorpicker_metainfo.full_path(),
    ]
  )
endif
