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
import string
import re
from lxml import etree
from xml.etree.ElementTree import ElementTree
import cookielib
import urllib2

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Cyri')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Cyri(callbacks.Plugin):
    """Add the help for "@plugin help Cyri" here
    This should describe *how* to use this plugin."""
    threaded = True

    def req(self, irc, msg, args, game):
        """<Game name>

        Gives minimum system requirements for desired game"""
        game_search = urllib2.urlopen('http://gamesystemrequirements.com/search.php?q=%s&w=2&method=OR' % '_'.join(game)).read()
        ga = etree.HTML(game_search)
        game_link = ga.xpath('.//tr[15]/td[1]//a')
        gl = [', '.join(['%s' % e.get('href')]) for e in game_link]
        game = urllib2.urlopen('http://gamesystemrequirements.com/' + gl[0]).read()
        game = etree.HTML(game)
        game_title = game.xpath('/html/head/title')
        game_title = [', '.join(['%s' % e.text]) for e in game_title]
        game_cpu = game.xpath('.//tr[21]/td//b')
        game_cpu = [', '.join(['%s' % e.text]) for e in game_cpu]
        cpu_info = game.xpath('.//tr[21]/td[2]')
        cpu_info = [', '.join(['%s' % e.text]) for e in cpu_info]
        game_ram = game.xpath('.//tr[23]/td//b')
        game_ram = [', '.join(['%s' % e.text]) for e in game_ram]
        ram_info = game.xpath('.//tr[23]/td[2]')
        ram_info = [', '.join(['%s' % e.text]) for e in ram_info]
        game_vga = game.xpath('.//tr[25]/td//b')
        game_vga = [', '.join(['%s' % e.text]) for e in game_vga]
        vga_info = game.xpath('.//tr[25]/td[2]')
        vga_info = [', '.join(['%s' % e.text]) for e in vga_info]
        game_os = game.xpath('.//tr[28]/td//b')
        game_os = [', '.join(['%s' % e.text]) for e in game_os]
        os_info = game.xpath('.//tr[28]/td[2]')
        os_info = [', '.join(['%s' % e.text]) for e in os_info]
        game_hdd = game.xpath('.//tr[31]/td//b')
        game_hdd = [', '.join(['%s' % e.text]) for e in game_hdd]
        hdd_info = game.xpath('.//tr[31]/td[2]')
        hdd_info = [', '.join(['%s' % e.text]) for e in hdd_info]
        game_sound = game.xpath('.//tr[33]/td//b')
        game_sound = [', '.join(['%s' % e.text]) for e in game_sound]
        sound_info = game.xpath('.//tr[33]/td[2]')
        sound_info = [', '.join(['%s' % e.text]) for e in sound_info]
        irc.reply('\x02%s\x02, \x0310%s\x03: \x02%s\x02, \x0310%s\x03: \x02%s\x02, \x0310%s\x03: \x02%s\x02, \x0310%s\x03: \x02%s\x02, \x0310%s\x03: \x02%s\x02, \x0310%s\x03: \x02%s\x02' % (game_title, game_cpu, cpu_info, game_ram, ram_info, game_vga, vga_info, game_os, os_info, game_hdd, hdd_info, game_sound, sound_info))
    req = wrap(req, [many('something')])

    def bq(self, irc, msg, args, game):
        """not

        Give link"""
        kk = urllib2.urlopen('http://gamesystemrequirements.com/search.php?q=oblivion&w=2').read()
        with open('bq.txt', 'w') as k:
            k.write(kk)
        irc.reply('Done')
    bq = wrap(bq, ['something'])


Class = Cyri


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
