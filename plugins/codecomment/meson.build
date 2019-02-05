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

custom_target(
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

if install_metainfo
  custom_target(
    'gedit-codecomment.metainfo.xml',
    input: 'gedit-codecomment.metainfo.xml.in',
    output: 'gedit-codecomment.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
