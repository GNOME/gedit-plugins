install_subdir(
  'synctex',
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

synctex_plugin_in = configure_file(
  input: 'synctex.plugin.desktop.in.in',
  output: 'synctex.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

custom_target(
  'synctex.plugin',
  input: synctex_plugin_in,
  output: 'synctex.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

if install_metainfo
  custom_target(
    'gedit-synctex.metainfo.xml',
    input: 'gedit-synctex.metainfo.xml.in',
    output: 'gedit-synctex.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
