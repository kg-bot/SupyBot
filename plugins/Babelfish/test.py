###
# Copyright (c) 2002-2004, Jeremiah Fincher
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

from supybot.test import *

class BabelFishTestCase(PluginTestCase):
    plugins = ('Babelfish',)
    if network:
        def testTranslate(self):
            self.assertResponse('translate en sp food',
                                'alimento')
            self.assertResponse('translate en to sp food',
                                'alimento')
            self.assertError('translate foo en food')
            self.assertError('translate en foo food')

        def testBabelize(self):
            self.assertNotError('babelize en sp foo')
            self.assertError('babelize sp fr foo')
            self.assertResponse('babelize german english sprache', 'Language')

        def testLanguageRandom(self):
            self.assertNotError('language random')
            try:
                orig = conf.supybot.plugins.Babelfish.languages()
                conf.supybot.plugins.Babelfish.languages.setValue([])
                self.assertError('language random')
            finally:
                conf.supybot.plugins.Babelfish.languages.setValue(orig)

        def testDisabledLanguages(self):
            langs = conf.supybot.plugins.Babelfish.languages
            try:
                orig = langs()
                langs.setValue(['Spanish', 'English'])
                self.assertResponse('translate sp en hola', 'hello')
                langs.setValue([])
                self.assertRegexp('translate sp en hola', 'do not speak')
                self.assertRegexp('translate en sp hola', 'do not speak')
                langs.setValue(['Spanish', 'Italian'])
                self.assertRegexp('translate sp en hola', 'only speak')
                self.assertRegexp('translate en it hello', 'only speak')
                langs.setValue(['English', 'Italian'])
                self.assertResponse('translate en it hello', 'ciao')
            finally:
                langs.setValue(orig)

        def testHtmlToText(self):
            self.assertNotRegexp('translate fr en Qu\'y', '&#39;')
            self.assertNotRegexp('babelize fr en Qu\'y', '&#39;')


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

