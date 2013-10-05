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

