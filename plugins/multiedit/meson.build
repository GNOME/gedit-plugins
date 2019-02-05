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

multiedit_plugin = custom_target(
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

multiedit_metainfo = i18n.merge_file(
  'gedit-multiedit.metainfo.xml',
  input: 'gedit-multiedit.metainfo.xml.in',
  output: 'gedit-multiedit.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-gedit-multiedit.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      multiedit_metainfo.full_path(),
    ]
  )
endif
