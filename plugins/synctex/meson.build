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

synctex_plugin = custom_target(
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

synctex_metainfo = i18n.merge_file(
  'gedit-synctex.metainfo.xml',
  input: 'gedit-synctex.metainfo.xml.in',
  output: 'gedit-synctex.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-gedit-synctex.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      synctex_metainfo.full_path(),
    ]
  )
endif
