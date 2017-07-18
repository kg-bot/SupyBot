###
# Copyright (c) 2013, KG-Bot
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
import urllib2
from lxml import etree
from xml.etree.ElementTree import ElementTree
import string

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Urban')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Urban(callbacks.Plugin):
    """Add the help for "@plugin help Urban" here
    This should describe *how* to use this plugin."""
    threaded = True

    def urbandic(self, irc, msg, args, word):
            """<keyword>

            Queries urbandictionary\x0310DOT\x03com for given keyword and returns its definitions and examples"""
        #try:
            req = urllib2.urlopen('http://www.urbandictionary.com/define.php?term=%s' % '_'.join(word)).read()
            l = etree.HTML(req)
            definitions = l.xpath(".//div[31]/div")
            dafinitions = [', '.join(['%s' % e.text]) for e in definitions]
            error = l.xpath(".//div[@id='not_defined_yet']/h3/br")
            error = [', '.join(['%s' % e.text]) for e in error]
            try:
                split_def = string.split(dafinitions[0], "\r")
                split_def1 = string.split(split_def[0], '.')
                split_examp = string.split(dafinitions[1], "\r")
                split_examp1 = string.split(split_examp[0], '.')
                if split_def1[0] == '1' and split_examp1[0] == '1':
                    irc.reply('\x0310Definition\x03: \x02%s\x02 - \x0310Example\x03: \x02%s\x02' % (split_def1[1], split_examp1[1]))
                else:
                    irc.reply('\x0310Definition\x03: \x02%s\x02 - \x0310Example\x03: \x02%s\x02' % (split_def1[0], split_examp1[0]))
            except:
                irc.reply(("\x02%s\x02 isn't defined. Can you define it?" % ' '.join(word)))
        #except:
            #irc.reply("\x02%s\x02 isn't defined. Can you define it?" % ' '.join(word))
    urbandic = wrap(urbandic, [many('something')])


Class = Urban


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
