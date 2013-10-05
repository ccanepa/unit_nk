from locale import getlocale, setlocale, LC_ALL, normalize
import sys

to_try = [
    'C',
    'en',
    'en_US',
    'es',
    'es_AR'
]



print('\nTrying the naked locale')
for loc in to_try:
    try:
        setlocale(LC_ALL, loc)
        res = getlocale()
    except Exception:
        res = '<fail>'
    print(loc, ':', res)

print('\nTrying appending .utf8')
for loc in to_try:
    try:
        setlocale(LC_ALL, loc + '.utf8')
        res = getlocale()
    except Exception:
        res = '<fail>'
    print((loc + '.utf8'), ':', res)

print('\nTrying tuples')
for loc in to_try:
    try:
        setlocale(LC_ALL, (loc, 'utf8'))
        res = getlocale()
    except Exception:
        res = '<fail>'
    print('('+ loc + ', utf8)', ':', res)


print('\nTrying locale.normalize:')
langs = [
    'bg',
    'ca',
    'de',
    'el',
    'en',
    'eo',
    'es',
    'fa',
    'fr',
    'hr',
    'it',
    'jp',
    'nl',
    'pl',
    'pt_br',
    'ru',
    'tr_tr',
    'zh_cn'
]

for e in langs:
    try:
        res = normalize(e)
    except Exception:
        res = '<fail>'
    print(e, ':', res)


try:
    setlocale(LC_ALL, '')
    res = getlocale()
except Exception:
        res = '<fail>'

print("\nLocale after setlocale(LC_ALL, ''):", res)

# In Travis, if the builder's locales are set in the travis.yml as suggested
# in http://about.travis-ci.org/docs/user/common-build-problems/#System%3A-Required-langauge-pack-isn't-installed
#
# before_install:
#   - sudo apt-get update
#   - sudo apt-get --reinstall install -qq language-pack-en language-pack-es
#
#
# We learn that in 2.6.8, 2.7.3, 3.3.
# The locales 'C', 'en_US.utf8', 'es_AR.utf8' are valid
# The locales 'C.utf8', 'en', 'es', 'en.utf8', 'es.utf8' are invalid
# The locales ('C', utf8), ('en', utf8), ('en_us', utf8), ('es', utf8),
# ('es_AR', utf8) are valid
# The prefered locale, obtained with getlocale(LC_ALL, '') is 'en_US.utf8'
# For the current nikola languajes, guessing the (string) locale by way of
# locale.normalize seems sensible.

# notice that locale functions don't coerce a string locale; string locale must
# be str in each python. It is safest then to express string locales in the way
# of locale_n = str('whatever') ; This makes it work for any python, with or
# without from future import unicode_literals
