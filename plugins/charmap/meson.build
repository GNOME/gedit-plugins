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

custom_target(
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

if install_metainfo
  custom_target(
    'gedit-charmap.metainfo.xml',
    input: 'gedit-charmap.metainfo.xml.in',
    output: 'gedit-charmap.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
