#!/usr/bin/env python3

import os
import subprocess
import sys

libdir = sys.argv[1]
datadir = sys.argv[2]

# Packaging tools define DESTDIR and this isn't needed for them
if 'DESTDIR' not in os.environ:
    print('Compiling gsettings schemas...')
    subprocess.call(['glib-compile-schemas',
                     os.path.join(datadir, 'glib-2.0', 'schemas')])

    print('Compiling python modules...')
    subprocess.call([sys.executable, '-m', 'compileall', '-f', '-q',
                     os.path.join(libdir, 'gedit', 'plugins'),
                     os.path.join(datadir, 'gedit', 'plugins')])

    print('Compiling python modules (optimized versions) ...')
    subprocess.call([sys.executable, '-O', '-m', 'compileall', '-f', '-q',
                     os.path.join(libdir, 'gedit', 'plugins'),
                     os.path.join(datadir, 'gedit', 'plugins')])
