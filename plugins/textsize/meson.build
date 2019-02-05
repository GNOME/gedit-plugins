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

custom_target(
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

if install_metainfo
  custom_target(
    'gedit-textsize.metainfo.xml',
    input: 'gedit-textsize.metainfo.xml.in',
    output: 'gedit-textsize.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
