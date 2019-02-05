install_subdir(
  'git',
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

git_plugin_in = configure_file(
  input: 'git.plugin.desktop.in.in',
  output: 'git.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

git_plugin = custom_target(
  'git.plugin',
  input: git_plugin_in,
  output: 'git.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

git_metainfo = i18n.merge_file(
  'gedit-git.metainfo.xml',
  input: 'gedit-git.metainfo.xml.in',
  output: 'gedit-git.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-gedit-git.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      git_metainfo.full_path(),
    ]
  )
endif
