from __future__ import print_function, unicode_literals
import sys
import locale
from . import utils

def is_valid_locale(locale_n):
    valid = False
    try:
        locale.setlocale(locale.LC_ALL, locale_n)
        valid = True
    except locale.Error as e:
        print(e)
        pass
    if valid:
        locale.setlocale(locale.LC_ALL, locale_n)
        try:
            locale.getlocale()
        except locale.Error:
            msg = 'setlocale(getlocale()) fails for locale {0}; some calendar results can be wrong'
            utils.LOGGER.warn(msg.format(locale_n))
    return valid


def valid_locale_fallback(desired_locale=None):
    """returns a default fallback_locale, a string that locale.setlocale will accept"""
    # Whenever fallbacks change, adjust test TestHarcodedFallbacksWork
    candidates_windows = [str('English'), str('C')]
    candidates_linux = [str('en_US.utf8'), str('C')]
    candidates = candidates_windows if sys.platform == 'win32' else candidates_linux
    if desired_locale:
        candidates = list(candidates)
        candidates.insert(0, desired_locale)
    found_valid = False
    for locale_n in candidates:
        found_valid = is_valid_locale(locale_n)
        if found_valid:
            break
    if not found_valid:
        msg = 'Could not find a valid fallback locale, tried: {0}'
        utils.LOGGER.warn(msg.format(candidates))
    elif desired_locale and (desired_locale != locale_n):
        msg = 'Desired fallback locale {0} could not be set, using: {1}'
        utils.LOGGER.warn(msg.format(desired_locale, locale_n))
    return locale_n


def sanitized_locales(locale_fallback, locale_default, locales, translations):
    locale_fallback = valid_locale_fallback(locale_fallback)
    # locales for languages not in translations are ignored
    extras = set(locales) - set(translations)
    if extras:
        msg = 'Unexpected languages in LOCALES, ignoring them: {0}'
        utils.LOGGER.warn(msg.format(extras))
        for lang in extras:
            del locales[lang]

    # explicit but invalid locales are replaced with the sanitized locale_fallback
    for lang in locales:
        if not is_valid_locale(locales[lang]):
            msg = 'Locale {0} for language {1} not accepted by python locale.'
            utils.LOGGER.warn(msg.format(locales[lang], lang))
            locales[lang] = locale_fallback

    # languages with no explicit locale
    missing = set(translations) - set(locales)
    if locale_default:
        # are set to the sanitized locale_default if it was explicitly set
        if not is_valid_locale(locale_default):
            msg = 'LOCALE_DEFAULT {0} could not be set, using {1}'
            utils.LOGGER.warn(msg.format(locale_default, locale_fallback))
            locale_default = locale_fallback
        for lang in missing:
            locales[lang] = locale_default
    else:
        # are set to sanitized guesses compatible with v 6.0.4 in Linux-Mac (was broken in Windows)
        if sys.platform == 'win32':
            guess_locale_fom_lang = guess_locale_from_lang_windows
        else:
            guess_locale_fom_lang = guess_locale_from_lang_linux
        for lang in missing:
            locale_n = guess_locale_fom_lang(lang)
            if not locale:
                locale_n = locale_fallback
                msg = "Could not guess locale for language {0}, using locale {1}"
                utils.LOGGER.warn(msg.format(lang, locale_n))
            locales[lang] = locale_n

    return locale_fallback, locale_default, locales


def guess_locale_from_lang_windows(lang):
    return _windows_locale_guesses.get(lang, None)


def guess_locale_from_lang_linux(lang):
    # compatibility v6.0.4
    if is_valid_locale(lang):
        locale_n = lang
    else:
        # this works in Travis when locale support set by Travis suggestion
        locale_n = (locale.normalize(lang).split('.')[0]) + '.utf8'
    return locale_n


_windows_locale_guesses = {
    # some languages may need that the appropiate Language Pack from
    # Microsoft be instaled
    "en":     "English",
    "bg":     "Bulgarian",
    "ca":     "Catalan",
    "zh_cn":  "Chinese_China",  # Chinese (Simplified)"
    "hr":     "Croatian",
    "nl":     "Dutch",
    "fr":     "French",
    "el":     "Greek",
    "de":     "German",
    "it":     "Italian",
    "jp":     "Japanese",
    "fa":     "Farsi",  # Persian
    "pl":     "Polish",
    "pt_br":  "Portuguese_Brazil",
    "ru":     "Russian",
    "es":     "Spanish",
    "tr_tr":  "Turkish",
    "eo":     "Esperanto",
}

