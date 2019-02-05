libfindinfiles_sources = files(
  'dialog.vala',
  'job.vala',
  'matcher.vala',
  'plugin.vala',
  'result-panel.vala',
)

libfindinfiles_deps = [
  valac.find_library('config', dirs: vapi_dir),
  valac.find_library('posix'),
  libpeas_dep,
  gedit_dep,
]

libfindinfiles_c_args = [
  '-DGETTEXT_PACKAGE="@0@"'.format(package_name),
  '-DGP_LOCALEDIR="@0@"'.format(localedir),
]

libfindinfiles_res = gnome.compile_resources(
  'findinfiles-resources',
  'findinfiles.gresource.xml',
)

libfindinfiles_sources += [
  libfindinfiles_res.get(0),
]

libfindinfiles_sha = shared_module(
  'findinfiles',
  sources: libfindinfiles_sources,
  include_directories: rootdir,
  dependencies: libfindinfiles_deps,
  c_args: libfindinfiles_c_args,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

findinfiles_plugin_in = configure_file(
  input: 'findinfiles.plugin.desktop.in.in',
  output: 'findinfiles.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

custom_target(
  'findinfiles.plugin',
  input: findinfiles_plugin_in,
  output: 'findinfiles.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

if install_metainfo
  custom_target(
    'gedit-findinfiles.metainfo.xml',
    input: 'gedit-findinfiles.metainfo.xml.in',
    output: 'gedit-findinfiles.metainfo.xml',
    command: msgfmt_appstream_cmd,
    install: true,
    install_dir: appstreamdir,
  )
endif
