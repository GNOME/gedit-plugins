install_subdir(
  'sessionsaver',
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

sessionsaver_plugin_in = configure_file(
  input: 'sessionsaver.plugin.desktop.in.in',
  output: 'sessionsaver.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

sessionsaver_plugin = custom_target(
  'sessionsaver.plugin',
  input: sessionsaver_plugin_in,
  output: 'sessionsaver.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)


