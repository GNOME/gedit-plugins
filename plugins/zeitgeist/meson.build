libzeitgeist_sources = files(
  'gedit-zeitgeist-plugin.c',
)

libzeitgeist_deps = [
  gedit_dep,
  zeitgeist_dep,
]

libzeitgeist_c_args = [
  '-DHAVE_CONFIG_H',
]

libzeitgeist_sha = shared_module(
  'zeitgeist',
  sources: libzeitgeist_sources,
  include_directories: rootdir,
  dependencies: libzeitgeist_deps,
  c_args: libzeitgeist_c_args,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

zeitgeist_plugin = custom_target(
  'zeitgeist.plugin',
  input: 'zeitgeist.plugin.desktop.in',
  output: 'zeitgeist.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

zeitgeist_metainfo = i18n.merge_file(
'gedit-zeitgeist.metainfo.xml',
  input: 'gedit-zeitgeist.metainfo.xml.in',
  output: 'gedit-zeitgeist.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-gedit-zeitgeist.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      zeitgeist_metainfo.full_path(),
    ]
  )
endif
