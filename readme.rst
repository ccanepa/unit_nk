unit_nk
=======

.. image:: https://travis-ci.org/ccanepa/unit_nk.png
   :target: https://travis-ci.org/ccanepa/unit_nk


helper to test nikola, transitorio

What was learned here ?

 In Travis, if the builder's locales are set in the travis.yml as suggested in http://about.travis-ci.org/docs/user/common-build-problems/#System%3A-Required-langauge-pack-isn't-installed::

	 before_install:
	   - sudo apt-get update
	   - sudo apt-get --reinstall install -qq language-pack-en language-pack-es

 We learn that in 2.6.8, 2.7.3, 3.3.

	* The locales 'C', 'en_US.utf8', 'es_AR.utf8' are valid
	* The locales 'C.utf8', 'en', 'es', 'en.utf8', 'es.utf8' are invalid
	* The locales ('C', utf8), ('en', utf8), ('en_us', utf8), ('es', utf8), ('es_AR', utf8) are valid
	* The prefered locale, obtained with getlocale(LC_ALL, '') is 'en_US.utf8'
	* For the current nikola languajes, guessing the (string) locale by way of locale.normalize seems sensible.

Notice that locale functions don't coerce a string locale; string locale must  be str in each python. It is safest then to express string locales in the way of locale_n = str('whatever'). This makes it work for any python, with or# without from future import unicode_literals


