libwordcompletion_sources = files(
  'gedit-word-completion-plugin.c',
)

libwordcompletion_deps = [
  gedit_dep,
]

libwordcompletion_res = gnome.compile_resources(
  'gedit-word-completion-resources',
  'gedit-word-completion.gresource.xml',
)

libwordcompletion_sources += [
  libwordcompletion_res.get(0),
]

libwordcompletion_sha = shared_module(
  'wordcompletion',
  sources: libwordcompletion_sources,
  include_directories: root_include_dir,
  dependencies: libwordcompletion_deps,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

wordcompletion_plugin_in = configure_file(
  input: 'wordcompletion.plugin.desktop.in.in',
  output: 'wordcompletion.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

wordcompletion_plugin = custom_target(
  'wordcompletion.plugin',
  input: wordcompletion_plugin_in,
  output: 'wordcompletion.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

install_data(
  'org.gnome.gedit.plugins.wordcompletion.gschema.xml',
  install_dir: join_paths(
    glibdir,
    'schemas',
  )
)

wordcompletion_metainfo = i18n.merge_file(
  input: 'gedit-wordcompletion.metainfo.xml.in',
  output: 'gedit-wordcompletion.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-gedit-wordcompletion.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      wordcompletion_metainfo.full_path(),
    ]
  )
endif
