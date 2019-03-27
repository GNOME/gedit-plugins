# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Jordi Mas i Hernandez <jmas@softcatala.org>
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
from services.apertium import Apertium
from unittest.mock import patch, MagicMock
from unittest.mock import Mock


class TestApertium(unittest.TestCase):

    def setUp(self):
        Apertium._clean_for_ut()

    @patch('urllib.request.urlopen')
    def test_translate_text(self, mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = bytes('{"responseData": {"translatedText": "Hauries d\'haver-hi rebut una c\u00f2pia"}, "responseDetails": null, "responseStatus": 200}', 'utf-8')
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        apertium = Apertium()
        translated = apertium.translate_text('You should have received a copy', 'eng|cat')
        self.assertEqual('Hauries d\'haver-hi rebut una còpia', translated)
        mock_urlopen.assert_called_with("https://www.apertium.org/apy/translate?langpair=eng|cat&markUnknown=no&q=You+should+have+received+a+copy")

    def test_fetch_remote_language_names_and_pairs_localized(self):
        mockObject = Apertium()
        mockObject._get_user_locale = Mock(return_value='ca')
        mockObject._get_remote_language_pairs = Mock(return_value=[['es'], ['en'], ['es', 'en'], ['es|en']])
        mockObject._get_remote_language_names = Mock(return_value={'es': 'Espanyol', 'en': 'Anglès'})

        mockObject._fetch_remote_language_names_and_pairs()
        self.assertEqual({'en': 'Anglès', 'es': 'Espanyol'}, Apertium.g_locales_names)
        self.assertEqual(['Espanyol -> Anglès'], Apertium.g_language_names)
        self.assertEqual(['es|en'], Apertium.g_language_codes)

    def test_fetch_remote_language_names_and_pairs_non_localized(self):
        mockObject = Apertium()
        mockObject._get_user_locale = Mock(return_value='ca_ES')
        mockObject._get_remote_language_pairs = Mock(return_value=[['ca'], ['en'], ['ca', 'en'], ['ca|en']])
        mockObject._get_remote_language_names = Mock(return_value={'es': 'Espanyol', 'en': 'Anglès'})
        mockObject._add_missing_locale_names_in_english = Mock(return_value={'ca': 'Català', 'en': 'English'})

        mockObject._fetch_remote_language_names_and_pairs()
        self.assertEqual({'en': 'English', 'ca': 'Català'}, Apertium.g_locales_names)
        self.assertEqual(['Català -> English'], Apertium.g_language_names)
        self.assertEqual(['ca|en'], Apertium.g_language_codes)

    @patch('urllib.request.urlopen')
    def test_get_remote_language_pairs(self, mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = bytes('{"responseStatus": 200, "responseData": [{"targetLanguage": "cat", "sourceLanguage": "oci_aran"}]}', 'utf-8')
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        apertium = Apertium()
        language_pair_source, language_pair_target, locales, language_codes = apertium._get_remote_language_pairs()
        self.assertEqual(['oci_aran'], language_pair_source)
        self.assertEqual(['cat'], language_pair_target)
        self.assertEqual({'oci_aran', 'cat'}, locales)
        self.assertEqual(['oci_aran|cat'], language_codes)
        mock_urlopen.assert_called_with("https://www.apertium.org/apy/listPairs")



if __name__ == '__main__':
    unittest.main()
