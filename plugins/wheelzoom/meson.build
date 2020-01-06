libwheelzoom_sources = files(
  'gedit-wheelzoom-plugin.c',
)

libwheelzoom_deps = [
  gedit_dep,
]

libwheelzoom_c_args = [
]

libwheelzoom_sha = shared_module(
  'wheelzoom',
  sources: libwheelzoom_sources,
  dependencies: libwheelzoom_deps,
  c_args: libwheelzoom_c_args,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  ),
)

custom_target(
  'wheelzoom.plugin',
  input: 'wheelzoom.plugin.desktop.in',
  output: 'wheelzoom.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)
