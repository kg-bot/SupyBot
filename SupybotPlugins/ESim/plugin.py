###
# Copyright (c) 2013, KG-Bot
# All rights reserved.
#
#
###
	

import re
import json

import string
 
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('ESim')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

def flatten_subdicts(dicts, flat=None):
    """Change dict of dicts into a dict of strings/integers. Useful for
using in string formatting."""
    if flat is None:
        # Instanciate the dictionnary when the function is run and now when it
        # is declared; otherwise the same dictionnary instance will be kept and
        # it will have side effects (memory exhaustion, ...)
        flat = {}
    if isinstance(dicts, list):
        return flatten_subdicts(dict(enumerate(dicts)))
    elif isinstance(dicts, dict):
        for key, value in dicts.items():
            if isinstance(value, dict):
                value = dict(flatten_subdicts(value))
                for subkey, subvalue in value.items():
                    flat['%s__%s' % (key, subkey)] = subvalue
            else:
                flat[key] = value
        return flat
    else:
        return dicts


class Template(string.Template):
    # Original string.Template does not accept variables starting with a
    # number.
    idpattern = r'[_a-z0-9]+'
	
class ESim(callbacks.Plugin):
        """Add the help for "@plugin help ESim" here
        This should describe *how* to use this plugin."""
        threaded = True
       
        def citinfo(self, irc, msg, args, server, name):
            """<server> <name>
            Provides info about citizen."""
            base = 'http://api.cscpro.org/esim/%s/citizen/name/%s.json'
            data = json.load(utils.web.getUrlFd(base % (server, name)))
            name = data['name']
            strength = data['strength']
            rank = data['rank']['name']
            rankdmg = data['rank']['damage']
            q1dmg = data['hit']['q1']
            q2dmg = data['hit']['q2']
            q3dmg = data['hit']['q3']
            q4dmg = data['hit']['q4']
            q5dmg = data['hit']['q5']
            level = data['level']
            age = data['age']
            ecoSkill = data['economy_skill']
            news = data['newspaper']['name']
            mu = data['military_unit']['name']
            muid = data['military_unit']['id']
            online = data['is_online']
            ban = data['ban']
            party = data['party']['name']
            id = data['id']
            avatar = data['avatar_link']
            irc.reply('\x037Name:\x03 %s, \x034Strength:\x03 %s, \x034Rank-name:\x03 %s, \x034Damage:\x03 %s, \x034Damage with:\x03 \x02\x0310q1\x03\x02-%s, \x02\x0310q2\x03\x02-%s, \x02\x0310q3\x03\x02-%s, \x02\x0310q4\x03\x02-%s, \x02\x0310q5\x03\x02-%s,' 
                ' \x034Level:\x03 %s, \x034Age:\x03 %s, \x034Eco skill:\x03 %s, \x034News:\x03 %s, \x034MU:\x03 %s, \x034MU id:\x03 %sx034Online:\x03 %s, \x034Ban:\x03 %s, \x034Party:\x03 %s, \x034ID:\x03 %s, \x034Avatar:\x03 %s' % (name, strength, rank, rankdmg, 
                q1dmg, q2dmg, q3dmg, q4dmg, q5dmg, level, age, ecoSkill, news, mu, muid, online, ban, party, id, avatar))
        citinfo = wrap(citinfo, ['something', optional('something')])
		
        def battinfo(self, irc, msg, args, server, battle, round):
            """<server> <battle-id> [<round>]

            Gives info about <battle-id>, you can specifie [<round>] if you want to see info about some round."""
            base = 'http://api.cscpro.org/esim/%s/battle/%s/%s.json'
            data = json.load(utils.web.getUrlFd(base % (server, battle, round)))
            status = data['status']
            region = data['region']['name']
            attacker = data['attacker']['name']
            atthero = data['attacker']['hero']
            awin = data['attacker']['roundwin']
            admg = data['attacker']['damage']
            aproc = data['attacker']['bar']
            defender = data['defender']['name']
            defhero = data['defender']['hero']
            dwin = data['defender']['roundwin']
            ddmg = data['defender']['damage']
            dproc = data['defender']['bar']
            durationh = data['time']['hour']
            durationm = data['time']['minute']
            durations = data['time']['second']
            round = data['round']
            irc.reply('\x034Status:\x03 %s, \x034Region:\x03 %s, \x0310Attacker name:\x03 %s, \x0310Attacker hero:\x03 http://%s.e-sim.org/profile.html?id=%s, \x0310Rounds won by attacker:\x03 %s, \x0310Damage done by attacker:\x03 %s, \x0310Attacker damage in procents:\x03 %s'
                ' \x037Defender name:\x03 %s, \x037Defender hero:\x03 http://%s.e-sim.org/profile.html?id=%s, \x037Rounds won by defender:\x03 %s, \x037Damage done by defender:\x03 %s, \x037Defender damage in procents:\x03 %s'
                ' \x034Battle duration:\x03 %sh, %sm, %ss, \x034Battle round:\x03 %s' % (status, region, attacker, server, atthero, awin, admg, aproc, defender, server, defhero, dwin, ddmg, dproc, durationh, durationm, durations, round))
        battinfo = wrap(battinfo, ['something', 'int', optional('int')])
		
        def doinfo(self, irc, msg, args, server, id):
            """<server> <id>
            
            Provides info about MU and daily orders"""
            base = 'http://api.cscpro.org/esim/%s/units/%s.json'
            data = json.load(utils.web.getUrlFd(base % (server, id)))
            muname = data['army']['name']
            murank = data['army']['rank']
            totdamage = data['army']['damage']['total']
            toddamage = data['army']['damage']['today']
            memcurr = data['army']['member']['current']
            memmax = data['army']['member']['max']
            leadid = data['army']['leader']['id']
            leadname = data['army']['leader']['name']
            orderbatid = data['order']['battleid']
            orderreg = data['order']['region']
            orderside = data['order']['side']
            orderstat = data['order']['status']
            irc.reply('\x034MU name:\x03 %s, \x034MU rank:\x03 %s, \x034Total damage:\x03 %s, \x034Today damage:\x03 %s, \x034Current members:\x03 %s, \x034Max members:\x03 %s, \x034Leader id:\x03 %s, \x034Leader name:\x03 %s, \x034DO id:\x03 %s, \x034DO region:\x03 %s, \x034DO side:\x03 %s, \x034DO status:\x03 %s' % (muname, murank, totdamage, toddamage, memcurr, memmax, 
                leadid, leadname, orderbatid, orderreg, orderside, orderstat))
        doinfo = wrap(doinfo, ['something', 'int'])
		
        def partyinfo(self, irc, msg, args, server, id, page):
            """<server> <id> <page>
            
            Gives basic info about party"""
            base = 'http://api.cscpro.org/esim/%s/party/%s/%s.json'
            data = json.load(utils.web.getUrlFd(base % (server, id, page)))
            partyid = data['party']['id']
            partyname = data['party']['name']
            partyava = data['party']['avatar']
            partymem = data['party']['member']
            leaderid = data['leader']['id']
            leadername = data['leader']['name']
            irc.reply('\x034Party name:\x03 %s, \x034Party ID:\x03 %s, \x034Number of members:\x03 %s, \x034Party avatar:\x03 %s, \x034Leader ID:\x03 %s, \x034Leader name:\x03 %s' % (partyname, partyid, partymem, partyava, leaderid, leadername))
        partyinfo = wrap(partyinfo, ['something', 'int', 'int'])
			

Class = ESim


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79: