translate_tests = {
  'apertium': files('testapertium.py'),
  'yandex': files('testyandex.py'),
}

translate_srcdir = join_paths(
  srcdir,
  'plugins',
  'translate',
  'translate',
)

foreach test_name, test_script : translate_tests
  test(
    'test-translate-@0@'.format(test_name),
    python3,
    args: [test_script],
    env: [
      'PYTHONPATH=@0@'.format(translate_srcdir),
    ]
  )
endforeach
