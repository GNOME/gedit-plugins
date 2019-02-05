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

custom_target(
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

if install_metainfo
  custom_target(
    'gedit-colorpicker.metainfo.xml',
    input: 'gedit-colorpicker.metainfo.xml.in',
    output: 'gedit-colorpicker.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
