msgfmt_plugin_cmd = [
  find_program('msgfmt'),
  '--desktop',
  '--keyword=Name',
  '--keyword=Description',
  '--template=@INPUT@',
  '-d', join_paths(srcdir, 'po'),
  '--output=@OUTPUT@'
]

plugin_in = configuration_data()
plugin_in.set('VERSION', meson.project_version())

gpdefs_py = configuration_data()
gpdefs_py.set('GETTEXT_PACKAGE', meson.project_name())

configure_file(
  input: 'gpdefs.py.in',
  output: 'gpdefs.py',
  configuration: gpdefs_py,
  install: true,
  install_dir: get_option('libdir') / 'gedit/plugins',
)

foreach plugin_name : enabled_c_plugins
  subdir(plugin_name)
endforeach

foreach plugin_name : enabled_python_plugins
  subdir(plugin_name)
endforeach
