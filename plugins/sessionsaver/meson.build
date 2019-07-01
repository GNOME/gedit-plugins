install_subdir(
  'sessionsaver',
  exclude_directories: ['ui'],
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

install_data(
  'sessionsaver/ui/sessionsaver.ui',
  install_dir: join_paths(
    pkgdatadir,
    'plugins',
    'sessionsaver',
    'ui',
  )
)

subdir('tests')

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


