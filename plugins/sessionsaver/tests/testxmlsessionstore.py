# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.


import unittest
import tempfile
from store.session import Session
from store.xmlsessionstore import XMLSessionStore
from os import path

class TestXmlSessionStore(unittest.TestCase):

    def test_load(self):

        store_file = path.dirname(path.realpath(__file__))
        store_file += '/test-saved-sessions.xml'
        print(store_file)

        store = XMLSessionStore(store_file)
        self.assertEqual(3, len(store))
        self.assertEqual('files', store[0].name)
        self.assertEqual('gspell', store[1].name)
        self.assertEqual('window-activable', store[2].name)

        self.assertEqual(1, len(store[0].files))
        self.assertEqual("/xmlsessionstore.py", store[0].files[0].get_path())

    def test_save(self):
        session_name = "session_A"
        tmpfile = tempfile.NamedTemporaryFile()
        store = XMLSessionStore(tmpfile.name)
        session = Session(session_name)
        store.add(session)
        store.save()

        store = XMLSessionStore(tmpfile.name)
        self.assertEqual(1, len(store))
        self.assertEqual(session_name, store[0].name)


if __name__ == '__main__':
    unittest.main()
