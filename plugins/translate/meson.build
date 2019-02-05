install_subdir(
  'translate',
  exclude_directories: ['ui'],
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

install_data(
  'translate/ui/preferences.ui',
  install_dir: join_paths(
    pkgdatadir,
    'plugins',
    'translate',
    'ui',
  )
)

translate_plugin_in = configure_file(
  input: 'translate.plugin.desktop.in.in',
  output: 'translate.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

custom_target(
  'translate.plugin',
  input: translate_plugin_in,
  output: 'translate.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

install_data(
  'org.gnome.gedit.plugins.translate.gschema.xml',
  install_dir: join_paths(
    glibdir,
    'schemas',
  )
)

if install_metainfo
  custom_target(
    'gedit-translate.metainfo.xml',
    input: 'gedit-translate.metainfo.xml.in',
    output: 'gedit-translate.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
