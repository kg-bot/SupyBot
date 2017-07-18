###
# Copyright (c) 2002-2004, James Vega
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

import babelfish

import supybot.conf as conf
import supybot.utils as utils
from supybot.commands import *
import supybot.callbacks as callbacks

class Babelfish(callbacks.Plugin):
    threaded = True
    _abbrevs = utils.abbrev(map(str.lower, babelfish.available_languages))
    _abbrevs['de'] = 'german'
    _abbrevs['jp'] = 'japanese'
    _abbrevs['kr'] = 'korean'
    _abbrevs['es'] = 'spanish'
    _abbrevs['pt'] = 'portuguese'
    _abbrevs['it'] = 'italian'
    _abbrevs['zh'] = 'chinese_simple'
    _abbrevs['zt'] = 'chinese_traditional'
    _abbrevs['nl'] = 'dutch'
    _abbrevs['el'] = 'greek'
    for language in babelfish.available_languages:
        _abbrevs[language] = language

    def _getLang(self, fromLang, toLang, chan):
        fromLang = self._abbrevs[fromLang.lower()]
        toLang = self._abbrevs[toLang.lower()]
        languages = map(str.lower, self.registryValue('languages',chan))
        if fromLang not in languages:
            fromLang = None
        if toLang not in languages:
            toLang = None
        return (fromLang, toLang)

    class language(callbacks.Commands):
        def list(self, irc, msg, args):
            """takes no arguments

            Returns the languages that Babelfish can translate to/from.
            """
            irc.reply(format('%L', babelfish.available_languages))

        def random(self, irc, msg, args, optlist):
            """[--allow-english]

            Returns a random language supported by babelfish.  If --allow-english
            is provided, will include English in the list of possible languages.
            """
            allowEnglish = False
            for (option, arg) in optlist:
                if option == 'allow-english':
                    allowEnglish = True
            languages = conf.get(conf.supybot.plugins.Babelfish.languages,
                                 msg.args[0])
            if not languages:
                irc.error('I can\'t speak any other languages.', Raise=True)
            language = utils.iter.choice(languages)
            while not allowEnglish and language == 'English':
                language = utils.iter.choice(languages)
            irc.reply(language)
        random = wrap(random, [getopts({'allow-english': ''})])

    def translate(self, irc, msg, args, fromLang, toLang, text):
        """<from-language> [to] <to-language> <text>

        Returns <text> translated from <from-language> into <to-language>.
        Beware that translating to or from languages that use multi-byte
        characters may result in some very odd results.
        """
        chan = msg.args[0]
        try:
            (fromLang, toLang) = self._getLang(fromLang, toLang, chan)
            if not fromLang or not toLang:
                langs = list(self.registryValue('languages', chan))
                if not langs:
                    irc.error('I do not speak any other languages.')
                    return
                else:
                    irc.error(format('I only speak %L.', langs))
                    return
            translation = babelfish.translate(text, fromLang, toLang)
            irc.reply(utils.web.htmlToText(translation))
        except (KeyError, babelfish.LanguageNotAvailableError), e:
            languages = self.registryValue('languages', chan)
            if languages:
                languages = format('Valid languages include %L',
                                   sorted(languages))
            else:
                languages = 'I do not speak any other languages.'
            irc.errorInvalid('language', str(e), languages)
        except babelfish.BabelizerIOError, e:
            irc.error(str(e))
        except babelfish.BabelfishChangedError, e:
            irc.error('Babelfish has foiled our plans by changing its '
                      'webpage format.')
    translate = wrap(translate, ['something', 'to', 'something', 'text'])

    def babelize(self, irc, msg, args, fromLang, toLang, text):
        """<from-language> <to-language> <text>

        Translates <text> repeatedly between <from-language> and <to-language>
        until it doesn't change anymore or 12 times, whichever is fewer.  One
        of the languages must be English.
        """
        chan = msg.args[0]
        try:
            (fromLang, toLang) = self._getLang(fromLang, toLang, chan)
            if fromLang != 'english' and toLang != 'english':
                irc.error('One language in babelize must be English.')
                return
            if not fromLang or not toLang:
                langs = self.registryValue('languages', chan)
                if not langs:
                    irc.error('I do not speak any other languages.')
                    return
                else:
                    irc.error(format('I only speak %L.', (langs, 'or')))
                    return
            translations = babelfish.babelize(text, fromLang, toLang)
            irc.reply(utils.web.htmlToText(translations[-1]))
        except (KeyError, babelfish.LanguageNotAvailableError), e:
            languages = self.registryValue('languages', chan)
            if languages:
                languages = format('Valid languages include %L',
                                   sorted(languages))
            else:
                languages = 'I do not speak any other languages.'
            irc.errorInvalid('language', str(e), languages)
        except babelfish.BabelizerIOError, e:
            irc.reply(e)
        except babelfish.BabelfishChangedError, e:
            irc.reply('Babelfish has foiled our plans by changing its '
                      'webpage format.')
    babelize = wrap(babelize, ['something', 'something', 'text'])

Class = Babelfish

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
