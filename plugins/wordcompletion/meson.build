libwordcompletion_sources = files(
  'gedit-word-completion-plugin.c',
)

libwordcompletion_deps = [
  gedit_dep,
]

libwordcompletion_c_args = [
  '-DHAVE_CONFIG_H',
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
  include_directories: rootdir,
  dependencies: libwordcompletion_deps,
  c_args: libwordcompletion_c_args,
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

custom_target(
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

if install_metainfo
  custom_target(
    'gedit-wordcompletion.metainfo.xml',
    input: 'gedit-wordcompletion.metainfo.xml.in',
    output: 'gedit-wordcompletion.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
