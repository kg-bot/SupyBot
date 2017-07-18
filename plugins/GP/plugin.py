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
import json
import html2text
import urllib2
import os

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('GP')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class GP(callbacks.Plugin):
    """Add the help for "@plugin help GP" here
    This should describe *how* to use this plugin."""
    threaded = True

    def prio(self, irc, msg, args, opt, id):
        """[<opt>]

        Upisivanje/pregled/brisanje prioriteta (bitaka). Da pregledate bitke kucate samo +prio bez icega, za dodavanje bitke kucate +prio --add ID-bitke, za brisanje kucate +prio --del ID-bitke"""
        if '--add' in msg.args[1]:
            if id is not None:
                try:
                    url = 'http://www.cscpro.org/secura/battle/%s.json' % id
                    data = json.load(utils.web.getUrlFd(url))
                    attacker = data['attacker']['name']
                    defender = data['defender']['name']
                    region = data['region']['name']
                    with open('G:\supybot\eRep\GP\prio.json', 'r') as prio:
                        b = json.loads(prio.read())
                        if id in b:
                            irc.reply("Ova bitka je vec upisana u bazu, \x034NAPOMENA\x03: \x02Pre nego sto pokusate da upisete neku bitku u prio odradite komandu \x0310+prio\x03 beze opcija --add ili --del, da vidite trenutni sadrzaj prio bitaka")
                        else:
                            b.append(id)
                            with open('G:\supybot\eRep\GP\prio.json', 'w') as prio:
                                prio.write(json.dumps(b))
                                irc.reply("Bitka u regiji \x02%s\x02 - \x02%s vs %s\x02 je dodana u bazu." % (region, attacker, defender))
                except:
                    irc.reply("Ova bitka ne postoji.")
            else:
                irc.reply("Niste upisali ID bitke, kada koristite opciju --add ili --del morate da upisete i ID bitke.")
        elif '--del' in msg.args[1]:
            if id is not None:
                try:
                    url = 'http://www.cscpro.org/secura/battle/%s.json' % id
                    data = json.load(utils.web.getUrlFd(url))
                    attacker = data['attacker']['name']
                    defender = data['defender']['name']
                    region = data['region']['name']
                    with open('G:\supybot\eRep\GP\prio.json', 'r+') as prio:
                        b = json.loads(prio.read())
                        b.remove(id)
                        with open('G:\supybot\eRep\GP\prio.json', 'w') as prio:
                            prio.write(json.dumps(b))
                        irc.reply("Bitka u regiji \x02%s\x02 - \x02%s vs %s\x02 je obrisana iz baze." % (region, attacker, defender))
                except:
                    irc.reply("Ova bitka ne postoji u bazi.")
            else:
                irc.reply("Niste upisali ID bitke, kada koristite opciju --add ili --del morate da upisete i ID bitke.")
        else:
            with open('G:\supybot\eRep\GP\prio.json', 'r+') as prio:
                b = json.loads(prio.read())
                if b == []:
                    irc.reply("Trenutno nema upisanih prio bitaka")
                else:
                    irc.reply("Trenutno su u bazu upisane sledece bitke: %s" % ', '.join([', '.join(['%s' % v]) for v in b]))
    prio = wrap(prio, [optional('something'), optional('int')])

    def provera(self, irc, msg, args):
        """bez argumenata

        Proverava koliko je ko tenkova ispucao u toku dana"""
        # Here starts MU 136 (vss) check
        url = 'http://www.cscpro.org/secura/damage/136-1.json'
        data = json.load(utils.web.getUrlFd(url))
        members = data['members']
        memlen = len(members)
        for i in xrange(memlen):
            global soldier_name
            soldier_name = members[i]['name']
            x = {}
            x['name'] = soldier_name
            na = 'vss\soldiers\%s.json' % soldier_name
            with open('G:\supybot\eRep\GP\%s' % na, 'w') as erep:
                erep.write(json.dumps(x))
        irc.reply("Finished logging soldiers for military unit: \x02%s\x02." % data['army']['name'])
        with open('G:\supybot\eRep\GP\prio.json', 'r') as prio:
            b = json.loads(prio.read())
        for i in b:
            for l in xrange(1, 16):
                url = ('http://prvisajtzakuvanje.orgfree.com/showMU.php?MU=136&battle=%s&round=%s' % (i, l))
                url = urllib2.urlopen(url).read()
                b = html2text.html2text(url)
                global ba
                ba = ('vss\%s\%s-%s.txt' % ('battles', i, l))
                with open('G:\supybot\eRep\GP\%s' % ba, 'w') as info:
                    info.write(b)
        irc.reply("Finished writing info for battles and rounds")
        bats = ('vss\%s' % 'battles')
        files = os.listdir('G:\supybot\eRep\GP\%s' % bats)
        for i in files:
            with open('G:\supybot\eRep\GP\%s\%s' % (bats, i), 'r') as info:
                b = info.readlines()
                for l in b:
                    irc.reply(soldier_name)
                    if 'Q0' in l:
                        pass
                    elif soldier_name in l:
                        irc.reply(l)
    provera = wrap(provera)

    def sol(self, irc, msg, args):
        """none

        None"""
        url = 'http://www.cscpro.org/secura/damage/136-1.json'
        data = json.load(utils.web.getUrlFd(url))
        memberes = data['members']
        memlength = len(memberes)
        with open('G:\supybot\eRep\GP\prio.json', 'r') as prio:
            kaba = json.loads(prio.read())
        for borda in xrange(memlength):
            global soldier_name
            soldier_namer = memberes[borda]['id']
            for olas in kaba:
                for rola in xrange(1, 16):
                    irc.reply(rola)
                    urla = ('url=http://prvisajtzakuvanje.orgfree.com/showplayer.php?player=%s&battle=%s&round=%s' % (soldier_namer, olas, rola))
                    urlas = ('http://html2text.theinfo.org/?%s' % urla)
                    irc.reply(urlas)
                    urlis = urllib2.urlopen(urlas).read()
                    burdus = html2text.html2text(urlis)
                    with open('G:\supybot\eRep\GP\%s.txt' % soldier_namer, 'w') as sold:
                        sold.write(burdus)
        irc.reply("Done")
    sol = wrap(sol)

Class = GP


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
