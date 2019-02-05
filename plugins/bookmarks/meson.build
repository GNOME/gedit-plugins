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

custom_target(
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

if install_metainfo
  custom_target(
    'gedit-bookmarks.metainfo.xml',
    input: 'gedit-bookmarks.metainfo.xml.in',
    output: 'gedit-bookmarks.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
