# -*- coding: utf-8 -*-
#
#  Copyrignt (C) 2017 Jordi Mas <jmas@softcatala.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301, USA.

import urllib.request, urllib.parse, urllib.error
import json
from .service import Service

try:
    import gettext
    gettext.bindtextdomain('gedit-plugins')
    gettext.textdomain('gedit-plugins')
    _ = gettext.gettext
except:
    _ = lambda s: s


class Yandex(Service):

    g_language_codes = []
    g_language_names = []
    g_locales_names = {}

    DEFAULT_LANGUAGE_NAMES = ["Spanish -> English",
            "English -> Spanish",
            "Catalan -> English",
            "English -> Catalan"]

    DEFAULT_LANGUAGE_CODES = ["es|en",
            "en|es",
            "ca|en",
            "en|ca",
    ]

    SERVER = "https://translate.yandex.net/api/v1.5/tr.json"

    g_language_codes = []
    g_language_names = []

    @staticmethod
    def _clean_for_ut():
        Yandex.g_language_codes = []
        Yandex.g_language_names = []
        Yandex.g_locales_names = {}

    def get_default_language_codes(self):
        return 'en|es'

    def get_api_hint(self):
        return _("You need to obtain a free API key at <a href='https://tech.yandex.com/translate/'>https://tech.yandex.com/translate/</a>")

    def has_api_key(self):
        return True

    def set_api_key(self, key):
        self._key = key

    def init(self):
        self._fetch_remote_language_names()

    def get_language_names(self):
        if len(Yandex.g_language_codes) > 0 and len(Yandex.g_language_names) > 0:
            return Yandex.g_language_names

        return self.DEFAULT_LANGUAGE_NAMES

    def get_language_codes(self):
        if len(Yandex.g_language_codes) > 0 and len(Yandex.g_language_names) > 0:
            return Yandex.g_language_codes

        return self.DEFAULT_LANGUAGE_CODES

    def get_language_pair_name(self, source, target, locales_names=None):
        if locales_names is None:
            locales_names = Yandex.g_locales_names

        source = self._get_language_name(source, locales_names)
        target = self._get_language_name(target, locales_names)
        return "{0} -> {1}".format(source, target)

    def _get_language_name(self, langcode, locales_names):
        return locales_names[langcode]

    def _fetch_remote_language_names(self):

        try:

            if len(self._key) == 0:
                return

            if (len(Yandex.g_locales_names) > 0 and
               len(Yandex.g_language_names) > 0 and
               len(Yandex.g_language_codes) > 0):
                    return

            url = "{0}/getLangs?ui=en&key={1}".format(self.SERVER, self._key)
            response = urllib.request.urlopen(url)
            payload = json.loads(response.read().decode("utf-8"))

            language_codes = payload['dirs']
            language_codes = [x.replace('-', '|') for x in language_codes]
            locales_names = payload['langs']

            language_names = []
            for lang_pair in language_codes:
                langs = lang_pair.split('|')
                source = langs[0]
                target = langs[1]
                name = self.get_language_pair_name(source, target, locales_names)
                language_names.append(name)

            Yandex.g_locales_names = locales_names
            Yandex.g_language_names = language_names
            Yandex.g_language_codes = language_codes

        except Exception as e:
            print("_fetch_remote_language_names exception {0}".format(e))

    def translate_text(self, text, language_pair):
        language_pair = language_pair.replace('|', '-')
        url = "{0}/translate?lang={1}&format=plain&key={2}".format(self.SERVER, language_pair, self._key)
        url += "&text=" + urllib.parse.quote_plus(text.encode('utf-8'))
        response = urllib.request.urlopen(url)
        r = response.read().decode("utf-8")
        data = json.loads(r)
        all_text = ''

        texts = data['text']
        for text in texts:
            all_text += text
        return all_text
