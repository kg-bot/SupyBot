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
import json
import string

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Wiki')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Wiki(callbacks.Plugin):
    """Add the help for "@plugin help Wiki" here
    This should describe *how* to use this plugin."""
    threaded = True

    def wiki(self, irc, msg, args, word):
        """<keyword>

        Queries Wikipedia\x0310DOT\x03com for the given <keyword> and returns first found link to the page"""
        try:
            search = json.load(utils.web.getUrlFd('http://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch=%s' % '_'.join(word)))
            search = search['query']['search'][0].values()[0]
            req = json.load(utils.web.getUrlFd('http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s' % string.replace(search, ' ', '_')))
            split = req['query']['pages'].items()[0][0]
            title = req['query']['pages'].items()[0][1].items()[2][1]
            pageid = 'http://en.wikipedia.org/wiki/?curid=%s' % split if split != '-1' else 'There is no page on Wikipedia for given keyword, try changing it and then query again'
            irc.reply('%s - \x02\x0310%s\x03\x02' % (pageid, search))
        except:
            irc.reply("Couldn't find anything for given keyword, try changing it a bit")
    wiki = wrap(wiki, [many('something')])

    def wikihow(self, irc, msg, args, word):
        """<keyword>

        Queries wikihow\x0310DOT\x03com for the given <keyword> and returns first found link to the page"""
        try:
            search = json.load(utils.web.getUrlFd('http://www.wikihow.com/api.php?action=app&subcmd=search&format=json&q=%s' % '_'.join(word)))
            url = search['app']['articles'][0].values()[1]
            title = search['app']['articles'][0].values()[4]
            irc.reply('%s - \x02\x0310%s\x03\x02' % (url, title))
        except:
            irc.reply("Couldn't find anything for given keyword, try changing it a bit")
    wikihow = wrap(wikihow, [many('something')])


Class = Wiki


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
