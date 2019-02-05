libbookmarks_sources = files(
  'gedit-bookmarks-app-activatable.c',
  'gedit-bookmarks-plugin.c',
)

libbookmarks_deps = [
  gedit_dep,
]

libbookmarks_c_args = [
  '-DHAVE_CONFIG_H',
]

subdir('messages')

libbookmarks_sha = shared_module(
  'bookmarks',
  sources: libbookmarks_sources,
  include_directories: rootdir,
  dependencies: libbookmarks_deps,
  c_args: libbookmarks_c_args,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

bookmarks_plugin_in = configure_file(
  input: 'bookmarks.plugin.desktop.in.in',
  output: 'bookmarks.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

bookmarks_plugin = custom_target(
  'bookmarks.plugin',
  input: bookmarks_plugin_in,
  output: 'bookmarks.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

bookmarks_metainfo = i18n.merge_file(
  'gedit-bookmarks.metainfo.xml',
  input: 'gedit-bookmarks.metainfo.xml.in',
  output: 'gedit-bookmarks.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-gedit-bookmarks.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      bookmarks_metainfo.full_path(),
    ]
  )
endif
