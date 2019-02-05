terminal_sources = files(
  'terminal.py',
)

install_data(
  terminal_sources,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

terminal_plugin_in = configure_file(
  input: 'terminal.plugin.desktop.in.in',
  output: 'terminal.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

custom_target(
  'terminal.plugin',
  input: terminal_plugin_in,
  output: 'terminal.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

install_data(
  'org.gnome.gedit.plugins.terminal.gschema.xml',
  install_dir: join_paths(
    glibdir,
    'schemas',
  )
)

if install_metainfo
  custom_target(
    'gedit-terminal.metainfo.xml',
    input: 'gedit-terminal.metainfo.xml.in',
    output: 'gedit-terminal.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
