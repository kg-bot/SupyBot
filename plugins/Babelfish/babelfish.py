# babelizer.py - API for simple access to babelfish.altavista.com.
#                Requires python 2.0 or better.
#
# See it in use at http://babel.MrFeinberg.com/

"""API for simple access to babelfish.altavista.com.

Summary:

    import babelizer

        print ' '.join(babelizer.available_languages)

    print babelizer.translate( 'How much is that doggie in the window?',
                                       'English', 'French' )

    def babel_callback(phrase):
                print phrase
                sys.stdout.flush()

        babelizer.babelize( 'I love a reigning knight.',
                                                'English', 'German',
                                                callback = babel_callback )

available_languages
    A list of languages available for use with babelfish.

translate( phrase, from_lang, to_lang )
    Uses babelfish to translate phrase from from_lang to to_lang.

babelize(phrase, from_lang, through_lang, limit = 12, callback = None)
    Uses babelfish to translate back and forth between from_lang and
    through_lang until either no more changes occur in translation or
    limit iterations have been reached, whichever comes first.  Takes
    an optional callback function which should receive a single
    parameter, being the next translation.  Without the callback
    returns a list of successive translations.

It's only guaranteed to work if 'english' is one of the two languages
given to either of the translation methods.

Both translation methods throw exceptions which are all subclasses of
BabelizerError.  They include

LanguageNotAvailableError
    Thrown on an attempt to use an unknown language.

BabelfishChangedError
    Thrown when babelfish.altavista.com changes some detail of their
    layout, and babelizer can no longer parse the results or submit
    the correct form (a not infrequent occurance).

BabelizerIOError
    Thrown for various networking and IO errors.

Version: $Id: babelfish.py,v 1.9 2005/01/13 18:09:21 jamessan Exp $
Author: Jonathan Feinberg <jdf@pobox.com>
"""
import re, string, urllib

"""
Various patterns I have encountered in looking for the babelfish result.
We try each of them in turn, based on the relative number of times I've
seen each of these patterns.  $1.00 to anyone who can provide a heuristic
for knowing which one to use.   This includes AltaVista employees.
"""
__where = [ re.compile(r'lang=..>([^<]*)</div'),
            re.compile(r'name=\"q\" value=\"([^\"]*)\">'),
            re.compile(r'div style=padding:10px;>([^<]+)</div'),
          ]

__languages = { 'english'   : 'en',
                'chinese_simple'   : 'zh',
                'chinese_traditional'   : 'zt',
                'french'    : 'fr',
                'german'    : 'de',
                'italian'   : 'it',
                'japanese'  : 'ja',
                'korean'    : 'ko',
                'spanish'   : 'es',
                'portuguese' : 'pt',
                'russian'   : 'ru',
                'greek'     : 'el',
                'dutch'     : 'nl',
              }

"""
  All of the available language names.
"""
available_languages = [ x.title() for x in __languages.keys() ]

"""
  Calling translate() or babelize() can raise a BabelizerError
"""
class BabelizerError(Exception):
    pass

class LanguageNotAvailableError(BabelizerError):
    pass
class BabelfishChangedError(BabelizerError):
    pass
class BabelizerIOError(BabelizerError):
    pass

def clean(text):
    return ' '.join(string.replace(text.strip(), "\n", ' ').split())

def translate(phrase, from_lang, to_lang):
    phrase = clean(phrase)
    try:
        from_code = __languages[from_lang.lower()]
        to_code = __languages[to_lang.lower()]
    except KeyError, lang:
        raise LanguageNotAvailableError(lang)

    params = urllib.urlencode( { 'BabelFishFrontPage' : 'yes',
                                 'doit' : 'done',
                                 'tt' : 'urltext',
                                 'intl' : '1',
                                 'urltext' : phrase,
                                 'lp' : from_code + '_' + to_code } )
    try:
        response = urllib.urlopen('http://babelfish.altavista.com/babelfish/tr', params)
    except IOError, what:
        raise BabelizerIOError("Couldn't talk to server: %s" % what)
    except:
        print "Unexpected error:", sys.exc_info()[0]

    html = response.read()
    try:
        begin = html.index('<!-- Target text (content) -->')
        end = html.index('<!-- end: Target text (content) -->')
        html = html[begin:end]
    except ValueError:
        pass
    for regex in __where:
        match = regex.search(html)
        if match:
            break
    if not match:
        raise BabelfishChangedError("Can't recognize translated string.")
    return clean(match.group(1))

def babelize(phrase, from_language, through_language, limit = 12, callback = None):
    phrase = clean(phrase)
    seen = { phrase: 1 }
    results = []
    if callback:
        def_callback = callback
    else:
        def_callback = results.append
    def_callback(phrase)
    flip = { from_language: through_language, through_language: from_language }
    next = from_language
    for i in range(limit):
        phrase = translate(phrase, next, flip[next])
        if seen.has_key(phrase):
            break
        seen[phrase] = 1
        def_callback(phrase)
        next = flip[next]
    # next is set to the language of the last entry.  this should be the same
    # as the language we are translating to
    if next != through_language:
        phrase = translate(phrase, next, flip[next])
        def_callback(phrase)
    if not callback:
        return results

if __name__ == '__main__':
    import sys
    def printer(x):
        print x
        sys.stdout.flush();


    babelize("I won't take that sort of treatment from you, or from your doggie!",
             'english', 'french', callback = printer)

