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
import mechanize
import cookielib
from lxml import etree
from xml.etree.ElementTree import ElementTree
import string
import re

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('TPB')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class TPB(callbacks.Plugin):
    """Add the help for "@plugin help TPB" here
    This should describe *how* to use this plugin."""
    threaded = True

    def tpb(self, irc, msg, args, keyword):
        """<keyword>

        Looks for keyword on The Pirate Bay and returns first 3 torrents with some basic info"""
        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        br.open('http://thepiratebay.sx/search/%s/0/7/0' % '_'.join(keyword))
        k = br.response().read()
        l = etree.HTML(k)
        # Everything for torrent #1
        name1 = l.xpath('.//tr[2]/td[2]//a')
        na1 = [', '.join(['%s' % e.text]) for e in name1]
        type1 = l.xpath('.//tr[2]/td/center//a')
        type11 = l.xpath('.//tr[2]/td/center//a[2]')
        ty1 = [','.join(['%s' % e.text]) for e in type1]
        ty11 = [','.join(['%s' % e.text]) for e in type11]
        seeders1 = l.xpath('.//tr[2]/td[3]')
        se1 = [', '.join(['%s' % e.text]) for e in seeders1]
        magnet1 = l.xpath('.//tr[2]/td[2]//a')
        magnet11 = [', '.join(['%s' % e.get('href')]) for e in magnet1]
        # Tiny magnet link, torrent #1
        mag1 = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + magnet11[1])
        mag1 = mag1.decode()

        # Everything for torrent #2
        name2 = l.xpath('.//tr[3]/td[2]//a')
        na2 = [', '.join(['%s' % e.text]) for e in name2]
        type2 = l.xpath('.//tr[3]/td/center//a')
        type22 = l.xpath('.//tr[3]/td/center//a[2]')
        ty2 = [','.join(['%s' % e.text]) for e in type2]
        ty22 = [','.join(['%s' % e.text]) for e in type22]
        seeders2 = l.xpath('.//tr[3]/td[3]')
        se2 = [', '.join(['%s' % e.text]) for e in seeders2]
        magnet2 = l.xpath('.//tr[3]/td[2]//a')
        magnet22 = [', '.join(['%s' % e.get('href')]) for e in magnet2]
        # Tiny magnet link, torrent #2
        mag2 = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + magnet22[1])
        mag2 = mag2.decode()

        # Everything for torrent #3
        name3 = l.xpath('.//tr[4]/td[2]//a')
        na3 = [', '.join(['%s' % e.text]) for e in name3]
        type3 = l.xpath('.//tr[4]/td/center//a')
        type33 = l.xpath('.//tr[4]/td/center//a[2]')
        ty3 = [','.join(['%s' % e.text]) for e in type3]
        ty33 = [','.join(['%s' % e.text]) for e in type33]
        seeders3 = l.xpath('.//tr[4]/td[3]')
        se3 = [', '.join(['%s' % e.text]) for e in seeders3]
        magnet3 = l.xpath('.//tr[4]/td[2]//a')
        magnet33 = [', '.join(['%s' % e.get('href')]) for e in magnet3]
        # Tiny magnet link, torrent #3
        mag3 = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + magnet33[1])
        mag3 = mag3.decode()
        irc.reply('\x02\x0310Name\x03\x02: %s, \x02\x0310Type\x03\x02: %s(%s), \x02\x0310Seeders\x03\x02: %s, \x02\x0310Magnet Link:\x03\02: %s \x0311<>\x03 \x02\x0307Name\x03\x02: %s, \x02\x0307Type\x03\x02: %s(%s), \x02\x0307Seeders\x03\x02: %s, \x02\x0307Magnet Link:\x03\02: %s \x0311<>\x03 \x02\x0304Name\x03\x02: %s, \x02\x0304Type\x03\x02: %s(%s), \x02\x0304Seeders\x03\x02: %s, \x02\x0304Magnet Link:\x03\02: %s' % (na1[0], ty1[0], ty11[0], se1[0], mag1, na2[0], ty2[0], ty22[0], se2[0], mag2, na3[0], ty3[0], ty33[0], se3[0], mag3))
    tpb = wrap(tpb, [many('something')])


Class = TPB


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
