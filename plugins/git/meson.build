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

custom_target(
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

if install_metainfo
  custom_target(
    'gedit-git.metainfo.xml',
    input: 'gedit-git.metainfo.xml.in',
    output: 'gedit-git.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
