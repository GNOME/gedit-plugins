install_subdir(
  'multiedit',
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

multiedit_plugin_in = configure_file(
  input: 'multiedit.plugin.desktop.in.in',
  output: 'multiedit.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

custom_target(
  'multiedit.plugin',
  input: multiedit_plugin_in,
  output: 'multiedit.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

if install_metainfo
  custom_target(
    'gedit-multiedit.metainfo.xml',
    input: 'gedit-multiedit.metainfo.xml.in',
    output: 'gedit-multiedit.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
