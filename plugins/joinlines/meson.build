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

custom_target(
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

if install_metainfo
  custom_target(
    'gedit-joinlines.metainfo.xml',
    input: 'gedit-joinlines.metainfo.xml.in',
    output: 'gedit-joinlines.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
