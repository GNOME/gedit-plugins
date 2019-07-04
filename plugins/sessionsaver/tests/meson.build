sessionsaver_tests = {
  'session': files('testsession.py'),
  'sessionstore': files('testsessionstore.py'),
  'xmlsessionstore': files('testxmlsessionstore.py'),
}

sessionsaver_srcdir = join_paths(
  srcdir,
  'plugins',
  'sessionsaver',
  'sessionsaver',
)

foreach test_name, test_script : sessionsaver_tests
  test(
    'test-sessionsaver-@0@'.format(test_name),
    python3,
    args: [test_script],
    env: [
      'PYTHONPATH=@0@'.format(sessionsaver_srcdir),
    ]
  )
endforeach
