shared_module(
  'smartspaces',
  sources: files(
    'gedit-smart-spaces-view-activatable.c',
  ),
  dependencies: [
    gedit_dep,
  ],
  include_directories: root_include_dir,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

smartspaces_plugin_in = configure_file(
  input: 'smartspaces.plugin.desktop.in.in',
  output: 'smartspaces.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

smartspaces_plugin = custom_target(
  'smartspaces.plugin',
  input: smartspaces_plugin_in,
  output: 'smartspaces.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

smartspaces_metainfo = i18n.merge_file(
  input: 'gedit-smartspaces.metainfo.xml.in',
  output: 'gedit-smartspaces.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-gedit-smartspaces.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      smartspaces_metainfo.full_path(),
    ]
  )
endif
