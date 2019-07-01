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
from session import Session

class TestSession(unittest.TestCase):

    def test_add_file(self):
        session = Session("session_A")
        session.add_file('file')
        self.assertEqual(1, len(session.files))

    def test_compare_objects(self):
        session_a = Session("session_A")
        session_b = Session("session_B")
        self.assertTrue(session_a < session_b)
        self.assertTrue(session_b > session_a)
        self.assertTrue(session_a != session_b)


if __name__ == '__main__':
    unittest.main()
