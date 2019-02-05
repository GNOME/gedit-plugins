bracketcompletion_sources = files(
  'bracketcompletion.py',
)

install_data(
  bracketcompletion_sources,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

bracketcompletion_plugin_in = configure_file(
  input: 'bracketcompletion.plugin.desktop.in.in',
  output: 'bracketcompletion.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

bracketcompletion_plugin = custom_target(
  'bracketcompletion.plugin',
  input: bracketcompletion_plugin_in,
  output: 'bracketcompletion.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

bracketcompletion_metainfo = i18n.merge_file(
  'gedit-bracketcompletion.metainfo.xml',
  input: 'gedit-bracketcompletion.metainfo.xml.in',
  output: 'gedit-bracketcompletion.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-gedit-bracketcompletion.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      bracketcompletion_metainfo.full_path(),
    ]
  )
endif
