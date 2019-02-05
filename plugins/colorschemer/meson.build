install_subdir(
  'schemer',
  exclude_files: 'Makefile.am',
  strip_directory : true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
    'colorschemer',
  )
)

install_data(
  'schemer.ui',
  install_dir: join_paths(
    pkgdatadir,
    'plugins',
    'colorschemer',
    'ui',
  )
)

colorschemer_plugin_in = configure_file(
  input: 'colorschemer.plugin.desktop.in.in',
  output: 'colorschemer.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

custom_target(
  'colorschemer.plugin',
  input: colorschemer_plugin_in,
  output: 'colorschemer.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

if install_metainfo
  custom_target(
    'gedit-colorschemer.metainfo.xml',
    input: 'gedit-colorschemer.metainfo.xml.in',
    output: 'gedit-colorschemer.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
