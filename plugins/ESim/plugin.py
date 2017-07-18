###
# Copyright (c) 2013, KG-Bot
# All rights reserved.
#
#
###
	

import re
import json
import urllib2
import urllib
import supybot.schedule as schedule
import datetime
import time
from operator import itemgetter
import locale

import string
 
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    from supybot.i18n import internationalizeDocstring
    _ = PluginInternationalization('ESim')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x
    internationalizeDocstring = lambda x:x

def flatten_subdicts(dicts, flat=None):
    """Change dict of dicts into a dict of strings/integers. Useful for
    using in string formatting."""
    if flat is None:
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
        threaded = True
        def citinfo(self, irc, msg, args, server, name):
            """<server> <name>
            Provides info about citizen."""
            if name is None:
                if server == 'secura':
                    with open('Esim/Profiles/Secura/%s.json' % msg.nick, 'r') as profile:
                        profile_dict = json.loads(profile.read())
                        id = profile_dict['id']
                        base = 'http://cscpro.org/%s/citizen/%s.json'
                        # data = json.load(utils.web.getUrlFd(base % (server, '%20'.join(name))))
                        data = json.load(utils.web.getUrlFd(base % (server, id)))
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
                        color = 3 if data['is_online'] else 4
                        party = data['party']['name']
                        partyid = data['party']['id']
                        id = data['id']
                        avatar = data['avatar_link']
                        irc.reply('\x034Name:\x03 \x030%i%s\x03, \x034Strength:\x03 %s, \x034Rank-name:\x03 %s, \x034Damage:\x03 %s, \x034Damage with:\x03 \x02\x0310q1\x03\x02-%s, \x02\x0310q2\x03\x02-%s, \x02\x0310q3\x03\x02-%s, \x02\x0310q4\x03\x02-%s, \x02\x0310q5\x03\x02-%s,' 
                            ' \x034Level:\x03 %s, \x034Age:\x03 %s, \x034Eco skill:\x03 %s, \x034News:\x03 %s, \x034MU:\x03 %s, \x034MU id:\x03 %s, \x034Party:\x03 %s, \x034Party id:\x03 %s, \x034ID:\x03 %s, \x034Avatar:\x03 %s' % (color, name, strength, rank, rankdmg, 
                            q1dmg, q2dmg, q3dmg, q4dmg, q5dmg, level, age, ecoSkill, news, mu, muid, party, partyid, id, avatar))
                elif server == 'primera':
                    with open('Esim/Profiles/Primera/%s.json' % msg.nick, 'r') as profile:
                        profile_dict = json.loads(profile.read())
                        id = profile_dict['id']
                        base = 'http://cscpro.org/%s/citizen/%s.json'
                        # data = json.load(utils.web.getUrlFd(base % (server, '%20'.join(name))))
                        data = json.load(utils.web.getUrlFd(base % (server, id)))
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
                        color = 3 if data['is_online'] else 4
                        party = data['party']['name']
                        partyid = data['party']['id']
                        id = data['id']
                        avatar = data['avatar_link']
                        irc.reply('\x034Name:\x03 \x030%i%s\x03, \x034Strength:\x03 %s, \x034Rank-name:\x03 %s, \x034Damage:\x03 %s, \x034Damage with:\x03 \x02\x0310q1\x03\x02-%s, \x02\x0310q2\x03\x02-%s, \x02\x0310q3\x03\x02-%s, \x02\x0310q4\x03\x02-%s, \x02\x0310q5\x03\x02-%s,' 
                            ' \x034Level:\x03 %s, \x034Age:\x03 %s, \x034Eco skill:\x03 %s, \x034News:\x03 %s, \x034MU:\x03 %s, \x034MU id:\x03 %s, \x034Party:\x03 %s, \x034Party id:\x03 %s, \x034ID:\x03 %s, \x034Avatar:\x03 %s' % (color, name, strength, rank, rankdmg, 
                            q1dmg, q2dmg, q3dmg, q4dmg, q5dmg, level, age, ecoSkill, news, mu, muid, party, partyid, id, avatar))
                elif server == 'suna':
                    with open('Esim/Profiles/Secura/%s.json' % msg.nick, 'r') as profile:
                        profile_dict = json.loads(profile.read())
                        id = profile_dict['id']
                        base = 'http://cscpro.org/%s/citizen/%s.json'
                        # data = json.load(utils.web.getUrlFd(base % (server, '%20'.join(name))))
                        data = json.load(utils.web.getUrlFd(base % (server, id)))
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
                        color = 3 if data['is_online'] else 4
                        party = data['party']['name']
                        partyid = data['party']['id']
                        id = data['id']
                        avatar = data['avatar_link']
                        irc.reply('\x034Name:\x03 \x030%i%s\x03, \x034Strength:\x03 %s, \x034Rank-name:\x03 %s, \x034Damage:\x03 %s, \x034Damage with:\x03 \x02\x0310q1\x03\x02-%s, \x02\x0310q2\x03\x02-%s, \x02\x0310q3\x03\x02-%s, \x02\x0310q4\x03\x02-%s, \x02\x0310q5\x03\x02-%s,' 
                            ' \x034Level:\x03 %s, \x034Age:\x03 %s, \x034Eco skill:\x03 %s, \x034News:\x03 %s, \x034MU:\x03 %s, \x034MU id:\x03 %s, \x034Party:\x03 %s, \x034Party id:\x03 %s, \x034ID:\x03 %s, \x034Avatar:\x03 %s' % (color, name, strength, rank, rankdmg, 
                            q1dmg, q2dmg, q3dmg, q4dmg, q5dmg, level, age, ecoSkill, news, mu, muid, party, partyid, id, avatar))
                else:
                    irc.reply("You didn't provide any valid e-Sim server.")
            else:
                base = 'http://cscpro.org/%s/citizen/%s.json'
                data = json.load(utils.web.getUrlFd(base % (server, '%20'.join(name))))
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
                color = 3 if data['is_online'] else 4
                party = data['party']['name']
                partyid = data['party']['id']
                id = data['id']
                avatar = data['avatar_link']
                irc.reply('\x034Name:\x03 \x030%i%s\x03, \x034Strength:\x03 %s, \x034Rank-name:\x03 %s, \x034Damage:\x03 %s, \x034Damage with:\x03 \x02\x0310q1\x03\x02-%s, \x02\x0310q2\x03\x02-%s, \x02\x0310q3\x03\x02-%s, \x02\x0310q4\x03\x02-%s, \x02\x0310q5\x03\x02-%s,' 
                    ' \x034Level:\x03 %s, \x034Age:\x03 %s, \x034Eco skill:\x03 %s, \x034News:\x03 %s, \x034MU:\x03 %s, \x034MU id:\x03 %s, \x034Party:\x03 %s, \x034Party id:\x03 %s, \x034ID:\x03 %s, \x034Avatar:\x03 %s' % (color, name, strength, rank, rankdmg, 
                    q1dmg, q2dmg, q3dmg, q4dmg, q5dmg, level, age, ecoSkill, news, mu, muid, party, partyid, id, avatar))
        citinfo = wrap(citinfo, ['something', optional(many('something'))])
		
        def battinfo(self, irc, msg, args, server, battle, round):
            """<server> <battle-id> [<round>]

            Gives info about <battle-id>, you can specify [<round>] if you want to see info about some round."""
            base = 'http://cscpro.org/%s/battle/%s-%s.json'
            data = json.load(utils.web.getUrlFd(base % (server, battle, round)))
            status = data['status']
            region = data['region']['name']
            attacker = data['attacker']['name']
            atthero = data['attacker']['hero']
            admg = data['attacker']['damage']
            aproc = data['attacker']['bar']
            defender = data['defender']['name']
            defhero = data['defender']['hero']
            ddmg = data['defender']['damage']
            dproc = data['defender']['bar']
            durationh = data['time']['hour']
            durationm = data['time']['minute']
            durations = data['time']['second']
            round = data['round']
            irc.reply('\x034Status:\x03 %s, \x034Region:\x03 %s, \x0310Attacker name:\x03 %s, \x0310Attacker hero:\x03 http://%s.e-sim.org/profile.html?id=%s, \x0310Damage done by attacker:\x03 %s, \x0310Attacker damage in procents:\x03 %s'
                ' \x037Defender name:\x03 %s, \x037Defender hero:\x03 http://%s.e-sim.org/profile.html?id=%s, \x037Damage done by defender:\x03 %s, \x037Defender damage in procents:\x03 %s'
                ' \x034Battle duration:\x03 %sh, %sm, %ss, \x034Battle round:\x03 %s' % (status, region, attacker, server, atthero, admg, aproc, defender, server, defhero, ddmg, dproc, durationh, durationm, durations, round))
        battinfo = wrap(battinfo, ['something', 'int', optional('int')])
		
        def doinfo(self, irc, msg, args, server, id):
            """<server> <id>
            
            Provides info about MU and daily orders"""
            base = 'http://cscpro.org/%s/units/%s.json'
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
            base = 'http://cscpro.org/%s/party/%s-%s.json'
            page = page or 1
            data = json.load(utils.web.getUrlFd(base % (server, id, page)))
            partyid = data['party']['id']
            partyname = data['party']['name']
            partyava = data['party']['avatar']
            partymem = data['party']['member']
            leaderid = data['leader']['id']
            leadername = data['leader']['name']
            irc.reply('\x034Party name:\x03 %s, \x034Party ID:\x03 %s, \x034Number of members:\x03 %s, \x034Party avatar:\x03 %s , \x034Leader ID:\x03 %s, \x034Leader name:\x03 %s' % (partyname, partyid, partymem, partyava, leaderid, leadername))
        partyinfo = wrap(partyinfo, ['something', 'int', optional('int')])
		
        def medals(self, irc, msg, args, server, name):
            """<primera | secura> <name>
            
            Gives info about medals"""
            if name is None:
                if server == 'secura':
                    try:
                        with open('Esim/Profiles/Secura/%s.json' % msg.nick, 'r') as profile:
                            profile_dict = json.loads(profile.read())
                            id = profile_dict['id']
                            # base = ('http://cscpro.org/%s/citizen/%s.json' % (server, '%20'.join(name)))
                            base = ('http://cscpro.org/%s/citizen/%s.json' % (server, id))
                            bata = json.load(utils.web.getUrlFd(base))
                            nam = bata['name']
                            medals = bata['medal']
                            medadict = dict(i.items()[0] for i in medals)
                            medasum = sum(medadict.values())
                            congressman = medadict.values()[7]
                            president = medadict.values()[6]
                            ss = medadict.values()[4]
                            sb = medadict.values()[5]
                            mm = medadict.values()[0]
                            hw = medadict.values()[1]
                            bh = medadict.values()[3]
                            rh = medadict.values()[8]
                            tester = medadict.values()[2]
                            irc.reply('%s has the following medal(s): Congressman: \x02%s\x02, President: \x02%s\x02, Super Soldier: \x02%s\x02, Society Builder: \x02%s\x02, Media Mogul: \x02%s\x02, Hard Worker: \x02%s\x02, Battle Hero: \x02%s\x02, Resistance Hero: \x02%s\x02, Tester: \x02%s\x02. Total number of medals is: \x02%s\x02.' % (nam, congressman, president, ss, sb, mm, hw, bh, rh, tester, medasum))
                    except IOError:
                        irc.reply("You didn't linked any profile from Secura server with your IRC nick.")
                elif server == 'primera':
                    try:
                        with open('Esim/Profiles/Primera/%s.json' % msg.nick, 'r') as profile:
                            profile_dict = json.loads(profile.read())
                            id = profile_dict['id']
                            # base = ('http://cscpro.org/%s/citizen/%s.json' % (server, '%20'.join(name)))
                            base = ('http://cscpro.org/%s/citizen/%s.json' % (server, id))
                            bata = json.load(utils.web.getUrlFd(base))
                            nam = bata['name']
                            medals = bata['medal']
                            medadict = dict(i.items()[0] for i in medals)
                            medasum = sum(medadict.values())
                            congressman = medadict.values()[7]
                            president = medadict.values()[6]
                            ss = medadict.values()[4]
                            sb = medadict.values()[5]
                            mm = medadict.values()[0]
                            hw = medadict.values()[1]
                            bh = medadict.values()[3]
                            rh = medadict.values()[8]
                            tester = medadict.values()[2]
                            irc.reply('%s has the following medal(s): Congressman: \x02%s\x02, President: \x02%s\x02, Super Soldier: \x02%s\x02, Society Builder: \x02%s\x02, Media Mogul: \x02%s\x02, Hard Worker: \x02%s\x02, Battle Hero: \x02%s\x02, Resistance Hero: \x02%s\x02, Tester: \x02%s\x02. Total number of medals is: \x02%s\x02.' % (nam, congressman, president, ss, sb, mm, hw, bh, rh, tester, medasum))
                    except IOError:
                        irc.reply("You didn't linked any profile from Secura server with your IRC nick.")
                elif server == 'suna':
                    try:
                        with open('Esim/Profiles/Suna/%s.json' % msg.nick, 'r') as profile:
                            profile_dict = json.loads(profile.read())
                            id = profile_dict['id']
                            # base = ('http://cscpro.org/%s/citizen/%s.json' % (server, '%20'.join(name)))
                            base = ('http://cscpro.org/%s/citizen/%s.json' % (server, id))
                            bata = json.load(utils.web.getUrlFd(base))
                            nam = bata['name']
                            medals = bata['medal']
                            medadict = dict(i.items()[0] for i in medals)
                            medasum = sum(medadict.values())
                            congressman = medadict.values()[7]
                            president = medadict.values()[6]
                            ss = medadict.values()[4]
                            sb = medadict.values()[5]
                            mm = medadict.values()[0]
                            hw = medadict.values()[1]
                            bh = medadict.values()[3]
                            rh = medadict.values()[8]
                            tester = medadict.values()[2]
                            irc.reply('%s has the following medal(s): Congressman: \x02%s\x02, President: \x02%s\x02, Super Soldier: \x02%s\x02, Society Builder: \x02%s\x02, Media Mogul: \x02%s\x02, Hard Worker: \x02%s\x02, Battle Hero: \x02%s\x02, Resistance Hero: \x02%s\x02, Tester: \x02%s\x02. Total number of medals is: \x02%s\x02.' % (nam, congressman, president, ss, sb, mm, hw, bh, rh, tester, medasum))
                    except IOError:
                        irc.reply("You didn't linked any profile from Secura server with your IRC nick.")
                else:
                    irc.reply("You didn't provide any valid e-Sim server.")
            else:
                base = ('http://cscpro.org/%s/citizen/%s.json' % (server, '%20'.join(name)))
                bata = json.load(utils.web.getUrlFd(base))
                nam = bata['name']
                medals = bata['medal']
                medadict = dict(i.items()[0] for i in medals)
                medasum = sum(medadict.values())
                congressman = medadict.values()[7]
                president = medadict.values()[6]
                ss = medadict.values()[4]
                sb = medadict.values()[5]
                mm = medadict.values()[0]
                hw = medadict.values()[1]
                bh = medadict.values()[3]
                rh = medadict.values()[8]
                tester = medadict.values()[2]
                irc.reply('%s has the following medal(s): Congressman: \x02%s\x02, President: \x02%s\x02, Super Soldier: \x02%s\x02, Society Builder: \x02%s\x02, Media Mogul: \x02%s\x02, Hard Worker: \x02%s\x02, Battle Hero: \x02%s\x02, Resistance Hero: \x02%s\x02, Tester: \x02%s\x02. Total number of medals is: \x02%s\x02.' % (nam, congressman, president, ss, sb, mm, hw, bh, rh, tester, medasum))
        medals = wrap(medals, ['something', optional(many('something'))])

        def battles(self, irc, msg, args, server):
            """<server>

            Returns all active battles on <server>"""
            base = ('http://cscpro.org/%s/battles/1.json' % (server))
            data = json.load(utils.web.getUrlFd(base))
            battle_ids = []
            for battle in data.keys():
                battle_ids.append(data[battle]['id'])
            irc.reply('Active battles are: %s' % ', '.join(battle_ids))
        battles = wrap(battles, ['something'])

        def partymem(self, irc, msg, args, server, id, page):
            """<server> <party id> <page>

            Gives list of party members"""
            base = ('http://cscpro.org/%s/party/%s-%s.json' % (server, id, page))
            data = json.load(utils.web.getUrlFd(base))
            members = [', '.join(['%s: %s' % x for x in d.items()]) for d in data['members']]
            irc.reply('This party has following members: %s' % ('\x0310<=====>\x03'.join(members)))
        partymem = wrap(partymem, ['something', 'something', 'something'])

        def monex(self, irc, msg, args, server, buy, sell):
            """<server> <buy> <sell>

            Gives info about offers on monetary market, <buy> is currency that you want to buy, and <sell> is currency you want to sell, currency codes can be viewed here 'http://tinyurl.com/qgzmtmj'."""
            try:
                base = ('http://cscpro.org/%s/exchange/%s-%s.json' % (server, buy, sell))
                data = json.load(utils.web.getUrlFd(base))
                seller = data['offer'][0]['seller']['name'] # Seller name
                seller_id = data['offer'][0]['seller']['id'] # Seller ID
                amount = data['offer'][0]['amount']
                rate = data['offer'][0]['rate']
                irc.reply('Seler name/ID: \x02%s/%s\x02, Rate: \x02%s\x02, Amount: \x02%s\x02' % (seller, seller_id, amount, rate))
            except:
                irc.reply('Wrong currency or no server specified.')
        monex = wrap(monex, ['something', 'something', 'something'])

        def elink(self, irc, msg, args, server, name):
            """<name>

            Return link for <name>."""
            if name is None:
                if server == 'secura':
                    try:
                        with open('Esim/Profiles/Secura/%s.json' % msg.nick, 'r') as profile:
                            profile_dict = json.loads(profile.read())
                            id = profile_dict['id']
                            # base = ('http://cscpro.org/%s/citizen/%s.json' % (server, '%20'.join(name)))
                            base = ('http://cscpro.org/%s/citizen/%s.json' % (server, id))
                            data = json.load(utils.web.getUrlFd(base))
                            # id = data['id']
                            na = data['name']
                            irc.reply("%s's link is http://secura.e-sim.org/profile.html?id=%s" % (na, id))
                    except IOError:
                        irc.reply("You didn't linked any profile from Secura server with your IRC nick.")
                elif server == 'primera':
                    try:
                        with open('Esim/Profiles/Primera/%s.json' % msg.nick, 'r') as profile:
                            profile_dict = json.loads(profile.read())
                            id = profile_dict['id']
                            # base = ('http://cscpro.org/%s/citizen/%s.json' % (server, '%20'.join(name)))
                            base = ('http://cscpro.org/%s/citizen/%s.json' % (server, id))
                            data = json.load(utils.web.getUrlFd(base))
                            # id = data['id']
                            na = data['name']
                            irc.reply("%s's link is http://secura.e-sim.org/profile.html?id=%s" % (na, id))
                    except IOError:
                        irc.reply("You didn't linked any profile from Primera server with your IRC nick.")
                elif server == 'suna':
                    try:
                        with open('Esim/Profiles/Suna/%s.json' % msg.nick, 'r') as profile:
                            profile_dict = json.loads(profile.read())
                            id = profile_dict['id']
                            # base = ('http://cscpro.org/%s/citizen/%s.json' % (server, '%20'.join(name)))
                            base = ('http://cscpro.org/%s/citizen/%s.json' % (server, id))
                            data = json.load(utils.web.getUrlFd(base))
                            # id = data['id']
                            na = data['name']
                            irc.reply("%s's link is http://secura.e-sim.org/profile.html?id=%s" % (na, id))
                    except IOError:
                        irc.reply("You didn't linked any profile from Suna server with your IRC nick.")
                else:
                    irc.reply("You didn't provide any valid e-Sim server.")
            else:
                base = ('http://cscpro.org/%s/citizen/%s.json' % (server, '%20'.join(name)))
                data = json.load(utils.web.getUrlFd(base))
                id = data['id']
                na = data['name']
                irc.reply("%s's link is http://secura.e-sim.org/profile.html?id=%s" % (na, id))
        elink = wrap(elink, ['something', optional(many('something'))])

        def simid(self, irc, msg, args, server, id):
            """<profile id>

            Links your profile with IRC nick."""
            nick = msg.nick
            profile_dict = {}
            profile_dict['id'] = id
            if id:
                if server == "secura":
                    with open('Esim/Profiles/Secura/%s.json' % nick, 'w') as profile:
                        profile.write(json.dumps(profile_dict))
                        irc.reply("You have successfully linked your Secura profile with your IRC nick.")
                elif server == "primera":
                    with open('Esim/Profiles/Primera/%s.json' % nick, 'w') as profile:
                        profile.write(json.dumps(profile_dict))
                        irc.reply("You have successfully linked your Primera profile with your IRC nick.")
                elif server == "suna":
                    with open('Esim/Profiles/Secura/%s.json' % nick, 'w') as profile:
                        profile.write(json.dumps(profile_dict))
                        irc.reply("You have successfully linked your Secura profile with your IRC nick.")
                else:
                    irc.reply("You didn't provide any valid server for linking.")
            else:
                irc.reply("You didn't provide any valid ID for linking.")
        simid = wrap(simid, ['something', 'int'])

        def return_battle_info(self, server, battle):
            base = 'http://cscpro.org/%s/battle/%s.json'
            data = json.load(utils.web.getUrlFd(base % (server, battle)))
            return data

        def battles_list(self, server):
            base = ('http://cscpro.org/%s/battles/1.json' % (server))
            data = json.load(utils.web.getUrlFd(base))
            battle_ids = []
            battles = data['battles']
            battle_len = len(battles)
            battle_minus_1 = battle_len - 1
            for i in xrange(battle_minus_1):
                battle_ids.append(battles[i]['id'])
            return battle_ids

        def transform_to_seconds(self, minutes):
            seconds = minutes * 60
            return seconds

        def stop_previous_task(self, task):
            try:
                schedule.removeEvent(task)
                return 'Stopped'
                pass
            except:
                pass

        def track(self, irc, msg, args, server, battle, minutes):
            """<server> <battle> <minutes>

            Starts watching battle and returning info every <minutes> minutes."""
            channel = msg.args[0]
            schedule_name = '%s-esim-battle-track' % channel
            self.stop_previous_task(schedule_name)
            if channel.startswith('#'):
                opers = irc.state.channels[channel].ops
                nick = msg.nick
                if nick not in opers:
                    irc.reply("Only channel ops can use this command.")
                else:
                    if minutes < 5 or minutes > 10:
                        irc.reply("You can't use minutes lower than 5 or higher than 10.")
                    else:
                        seconds = self.transform_to_seconds(minutes)
                        if server == "suna":
                            battles = self.battles_list(server)
                            if battle in battles:
                                get_battle_info = self.return_battle_info(server, battle)
                                if get_battle_info['defender']['name']:
                                    def start_collecting():
                                        data = self.return_battle_info(server, battle)
                                        status = data['status']
                                        if status == 'active':
                                            region = data['region']['name']
                                            attacker = data['attacker']['name']
                                            atthero = data['attacker']['hero']
                                            admg = data['attacker']['damage']
                                            aproc = data['attacker']['bar']
                                            defender = data['defender']['name']
                                            defhero = data['defender']['hero']
                                            ddmg = data['defender']['damage']
                                            dproc = data['defender']['bar']
                                            durationh = data['time']['hour']
                                            durationm = data['time']['minute']
                                            durations = data['time']['second']
                                            round = data['round']
                                            irc.reply('\x034Status:\x03 %s, \x034Region:\x03 %s, \x0310Attacker name:\x03 %s, \x0310Attacker hero:\x03 http://%s.e-sim.org/profile.html?id=%s, \x0310Damage done by attacker:\x03 %s, \x0310Attacker damage in procents:\x03 %s'
                                                ' \x037Defender name:\x03 %s, \x037Defender hero:\x03 http://%s.e-sim.org/profile.html?id=%s, \x037Damage done by defender:\x03 %s, \x037Defender damage in procents:\x03 %s'
                                                ' \x034Battle duration:\x03 %sh, %sm, %ss, \x034Battle round:\x03 %s' % (status, region, attacker, server, atthero, locale.format('%d', admg, True), aproc, defender, server, defhero, locale.format('%d', ddmg, True), dproc, durationh, durationm, durations, round))
                                        else:
                                            irc.reply("This battle is over, tracking is stopped.")
                                    schedule.addPeriodicEvent(start_collecting, seconds, schedule_name)
                                else:
                                    irc.reply("There was some internal API problem, this isn't available now, try again later.")
                            else:
                                self.stop_previous_task(schedule_name)
                                irc.reply("This battle is already finished, I won't track it.")
                        elif server == "primera":
                            battles = self.battles_list(server)
                            if battle in battles:
                                get_battle_info = self.return_battle_info(server, battle)
                                if get_battle_info['defender']['name']:
                                    def start_collecting():
                                        data = self.return_battle_info(server, battle)
                                        status = data['status']
                                        if status == 'active':
                                            region = data['region']['name']
                                            attacker = data['attacker']['name']
                                            atthero = data['attacker']['hero']
                                            admg = data['attacker']['damage']
                                            aproc = data['attacker']['bar']
                                            defender = data['defender']['name']
                                            defhero = data['defender']['hero']
                                            ddmg = data['defender']['damage']
                                            dproc = data['defender']['bar']
                                            durationh = data['time']['hour']
                                            durationm = data['time']['minute']
                                            durations = data['time']['second']
                                            round = data['round']
                                            irc.reply('\x034Status:\x03 %s, \x034Region:\x03 %s, \x0310Attacker name:\x03 %s, \x0310Attacker hero:\x03 http://%s.e-sim.org/profile.html?id=%s, \x0310Damage done by attacker:\x03 %s, \x0310Attacker damage in procents:\x03 %s'
                                                ' \x037Defender name:\x03 %s, \x037Defender hero:\x03 http://%s.e-sim.org/profile.html?id=%s, \x037Damage done by defender:\x03 %s, \x037Defender damage in procents:\x03 %s'
                                                ' \x034Battle duration:\x03 %sh, %sm, %ss, \x034Battle round:\x03 %s' % (status, region, attacker, server, atthero, locale.format('%d', admg, True), aproc, defender, server, defhero, locale.format('%d', ddmg, True), dproc, durationh, durationm, durations, round))
                                        else:
                                            self.stop_previous_task(schedule_name)
                                            irc.reply("This battle is over, tracking is stopped.")
                                    schedule.addPeriodicEvent(start_collecting, seconds, schedule_name)
                                else:
                                    irc.reply("There was some internal API problem, this isn't available now, try again later.")
                            else:
                                irc.reply("This battle is already finished, I won't track it.")
                        elif server == "ssecura":
                            battles = self.battles_list(server)
                            if battle in battles:
                                get_battle_info = self.return_battle_info(server, battle)
                                if get_battle_info['defender']['name']:
                                    def start_collecting():
                                        data = self.return_battle_info(server, battle)
                                        status = data['status']
                                        if status == 'active':
                                            region = data['region']['name']
                                            attacker = data['attacker']['name']
                                            atthero = data['attacker']['hero']
                                            admg = data['attacker']['damage']
                                            aproc = data['attacker']['bar']
                                            defender = data['defender']['name']
                                            defhero = data['defender']['hero']
                                            ddmg = data['defender']['damage']
                                            dproc = data['defender']['bar']
                                            durationh = data['time']['hour']
                                            durationm = data['time']['minute']
                                            durations = data['time']['second']
                                            round = data['round']
                                            irc.reply('\x034Status:\x03 %s, \x034Region:\x03 %s, \x0310Attacker name:\x03 %s, \x0310Attacker hero:\x03 http://%s.e-sim.org/profile.html?id=%s, \x0310Damage done by attacker:\x03 %s, \x0310Attacker damage in procents:\x03 %s'
                                                ' \x037Defender name:\x03 %s, \x037Defender hero:\x03 http://%s.e-sim.org/profile.html?id=%s, \x037Damage done by defender:\x03 %s, \x037Defender damage in procents:\x03 %s'
                                                ' \x034Battle duration:\x03 %sh, %sm, %ss, \x034Battle round:\x03 %s' % (status, region, attacker, server, atthero, locale.format('%d', admg, True), aproc, defender, server, defhero, locale.format('%d', ddmg, True), dproc, durationh, durationm, durations, round))
                                        else:
                                            self.stop_previous_task(schedule_name)
                                            irc.reply("This battle is over, tracking is stopped.")
                                    schedule.addPeriodicEvent(start_collecting, seconds, schedule_name)
                                else:
                                    irc.reply("There was some internal API problem, this isn't available now, try again later.")
                            else:
                                irc.reply("This battle is already finished, I won't track it.")
                        else:
                            irc.reply("You've given me invalid server and I can't find anything about it.")
            else:
                irc.reply("This channel is available only on channel.")
        track = wrap(track, ['something', 'int', 'int'])

        def stoptrack(self, irc, msg, args):
            """Takes no arguments

            Stops battle tracker."""
            channel = msg.args[0]
            if channel.startswith('#'):
                opers = irc.state.channels[channel].ops
                nick = msg.nick
                if nick in opers:
                    schedule_name = '%s-esim-battle-track' % channel
                    stop_it = self.stop_previous_task(schedule_name)
                    if stop_it == 'Stopped':
                       irc.reply("Tracking stopped.")
                    else:
                       irc.reply("There was no tracker for this channel, so I couldn't stop it.")
                else:
                    irc.reply("You're not OP and you can't stop battle track.")
            else:
                irc.reply("This command is available only on channel.")
        stoptrack = wrap(stoptrack)

Class = ESim


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79: