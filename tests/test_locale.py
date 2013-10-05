from __future__ import unicode_literals

import locale
import unittest
import unit_nk.unit_nk as nikola


# all locales specified as str('zxzxz') because locale.setlocale fails
# if it sees a string of the wrong type (no automatic coercion)
# and this module, like most of nikola, uses the unicode_literal thingy

import sys
if sys.platform == 'win32':
    loc_eng = str('English')
    loc_spa = str('Spanish')
else:
    loc_eng = str('en.utf8')
    loc_spa = str('es.utf8')
loc_C = str('C')
loc_Cutf8 = str('C.utf8')


class TestExploreTravis(unittest.TestCase):
    def test_C_locale(self):
        self.assertTrue(nikola.is_valid_locale(loc_C), "'C' locale not available")

    def test_Cutf8_locale(self):
        self.assertTrue(nikola.is_valid_locale(loc_Cutf8), "'C.utf8' locale not available")


class TestTestPreconditions(unittest.TestCase):
    """if this fails the other test in this module are mostly nonsense
       failure probably means the OS support for the failing locale is not
       instaled
    """
    def test_locale_eng_availability(self):
        self.assertTrue(nikola.is_valid_locale(loc_eng), "META ERROR: locale for english should be valid")

    def test_locale_esp_availability(self):
        self.assertTrue(nikola.is_valid_locale(loc_spa), "META ERROR: locale for spanish should be valid")


class TestConfigLocale(unittest.TestCase):

    def test_implicit_fallback(self):
        locale_fallback = None
        sanitized_fallback = nikola.valid_locale_fallback(desired_locale=locale_fallback)
        self.assertTrue(nikola.is_valid_locale(sanitized_fallback))

    def test_explicit_good_fallback(self):
        locale_fallback = loc_spa
        sanitized_fallback = nikola.valid_locale_fallback(desired_locale=locale_fallback)
        self.assertEquals(sanitized_fallback, locale_fallback)
            
    def test_explicit_bad_fallback(self):
        locale_fallback = str('xyz')
        sanitized_fallback = nikola.valid_locale_fallback(desired_locale=locale_fallback)
        self.assertTrue(nikola.is_valid_locale(sanitized_fallback))

    def test_explicit_good_default(self):
        locale_fallback, locale_default, LOCALES, translations = (
            loc_spa,
            loc_eng,
            {},
            {'en': ''},
            )
        fallback, default, locales = nikola.sanitized_locales(locale_fallback,
                                                              locale_default,
                                                              LOCALES,
                                                              translations) 
        self.assertEquals(fallback, locale_fallback)
        self.assertEquals(default, locale_default)
        
    def test_explicit_bad_default(self):
        locale_fallback, locale_default, LOCALES, translations = (
            loc_spa,
            str('xyz'),
            {},
            {'en': ''},
            )
        fallback, default, locales = nikola.sanitized_locales(locale_fallback,
                                                              locale_default,
                                                              LOCALES,
                                                              translations) 
        self.assertEquals(fallback, locale_fallback)
        self.assertEquals(default, fallback)

    def test_implicit_default(self):
        locale_fallback, locale_default, LOCALES, translations = (
            loc_spa,
            None,
            {},
            {'en': ''},
            )
        fallback, default, locales = nikola.sanitized_locales(locale_fallback,
                                                              locale_default,
                                                              LOCALES,
                                                              translations)
        self.assertEquals(locales['en'], loc_eng)
        
    def test_extra_locales_deleted(self):
        locale_fallback, locale_default, LOCALES, translations = (
            loc_spa,
            None,
            {'@z': loc_spa},
            {'en': ''},
            )
        fallback, default, locales = nikola.sanitized_locales(locale_fallback,
                                                              locale_default,
                                                              LOCALES,
                                                              translations)
        self.assertTrue('@z' not in locales)
    
    def test_explicit_good_locale_retained(self):
        locale_fallback, locale_default, LOCALES, translations = (
            None,
            loc_spa,
            {'en': loc_eng},
            {'en': ''},
            )
        fallback, default, locales = nikola.sanitized_locales(locale_fallback,
                                                              locale_default,
                                                              LOCALES,
                                                              translations)
        self.assertEquals(locales['en'], LOCALES['en'])


    def test_explicit_bad_locale_replaced_with_fallback(self):
        locale_fallback, locale_default, LOCALES, translations = (
            loc_spa,
            loc_eng,
            {'en': str('xyz')},
            {'en': ''},
            )
        fallback, default, locales = nikola.sanitized_locales(locale_fallback,
                                                              locale_default,
                                                              LOCALES,
                                                              translations)
        self.assertEquals(locales['en'], locale_fallback)

    def test_impicit_locale_when_default_locale_defined(self):
        locale_fallback, locale_default, LOCALES, translations = (
            loc_eng,
            loc_spa,
            {},
            {'en': ''},
            )
        fallback, default, locales = nikola.sanitized_locales(locale_fallback,
                                                              locale_default,
                                                              LOCALES,
                                                              translations)
        self.assertEquals(locales['en'], locale_default)
        
    def test_impicit_locale_when_default_locale_is_not_defined(self):
        # legacy mode, compat v6.0.4 : guess locale from lang
        locale_fallback, locale_default, LOCALES, translations = (
            loc_spa,
            None,
            {},
            {'en': ''},
            )
        fallback, default, locales = nikola.sanitized_locales(locale_fallback,
                                                              locale_default,
                                                              LOCALES,
                                                              translations)
        if sys.platform == 'win32':
            guess_locale_for_lang = nikola.guess_locale_from_lang_windows
        else:
            guess_locale_for_lang = nikola.guess_locale_from_lang_linux

        self.assertEquals(locales['en'], guess_locale_for_lang('en'))
