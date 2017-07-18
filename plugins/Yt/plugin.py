# -*- coding: utf8 -*-
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
from operator import itemgetter

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Yt')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Yt(callbacks.Plugin):
    """Add the help for "@plugin help Yt" here
    This should describe *how* to use this plugin."""
    threaded = True

    def yt(self, irc, msg, args, name):
        """<name>

        Returns <name> (song name) from YouTube with some basic info."""
        p = etree.HTML(urllib2.urlopen('http://www.youtube.com/results?search_query=%s' % '+'.join(name)).read())
        #el = p.xpath("/html/body/div/div[4]/div/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/ol/li/div[2]/h3/a") - stari xpath (promenjen 17/11/2013)
        el = p.xpath(".//div/div[2]/div/div[2]/ol/li/div[2]/h3//a")
        viev = p.xpath(".//div/div[2]/div/div[2]/ol//li")
        #viev = p.xpath("/html/body/div/div[4]/div/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/ol/li") - stari xpath (promenjen 17/11/2013)
        viv = [', '.join(['%s' % e.get('data-context-item-views')]) for e in viev]
        user = [', '.join(['%s' % e.get('data-context-item-user')]) for e in viev]
        tt = [', '.join(['%s' % e.get('title')]) for e in el]
        ll = [', '.join(['%s' % e.get('href')]) for e in el]
        vi = etree.HTML(urllib2.urlopen('http://www.youtube.com%s' % (''.join(itemgetter(0)(ll)))).read())
        la = vi.xpath("/html/body/div/div[4]/div/div[3]/div/div/div/div/div/div[2]/div/span[2]/span")
        lajk = [', '.join(['%s' % e.text]) for e in la]
        irc.reply('\x02Link\x02: http://youtube.com%s \x02Name\x02: %s, \x02Views\x02: %s, \x02Uploaded by\x02: %s, \x02Likes/Dislikes\x02: %s' % (''.join(itemgetter(0)(ll)), ''.join(itemgetter(0)(tt)), ''.join(itemgetter(0)(viv)), ''.join(itemgetter(0)(user)), '\x02-\02'.join(lajk)))
    yt = wrap(yt, [many('anything')])


Class = Yt


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
