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
from store.session import Session
from store.sessionstore import SessionStore

class TestSessionStore(unittest.TestCase):

    def test_new_two_objects(self):
        session_a = Session("session_A")
        store_a = SessionStore()
        store_a.add(session_a)

        session_b = Session("session_B")
        session_c = Session("session_C")
        store_b = SessionStore()
        store_b.add(session_b)
        store_b.add(session_c)

        self.assertEqual(1, len(store_a))
        self.assertEqual(2, len(store_b))

    def _on_session_added(self, store, session):
        self.added_called = True

    def test_add(self):
        self.added_called = False
        session = Session("session_A")
        store = SessionStore()
        store.connect_after('session-added', self._on_session_added)
        store.add(session)

        self.assertEqual(1, len(store))
        self.assertTrue(self.added_called)

    def _on_session_updated(self, store, session):
        self.updated_called = True


    def test_add_same_object_update(self):
        self.updated_called = False
        session = Session("session_A")
        store = SessionStore()
        store.connect_after('session-added', self._on_session_updated)
        store.add(session)
        session.name = 'Session B'
        store.add(session)

        self.assertEqual(1, len(store))
        self.assertEqual('Session B', store[0].name)
        self.assertTrue(self.updated_called)

    def test_add_equal_object(self):
        session_a = Session("session_A")
        session_b = Session("session_A")
        store = SessionStore()
        store.add(session_a)
        store.add(session_b)
        self.assertEqual(1, len(store))

    def test_remove(self):
        session = Session("session_A")
        store = SessionStore()
        store.add(session)
        store.remove(session)
        self.assertEqual(0, len(store))

if __name__ == '__main__':
    unittest.main()
