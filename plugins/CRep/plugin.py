###
# Copyright (c) 2013, Kg-Bot
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

import re
import urllib2
from xml.dom import minidom
from xml.dom.minidom import parseString

import supybot.conf as conf
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('CRep')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class CRep(callbacks.Plugin):
    """Add the help for "@plugin help CRep" here
    This should describe *how* to use this plugin."""
    threaded = True

    def cit(self, irc, msg, args, server, name):
        """<server> <name>

        Gives info about <name> (citizen ID or NAME goes here) on <server> (\x0310com\x03 \x02or\x02 \x0310net\x03)"""
        if name.isdigit():
            url = ('http://api.cyberrepublik.%s/citizens/%s' % (server, name))
            file = urllib2.urlopen(url)
            data = file.read()
            file.close()
            dom = parseString(data)
            xmlTag = dom.getElementsByTagName('citizen')[0]
            self.n = xmlTag.getElementsByTagName('name')[0].firstChild.data.strip() #citizen name
            self.xp = xmlTag.getElementsByTagName('exp')[0].firstChild.data.strip() #cit. experience
            self.bir = xmlTag.getElementsByTagName('birthday')[0].firstChild.data.strip() #date of creation
            self.lvl = xmlTag.getElementsByTagName('level')[0].firstChild.data.strip() #cit. level
        #MU skills below
            self.weapon = dom.getElementsByTagName('skill')[0] #weapon skill
            wpon = self.weapon.getElementsByTagName('points')[0].firstChild.data.strip() #weapon skill points
            self.tank = dom.getElementsByTagName('skill')[1] #tank skill
            tpon = self.tank.getElementsByTagName('points')[0].firstChild.data.strip() #tank skill points
            self.heli = dom.getElementsByTagName('skill')[2] #heli skill
            hpon = self.heli.getElementsByTagName('points')[0].firstChild.data.strip() #heli skill points
            self.mine = dom.getElementsByTagName('skill')[3] #mine skill
            mpon = self.mine.getElementsByTagName('points')[0].firstChild.data.strip() #mine skill points
        #End of the MU skills <=====> ECO skills below
            self.manu = dom.getElementsByTagName('skill')[4] #manufacture skill
            manu = self.manu.getElementsByTagName('points')[0].firstChild.data.strip() #manufacture skill points
            self.land = dom.getElementsByTagName('skill')[5] #land skill
            land = self.land.getElementsByTagName('points')[0].firstChild.data.strip() #land skill points
            self.cons = dom.getElementsByTagName('skill')[6] #Construction skill
            cons = self.cons.getElementsByTagName('points')[0].firstChild.data.strip() #Construction skill points
        #End of the ECO skills <=====> CS and residence info below
            self.residence = dom.getElementsByTagName('region')[0]
            region = self.residence.getElementsByTagName('name')[0].firstChild.data.strip() #residence region name
            regid = self.residence.getElementsByTagName('id')[0].firstChild.data.strip() #residence region id
            self.country = dom.getElementsByTagName('country')[0]
            country = self.country.getElementsByTagName('name')[0].firstChild.data.strip() #residence country name
            conid = self.country.getElementsByTagName('id')[0].firstChild.data.strip() #residence country id
		#CS and residence info ends here <=====> Politic party and military unit basic info
            party = dom.getElementsByTagName('party')[0].firstChild.data.strip() #Party name
            murank = dom.getElementsByTagName('military-rank')[0].firstChild.data.strip() #MU rank lvl
            totdmg = dom.getElementsByTagName('total-dmg')[0].firstChild.data.strip() #Total damage done
            tothit = dom.getElementsByTagName('total-hits')[0].firstChild.data.strip() #Total number of hits
            irc.reply('Name: \x02%s\x02, XP: \x02%s\x02, Birthday: \x02%s\x02, lvl: \x02%s\x02, \x02Military skill points\x02 ===>> Weapon pts: \x0310%s\x03, Tank pts: \x0307%s\x03, Heli pts: \x0309%s\x03 <<===, \x02Economy skill points\x02 ===>> Manu pts: \x0310%s\x03, Land pts: \x0307%s\x03, Cons pts: \x0309%s\x03 <<===, Residence region name: \x02%s\x02, Residence region ID: \x02%s\x02, Residence country name: \x02%s\x02, Residence country ID: \x02%s\x02, Party name: \x02%s\x02, MU rank: \x0310%s\x03, Total dmg: \x0310%s\x03, Total hits: \x0310%s\x03' % (self.n, self.xp, self.bir, self.lvl, wpon, tpon, hpon, manu, land, cons, region, regid, country, conid, party, murank, totdmg, tothit))
        else:
            url = ('http://api.cyberrepublik.%s/citizen_by_name/%s' % (server, name))
            file = urllib2.urlopen(url)
            data = file.read()
            file.close()
            dom = parseString(data)
            xmlTag = dom.getElementsByTagName('citizen')[0]
            self.n = xmlTag.getElementsByTagName('name')[0].firstChild.data.strip() #citizen name
            self.xp = xmlTag.getElementsByTagName('exp')[0].firstChild.data.strip() #cit. experience
            self.bir = xmlTag.getElementsByTagName('birthday')[0].firstChild.data.strip() #date of creation
            self.lvl = xmlTag.getElementsByTagName('level')[0].firstChild.data.strip() #cit. level
        #MU skills below
            self.weapon = dom.getElementsByTagName('skill')[0] #weapon skill
            wpon = self.weapon.getElementsByTagName('points')[0].firstChild.data.strip() #weapon skill points
            self.tank = dom.getElementsByTagName('skill')[1] #tank skill
            tpon = self.tank.getElementsByTagName('points')[0].firstChild.data.strip() #tank skill points
            self.heli = dom.getElementsByTagName('skill')[2] #heli skill
            hpon = self.heli.getElementsByTagName('points')[0].firstChild.data.strip() #heli skill points
        #End of the MU skills <=====> ECO skills below
            self.manu = dom.getElementsByTagName('skill')[4] #manufacture skill
            manu = self.manu.getElementsByTagName('points')[0].firstChild.data.strip() #manufacture skill points
            self.land = dom.getElementsByTagName('skill')[5] #land skill
            land = self.land.getElementsByTagName('points')[0].firstChild.data.strip() #land skill points
            self.cons = dom.getElementsByTagName('skill')[6] #Construction skill
            cons = self.cons.getElementsByTagName('points')[0].firstChild.data.strip() #Construction skill points
        #End of the ECO skills <=====> CS and residence info below
            self.residence = dom.getElementsByTagName('region')[0]
            region = self.residence.getElementsByTagName('name')[0].firstChild.data.strip() #residence region name
            regid = self.residence.getElementsByTagName('id')[0].firstChild.data.strip() #residence region id
            self.country = dom.getElementsByTagName('country')[0]
            country = self.country.getElementsByTagName('name')[0].firstChild.data.strip() #residence country name
            conid = self.country.getElementsByTagName('id')[0].firstChild.data.strip() #residence country id
		#CS and residence info ends here <=====> Politic party and military unit basic info
            party = dom.getElementsByTagName('party')[0].firstChild.data.strip() #Party name Party status
            murank = dom.getElementsByTagName('military-rank')[0].firstChild.data.strip() #MU rank lvl
            totdmg = dom.getElementsByTagName('total-dmg')[0].firstChild.data.strip() #Total damage done
            tothit = dom.getElementsByTagName('total-hits')[0].firstChild.data.strip() #Total number of hits
            irc.reply('Name: \x02%s\x02, XP: \x02%s\x02, Birthday: \x02%s\x02, lvl: \x02%s\x02, \x02Military skill points\x02 ===>> Weapon pts: \x0310%s\x03, Tank pts: \x0307%s\x03, Heli pts: \x0309%s\x03 <<===, \x02Economy skill points\x02 ===>> Manu pts: \x0310%s\x03, Land pts: \x0307%s\x03, Cons pts: \x0309%s\x03 <<===, Residence region name: \x02%s\x02, Residence region ID: \x02%s\x02, Residence country name: \x02%s\x02, Residence country ID: \x02%s\x02, Party name: \x02%s\x02, MU rank: \x0310%s\x03, Total dmg: \x0310%s\x03, Total hits: \x0310%s\x03' % (self.n, self.xp, self.bir, self.lvl, wpon, tpon, hpon, manu, land, cons, region, regid, country, conid, party, murank, totdmg, tothit)) 
    cit = wrap(cit, ['something', 'something'])

    def cmedals(self, irc, msg, args, server, name):
        """<server> <name>

        Gives info about <name> (citizen ID or NAME goes here) medals on <server> (\x0310com\x03 \x02or\x02 \x0310net\x03)"""
        if name.isdigit():			
            url = ('http://api.cyberrepublik.%s/citizens/%s' % (server, name))
            file = urllib2.urlopen(url)
            data = file.read()
            file.close()
            dom = parseString(data)
            citizen = dom.getElementsByTagName('name')[0].firstChild.data.strip()
            self.hw = dom.getElementsByTagName('medal')[0]
            hw = self.hw.getElementsByTagName('amount')[0].firstChild.data.strip() #Hard Worker medals number
            self.cm = dom.getElementsByTagName('medal')[1]
            cm = self.cm.getElementsByTagName('amount')[0].firstChild.data.strip() #Congress Member medals number
            self.cp = dom.getElementsByTagName('medal')[2]
            cp = self.cp.getElementsByTagName('amount')[0].firstChild.data.strip() #Country President medals number
            self.mm = dom.getElementsByTagName('medal')[3]
            mm = self.mm.getElementsByTagName('amount')[0].firstChild.data.strip() #Media Mogul medals number
            self.bh = dom.getElementsByTagName('medal')[4]
            bh = self.bh.getElementsByTagName('amount')[0].firstChild.data.strip() #Battle Hero medals number
            self.rh = dom.getElementsByTagName('medal')[5]
            rh = self.rh.getElementsByTagName('amount')[0].firstChild.data.strip() #Resistance Hero medals number
            self.ss = dom.getElementsByTagName('medal')[6]
            ss = self.ss.getElementsByTagName('amount')[0].firstChild.data.strip() #Super Soldier medals number
            self.sb = dom.getElementsByTagName('medal')[7]
            sb = self.sb.getElementsByTagName('amount')[0].firstChild.data.strip() #Society Builder medals number
            irc.reply('\x02%s\x02 has following medals: Hard Worker: \x02%s\x02, Congress Member: \x02%s\x02, Country President: \x02%s\x02, Media Mogul: \x02%s\x02, Battle Hero: \x02%s\x02, Resistance Hero: \x02%s\x02, Super Soldier: \x02%s\x02, Society Builder: \x02%s\x02' % (citizen, hw, cm, cp, mm, bh, rh, ss, sb))
        else:
            url = ('http://api.cyberrepublik.%s/citizen_by_name/%s' % (server, name))
            file = urllib2.urlopen(url)
            data = file.read()
            file.close()
            dom = parseString(data)
            citizen = dom.getElementsByTagName('name')[0].firstChild.data.strip()
            self.hw = dom.getElementsByTagName('medal')[0]
            hw = self.hw.getElementsByTagName('amount')[0].firstChild.data.strip() #Hard Worker medals number
            self.cm = dom.getElementsByTagName('medal')[1]
            cm = self.cm.getElementsByTagName('amount')[0].firstChild.data.strip() #Congress Member medals number
            self.cp = dom.getElementsByTagName('medal')[2]
            cp = self.cp.getElementsByTagName('amount')[0].firstChild.data.strip() #Country President medals number
            self.mm = dom.getElementsByTagName('medal')[3]
            mm = self.mm.getElementsByTagName('amount')[0].firstChild.data.strip() #Media Mogul medals number
            self.bh = dom.getElementsByTagName('medal')[4]
            bh = self.bh.getElementsByTagName('amount')[0].firstChild.data.strip() #Battle Hero medals number
            self.rh = dom.getElementsByTagName('medal')[5]
            rh = self.rh.getElementsByTagName('amount')[0].firstChild.data.strip() #Resistance Hero medals number
            self.ss = dom.getElementsByTagName('medal')[6]
            ss = self.ss.getElementsByTagName('amount')[0].firstChild.data.strip() #Super Soldier medals number
            self.sb = dom.getElementsByTagName('medal')[7]
            sb = self.sb.getElementsByTagName('amount')[0].firstChild.data.strip() #Society Builder medals number
            irc.reply('\x02%s\x02 has following medals: Hard Worker: \x02%s\x02, Congress Member: \x02%s\x02, Country President: \x02%s\x02, Media Mogul: \x02%s\x02, Battle Hero: \x02%s\x02, Resistance Hero: \x02%s\x02, Super Soldier: \x02%s\x02, Society Builder: \x02%s\x02' % (citizen, hw, cm, cp, mm, bh, rh, ss, sb))
    cmedals = wrap(cmedals, ['something', 'something'])

    def clink(self, irc, msg, args, server, name):
        """[<server>] <name>

        Returns <id> (citizen ID or NAME goes here) link on <server> (\x0310com\x03 \x02or\x02 \x0310net\x03)"""
        serv = 'net' or server
        if name.isdigit():
            url = ('http://www.cyberrepublik.%s/en/citizens/%s' % (serv, name))
            file = urllib2.urlopen(url)
            data = file.read()
            file.close()
            dom = parseString(data)
            citizen = dom.getElementsByTagName('name')[0].firstChild.data.strip()
            uri = ('http://www.cyberrepublik.%s/en/profile/%s' % (serv, name))
            irc.reply('\x02%s\x02 link is: %s' % (citizen, uri))
        else:
            url = ('http://api.cyberrepublik.%s/citizen_by_name/%s' % (server, name))
            file = urllib2.urlopen(url)
            data = file.read()
            file.close()
            dom = parseString(data)
            citizen = dom.getElementsByTagName('citizen')[0]
            nam = citizen.getElementsByTagName('name')[0].firstChild.data.strip()
            id = citizen.getElementsByTagName('id')[0].firstChild.data.strip()
            irc.reply('\x02%s\x02 link is: http://www.cyberrepublik.%s/en/profile/%s' % (nam, server, id))
    clink = wrap(clink, [optional('anything'), 'something'])

    def cfc(self, irc, msg, args, server, name, wq, aq):
        """<server> <name> <weapon quality> <ammo quality>

        Calculates <name> (citizen ID or NAME goes here) possible damage on <server> (\x0310com\x03 \x02or\x02 \x0310net\x03)"""
        if name.isdigit():
            url = ('http://api.cyberrepublik.%s/dmg/%s/%s/%s' % (server, name, wq, aq))
            file = urllib2.urlopen(url)
            data = file.read()
            file.close()
            dom = parseString(data)
            uri = ('http://api.cyberrepublik.%s/citizens/%s' % (server, name))
            file = urllib2.urlopen(uri)
            bata = file.read()
            file.close()
            bom = parseString(bata)
            citizen = bom.getElementsByTagName('name')[0].firstChild.data.strip() 
            rank = dom.getElementsByTagName('rank')[0].firstChild.data.strip() # Military rank
            hs = dom.getElementsByTagName('skillH')[0].firstChild.data.strip() #Heli skill
            hd = dom.getElementsByTagName('dmgH')[0].firstChild.data.strip() #Heli damage
            ts = dom.getElementsByTagName('skillT')[0].firstChild.data.strip() #Tank skill
            td = dom.getElementsByTagName('dmgT')[0].firstChild.data.strip() #Tank damage
            gs = dom.getElementsByTagName('skillG')[0].firstChild.data.strip() #Gun skill
            gd = dom.getElementsByTagName('dmgW')[0].firstChild.data.strip() #Gun damage
            irc.reply('\x02%s\x02 is military rank \x02%s\x02, his skills are: Heli - \x0310%s\x03, Tank - \x0310%s\x03, Gun - \x0310%s\x03, and he hits: \x0307%s\x03 with Heli, \x0307%s\x03 with Tank, \x0307%s\x03 with Gun.' % (citizen, rank, hs, ts, gs, hd, td, gd))
        else:
            url = ('http://api.cyberrepublik.%s/citizen_by_name/%s' % (server, name))
            file = urllib2.urlopen(url)
            data = file.read()
            file.close()
            dom = parseString(data)
            citizen = dom.getElementsByTagName('citizen')[0]
            id = citizen.getElementsByTagName('id')[0].firstChild.data.strip()
            cit = citizen.getElementsByTagName('name')[0].firstChild.data.strip()
            uri = ('http://api.cyberrepublik.%s/dmg/%s/%s/%s' % (server, id, wq, aq))
            file = urllib2.urlopen(uri)
            bata = file.read()
            file.close()
            bom = parseString(bata)
            rank = bom.getElementsByTagName('rank')[0].firstChild.data.strip() # Military rank
            hs = bom.getElementsByTagName('skillH')[0].firstChild.data.strip() #Heli skill
            hd = bom.getElementsByTagName('dmgH')[0].firstChild.data.strip() #Heli damage
            ts = bom.getElementsByTagName('skillT')[0].firstChild.data.strip() #Tank skill
            td = bom.getElementsByTagName('dmgT')[0].firstChild.data.strip() #Tank damage
            gs = bom.getElementsByTagName('skillG')[0].firstChild.data.strip() #Gun skill
            gd = bom.getElementsByTagName('dmgW')[0].firstChild.data.strip() #Gun damage
            irc.reply('\x02%s\x02 is military rank \x02%s\x02, his skills are: Heli - \x0310%s\x03, Tank - \x0310%s\x03, Gun - \x0310%s\x03, and he hits: \x0307%s\x03 with Heli, \x0307%s\x03 with Tank, \x0307%s\x03 with Gun.' % (cit, rank, hs, ts, gs, hd, td, gd))
    cfc = wrap(cfc, ['something', 'something', 'int', 'int'])
Class = CRep


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
