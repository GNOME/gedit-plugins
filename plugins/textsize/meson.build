install_subdir(
  'textsize',
  install_dir: get_option('libdir') / 'gedit/plugins',
)

textsize_plugin_in = configure_file(
  input: 'textsize.plugin.desktop.in.in',
  output: 'textsize.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

textsize_plugin = custom_target(
  'textsize.plugin',
  input: textsize_plugin_in,
  output: 'textsize.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: get_option('libdir') / 'gedit/plugins',
)
