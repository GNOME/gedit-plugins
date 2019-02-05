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
plugin_in.set('VERSION', version)

gpdefs_py = configuration_data()
gpdefs_py.set('PACKAGE', package_name)
gpdefs_py.set('PACKAGE_STRING', package_string)
gpdefs_py.set('GETTEXT_PACKAGE', package_name)
gpdefs_py.set('VERSION', version)

gpdefs_py.set('prefix', prefix)

configure_file(
  input: 'gpdefs.py.in',
  output: 'gpdefs.py',
  configuration: gpdefs_py,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

vapi_dir = join_paths(
  srcdir,
  'plugins',
)

foreach plugin_name : active_plugins
  subdir(plugin_name)
endforeach
