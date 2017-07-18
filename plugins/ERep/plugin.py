###
# Copyright (c) 2013, KG-Bot
# Contributor - Crazy_Hospy
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
import time
import os
import re
import simplejson as json
import math
import string
import supybot.conf as conf
import locale
import supybot.schedule as schedule

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('ERep')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x
url = conf.supybot.plugins.ERep.url()
_profiles = 'plugins/ERep/Registar.json'
_error = "Ooooops, something went wrong. Please try again later."
_blue_delimeter = "\x02\x0310:::\x03\x02"
_red_delimeter = "\x02\x034:::\x03\x02"
_yellow_delimeter = "\x02\x038:::\x03\x02"
_white_delimeter = "\x02\x030:::\x03\x02"
_black_delimeter = "\x02\x031:::\x03\x02"
_green_delimeter = "\x02\x033:::\x03\x02"
_grey_delimeter = "\x02\x0314:::\x03\x02"
_dark_blue_delimeter = "\x02\x0312:::\x03\x02"

class ERep(callbacks.Plugin):
    """Add the help for "@plugin help ERep" here
    This should describe *how* to use this plugin."""
    threaded = True

    __Author__ = "Stefan Ninic"

    def read_profiles(self):
        with open(_profiles, 'r') as profiles:
            players = json.loads(profiles.read())
            return players

    def write_profile(self, irc, msg, profile, nick, citizen):
        with open(_profiles, 'w') as profiles:
            profiles.write(json.dumps(profile))
            irc.reply("You have successfully linked your IRC nick \x02%s\x02 with eRepublik citizen \x02%s\x02." % (nick, citizen))

    def remove_profile(self, irc, profile, citizen, id):
        with open(_profiles, 'w') as profiles:
            profiles.write(json.dumps(profile))
            irc.reply("\x02%s\x02 with id \x02%s\x02 is removed from database." % (citizen, id))

    def active_battles(self):
        base = '%sbattle/active.json'
        data = json.load(utils.web.getUrlFd(base % (url)))
        return data

    def battles(self, irc, msg, args):
        """<no arguments>

        Gives list of active battles"""
        #url = conf.supybot.plugins.ERep.url()
        #base = '%sbattle/active.json'
        #data = json.load(utils.web.getUrlFd(base % (url)))
        data = self.active_battles()
        if 'message' in data:
            irc.reply("Something terrible happened, please try again, if it won't show again contact my owner.")
        else:
            try:
                battles = []
                for battle in data:
                    battles.append(str(battle))
                irc.reply('Right now there are these active battles: \x02%s\x02, use \x02+battle <battle-ID>\x02 to see more info about specific battle.' % ', '.join(battles))
            except:
                irc.reply(_error)
    battles = wrap(battles)

    def battle(self, irc, msg, args, id):
        """<ID>

        Gives advanced info about battles. Use \x02+battles\x02 command to get list of available IDs."""
        data = self.active_battles()
        if id not in data:
            irc.reply("This battle is finished and I'm not giving info about finished battles.")
        else:
            base = json.load(utils.web.getUrlFd('%sbattle/%s.json' % (url, id)))
            if 'message' in base.keys():
                irc.reply(_error)
            else:
                try:
                    region_name = base['region']['name']
                    is_resistance = base['is_resistance']
                    country = base['region']['original_owner_country']['name']
                    link = base['url']
                    attacker = base['attacker']['country']['name']
                    attackerpts = base['attacker']['points']
                    attdiv1pts = base['attacker']['divisions']['1']['points']
                    attdiv1bar = '%.2f' % base['attacker']['divisions']['1']['bar']
                    attdiv1domination = base['attacker']['divisions']['1']['domination']
                    attdiv2pts = base['attacker']['divisions']['2']['points']
                    attdiv2bar = '%.2f' % base['attacker']['divisions']['2']['bar']
                    attdiv2domination = base['attacker']['divisions']['2']['domination']
                    attdiv3pts = base['attacker']['divisions']['3']['points']
                    attdiv3bar = '%.2f' % base['attacker']['divisions']['3']['bar']
                    attdiv3domination = base['attacker']['divisions']['3']['domination']
                    attdiv4pts = base['attacker']['divisions']['4']['points']
                    attdiv4bar = '%.2f' % base['attacker']['divisions']['4']['bar']
                    attdiv4domination = base['attacker']['divisions']['4']['domination']
                    defender = base['defender']['country']['name']
                    defenderpts = base['defender']['points']
                    defdiv1pts = base['defender']['divisions']['1']['points']
                    defdiv1bar = '%.2f' % base['defender']['divisions']['1']['bar']
                    defdiv1domination = base['defender']['divisions']['1']['domination']
                    defdiv2pts = base['defender']['divisions']['2']['points']
                    defdiv2bar = '%.2f' % base['defender']['divisions']['2']['bar']
                    defdiv2domination = base['defender']['divisions']['2']['domination']
                    defdiv3pts = base['defender']['divisions']['3']['points']
                    defdiv3bar = '%.2f' % base['defender']['divisions']['3']['bar']
                    defdiv3domination = base['defender']['divisions']['3']['domination']
                    defdiv4pts = base['defender']['divisions']['4']['points']
                    defdiv4bar = '%.2f' % base['defender']['divisions']['4']['bar']
                    defdiv4domination = base['defender']['divisions']['4']['domination'] 
                    #att = base['attacker']['divisions']['1']['top_fighters'][0] # full attacker dict
                    #attacker_name = att.values()[0] # attacker top fighter name
                    #attacker_dmg = att.values()[1]
                    #attac = attacker.values()[0]
                    if is_resistance != True:
                        irc.reply('Region: \x02\x03%s\x03\x02, Link: \x02%s\x02 %s Attacker Country: \x02%s\x02, Attacker Points; Total: \x02%s\x02, D1 Points/Bar/Domination: \x02%s %s %s% %s %s\x02, D2: \x02%s %s %s% %s %s\x02, D3: \x02%s %s %s% %s %s\x02, D4: \x02%s %s %s %s %s\x02 %s Defender Country: \x02%s\x02, Defender Points; Total: \x02%s\x02, D1: \x02%s %s %s %s %s\x02, D2: \x02%s %s %s %s %s\x02, D3: \x02%s %s %s %s %s\x02, D4: \x02%s %s %s %s %s\x02.' % (region_name, link, _red_delimeter, attacker, attackerpts, attdiv1pts, _grey_delimeter, attdiv1bar, _grey_delimeter, attdiv1domination, attdiv2pts, _grey_delimeter, attdiv2bar, _grey_delimeter, attdiv2domination, attdiv3pts, _grey_delimeter, attdiv3bar, _grey_delimeter, attdiv3domination, attdiv4pts, _grey_delimeter, attdiv4bar, _grey_delimeter, attdiv4domination, _yellow_delimeter, defender, defenderpts, defdiv1pts, _grey_delimeter, defdiv1bar, _grey_delimeter, defdiv1domination, defdiv2pts, _grey_delimeter, defdiv2bar, _grey_delimeter, defdiv2domination, defdiv3pts, _grey_delimeter, defdiv3bar, _grey_delimeter, defdiv3domination, defdiv4pts, _grey_delimeter, defdiv4bar, _grey_delimeter, defdiv4domination))
                    else:
                        irc.reply('[\x033RESISTANCE\x03] %s Region: \x02\x03%s\x03\x02, Link: \x02%s\x02 %s Attacker Country: \x02%s\x02, Attacker Points; Total: \x02%s\x02, D1 Points/Bar/Domination: \x02%s %s %s %s %s\x02, D2: \x02%s %s %s %s %s\x02, D3: \x02%s %s %s %s %s\x02, D4: \x02%s %s %s %s %s\x02 %s Defender Country: \x02%s\x02, Defender Points; Total: \x02%s\x02, D1: \x02%s %s %s %s %s\x02, D2: \x02%s %s %s %s %s\x02, D3: \x02%s %s %s %s %s\x02, D4: \x02%s %s %s %s %s\x02.' % (_blue_delimeter, region_name, link, _red_delimeter, attacker, attackerpts, attdiv1pts, _grey_delimeter, attdiv1bar, _grey_delimeter, attdiv1domination, attdiv2pts, _grey_delimeter, attdiv2bar, _grey_delimeter, attdiv2domination, attdiv3pts, _grey_delimeter, attdiv3bar, _grey_delimeter, attdiv3domination, attdiv4pts, _grey_delimeter, attdiv4bar, _grey_delimeter, attdiv4domination, _yellow_delimeter, defender, defenderpts, defdiv1pts, _grey_delimeter, defdiv1bar, _grey_delimeter, defdiv1domination, defdiv2pts, _grey_delimeter, defdiv2bar, _grey_delimeter, defdiv2domination, defdiv3pts, _grey_delimeter, defdiv3bar, _grey_delimeter, defdiv3domination, defdiv4pts, _grey_delimeter, defdiv4bar, _grey_delimeter, defdiv4domination))
                except:
                    irc.reply(_error)
    battle = wrap(battle, ['int'])

    def topfight(self, irc, msg, args, id):
        """<ID>

        Gives advanced info about top fighters in some battle. Use \x02+battles\x02 commands to get list of available IDs, to see info about other battle facts use command \x02+battle\x02."""
        data = self.active_battles()
        if id not in data:
            irc.reply("This battle is finished and I'm not giving info about finished battles.")
        else:
            base = json.load(utils.web.getUrlFd('%sbattle/%s.json' % (url, id)))
            if 'message' in base.keys():
                irc.reply(_error)
            else:
                try:
                    base = json.load(utils.web.getUrlFd('%sbattle/%s.json' % (url, id)))
                    att1 = base['attacker']['divisions']['1']['top_fighters'][0] # full attacker tf  DIV1 dictionary
                    attacker_name1 = att1.values()[0] # attacker tf name
                    attacker_kills1 = att1.values()[1] # attacker tf kills
                    attacker_cs_dict1 = att1.values()[2] # attacker cs dictionary
                    attacker_cs1 = attacker_cs_dict1.values()[2] #attacker tf citizenship
                    attacker_dmg1 = att1.values()[3]
                    att2 = base['attacker']['divisions']['2']['top_fighters'][0] # full attacker tf  DIV2 dictionary
                    attacker_name2 = att2.values()[0] # attacker tf name
                    attacker_kills2 = att2.values()[1] # attacker tf kills
                    attacker_cs_dict2 = att2.values()[2] # attacker cs dictionary
                    attacker_cs2 = attacker_cs_dict2.values()[2] #attacker tf citizenship
                    attacker_dmg2 = att2.values()[3]
                    att3 = base['attacker']['divisions']['3']['top_fighters'][0] # full attacker tf  DIV3 dictionary
                    attacker_name3 = att3.values()[0] # attacker tf name
                    attacker_kills3 = att3.values()[1] # attacker tf kills
                    attacker_cs_dict3 = att3.values()[2] # attacker cs dictionary
                    attacker_cs3 = attacker_cs_dict3.values()[2] #attacker tf citizenship
                    attacker_dmg3 = att3.values()[3]
                    att4 = base['attacker']['divisions']['4']['top_fighters'][0] # full attacker tf  DIV3 dictionary
                    attacker_name4 = att4.values()[0] # attacker tf name
                    attacker_kills4 = att4.values()[1] # attacker tf kills
                    attacker_cs_dict4 = att4.values()[2] # attacker cs dictionary
                    attacker_cs4 = attacker_cs_dict4.values()[2] #attacker tf citizenship
                    attacker_dmg4 = att4.values()[3]
                    def1 = base['defender']['divisions']['1']['top_fighters'][0] # full defender tf  DIV1 dictionary
                    defender_name1 = def1.values()[0] # defender tf name
                    defender_kills1 = def1.values()[1] # defender tf kills
                    defender_cs_dict1 = def1.values()[2] # defender cs dictionary
                    defender_cs1 = defender_cs_dict1.values()[2] #defender tf citizenship
                    defender_dmg1 = def1.values()[3]
                    def2 = base['defender']['divisions']['2']['top_fighters'][0] # full defender tf  DIV2 dictionary
                    defender_name2 = def2.values()[0] # defender tf name
                    defender_kills2 = def2.values()[1] # defender tf kills
                    defender_cs_dict2 = def2.values()[2] # defender cs dictionary
                    defender_cs2 = defender_cs_dict2.values()[2] #defender tf citizenship
                    defender_dmg2 = def2.values()[3]
                    def3 = base['defender']['divisions']['3']['top_fighters'][0] # full defender tf  DIV3 dictionary
                    defender_name3 = def3.values()[0] # defender tf name
                    defender_kills3 = def3.values()[1] # defender tf kills
                    defender_cs_dict3 = def3.values()[2] # defender cs dictionary
                    defender_cs3 = defender_cs_dict3.values()[2] #defender tf citizenship
                    defender_dmg3 = def3.values()[3]
                    def4 = base['defender']['divisions']['4']['top_fighters'][0] # full defender tf  DIV4 dictionary
                    defender_name4 = def4.values()[0] # defender tf name
                    defender_kills4 = def4.values()[1] # defender tf kills
                    defender_cs_dict4 = def4.values()[2] # defender cs dictionary
                    defender_cs4 = defender_cs_dict4.values()[2] #defender tf citizenship
                    defender_dmg4 = def4.values()[3]
                    irc.reply('\x0310Attacker Hero \x039D1\x03; Attacker Hero Name: \x02%s\x02, Attacker Hero Citizenship: \x02%s\x02, Attacker Hero Kills: \x02%s\x02, Attacker Hero Damage: \x02%s\x02 %s \x0310Attacker Hero \x034D2\x03; Attacker Hero Name: \x02%s\x02, Attacker Hero Citizenship: \x02%s\x02, Attacker Hero Kills: \x02%s\x02, Attacker Hero Damage: \x02%s\x02 %s \x0310Attacker Hero \x037D3\x03; Attacker Hero Name: \x02%s\x02, Attacker Hero Citizenship: \x02%s\x02, Attacker Hero Kills: \x02%s\x02, Attacker Hero Damage: \x02%s\x02 %s \x0310Attacker Hero \x0312D4\x03; Attacker Hero Name: \x02%s\x02, Attacker Hero Citizenship: \x02%s\x02, Attacker Hero Kills: \x02%s\x02, Attacker Hero Damage: \x02%s\x02 %s%s%s \x037Defender Hero \x039D1\x03; Defender Hero Name: \x02%s\x02, Defender Hero Citizenship: \x02%s\x02, Defender Hero Kills: \x02%s\x02, Defender Hero Damage: \x02%s\x02 %s \x037Defender Hero \x034D2\x03; Defender Hero Name: \x02%s\x02, Defender Hero Citizenship: \x02%s\x02, Defender Hero Kills: \x02%s\x02, Defender Hero Damage: \x02%s\x02 %s \x037Defender Hero \x037D3\x03; Defender Hero Name: \x02%s\x02, Defender Hero Citizenship: \x02%s\x02, Defender Hero Kills: \x02%s\x02, Defender Hero Damage: \x02%s\x02 %s \x037Defender Hero \x0312D4\x03; Defender Hero Name: \x02%s\x02, Defender Hero Citizenship: \x02%s\x02, Defender Hero Kills: \x02%s\x02, Defender Hero Damage: \x02%s\x02' % (attacker_name1, attacker_cs1, attacker_kills1, '{:,}'.format(attacker_dmg1), _blue_delimeter, attacker_name2, attacker_cs2, attacker_kills2, '{:,}'.format(attacker_dmg2), _blue_delimeter, attacker_name3, attacker_cs3, attacker_kills3, '{:,}'.format(attacker_dmg3), _blue_delimeter, attacker_name4, attacker_cs4, attacker_kills4, '{:,}'.format(attacker_dmg4), _red_delimeter, _dark_blue_delimeter, _white_delimeter, defender_name1, defender_cs1, defender_kills1, '{:,}'.format(defender_dmg1), _blue_delimeter, defender_name2, defender_cs2, defender_kills2, '{:,}'.format(defender_dmg2), _blue_delimeter, defender_name3, defender_cs3, defender_kills3, '{:,}'.format(defender_dmg3), _blue_delimeter, defender_name4, defender_cs4, defender_kills4, '{:,}'.format(defender_dmg4)))
                except:
                    irc.reply(_error)
    topfight = wrap(topfight, ['int'])

    def fc(self, irc, msg, args, name):
        """<name>

        Fight calculator"""
        nick = msg.nick
        profiles = self.read_profiles()
        if name:
            if name[0].lower() in profiles.keys():
                id = profiles[name[0].lower()]['id']
                data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                color = 3 if data['online'] else 4
                name = data['name']
                rank = data['military']['rank']['name']
                strength = data['military']['strength']
                base = data['military']['base_hit']
                q1 = base * 1.2000373204
                q2 = q1 * 1.1666925828
                q3 = q2 * 1.14287618286
                q4 = q3 * 1.12501457726
                q5 = q4 * 1.1111226288
                q6 = q5 * 1.10000932923
                q7 = q6 * 1.36358239335
                #irc.reply('\x02\x03%i%s\x03\02 is \x02%s\x02, and he hits; \x02\x0310Q0:\x02\x03 %s, \x02\x0312Q1\x02\x03: %s, \x02\x0303Q2\x02\x03: %s, \x02\x0309Q3\x02\x03: %s, \x02\x0307Q4\x02\x03: %s, \x02\x0305Q5\x02\x03: %s, \x02\x0311Q6\x02\x03: %s, \x02\x0304Q7\x02\x03: %s' % (color, name, rank, '{:,}'.format(base), '{:,}'.format(int(q1)), '{:,}'.format(int(q2)), '{:,}'.format(int(q3)), '{:,}'.format(int(q4)), '{:,}'.format(int(q5)), '{:,}'.format(int(q6)), '{:,}'.format(int(q7))))
                irc.reply('\x02\x03%i%s\x03\02 is \x02%s\x02, and he hits; \x02\x0310Q0:\x02\x03 %s, \x02\x0312Q1\x02\x03: %s, \x02\x0303Q2\x02\x03: %s, \x02\x0309Q3\x02\x03: %s, \x02\x0307Q4\x02\x03: %s, \x02\x0305Q5\x02\x03: %s, \x02\x0311Q6\x02\x03: %s, \x02\x0304Q7\x02\x03: %s' % (color, name, rank, locale.format('%d', base, True), locale.format('%d', int(q1), True), locale.format('%d', int(q2), True), locale.format('%d', int(q3), True), locale.format('%d', int(q4), True), locale.format('%d', int(q5), True), locale.format('%d', int(q6), True), locale.format('%d', int(q7), True)))
            else:
                if len(name[0]) <= 2:
                    irc.reply("You can't use less than 3 characters for <name>.")
                else:
                    bata = json.load(utils.web.getUrlFd('%scitizen/search/%s/1.json' % (url, '_'.join(name))))
                    if bata != []:
                        id = str(bata[0]['id'])
                        data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                        color = 3 if data['online'] else 4
                        name = bata[0]['name']
                        rank = data['military']['rank']['name']
                        strength = data['military']['strength']
                        base = data['military']['base_hit']
                        q1 = base * 1.2000373204
                        q2 = q1 * 1.1666925828
                        q3 = q2 * 1.14287618286
                        q4 = q3 * 1.12501457726
                        q5 = q4 * 1.1111226288
                        q6 = q5 * 1.10000932923
                        q7 = q6 * 1.36358239335
                    #irc.reply('\x02\x03%i%s\x03\02 is \x02%s\x02, and he hits; \x02\x0310Q0:\x02\x03 %s, \x02\x0312Q1\x02\x03: %s, \x02\x0303Q2\x02\x03: %s, \x02\x0309Q3\x02\x03: %s, \x02\x0307Q4\x02\x03: %s, \x02\x0305Q5\x02\x03: %s, \x02\x0311Q6\x02\x03: %s, \x02\x0304Q7\x02\x03: %s' % (color, name, rank, '{:,}'.format(base), '{:,}'.format(int(q1)), '{:,}'.format(int(q2)), '{:,}'.format(int(q3)), '{:,}'.format(int(q4)), '{:,}'.format(int(q5)), '{:,}'.format(int(q6)), '{:,}'.format(int(q7))))
                        irc.reply('\x02\x03%i%s\x03\02 is \x02%s\x02, and he hits; \x02\x0310Q0:\x02\x03 %s, \x02\x0312Q1\x02\x03: %s, \x02\x0303Q2\x02\x03: %s, \x02\x0309Q3\x02\x03: %s, \x02\x0307Q4\x02\x03: %s, \x02\x0305Q5\x02\x03: %s, \x02\x0311Q6\x02\x03: %s, \x02\x0304Q7\x02\x03: %s' % (color, name, rank, locale.format('%d', base, True), locale.format('%d', int(q1), True), locale.format('%d', int(q2), True), locale.format('%d', int(q3), True), locale.format('%d', int(q4), True), locale.format('%d', int(q5), True), locale.format('%d', int(q6), True), locale.format('%d', int(q7), True)))
                    else:
                        irc.reply(_error)
        else:
            if nick.lower() in profiles.keys():
                id = profiles[nick.lower()]['id']
                data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                color = 3 if data['online'] else 4
                name = data['name']
                rank = data['military']['rank']['name']
                strength = data['military']['strength']
                base = data['military']['base_hit']
                q1 = base * 1.2000373204
                q2 = q1 * 1.1666925828
                q3 = q2 * 1.14287618286
                q4 = q3 * 1.12501457726
                q5 = q4 * 1.1111226288
                q6 = q5 * 1.10000932923
                q7 = q6 * 1.36358239335
                    #irc.reply('\x02\x03%i%s\x03\02 is \x02%s\x02, and he hits; \x02\x0310Q0:\x02\x03 %s, \x02\x0312Q1\x02\x03: %s, \x02\x0303Q2\x02\x03: %s, \x02\x0309Q3\x02\x03: %s, \x02\x0307Q4\x02\x03: %s, \x02\x0305Q5\x02\x03: %s, \x02\x0311Q6\x02\x03: %s, \x02\x0304Q7\x02\x03: %s' % (color, name, rank, '{:,}'.format(base), '{:,}'.format(int(q1)), '{:,}'.format(int(q2)), '{:,}'.format(int(q3)), '{:,}'.format(int(q4)), '{:,}'.format(int(q5)), '{:,}'.format(int(q6)), '{:,}'.format(int(q7))))
                irc.reply('\x02\x03%i%s\x03\02 is \x02%s\x02, and he hits; \x02\x0310Q0:\x02\x03 %s, \x02\x0312Q1\x02\x03: %s, \x02\x0303Q2\x02\x03: %s, \x02\x0309Q3\x02\x03: %s, \x02\x0307Q4\x02\x03: %s, \x02\x0305Q5\x02\x03: %s, \x02\x0311Q6\x02\x03: %s, \x02\x0304Q7\x02\x03: %s' % (color, name, rank, locale.format('%d', base, True), locale.format('%d', int(q1), True), locale.format('%d', int(q2), True), locale.format('%d', int(q3), True), locale.format('%d', int(q4), True), locale.format('%d', int(q5), True), locale.format('%d', int(q6), True), locale.format('%d', int(q7), True)))
            else:
                irc.reply(_error)
    fc = wrap(fc, [optional(many('anything'))])

    def dmg(self, irc, msg, args, hits, name):
        """<name> or <id>

        Calculates how much damage you can make with <hits> (number of hits) with q7 weapon. \x02\x1FPlease put citizen name in quotes, example of correct command: dmg "Plato" 10\x1F\x02. <hits> is optional argument, if it's not specified I'll use 1 hit."""
        hits = hits or 1
        nick = msg.nick
        profiles = self.read_profiles()
        if name:
            if name[0].lower() in profiles.keys():
                id = profiles[name[0].lower()]['id']
                citizen = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                color = 3 if citizen['online'] else 4
                na = citizen['name']
                base = citizen['military']['base_hit']
                con = base * 3.00015689556
                q1 = base * 1.2000373204
                q2 = q1 * 1.1666925828
                q3 = q2 * 1.14287618286
                q4 = q3 * 1.12501457726
                q5 = q4 * 1.1111226288
                q6 = q5 * 1.10000932923
                q7 = q6 * 1.36358239335
                coun = con * int(hits)
                counbus = q7 / 2
                buster = counbus + q7
                dmgbus = buster * int(hits)
                    #irc.reply('\x02\x03%i%s\x03\x02 can make \x02%s\02 damage with q7 weapon. He can make \x02%s\x02 damage with buster.' % (color, na, '{:,}'.format(int(coun)), '{:,}'.format(int(dmgbus))))
                irc.reply('\x02\x03%i%s\x03\x02 can make \x02%s\02 damage with \x02%s\x02 hit(s), with q7 weapon. He can make \x02%s\x02 damage with \x02%s\x02 hit(s), with buster.' % (color, na, locale.format('%d', int(coun), True), hits, locale.format('%d', int(dmgbus), True), hits))
            else:
                if len(name[0]) <= 2:
                    irc.reply("You can't use less than 3 characters for <name>.")
                else:
                    cit = json.load(utils.web.getUrlFd('%scitizen/search/%s/1.json' % (url, '_'.join(name))))
                    if cit != []:
                        id = cit[0]['id']
                        citizen = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                        color = 3 if citizen['online'] else 4
                        na = citizen['name']
                        base = citizen['military']['base_hit']
                        con = base * 3.00015689556
                        q1 = base * 1.2000373204
                        q2 = q1 * 1.1666925828
                        q3 = q2 * 1.14287618286
                        q4 = q3 * 1.12501457726
                        q5 = q4 * 1.1111226288
                        q6 = q5 * 1.10000932923
                        q7 = q6 * 1.36358239335
                        coun = con * int(hits)
                        counbus = q7 / 2
                        buster = counbus + q7
                        dmgbus = buster * int(hits)
                        #irc.reply('\x02\x03%i%s\x03\x02 can make \x02%s\02 damage with q7 weapon. He can make \x02%s\x02 damage with buster.' % (color, na, '{:,}'.format(int(coun)), '{:,}'.format(int(dmgbus))))
                        irc.reply('\x02\x03%i%s\x03\x02 can make \x02%s\02 damage with \x02%s\x02 hit(s), with q7 weapon. He can make \x02%s\x02 damage with \x02%s\x02 hit(s), with buster.' % (color, na, locale.format('%d', int(coun), True), hits, locale.format('%d', int(dmgbus), True), hits))
                    else:
                        irc.reply(_error)
        else:
            if nick.lower() in profiles.keys():
                id = profiles[nick.lower()]['id']
                citizen = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                color = 3 if citizen['online'] else 4
                na = citizen['name']
                base = citizen['military']['base_hit']
                con = base * 3.00015689556
                q1 = base * 1.2000373204
                q2 = q1 * 1.1666925828
                q3 = q2 * 1.14287618286
                q4 = q3 * 1.12501457726
                q5 = q4 * 1.1111226288
                q6 = q5 * 1.10000932923
                q7 = q6 * 1.36358239335
                coun = con * int(hits)
                counbus = q7 / 2
                buster = counbus + q7
                dmgbus = buster * int(hits)
                    #irc.reply('\x02\x03%i%s\x03\x02 can make \x02%s\02 damage with q7 weapon. He can make \x02%s\x02 damage with buster.' % (color, na, '{:,}'.format(int(coun)), '{:,}'.format(int(dmgbus))))
                irc.reply('\x02\x03%i%s\x03\x02 can make \x02%s\02 damage with \x02%s\x02 hit(s), with q7 weapon. He can make \x02%s\x02 damage with \x02%s\x02 hit(s), with buster.' % (color, na, locale.format('%d', int(coun), True), hits, locale.format('%d', int(dmgbus), True), hits))
            else:
                irc.reply(_error)
    dmg = wrap(dmg, [optional('int'), optional(many('something'))])

    def info(self, irc, msg, args, name):
        """<name>

        Gives info about citizen. You don't need to put citizen name in quotes for this command."""
        nick = msg.nick
        profiles = self.read_profiles()
        if name:
            if name[0].lower() in profiles.keys():
                id = profiles[name[0].lower()]['id']
                data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                name = data['name']
                color = 3 if data['online'] else 4
                birth = data['birth']
                level = data['level']
                division = data['division']
                exp = data['experience']
                strength = data['military']['strength']
                rank_name = data['military']['rank']['name']
                to_next_rank = '{:,}'.format(data['military']['rank']['toNext'])
                rank_points = data['military']['rank']['points']
                mu = data['military']['unit']['name'] if data['military']['unit'] else "N/A"
                mu_role = data['military']['unit']['role'] if data['military']['unit'] else "N/A"
                residence_region = data['residence']['region']['name']
                residence_country = data['residence']['country']['name']
                cs = data['citizenship']['name']
                party_name = data['party']['name'] if data['party'] else "N/A"
                party_role = data['party']['role'] if data['party'] else "N/A"
                news = data['newspaper']['name'] if data['newspaper'] else "N/A"
                true_patriot_damage = '{:,}'.format(data['true_patriot']['damage']) if data['true_patriot'] else "N/A"
                true_patriot_since = data['true_patriot']['since'] if data['true_patriot'] else "N/A"
                top_damage_damage = '{:,}'.format(data['top_damage']['damage']) if data['top_damage'] else "N/A"
                top_damage_date = data['top_damage']['date'] if data['top_damage'] else "N/A"
                top_damage_message = data['top_damage']['message'] if data['top_damage'] else "N/A"
                irc.reply('Name: \x02\x03%i%s\x03\x02, Birth: \x02%s\x02, Region: \x02%s\x02 - \x02%s\x02, Citizenship: \x02%s\x02, Lvl: \x02%s\x02, Exp: \x02%s\x02, Strength: \x02%s\x02, Rank: \x02%s\x02, Rank Points: \x02%s\x02, Points To Next Rank: \x02%s\x02, MU: \x02%s\x02 - \x02\x034%s\x03\x02, Party: \x02%s\x02 - \x02\x034%s\x03\x02, News: \x02%s\x02, Top Damage: \x02%s\x02 since \x02%s\x02, \x02%s\x02, True Patriot: \x02%s\x02 since \x02%s\x02 ' % (color, name, birth, residence_region, residence_country, cs, level, locale.format('%d', int(exp), True), locale.format('%d', int(strength), True), rank_name, locale.format('%d', int(rank_points), True), locale.format('%s', to_next_rank, True), mu, mu_role, party_name, party_role, news, locale.format('%s', top_damage_damage, True), top_damage_date, top_damage_message, locale.format('%s', true_patriot_damage, True), true_patriot_since))
            else:
                if len(name[0]) <= 2:
                    irc.reply("You can't use less than 3 characters for <name>.")
                else:
                    bata = json.load(utils.web.getUrlFd('%scitizen/search/%s/1.json' % (url, '_'.join(name))))
                    if bata != []:
                        id = str(bata[0]['id'])
                        data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                        name = data['name']
                        color = 3 if data['online'] else 4
                        birth = data['birth']
                        level = data['level']
                        division = data['division']
                        exp = data['experience']
                        strength = data['military']['strength']
                        rank_name = data['military']['rank']['name']
                        to_next_rank = '{:,}'.format(data['military']['rank']['toNext'])
                        rank_points = data['military']['rank']['points']
                        mu = data['military']['unit']['name'] if data['military']['unit'] else "N/A"
                        mu_role = data['military']['unit']['role'] if data['military']['unit'] else "N/A"
                        residence_region = data['residence']['region']['name']
                        residence_country = data['residence']['country']['name']
                        cs = data['citizenship']['name']
                        party_name = data['party']['name'] if data['party'] else "N/A"
                        party_role = data['party']['role'] if data['party'] else "N/A"
                        news = data['newspaper']['name'] if data['newspaper'] else "N/A"
                        true_patriot_damage = '{:,}'.format(data['true_patriot']['damage']) if data['true_patriot'] else "N/A"
                        true_patriot_since = data['true_patriot']['since'] if data['true_patriot'] else "N/A"
                        top_damage_damage = '{:,}'.format(data['top_damage']['damage']) if data['top_damage'] else "N/A"
                        top_damage_date = data['top_damage']['date'] if data['top_damage'] else "N/A"
                        top_damage_message = data['top_damage']['message'] if data['top_damage'] else "N/A"
                        irc.reply('Name: \x02\x03%i%s\x03\x02, Birth: \x02%s\x02, Region: \x02%s\x02 - \x02%s\x02, Citizenship: \x02%s\x02, Lvl: \x02%s\x02, Exp: \x02%s\x02, Strength: \x02%s\x02, Rank: \x02%s\x02, Rank Points: \x02%s\x02, Points To Next Rank: \x02%s\x02, MU: \x02%s\x02 - \x02\x034%s\x03\x02, Party: \x02%s\x02 - \x02\x034%s\x03\x02, News: \x02%s\x02, Top Damage: \x02%s\x02 since \x02%s\x02, \x02%s\x02, True Patriot: \x02%s\x02 since \x02%s\x02 ' % (color, name, birth, residence_region, residence_country, cs, level, locale.format('%d', int(exp), True), locale.format('%d', int(strength), True), rank_name, locale.format('%d', int(rank_points), True), locale.format('%s', to_next_rank, True), mu, mu_role, party_name, party_role, news, locale.format('%s', top_damage_damage, True), top_damage_date, top_damage_message, locale.format('%s', true_patriot_damage, True), true_patriot_since))
                    else:
                        irc.reply(_error)
        else:
            if nick.lower() in profiles.keys():
                id = profiles[nick.lower()]['id']
                data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                name = data['name']
                color = 3 if data['online'] else 4
                birth = data['birth']
                level = data['level']
                division = data['division']
                exp = data['experience']
                strength = data['military']['strength']
                rank_name = data['military']['rank']['name']
                to_next_rank = '{:,}'.format(data['military']['rank']['toNext'])
                rank_points = data['military']['rank']['points']
                mu = data['military']['unit']['name'] if data['military']['unit'] else "N/A"
                mu_role = data['military']['unit']['role'] if data['military']['unit'] else "N/A"
                residence_region = data['residence']['region']['name']
                residence_country = data['residence']['country']['name']
                cs = data['citizenship']['name']
                party_name = data['party']['name'] if data['party'] else "N/A"
                party_role = data['party']['role'] if data['party'] else "N/A"
                news = data['newspaper']['name'] if data['newspaper'] else "N/A"
                true_patriot_damage = '{:,}'.format(data['true_patriot']['damage']) if data['true_patriot'] else "N/A"
                true_patriot_since = data['true_patriot']['since'] if data['true_patriot'] else "N/A"
                top_damage_damage = '{:,}'.format(data['top_damage']['damage']) if data['top_damage'] else "N/A"
                top_damage_date = data['top_damage']['date'] if data['top_damage'] else "N/A"
                top_damage_message = data['top_damage']['message'] if data['top_damage'] else "N/A"
                irc.reply('Name: \x02\x03%i%s\x03\x02, Birth: \x02%s\x02, Region: \x02%s\x02 - \x02%s\x02, Citizenship: \x02%s\x02, Lvl: \x02%s\x02, Exp: \x02%s\x02, Strength: \x02%s\x02, Rank: \x02%s\x02, Rank Points: \x02%s\x02, Points To Next Rank: \x02%s\x02, MU: \x02%s\x02 - \x02\x034%s\x03\x02, Party: \x02%s\x02 - \x02\x034%s\x03\x02, News: \x02%s\x02, Top Damage: \x02%s\x02 since \x02%s\x02, \x02%s\x02, True Patriot: \x02%s\x02 since \x02%s\x02 ' % (color, name, birth, residence_region, residence_country, cs, level, locale.format('%d', int(exp), True), locale.format('%d', int(strength), True), rank_name, locale.format('%d', int(rank_points), True), locale.format('%s', to_next_rank, True), mu, mu_role, party_name, party_role, news, locale.format('%s', top_damage_damage, True), top_damage_date, top_damage_message, locale.format('%s', true_patriot_damage, True), true_patriot_since))
            else:
                irc.reply(_error)
    info = wrap(info, [optional(many('something'))])

    def medals(self, irc, msg, args, name):
        """<name>

        Displays the citizens medals."""
        nick = msg.nick
        profiles = self.read_profiles()
        if name:
            if name[0].lower() in profiles.keys():
                id = profiles[name[0].lower()]['id']
                data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                name = data['name']
                color = 3 if data['online'] else 4
                medadic = data['medals']
                medals_sum = medadic.values()
                battle_hero = medadic['battle_hero']
                campaign_hero = medadic['campaign_hero']
                congress_member = medadic['congress_member']
                country_president = medadic['country_president']
                freedom_fighter = medadic['freedom_fighter']
                hard_worker = medadic['hard_worker']
                media_mogul = medadic['media_mogul']
                mercenary = medadic['mercenary']
                resistance_hero = medadic['resistance_hero']
                society_builder = medadic['society_builder']
                super_soldier = medadic['super_soldier']
                top_fighter = medadic['top_fighter']
                true_patriot = medadic['true_patriot']
                total = sum(medals_sum)
                irc.reply('Congressman: \x02%s\x02, Media Mogul: \x02%s\x02, Hard Worker: \x02%s\x02, Top Fighter: \x02%s\x02, True Patriot: \x02%s\x02, Battle Hero: \x02%s\x02, Super Soldier: \x02%s\x02, Mercenary: \x02%s\x02, Campaign Hero: \x02%s\x02, Resistance Hero: \x02%s\x02, Country President: \x02%s\x02, Society Builder: \x02%s\x02, Freedom Fighter: \x02%s\x02. \x034Total\x03: \x02%s\x02' % (congress_member, media_mogul, hard_worker, top_fighter, true_patriot, battle_hero, super_soldier, mercenary, campaign_hero, resistance_hero, country_president, society_builder, freedom_fighter, total))
            else:
                if len(name[0]) <= 2:
                    irc.reply("You can't use less than 3 characters for <name>.")
                else:
                    bata = json.load(utils.web.getUrlFd('%scitizen/search/%s/1.json' % (url, '_'.join(name))))
                    if bata != []:
                        id = str(bata[0]['id'])
                        data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                        name = data['name']
                        color = 3 if data['online'] else 4
                        medadic = data['medals']
                        medals_sum = medadic.values()
                        battle_hero = medadic['battle_hero']
                        campaign_hero = medadic['campaign_hero']
                        congress_member = medadic['congress_member']
                        country_president = medadic['country_president']
                        freedom_fighter = medadic['freedom_fighter']
                        hard_worker = medadic['hard_worker']
                        media_mogul = medadic['media_mogul']
                        mercenary = medadic['mercenary']
                        resistance_hero = medadic['resistance_hero']
                        society_builder = medadic['society_builder']
                        super_soldier = medadic['super_soldier']
                        top_fighter = medadic['top_fighter']
                        true_patriot = medadic['true_patriot']
                        total = sum(medals_sum)
                        irc.reply('Congressman: \x02%s\x02, Media Mogul: \x02%s\x02, Hard Worker: \x02%s\x02, Top Fighter: \x02%s\x02, True Patriot: \x02%s\x02, Battle Hero: \x02%s\x02, Super Soldier: \x02%s\x02, Mercenary: \x02%s\x02, Campaign Hero: \x02%s\x02, Resistance Hero: \x02%s\x02, Country President: \x02%s\x02, Society Builder: \x02%s\x02, Freedom Fighter: \x02%s\x02. \x034Total\x03: \x02%s\x02' % (congress_member, media_mogul, hard_worker, top_fighter, true_patriot, battle_hero, super_soldier, mercenary, campaign_hero, resistance_hero, country_president, society_builder, freedom_fighter, total))
                    else:
                        irc.reply(_error)
        else:
            if nick.lower() in profiles.keys():
                id = profiles[nick.lower()]['id']
                data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                name = data['name']
                color = 3 if data['online'] else 4
                medadic = data['medals']
                medals_sum = medadic.values()
                battle_hero = medadic['battle_hero']
                campaign_hero = medadic['campaign_hero']
                congress_member = medadic['congress_member']
                country_president = medadic['country_president']
                freedom_fighter = medadic['freedom_fighter']
                hard_worker = medadic['hard_worker']
                media_mogul = medadic['media_mogul']
                mercenary = medadic['mercenary']
                resistance_hero = medadic['resistance_hero']
                society_builder = medadic['society_builder']
                super_soldier = medadic['super_soldier']
                top_fighter = medadic['top_fighter']
                true_patriot = medadic['true_patriot']
                total = sum(medals_sum)
                irc.reply('Congressman: \x02%s\x02, Media Mogul: \x02%s\x02, Hard Worker: \x02%s\x02, Top Fighter: \x02%s\x02, True Patriot: \x02%s\x02, Battle Hero: \x02%s\x02, Super Soldier: \x02%s\x02, Mercenary: \x02%s\x02, Campaign Hero: \x02%s\x02, Resistance Hero: \x02%s\x02, Country President: \x02%s\x02, Society Builder: \x02%s\x02, Freedom Fighter: \x02%s\x02. \x034Total\x03: \x02%s\x02' % (congress_member, media_mogul, hard_worker, top_fighter, true_patriot, battle_hero, super_soldier, mercenary, campaign_hero, resistance_hero, country_president, society_builder, freedom_fighter, total))
            else:
                irc.reply(_error)
    medals = wrap(medals, [optional(many('something'))])

    def link(self, irc, msg, args, name):
        """<name>

        Returns citizen profile link"""
        nick = msg.nick
        profiles = self.read_profiles()
        if name:
            if name[0].lower() in profiles.keys():
                id = profiles[name[0].lower()]['id']
                data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                name = data['name']
                irc.reply("\x02%s\x02's profile link: http://www.erepublik.com/en/citizen/profile/%s" % (name, id))
            else:
                if len(name[0]) <= 2:
                    irc.reply("You can't use less than 3 characters for <name>.")
                else:
                    bata = json.load(utils.web.getUrlFd('%scitizen/search/%s/1.json' % (url, '_'.join(name))))
                    if bata != []:
                        id = str(bata[0]['id'])
                        name = str(bata[0]['name'])
                        irc.reply("\x02%s\x02's profile link: http://www.erepublik.com/en/citizen/profile/%s" % (name, id))
                    else:
                        irc.reply(_error)
        else:
            if nick.lower() in profiles.keys():
                id = profiles[nick.lower()]['id']
                data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                name = data['name']
                irc.reply("\x02%s\x02's profile link: http://www.erepublik.com/en/citizen/profile/%s" % (name, id))
            else:
                irc.reply(_error)
    link = wrap(link, [optional(many('something'))])

    def avatar(self, irc, msg, args, name):
        """<name>

        Returns citizen avatar link"""
        nick = msg.nick
        profiles = self.read_profiles()
        if name:
            if name[0].lower() in profiles.keys():
                id = profiles[name[0].lower()]['id']
                data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                name = data['name']
                avatar = string.split(data['avatar'], '_')
                avvatar = string.split(avatar[1], '.')
                irc.reply("\x02%s\x02's avatar link: %s.%s" % (name, avatar[0], avvatar[1]))
            else:
                if len(name[0]) <= 2:
                    irc.reply("You can't use less than 3 characters for <name>.")
                else:
                    bata = json.load(utils.web.getUrlFd('%scitizen/search/%s/1.json' % (url, '_'.join(name))))
                    if bata != []:
                        id = str(bata[0]['id'])
                        name = str(bata[0]['name'])
                        data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                        avatar = string.split(data['avatar'], '_')
                        avvatar = string.split(avatar[1], '.')
                        irc.reply("\x02%s\x02's avatar link: %s.%s" % (name, avatar[0], avvatar[1]))
                    else:
                        irc.reply(_error)
        else:
            if nick.lower() in profiles.keys():
                id = profiles[nick.lower()]['id']
                data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                name = data['name']
                avatar = string.split(data['avatar'], '_')
                avvatar = string.split(avatar[1], '.')
                irc.reply("\x02%s\x02's avatar link: %s.%s" % (name, avatar[0], avvatar[1]))
            else:
                irc.reply(_error)
    avatar = wrap(avatar, [optional(many('something'))])

    def donate(self, irc, msg, args, name):
        """<name>

        Returns citizen donate links"""
        nick = msg.nick
        profiles = self.read_profiles()
        if name:
            if name[0].lower() in profiles.keys():
                id = profiles[name[0].lower()]['id']
                donate_items = ('http://www.erepublik.com/en/economy/donate-items/%s' % id)
                donate_money = ('http://www.erepublik.com/en/economy/donate-money/%s' % id)
                irc.reply('\x02Donate Items\x02: %s \x02Donate Money\x02: %s' % (donate_items, donate_money))
            else:
                if len(name[0]) <= 2:
                    irc.reply("You can't use less than 3 characters for <name>.")
                else:
                    bata = json.load(utils.web.getUrlFd('%scitizen/search/%s/1.json' % (url, '_'.join(name))))
                    if bata != []:
                        id = str(bata[0]['id'])
                        donate_items = ('http://www.erepublik.com/en/economy/donate-items/%s' % id)
                        donate_money = ('http://www.erepublik.com/en/economy/donate-money/%s' % id)
                        irc.reply('\x02Donate Items\x02: %s \x02Donate Money\x02: %s' % (donate_items, donate_money))
                    else:
                        irc.reply(_error)
        else:
            if nick.lower() in profiles.keys():
                id = profiles[nick.lower()]['id']
                donate_items = ('http://www.erepublik.com/en/economy/donate-items/%s' % id)
                donate_money = ('http://www.erepublik.com/en/economy/donate-money/%s' % id)
                irc.reply('\x02Donate Items\x02: %s \x02Donate Money\x02: %s' % (donate_items, donate_money))
            else:
                irc.reply(_error)
    donate = wrap(donate, [optional(many('something'))])

    def nrh(self, irc, msg, args, name):
        """<name>

        Calculates how much points you need to next rank"""
        nick = msg.nick
        profiles = self.read_profiles()
        if name:
            if name[0].lower() in profiles.keys():
                id = profiles[name[0].lower()]['id']
                citizen = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                color = 3 if citizen['online'] else 4
                na = citizen['name']
                base = citizen['military']['base_hit']
                rank_name = citizen['military']['rank']['name']
                rank_points = citizen['military']['rank']['points']
                strength = citizen['military']['strength']
                con = base * 3.00015689556
                q1 = base * 1.2000373204
                q2 = q1 * 1.1666925828
                q3 = q2 * 1.14287618286
                q4 = q3 * 1.12501457726
                q5 = q4 * 1.1111226288
                q6 = q5 * 1.10000932923
                q7 = q6 * 1.36358239335
                to_next = citizen['military']['rank']['toNext']
                hitt = int(to_next) / int(q7)
                dmg = int(to_next) * 10
                hits = hitt * 10
                if rank_points <= 14:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x021\x02 time with q7 weapons to next rank, which is \x02Private\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True)))
                elif rank_points <= 44 and rank_points >= 15:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02\%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Private*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 79 and rank_points >= 45:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Private**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 119 and rank_points >= 80:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Private***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 169 and rank_points >= 120:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Corporal\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 249 and rank_points >= 170:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Corporal*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 349 and rank_points >= 250:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Corporal**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 449 and rank_points >= 350:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Corporal***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 599 and rank_points >= 450:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Sergeant\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 799 and rank_points >= 600:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Sergeant*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 999 and rank_points >= 800:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Sergeant**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 1399 and rank_points >= 1000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Sergeant***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 1849 and rank_points >= 1400:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lieutenant\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 2349 and rank_points >= 1850:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lieutenant*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 2999 and rank_points >= 2350:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lieutenant**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 3749 and rank_points >= 3000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lieutenant***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 4999 and rank_points >= 3750:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Captain\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 6499 and rank_points >= 5000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Captain*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 8999 and rank_points >= 6500:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Captain**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 11999 and rank_points >= 9000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Captain***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 15499 and rank_points >= 12000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Major\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 19999 and rank_points >= 15500:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Major*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 24999 and rank_points >= 20000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Major**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 30999 and rank_points >= 25000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Major***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 39999 and rank_points >= 31000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Commander\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 51999 and rank_points >= 40000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Commander*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 66999 and rank_points >= 52000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Commander**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 84999 and rank_points >= 67000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Commander***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 109999 and rank_points >= 85000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lt. Colonel\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 139999 and rank_points >= 110000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lt. Colonel*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 179999 and rank_points >= 140000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lt. Colonel**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 224999 and rank_points >= 180000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lt. Colonel***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 284999 and rank_points >= 250000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Colonel\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 354999 and rank_points >= 285000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Colonel*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 434999 and rank_points >= 355000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Colonel**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 539999 and rank_points >= 435000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Colonel***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 659000 and rank_points >= 540000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02General\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 799999 and rank_points >= 660000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02General*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 949999 and rank_points >= 800000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02General**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 1139999 and rank_points >= 950000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02General***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 1349999 and rank_points >= 1140000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Field Marshal\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 1599999 and rank_points >= 1350000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Field Marshal*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 1874999 and rank_points >= 1600000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Field Marshal**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 2184999 and rank_points >= 1875000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Field Marshal***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 2549999 and rank_points >= 2185000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Supreme Marshal\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 2999999 and rank_points >= 2550000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Supreme Marshal*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 3499999 and rank_points >= 3000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Supreme Marshal**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 4149999 and rank_points >= 3500000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Supreme Marshal***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 4899999 and rank_points >= 4150000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02National Force\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 5799999 and rank_points >= 4900000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02National Force*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 6999999 and rank_points >= 5800000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02National Force**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 8999999 and rank_points >= 7000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02National Force***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 11499999 and rank_points >= 9000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02World Class Force\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 14499999 and rank_points >= 11500000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02World Class Force*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 17999999 and rank_points >= 14500000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02World Class Force**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 21999999 and rank_points >= 18000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02World Class Force***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 26499999 and rank_points >= 22000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Legendary Force\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 31499999 and rank_points >= 26500000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Legendary Force*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 36999999 and rank_points >= 31500000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Legendary Force**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 42999999 and rank_points >= 37000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Legendary Force***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 49999999 and rank_points >= 43000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02God of War\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 99999999 and rank_points >= 50000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02God of War*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 199999999 and rank_points >= 100000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02God of War**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 499999999 and rank_points >= 200000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02God of War***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 999999999 and rank_points >= 500000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Titan\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 1999999999 and rank_points >= 1000000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Titan*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 3999999999 and rank_points >= 2000000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Titan**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 9999999999 and rank_points >= 4000000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit %s times with q7 weapons to next rank, which is \x02Titan***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                else:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, there is no more ranks for you my boy, \x034Game Over\x03' % (color, na, rank_name, locale.format('%d', int(strength), True)))
            else:
                if len(name[0]) <= 2:
                    irc.reply("You can't use less than 3 characters for <name>.")
                else:
                    cit = json.load(utils.web.getUrlFd('%scitizen/search/%s/1.json' % (url, '_'.join(name))))
                    if cit != []:
                        id = cit[0]['id']
                        citizen = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                        color = 3 if citizen['online'] else 4
                        na = citizen['name']
                        base = citizen['military']['base_hit']
                        rank_name = citizen['military']['rank']['name']
                        rank_points = citizen['military']['rank']['points']
                        strength = citizen['military']['strength']
                        con = base * 3.00015689556
                        q1 = base * 1.2000373204
                        q2 = q1 * 1.1666925828
                        q3 = q2 * 1.14287618286
                        q4 = q3 * 1.12501457726
                        q5 = q4 * 1.1111226288
                        q6 = q5 * 1.10000932923
                        q7 = q6 * 1.36358239335
                        to_next = citizen['military']['rank']['toNext']
                        hitt = int(to_next) / int(q7)
                        dmg = int(to_next) * 10
                        hits = hitt * 10
                        if rank_points <= 14:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x021\x02 time with q7 weapons to next rank, which is \x02Private\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True)))
                        elif rank_points <= 44 and rank_points >= 15:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02\%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Private*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 79 and rank_points >= 45:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Private**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 119 and rank_points >= 80:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Private***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 169 and rank_points >= 120:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Corporal\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 249 and rank_points >= 170:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Corporal*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 349 and rank_points >= 250:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Corporal**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 449 and rank_points >= 350:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Corporal***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 599 and rank_points >= 450:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Sergeant\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 799 and rank_points >= 600:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Sergeant*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 999 and rank_points >= 800:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Sergeant**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 1399 and rank_points >= 1000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Sergeant***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 1849 and rank_points >= 1400:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lieutenant\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 2349 and rank_points >= 1850:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lieutenant*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 2999 and rank_points >= 2350:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lieutenant**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 3749 and rank_points >= 3000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lieutenant***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 4999 and rank_points >= 3750:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Captain\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 6499 and rank_points >= 5000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Captain*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 8999 and rank_points >= 6500:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Captain**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 11999 and rank_points >= 9000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Captain***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 15499 and rank_points >= 12000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Major\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 19999 and rank_points >= 15500:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Major*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 24999 and rank_points >= 20000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Major**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 30999 and rank_points >= 25000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Major***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 39999 and rank_points >= 31000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Commander\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 51999 and rank_points >= 40000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Commander*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 66999 and rank_points >= 52000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Commander**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 84999 and rank_points >= 67000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Commander***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 109999 and rank_points >= 85000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lt. Colonel\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 139999 and rank_points >= 110000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lt. Colonel*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 179999 and rank_points >= 140000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lt. Colonel**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 224999 and rank_points >= 180000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lt. Colonel***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 284999 and rank_points >= 250000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Colonel\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 354999 and rank_points >= 285000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Colonel*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 434999 and rank_points >= 355000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Colonel**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 539999 and rank_points >= 435000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Colonel***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 659000 and rank_points >= 540000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02General\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 799999 and rank_points >= 660000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02General*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 949999 and rank_points >= 800000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02General**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 1139999 and rank_points >= 950000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02General***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 1349999 and rank_points >= 1140000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Field Marshal\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 1599999 and rank_points >= 1350000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Field Marshal*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 1874999 and rank_points >= 1600000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Field Marshal**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 2184999 and rank_points >= 1875000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Field Marshal***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 2549999 and rank_points >= 2185000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Supreme Marshal\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 2999999 and rank_points >= 2550000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Supreme Marshal*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 3499999 and rank_points >= 3000000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Supreme Marshal**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 4149999 and rank_points >= 3500000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Supreme Marshal***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 4899999 and rank_points >= 4150000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02National Force\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 5799999 and rank_points >= 4900000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02National Force*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 6999999 and rank_points >= 5800000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02National Force**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 8999999 and rank_points >= 7000000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02National Force***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 11499999 and rank_points >= 9000000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02World Class Force\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 14499999 and rank_points >= 11500000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02World Class Force*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 17999999 and rank_points >= 14500000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02World Class Force**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 21999999 and rank_points >= 18000000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02World Class Force***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 26499999 and rank_points >= 22000000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Legendary Force\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 31499999 and rank_points >= 26500000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Legendary Force*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 36999999 and rank_points >= 31500000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Legendary Force**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 42999999 and rank_points >= 37000000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Legendary Force***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 49999999 and rank_points >= 43000000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02God of War\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 99999999 and rank_points >= 50000000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02God of War*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 199999999 and rank_points >= 100000000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02God of War**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 499999999 and rank_points >= 200000000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02God of War***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 999999999 and rank_points >= 500000000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Titan\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 1999999999 and rank_points >= 1000000000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Titan*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 3999999999 and rank_points >= 2000000000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Titan**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        elif rank_points <= 9999999999 and rank_points >= 4000000000:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit %s times with q7 weapons to next rank, which is \x02Titan***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                        else:
                            irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, there is no more ranks for you my boy, \x034Game Over\x03' % (color, na, rank_name, locale.format('%d', int(strength), True)))
                    else:
                        irc.reply(_error)
        else:
            if nick.lower() in profiles.keys():
                id = profiles[nick.lower()]['id']
                citizen = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                color = 3 if citizen['online'] else 4
                na = citizen['name']
                base = citizen['military']['base_hit']
                rank_name = citizen['military']['rank']['name']
                rank_points = citizen['military']['rank']['points']
                strength = citizen['military']['strength']
                con = base * 3.00015689556
                q1 = base * 1.2000373204
                q2 = q1 * 1.1666925828
                q3 = q2 * 1.14287618286
                q4 = q3 * 1.12501457726
                q5 = q4 * 1.1111226288
                q6 = q5 * 1.10000932923
                q7 = q6 * 1.36358239335
                to_next = citizen['military']['rank']['toNext']
                hitt = int(to_next) / int(q7)
                dmg = int(to_next) * 10
                hits = hitt * 10
                if rank_points <= 14:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x021\x02 time with q7 weapons to next rank, which is \x02Private\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True)))
                elif rank_points <= 44 and rank_points >= 15:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02\%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Private*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 79 and rank_points >= 45:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Private**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 119 and rank_points >= 80:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Private***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 169 and rank_points >= 120:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Corporal\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 249 and rank_points >= 170:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Corporal*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 349 and rank_points >= 250:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Corporal**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 449 and rank_points >= 350:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Corporal***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 599 and rank_points >= 450:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Sergeant\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 799 and rank_points >= 600:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Sergeant*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 999 and rank_points >= 800:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Sergeant**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 1399 and rank_points >= 1000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Sergeant***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 1849 and rank_points >= 1400:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lieutenant\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 2349 and rank_points >= 1850:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lieutenant*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 2999 and rank_points >= 2350:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lieutenant**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 3749 and rank_points >= 3000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lieutenant***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 4999 and rank_points >= 3750:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Captain\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 6499 and rank_points >= 5000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Captain*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 8999 and rank_points >= 6500:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Captain**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 11999 and rank_points >= 9000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Captain***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 15499 and rank_points >= 12000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Major\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 19999 and rank_points >= 15500:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Major*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 24999 and rank_points >= 20000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Major**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 30999 and rank_points >= 25000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Major***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 39999 and rank_points >= 31000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Commander\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 51999 and rank_points >= 40000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Commander*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 66999 and rank_points >= 52000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Commander**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 84999 and rank_points >= 67000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Commander***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 109999 and rank_points >= 85000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lt. Colonel\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 139999 and rank_points >= 110000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lt. Colonel*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 179999 and rank_points >= 140000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lt. Colonel**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 224999 and rank_points >= 180000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Lt. Colonel***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 284999 and rank_points >= 250000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Colonel\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 354999 and rank_points >= 285000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Colonel*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 434999 and rank_points >= 355000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Colonel**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 539999 and rank_points >= 435000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Colonel***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 659000 and rank_points >= 540000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02General\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 799999 and rank_points >= 660000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02General*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 949999 and rank_points >= 800000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02General**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 1139999 and rank_points >= 950000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02General***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 1349999 and rank_points >= 1140000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Field Marshal\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 1599999 and rank_points >= 1350000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Field Marshal*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 1874999 and rank_points >= 1600000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Field Marshal**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 2184999 and rank_points >= 1875000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Field Marshal***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 2549999 and rank_points >= 2185000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Supreme Marshal\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 2999999 and rank_points >= 2550000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Supreme Marshal*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 3499999 and rank_points >= 3000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Supreme Marshal**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 4149999 and rank_points >= 3500000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Supreme Marshal***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 4899999 and rank_points >= 4150000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02National Force\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 5799999 and rank_points >= 4900000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02National Force*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 6999999 and rank_points >= 5800000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02National Force**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 8999999 and rank_points >= 7000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02National Force***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 11499999 and rank_points >= 9000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02World Class Force\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 14499999 and rank_points >= 11500000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02World Class Force*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 17999999 and rank_points >= 14500000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02World Class Force**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 21999999 and rank_points >= 18000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02World Class Force***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 26499999 and rank_points >= 22000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Legendary Force\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 31499999 and rank_points >= 26500000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Legendary Force*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 36999999 and rank_points >= 31500000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Legendary Force**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 42999999 and rank_points >= 37000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Legendary Force***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 49999999 and rank_points >= 43000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02God of War\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 99999999 and rank_points >= 50000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02God of War*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 199999999 and rank_points >= 100000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02God of War**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 499999999 and rank_points >= 200000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02God of War***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 999999999 and rank_points >= 500000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Titan\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 1999999999 and rank_points >= 1000000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Titan*\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 3999999999 and rank_points >= 2000000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit \x02%s\x02 times with q7 weapons to next rank, which is \x02Titan**\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                elif rank_points <= 9999999999 and rank_points >= 4000000000:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, needs to make \x02%s\x02 damage and to hit %s times with q7 weapons to next rank, which is \x02Titan***\x02.' % (color, na, rank_name, locale.format('%d', int(strength), True), locale.format('%d', int(dmg), True), locale.format('%d', int(hits), True)))
                else:
                    irc.reply('\x02\x03%i%s\x03\x02 is \x02%s\x02, Strength: \x02%s\x02, there is no more ranks for you my boy, \x034Game Over\x03' % (color, na, rank_name, locale.format('%d', int(strength), True)))
            else:
                irc.reply(_error)
    nrh = wrap(nrh, [optional(many('something'))])

    def check_tc_1(self, irc, ugovor, day5, tc1, tc2, tc3, tc4):
        with open('eRep/TCs.json', 'r') as read_tcs:
            tcs = json.loads(read_tcs.read())
            returning_dict = {}
            returning_dict['days'] = day5
            returning_dict['contract'] = ugovor
            if tc1 == 1:
                returning_dict['price'] = 0
                returning_dict['strength'] = 5
            elif tc1 == 2:
                returning_dict['price'] = 0
                returning_dict['strength'] = 10
            elif tc1 == 3:
                returning_dict['price'] = 0
                returning_dict['strength'] = 15
            elif tc1 == 4:
                returning_dict['price'] = 0
                returning_dict['strength'] = 20
            with open('eRep/Tcs_calculated.json', 'r') as read_calc_tcs:
                tcs_dict = json.loads(read_calc_tcs.read())
                tcs_dict['1'] = returning_dict
                with open('eRep/Tcs_calculated.json', 'w') as write_calc_tcs:
                    write_calc_tcs.write(json.dumps(tcs_dict))
                    schedule.addEvent(self.check_tc_2, time.time() + 0.1, args=(irc, ugovor, tc2, tc3, tc4))

    def check_tc_2(self, irc, ugovor, tc2, tc3, tc4):
        returning_dict = {}
        if ugovor == 0:
            if tc2 == 0:
                returning_dict['price'] = 0
                returning_dict['strength'] = 0
            elif tc2 == 1:
                returning_dict['price'] = 0.19
                returning_dict['strength'] = 2.5
            elif tc2 == 2:
                returning_dict['price'] = 0.19
                returning_dict['strength'] = 5
            elif tc2 == 3:
                returning_dict['price'] = 0.19
                returning_dict['strength'] = 7.5
            elif tc2 == 4:
                returning_dict['price'] = 0.19
                returning_dict['strength'] = 10
            with open('eRep/Tcs_calculated.json', 'r') as read_calc_tcs:
                tcs_dict = json.loads(read_calc_tcs.read())
                tcs_dict['2'] = returning_dict
                with open('eRep/Tcs_calculated.json', 'w') as write_calc_tcs:
                    write_calc_tcs.write(json.dumps(tcs_dict))
                    schedule.addEvent(self.check_tc_3, time.time() + 0.1, args=(irc, ugovor, tc3, tc4))
        elif ugovor == 50:
            if tc2 == 0:
                returning_dict['price'] = 0
                returning_dict['strength'] = 0
            elif tc2 == 1:
                returning_dict['price'] = 0.09
                returning_dict['strength'] = 2.5
            elif tc2 == 2:
                returning_dict['price'] = 0.09
                returning_dict['strength'] = 5
            elif tc2 == 3:
                returning_dict['price'] = 0.09
                returning_dict['strength'] = 7.5
            elif tc2 == 4:
                returning_dict['price'] = 0.09
                returning_dict['strength'] = 10
            with open('eRep/Tcs_calculated.json', 'r') as read_calc_tcs:
                tcs_dict = json.loads(read_calc_tcs.read())
                tcs_dict['2'] = returning_dict
                with open('eRep/Tcs_calculated.json', 'w') as write_calc_tcs:
                    write_calc_tcs.write(json.dumps(tcs_dict))
                    schedule.addEvent(self.check_tc_3, time.time() + 0.1, args=(irc, ugovor, tc3, tc4))
        else:
            if tc2 == 0:
                returning_dict['price'] = 0
                returning_dict['strength'] = 0
            elif tc2 == 1:
                returning_dict['price'] = 0.02
                returning_dict['strength'] = 2.5
            elif tc2 == 2:
                returning_dict['price'] = 0.02
                returning_dict['strength'] = 5
            elif tc2 == 3:
                returning_dict['price'] = 0.02
                returning_dict['strength'] = 7.5
            elif tc2 == 4:
                returning_dict['price'] = 0.02
                returning_dict['strength'] = 10
            with open('eRep/Tcs_calculated.json', 'r') as read_calc_tcs:
                tcs_dict = json.loads(read_calc_tcs.read())
                tcs_dict['2'] = returning_dict
                with open('eRep/Tcs_calculated.json', 'w') as write_calc_tcs:
                    write_calc_tcs.write(json.dumps(tcs_dict))
                    schedule.addEvent(self.check_tc_3, time.time() + 0.1, args=(irc, ugovor, tc3, tc4))

    def check_tc_3(self, irc, ugovor, tc3, tc4):
        returning_dict = {}
        if ugovor == 0:
            if tc3 == 0:
                returning_dict['price'] = 0
                returning_dict['strength'] = 0
            elif tc3 == 1:
                returning_dict['price'] = 0.89
                returning_dict['strength'] = 5
            elif tc3 == 2:
                returning_dict['price'] = 0.89
                returning_dict['strength'] = 10
            elif tc3 == 3:
                returning_dict['price'] = 0.89
                returning_dict['strength'] = 15
            elif tc3 == 4:
                returning_dict['price'] = 0.89
                returning_dict['strength'] = 20
            with open('eRep/Tcs_calculated.json', 'r') as read_calc_tcs:
                tcs_dict = json.loads(read_calc_tcs.read())
                tcs_dict['3'] = returning_dict
                with open('eRep/Tcs_calculated.json', 'w') as write_calc_tcs:
                    write_calc_tcs.write(json.dumps(tcs_dict))
                    schedule.addEvent(self.check_tc_4, time.time() + 0.1, args=(irc, ugovor, tc4))
        elif ugovor == 50:
            if tc3 == 0:
                returning_dict['price'] = 0
                returning_dict['strength'] = 0
            elif tc3 == 1:
                returning_dict['price'] = 0.44
                returning_dict['strength'] = 5
            elif tc3 == 2:
                returning_dict['price'] = 0.44
                returning_dict['strength'] = 10
            elif tc3 == 3:
                returning_dict['price'] = 0.44
                returning_dict['strength'] = 15
            elif tc3 == 4:
                returning_dict['price'] = 0.44
                returning_dict['strength'] = 20
            with open('eRep/Tcs_calculated.json', 'r') as read_calc_tcs:
                tcs_dict = json.loads(read_calc_tcs.read())
                tcs_dict['3'] = returning_dict
                with open('eRep/Tcs_calculated.json', 'w') as write_calc_tcs:
                    write_calc_tcs.write(json.dumps(tcs_dict))
                    schedule.addEvent(self.check_tc_4, time.time() + 0.1, args=(irc, ugovor, tc4))
        elif ugovor == 90:
            if tc3 == 0:
                returning_dict['price'] = 0
                returning_dict['strength'] = 0
            elif tc3 == 1:
                returning_dict['price'] = 0.09
                returning_dict['strength'] = 5
            elif tc3 == 2:
                returning_dict['price'] = 0.09
                returning_dict['strength'] = 10
            elif tc3 == 3:
                returning_dict['price'] = 0.09
                returning_dict['strength'] = 15
            elif tc3 == 4:
                returning_dict['price'] = 0.09
                returning_dict['strength'] = 20
            with open('eRep/Tcs_calculated.json', 'r') as read_calc_tcs:
                tcs_dict = json.loads(read_calc_tcs.read())
                tcs_dict['3'] = returning_dict
                with open('eRep/Tcs_calculated.json', 'w') as write_calc_tcs:
                    write_calc_tcs.write(json.dumps(tcs_dict))
                    schedule.addEvent(self.check_tc_4, time.time() + 0.1, args=(irc, ugovor, tc4))

    def check_tc_4(self, irc, ugovor, tc4):
        returning_dict = {}
        if ugovor == 0:
            if tc4 == 0:
                returning_dict['price'] = 0
                returning_dict['strength'] = 0
            elif tc4 == 1:
                returning_dict['price'] = 1.79
                returning_dict['strength'] = 10
            elif tc4 == 2:
                returning_dict['price'] = 1.79
                returning_dict['strength'] = 20
            elif tc4 == 3:
                returning_dict['price'] = 1.79
                returning_dict['strength'] = 30
            elif tc4 == 4:
                returning_dict['price'] = 1.79
                returning_dict['strength'] = 40
            with open('eRep/Tcs_calculated.json', 'r') as read_calc_tcs:
                tcs_dict = json.loads(read_calc_tcs.read())
                tcs_dict['4'] = returning_dict
                with open('eRep/Tcs_calculated.json', 'w') as write_calc_tcs:
                    write_calc_tcs.write(json.dumps(tcs_dict))
                    schedule.addEvent(self.calculate_training_cost, time.time() + 0.1, args=(irc, ugovor))
        elif ugovor == 50:
            if tc4 == 0:
                returning_dict['price'] = 0
                returning_dict['strength'] = 0
            elif tc4 == 1:
                returning_dict['price'] = 0.89
                returning_dict['strength'] = 10
            elif tc4 == 2:
                returning_dict['price'] = 0.89
                returning_dict['strength'] = 20
            elif tc4 == 3:
                returning_dict['price'] = 0.89
                returning_dict['strength'] = 30
            elif tc4 == 4:
                returning_dict['price'] = 0.89
                returning_dict['strength'] = 40
            with open('eRep/Tcs_calculated.json', 'r') as read_calc_tcs:
                tcs_dict = json.loads(read_calc_tcs.read())
                tcs_dict['4'] = returning_dict
                with open('eRep/Tcs_calculated.json', 'w') as write_calc_tcs:
                    write_calc_tcs.write(json.dumps(tcs_dict))
                    schedule.addEvent(self.calculate_training_cost, time.time() + 0.1, args=(irc, ugovor))
        elif ugovor == 90:
            if tc4 == 0:
                returning_dict['price'] = 0
                returning_dict['strength'] = 0
            elif tc4 == 1:
                returning_dict['price'] = 0.18
                returning_dict['strength'] = 10
            elif tc4 == 2:
                returning_dict['price'] = 0.18
                returning_dict['strength'] = 20
            elif tc4 == 3:
                returning_dict['price'] = 0.18
                returning_dict['strength'] = 30
            elif tc4 == 4:
                returning_dict['price'] = 0.18
                returning_dict['strength'] = 40
            with open('eRep/Tcs_calculated.json', 'r') as read_calc_tcs:
                tcs_dict = json.loads(read_calc_tcs.read())
                tcs_dict['4'] = returning_dict
                with open('eRep/Tcs_calculated.json', 'w') as write_calc_tcs:
                    write_calc_tcs.write(json.dumps(tcs_dict))
                    schedule.addEvent(self.calculate_training_cost, time.time() + 0.1, args=(irc, ugovor))

    def calculate_training_cost(self, irc, ugovor):
        with open('eRep/Tcs_calculated.json', 'r') as read_calc_tcs:
            tcs_dict = json.loads(read_calc_tcs.read())
            bonus_days = tcs_dict['1']['days']
            type_of_contract = tcs_dict['1']['contract']
            if bonus_days == 'y':
                bonus_str = 1.8
            else:
                bonus_str = 0
            tc_1_price = tcs_dict['1']['price']
            tc_1_str = tcs_dict['1']['strength']
            tc_2_price = tcs_dict['2']['price']
            tc_2_str = tcs_dict['2']['strength']
            tc_3_price = tcs_dict['3']['price']
            tc_3_str = tcs_dict['3']['strength']
            tc_4_price = tcs_dict['4']['price']
            tc_4_str = tcs_dict['4']['strength']
            daily_str = bonus_str + tc_1_str + tc_2_str + tc_3_str + tc_4_str
            daily_cost = tc_1_price + tc_2_price + tc_3_price + tc_4_price
            formated_daily_cost = '%.3f' % daily_cost
            medals_by_day = 250 / daily_str
            formated_medals_by_day = '%.1f' % medals_by_day
            month_cost = daily_cost * 30
            max_str = daily_str * 30
            max_medals = max_str / 250
            gold_medals = max_medals * 5
            if type_of_contract == 0:
                contract_price = 0
            elif type_of_contract == 50:
                contract_price = 25
            else:
                contract_price = 53
            month_cost_last = month_cost + contract_price
            month_cost_minus_medals = month_cost_last - gold_medals
            formated_month_cost_minus_medals = '%.2f' % month_cost_minus_medals
            month_lost_per_day = month_cost_minus_medals / 30 
            formated_month_lost_per_day = '%.3f' % month_lost_per_day
            if month_cost_minus_medals < 0:
                plus_month_cost_minus_medals = month_cost_minus_medals - (month_cost_minus_medals * 2)
                formated_plus_month_cost_minus_medals = '%.2f' % plus_month_cost_minus_medals
                plus_month_lost_per_day = month_lost_per_day - (month_lost_per_day * 2)
                formated_plus_month_lost_per_day = '%.2f' % plus_month_lost_per_day
                irc.reply("Daily strength gain: \x02%s\x02, Daily training cost: \x02%s\x02 golds, SS medal every: \x02%s\x02 days, Monthly income: \x02%s\x02 golds, Daily income: \x02%s\x02 golds." % (daily_str, formated_daily_cost, formated_medals_by_day, formated_plus_month_cost_minus_medals, formated_plus_month_lost_per_day))
            else:
                irc.reply("Daily strength gain: \x02%s\x02, Daily training cost: \x02%s\x02 golds, SS medal every: \x02%s\x02 days, Monthly cost: \x02%s\x02 golds, Daily cost: \x02%s\x02 golds." % (daily_str, formated_daily_cost, formated_medals_by_day, formated_month_cost_minus_medals, formated_month_lost_per_day))
            
            
    def tccalc(self, irc, msg, args, ugovor, day5, tc1, tc2, tc3, tc4):
        """<contract type> <bonus days> <TC 1 quality> <TC 2 quality> <TC 3 quality> <TC 4 quality>

        Training calculator."""
        possible_contracts = [0, 50, 90]
        possible_days = ['y', 'n']
        possible_tcs = [0, 1, 2, 3, 4]
        if ugovor not in possible_contracts:
            irc.reply("Contract must be 0, 50 or 90.")
        elif day5 not in possible_days:
            irc.reply("<bonus days> must be \x02y\x02 or \x02no\x02.")
        elif tc1 == 0 or tc1 > 4:
            irc.reply("Training center 1 can't be 0 or higher than 4.")
        elif tc2 not in possible_tcs:
            irc.reply("Possible <training center 2 quality> is 0, 1, 2, 3 or 4. And training center one can't be 0.")
        elif tc3 not in possible_tcs:
            irc.reply("Possible <training center 3 quality> is 0, 1, 2, 3 or 4. And training center one can't be 0.")
        elif tc4 not in possible_tcs:
            irc.reply("Possible <training center 4 quality> is 0, 1, 2, 3 or 4. And training center one can't be 0.")
        else:
            self.check_tc_1(irc, ugovor, day5, tc1, tc2, tc3, tc4)
    tccalc = wrap(tccalc, ['int', 'something', 'int', 'int', 'int', 'int'])

    def duel(self, irc, msg, args, name, name1):
        """<name> <second name>

        Compares two citizens. \x02Put the first citizen name in quotes, like this \x1F+duel "Plato" Romper\x1F, the second one doesn't need to be in quotes."""
        try:
            bata = json.load(utils.web.getUrlFd('%scitizen/search/%s/1.json' % (url, string.replace(name, ' ', '_'))))
            bata1 = json.load(utils.web.getUrlFd('%scitizen/search/%s/1.json' % (url, '_'.join(name1))))
            id = str(bata[0]['id'])
            data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
            id1 = str(bata1[0]['id'])
            data1 = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id1)))
            medadic = data['medals']
            medals = medadic.values()
            total = sum(medals)
            medadic1 = data1['medals']
            medals1 = medadic1.values()
            total1 = sum(medals1)
            medals_color = 3 if total > total1 else 4
            medals1_color = 3 if total1 > total else 4
            name = data['name']
            color = 3 if data['online'] else 4
            name1 = data1['name']
            color1 = 3 if data1['online'] else 4
            level = data['level']
            level1 = data1['level']
            level_color = 3 if level > level1 else 4
            level1_color = 3 if level1 > level else 4
            exp = int(data['experience'])
            exp1 = int(data1['experience'])
            exp_color = 3 if exp > exp1 else 4
            exp1_color = 3 if exp1 > exp else 4
            strength = int(data['military']['strength'])
            color2 = 3 if data['military']['strength'] > data1['military']['strength'] else 4
            strength1 = int(data1['military']['strength'])
            color3 = 3 if strength1 > strength else 4
            rank_points = int(data['military']['rank']['points'])
            rank_points1 = int(data1['military']['rank']['points'])
            rank_points_color = 3 if rank_points > rank_points1 else 4
            rank_points1_color = 3 if rank_points1 > rank_points else 4
            nejac = ('%s Is \x0310L\x034o\x037S\x039e\x0312R\x03, he should delete account and start doing some dirty farmer work.' % name1)
            nejac1 = ('%s Is \x0310L\x034o\x037S\x039e\x0312R\x03, he should delete account and start doing some dirty farmer work.' % name)
            if level > level1 and exp > exp1 and strength > strength1 and rank_points > rank_points1 and total > total1:
                irc.reply("\x02\x03%i%s\x03\x02's Strength: \x03%i\x02%s\x02\x03, Lvl: \x03%i\x02%s\x02\x03, Exp: \x03%i\x02%s\x02\x03, Rank Points: \x03%i\x02%s\x02\x03, Medals: \x03%i\x02%s\x02\x03 \x0310<>\x03 \x02\x03%i%s\x03\x02's Strength: \x03%i\x02%s\x02\x03, Lvl: \x03%i\x02%s\x02\x03, Exp: \x03%i\x02%s\x02\x03, Rank Points: \x03%i\x02%s\x02\x03, Medals: \x03%i\x02%s\x02\x03 \x0310<>\x03 \x02%s\x02" % (color, name, color2, locale.format('%d', strength, True), level_color, level, exp_color, locale.format('%d', exp, True), rank_points_color, locale.format('%d', rank_points, True), medals_color, locale.format('%d', total, True), color1, name1, color3, locale.format('%d', strength1, True), level1_color, level1, exp1_color, locale.format('%d', exp1, True), rank_points1_color, locale.format('%d', rank_points1, True), medals1_color, locale.format('%d', total1, True), nejac))
            elif level < level1 and exp < exp1 and strength < strength1 and rank_points < rank_points1 and total < total1:
                irc.reply("\x02\x03%i%s\x03\x02's Strength: \x03%i\x02%s\x02\x03, Lvl: \x03%i\x02%s\x02\x03, Exp: \x03%i\x02%s\x02\x03, Rank Points: \x03%i\x02%s\x02\x03, Medals: \x03%i\x02%s\x02\x03 \x0310<>\x03 \x02\x03%i%s\x03\x02's Strength: \x03%i\x02%s\x02\x03, Lvl: \x03%i\x02%s\x02\x03, Exp: \x03%i\x02%s\x02\x03, Rank Points: \x03%i\x02%s\x02\x03, Medals: \x03%i\x02%s\x02\x03 \x0310<>\x03 \x02%s\x02" % (color, name, color2, locale.format('%d', strength, True), level_color, level, exp_color, locale.format('%d', exp, True), rank_points_color, locale.format('%d', rank_points, True), medals_color, locale.format('%d', total, True), color1, name1, color3, locale.format('%d', strength1, True), level1_color, level1, exp1_color, locale.format('%d', exp1, True), rank_points1_color, locale.format('%d', rank_points1, True), medals1_color, locale.format('%d', total1, True), nejac1))
            else:
                irc.reply("\x02\x03%i%s\x03\x02's Strength: \x03%i\x02%s\x02\x03, Lvl: \x03%i\x02%s\x02\x03, Exp: \x03%i\x02%s\x02\x03, Rank Points: \x03%i\x02%s\x02\x03, Medals: \x03%i\x02%s\x02\x03 \x0310<>\x03 \x02\x03%i%s\x03\x02's Strength: \x03%i\x02%s\x02\x03, Lvl: \x03%i\x02%s\x02\x03, Exp: \x03%i\x02%s\x02\x03, Rank Points: \x03%i\x02%s\x02\x03, Medals: \x03%i\x02%s\x02\x03" % (color, name, color2, locale.format('%d', strength, True), level_color, level, exp_color, locale.format('%d', exp, True), rank_points_color, locale.format('%d', rank_points, True), medals_color, locale.format('%d', total, True), color1, name1, color3, locale.format('%d', strength1, True), level1_color, level1, exp1_color, locale.format('%d', exp1, True), rank_points1_color, locale.format('%d', rank_points1, True), medals1_color, locale.format('%d', total1, True)))
        except:
            irc.reply(_error)
    duel = wrap(duel, ['something', many('something')])

    def odw(self, irc, msg, args, industry, quality, country):
        """<industry> <quality> <country code> 

        Gives info about one day work profit"""
        quality = quality or 7
        try:
            worker_salary_base = json.load(utils.web.getUrlFd('%sjobmarket/%s/1.json' % (url, country)))
            worker_salary = worker_salary_base[0]['salary']
            industry_base = json.load(utils.web.getUrlFd('%smarket/%s/%s/%s/1.json' % (url, country, industry, quality)))
            industry_price = industry_base[0]['price']
            vat_base = json.load(utils.web.getUrlFd('%scountry/%s/economy.json' % (url, country)))
            vat_food = vat_base['taxes']['food']['vat']
            vat_weapons = vat_base['taxes']['weapons']['vat']
            wrm_base = json.load(utils.web.getUrlFd('%smarket/%s/wrm/1/1.json' % (url, country)))
            wrm = wrm_base[0]['price']
            frm_base = json.load(utils.web.getUrlFd('%smarket/%s/frm/1/1.json' % (url, country)))
            frm = frm_base[0]['price']
            food_bonus = vat_base['bonuses']['food']
            weapons_bonus = vat_base['bonuses']['weapons']
                    #######################################################################
                    ########################   Weapons checking   #########################
                    #######################################################################
            if industry == 'weapons':
                vat = vat_weapons
                raw = wrm
                    ########################   Weapons checking for Q7 weapons   #########################
                if quality == 7:
                    if weapons_bonus == 1.0:
                        tanks = 20
                        wraw_amount = 4000
                    elif weapons_bonus == 0.8:
                        tanks = 18
                        wraw_amount = 3600
                    elif weapons_bonus == 0.6:
                        tanks = 16
                        wraw_amount = 3200
                    elif weapons_bonus == 0.4:
                        tanks = 14
                        wraw_amount = 2800
                    elif weapons_bonus == 0.2:
                        tanks = 12
                        wraw_amount = 2400
                    else:
                        tanks = 10
                        wraw_amount = 2000
                    tank_price = industry_price - (industry_price * vat)
                    raw_price = raw * wraw_amount
                    isplativost = (tank_price * tanks) - (raw_price + worker_salary)
                    irc.reply('Profitability per employee in q7 weapons factory is: \x02%s\x02, paycheck: \x02%s\x02, tank price: \x02%s\x02, raw price: \x02%s\x02, vat: \x02%s\x02.' % (isplativost, worker_salary, industry_price, raw, vat))
                    ########################   Weapons checking for Q6 weapons   #########################
                elif quality == 6:
                    if weapons_bonus == 1.0:
                        tanks = 20
                        wraw_amount = 1200
                    elif weapons_bonus == 0.8:
                        tanks = 18
                        wraw_amount = 1080
                    elif weapons_bonus == 0.6:
                        tanks = 16
                        wraw_amount = 960
                    elif weapons_bonus == 0.4:
                        tanks = 14
                        wraw_amount = 840
                    elif weapons_bonus == 0.2:
                        tanks = 12
                        wraw_amount = 720
                    else:
                        tanks = 10
                        wraw_amount = 600
                    tank_price = industry_price - (industry_price * vat)
                    raw_price = raw * wraw_amount
                    isplativost = (tank_price * tanks) - (raw_price + worker_salary)
                    irc.reply('Profitability per employee in q6 weapons factory is: \x02%s\x02, paycheck: \x02%s\x02, tank price: \x02%s\x02, raw price: \x02%s\x02, vat: \x02%s\x02.' % (isplativost, worker_salary, industry_price, raw, vat))
                    ########################   Weapons checking for Q5 weapons   #########################
                elif quality == 5:
                    if weapons_bonus == 1.0:
                        tanks = 20
                        wraw_amount = 1000
                    elif weapons_bonus == 0.8:
                        tanks = 18
                        wraw_amount = 900
                    elif weapons_bonus == 0.6:
                        tanks = 16
                        wraw_amount = 800
                    elif weapons_bonus == 0.4:
                        tanks = 14
                        wraw_amount = 700
                    elif weapons_bonus == 0.2:
                        tanks = 12
                        wraw_amount = 600
                    else:
                        tanks = 10
                        wraw_amount = 500
                    tank_price = industry_price - (industry_price * vat)
                    raw_price = raw * wraw_amount
                    isplativost = (tank_price * tanks) - (raw_price + worker_salary)
                    irc.reply('Profitability per employee in q5 weapons factory is: \x02%s\x02, paycheck: \x02%s\x02, tank price: \x02%s\x02, raw price: \x02%s\x02, vat: \x02%s\x02.' % (isplativost, worker_salary, industry_price, raw, vat))
                    ########################   Weapons checking for Q4 weapons   #########################
                elif quality == 4:
                    if weapons_bonus == 1.0:
                        tanks = 20
                        wraw_amount = 800
                    elif weapons_bonus == 0.8:
                        tanks = 18
                        wraw_amount = 720
                    elif weapons_bonus == 0.6:
                        tanks = 16
                        wraw_amount = 640
                    elif weapons_bonus == 0.4:
                        tanks = 14
                        wraw_amount = 560
                    elif weapons_bonus == 0.2:
                        tanks = 12
                        wraw_amount = 480
                    else:
                        tanks = 10
                        wraw_amount = 400
                    tank_price = industry_price - (industry_price * vat)
                    raw_price = raw * wraw_amount
                    isplativost = (tank_price * tanks) - (raw_price + worker_salary)
                    irc.reply('Profitability per employee in q4 weapons factory is: \x02%s\x02, paycheck: \x02%s\x02, tank price: \x02%s\x02, raw price: \x02%s\x02, vat: \x02%s\x02.' % (isplativost, worker_salary, industry_price, raw, vat))
                    ########################   Weapons checking for Q3 weapons   #########################
                elif quality == 3:
                    if weapons_bonus == 1.0:
                        tanks = 20
                        wraw_amount = 600
                    elif weapons_bonus == 0.8:
                        tanks = 18
                        wraw_amount = 540
                    elif weapons_bonus == 0.6:
                        tanks = 16
                        wraw_amount = 480
                    elif weapons_bonus == 0.4:
                        tanks = 14
                        wraw_amount = 420
                    elif weapons_bonus == 0.2:
                        tanks = 12
                        wraw_amount = 360
                    else:
                        tanks = 10
                        wraw_amount = 300
                    tank_price = industry_price - (industry_price * vat)
                    raw_price = raw * wraw_amount
                    isplativost = (tank_price * tanks) - (raw_price + worker_salary)
                    irc.reply('Profitability per employee in q3 weapons factory is: \x02%s\x02, paycheck: \x02%s\x02, tank price: \x02%s\x02, raw price: \x02%s\x02, vat: \x02%s\x02.' % (isplativost, worker_salary, industry_price, raw, vat))
                    ########################   Weapons checking for Q2 weapons   #########################
                elif quality == 2:
                    if weapons_bonus == 1.0:
                        tanks = 20
                        wraw_amount = 400
                    elif weapons_bonus == 0.8:
                        tanks = 18
                        wraw_amount = 360
                    elif weapons_bonus == 0.6:
                        tanks = 16
                        wraw_amount = 320
                    elif weapons_bonus == 0.4:
                        tanks = 14
                        wraw_amount = 280
                    elif weapons_bonus == 0.2:
                        tanks = 12
                        wraw_amount = 240
                    else:
                        tanks = 10
                        wraw_amount = 200
                    tank_price = industry_price - (industry_price * vat)
                    raw_price = raw * wraw_amount
                    isplativost = (tank_price * tanks) - (raw_price + worker_salary)
                    irc.reply('Profitability per employee in q2 weapons factory is: \x02%s\x02, paycheck: \x02%s\x02, tank price: \x02%s\x02, raw price: \x02%s\x02, vat: \x02%s\x02.' % (isplativost, worker_salary, industry_price, raw, vat))
                    ########################   Weapons checking for Q1 weapons   #########################
                elif quality == 1:
                    if weapons_bonus == 1.0:
                        tanks = 20
                        wraw_amount = 200
                    elif weapons_bonus == 0.8:
                        tanks = 18
                        wraw_amount = 180
                    elif weapons_bonus == 0.6:
                        tanks = 16
                        wraw_amount = 160
                    elif weapons_bonus == 0.4:
                        tanks = 14
                        wraw_amount = 140
                    elif weapons_bonus == 0.2:
                        tanks = 12
                        wraw_amount = 120
                    else:
                        tanks = 10
                        wraw_amount = 100
                    tank_price = industry_price - (industry_price * vat)
                    raw_price = raw * wraw_amount
                    isplativost = (tank_price * tanks) - (raw_price + worker_salary)
                    irc.reply('Profitability per employee in q1 weapons factory is: \x02%s\x02, paycheck: \x02%s\x02, tank price: \x02%s\x02, raw price: \x02%s\x02, vat: \x02%s\x02.' % (isplativost, worker_salary, industry_price, raw, vat))
                    ########################   Weapons wrong quality   #########################
                else:
                    irc.reply("There is no such quality as q%s." % quality)
                    #######################################################################
                    ########################   Food checking   ############################
                    #######################################################################
            elif industry == 'food':
                vat = vat_food
                raw = frm
                    ########################   Food checking for Q7 food   #########################
                if quality == 7:
                    if food_bonus == 1.0:
                        foods = 200
                        fraw_amount = 4000
                    elif food_bonus == 0.8:
                        foods = 180
                        fraw_amount = 3600
                    elif food_bonus == 0.6:
                        foods = 160
                        fraw_amount = 3200
                    elif food_bonus == 0.4:
                        foods = 140
                        fraw_amount = 2800
                    elif food_bonus == 0.2:
                        foods = 120
                        fraw_amount = 2400
                    else:
                        foods = 100
                        fraw_amount = 2000
                    food_price = industry_price - (industry_price * vat)
                    raw_price = raw * fraw_amount
                    isplativost = (food_price * foods) - (raw_price + worker_salary)
                    irc.reply('Profitability per employee in q7 foods factory is: \x02%s\x02, paycheck: \x02%s\x02, bread price: \x02%s\x02, raw price: \x02%s\x02, vat: \x02%s\x02.' % (isplativost, worker_salary, industry_price, raw, vat))
                    ########################   Food checking for Q6 food   #########################
                elif quality == 6:
                    if food_bonus == 1.0:
                        foods = 200
                        fraw_amount = 1200
                    elif food_bonus == 0.8:
                        foods = 180
                        fraw_amount = 1080
                    elif food_bonus == 0.6:
                        foods = 160
                        fraw_amount = 960
                    elif food_bonus == 0.4:
                        foods = 140
                        fraw_amount = 840
                    elif food_bonus == 0.2:
                        foods = 120
                        fraw_amount = 720
                    else:
                        foods = 100
                        fraw_amount = 600
                    food_price = industry_price - (industry_price * vat)
                    raw_price = raw * fraw_amount
                    isplativost = (food_price * foods) - (raw_price + worker_salary)
                    irc.reply('Profitability per employee in q6 foods factory is: \x02%s\x02, paycheck: \x02%s\x02, bread price: \x02%s\x02, raw price: \x02%s\x02, vat: \x02%s\x02.' % (isplativost, worker_salary, industry_price, raw, vat))
                    ########################   Food checking for Q5 food   #########################
                elif quality == 5:
                    if food_bonus == 1.0:
                        foods = 200
                        fraw_amount = 1000
                    elif food_bonus == 0.8:
                        foods = 180
                        fraw_amount = 900
                    elif food_bonus == 0.6:
                        foods = 160
                        fraw_amount = 800
                    elif food_bonus == 0.4:
                        foods = 140
                        fraw_amount = 700
                    elif food_bonus == 0.2:
                        foods = 120
                        fraw_amount = 600
                    else:
                        foods = 100
                        fraw_amount = 500
                    food_price = industry_price - (industry_price * vat)
                    raw_price = raw * fraw_amount
                    isplativost = (food_price * foods) - (raw_price + worker_salary)
                    irc.reply('Profitability per employee in q5 foods factory is: \x02%s\x02, paycheck: \x02%s\x02, bread price: \x02%s\x02, raw price: \x02%s\x02, vat: \x02%s\x02.' % (isplativost, worker_salary, industry_price, raw, vat))
                    ########################   Food checking for Q4 food   #########################
                elif quality == 4:
                    if food_bonus == 1.0:
                        foods = 200
                        fraw_amount = 800
                    elif food_bonus == 0.8:
                        foods = 180
                        fraw_amount = 720
                    elif food_bonus == 0.6:
                        foods = 160
                        fraw_amount = 640
                    elif food_bonus == 0.4:
                        foods = 140
                        fraw_amount = 560
                    elif food_bonus == 0.2:
                        foods = 120
                        fraw_amount = 480
                    else:
                        foods = 100
                        fraw_amount = 400
                    food_price = industry_price - (industry_price * vat)
                    raw_price = raw * fraw_amount
                    isplativost = (food_price * foods) - (raw_price + worker_salary)
                    irc.reply('Profitability per employee in q4 foods factory is: \x02%s\x02, paycheck: \x02%s\x02, bread price: \x02%s\x02, raw price: \x02%s\x02, vat: \x02%s\x02.' % (isplativost, worker_salary, industry_price, raw, vat))
                    ########################   Food checking for Q3 food   #########################
                elif quality == 3:
                    if food_bonus == 1.0:
                        foods = 200
                        fraw_amount = 600
                    elif food_bonus == 0.8:
                        foods = 180
                        fraw_amount = 540
                    elif food_bonus == 0.6:
                        foods = 160
                        fraw_amount = 480
                    elif food_bonus == 0.4:
                        foods = 140
                        fraw_amount = 420
                    elif food_bonus == 0.2:
                        foods = 120
                        fraw_amount = 360
                    else:
                        foods = 100
                        fraw_amount = 300
                    food_price = industry_price - (industry_price * vat)
                    raw_price = raw * fraw_amount
                    isplativost = (food_price * foods) - (raw_price + worker_salary)
                    irc.reply('Profitability per employee in q3 foods factory is: \x02%s\x02, paycheck: \x02%s\x02, bread price: \x02%s\x02, raw price: \x02%s\x02, vat: \x02%s\x02.' % (isplativost, worker_salary, industry_price, raw, vat))
                    ########################   Food checking for Q2 food   #########################
                elif quality == 2:
                    if food_bonus == 1.0:
                        foods = 200
                        fraw_amount = 400
                    elif food_bonus == 0.8:
                        foods = 180
                        fraw_amount = 360
                    elif food_bonus == 0.6:
                        foods = 160
                        fraw_amount = 320
                    elif food_bonus == 0.4:
                        foods = 140
                        fraw_amount = 280
                    elif food_bonus == 0.2:
                        foods = 120
                        fraw_amount = 240
                    else:
                        foods = 100
                        fraw_amount = 200
                    food_price = industry_price - (industry_price * vat)
                    raw_price = raw * fraw_amount
                    isplativost = (food_price * foods) - (raw_price + worker_salary)
                    irc.reply('Profitability per employee in q2 foods factory is: \x02%s\x02, paycheck: \x02%s\x02, bread price: \x02%s\x02, raw price: \x02%s\x02, vat: \x02%s\x02.' % (isplativost, worker_salary, industry_price, raw, vat))
                    ########################   Food checking for Q1 food   #########################
                elif quality == 1:
                    if food_bonus == 1.0:
                        foods = 200
                        fraw_amount = 200
                    elif food_bonus == 0.8:
                        foods = 180
                        fraw_amount = 180
                    elif food_bonus == 0.6:
                        foods = 160
                        fraw_amount = 160
                    elif food_bonus == 0.4:
                        foods = 140
                        fraw_amount = 140
                    elif food_bonus == 0.2:
                        foods = 120
                        fraw_amount = 120
                    else:
                        foods = 100
                        fraw_amount = 100
                    food_price = industry_price - (industry_price * vat)
                    raw_price = raw * fraw_amount
                    isplativost = (food_price * foods) - (raw_price + worker_salary)
                    irc.reply('Profitability per employee in q1 foods factory is: \x02%s\x02, paycheck: \x02%s\x02, bread price: \x02%s\x02, raw price: \x02%s\x02, vat: \x02%s\x02.' % (isplativost, worker_salary, industry_price, raw, vat))
                        ########################   Food wrong quality   #########################
                else:
                    irc.reply("There is no such quality as \x02q%s\x02." % quality)
            else:
                irc.reply("There is no such industry as \x02%s\x02." % industry)
        except:
            irc.reply("There was an error in processing your request, you've probably mistyped something. Correct syntax for this would be, example: \x02+odw weapons 7 rs\x02 or \x02+odw food 7 rs\x02, this would return you info about current profitability per employee in Serbia for the given industry and quality.")
    odw = wrap(odw, ['something', optional('int'), 'something'])

    def linkid(self, irc, msg, args, id):
        """<citizen id>

        Link your eRepublik profile with your IRC nick"""
        nick = msg.nick
        profiles = self.read_profiles()
        if nick.lower() in profiles.keys():
            irc.reply("You've already linked your profile with your IRC nick.")
        else:
            data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
            if 'message' in data.keys():
                irc.reply("There is no eRepublik citizen with this id.")
            else:
                citizen = data['name']
                today_date = datetime.date.today().strftime('%d/%m/%Y') # datetime.date.today().strftime('%d')
                today_hour = datetime.datetime.now().hour
                today = '%s_%s' % (today_date, today_hour)
                citizen_id = {}
                citizen_id['id'] = id
                citizen_id['nick'] = nick
                citizen_id['name'] = citizen
                citizen_id['vreme'] = today
                new_profile = profiles[nick.lower()] = citizen_id
                self.write_profile(new_profile, nick, citizen)
    linkid = wrap(linkid, ['int'])

    def rmid(self, irc, msg, args, name):
        """<irc nick>

        Removes citizens id from database."""
        nick = msg.nick
        profiles = self.read_profiles()
        if nick == "DonVitoCorleone":
            if name.lower() in profiles.keys():
                id = profiles[name.lower()]['id']
                citizen = profiles[name.lower()]['name']
                del profiles[name.lower()]
                self.remove_profile(profiles, citizen, id)
            else:
                irc.reply(_error)
        else:
            irc.reply("You don't have permission to remove citizen from my database. If this is your profile that you want to delete please contact my owner, DonVitoCorleone.")
    rmid = wrap(rmid, ['something'])

    def listusers(self, irc, msg, args, name):
        """Takes no arguments

        List linked profiles from database"""
        nick = msg.nick
        profiles = self.read_profiles()
        if nick == "DonVitoCorleone":
            if name is None:
                users = []
                for citizen in profiles.keys():
                    citizen = users.append(citizen)
                irc.reply("Currently there are \x02%s\x02 users in my database, and their IRC nicks are: \x02%s\x02." % (len(users), ', '.join(users)))
            else:
                if name.lower() not in profiles.keys():
                    irc.reply("\x02%s\x02 is not in users database." % name)
                else:
                    name = profiles[name.lower()]['name']
                    id = profiles[name.lower()]['id']
                    vreme = profiles[name.lower()]['vreme']
                    irc.reply("\x02%s\x02 has linked his eRep profile on \x02%s\x02 with id \x02%s\x02." % (name, vreme, id))
        else:
            irc.reply("You don't have permission to list linked users.")
    listusers = wrap(listusers, [optional('nick')])

    def mom(self, irc, msg, args, industry, quality):
        """<industry> [<quality>]

        Looks for minimal offer on every market and returns one market."""
        country_list = []
        url = conf.supybot.plugins.ERep.url()
        if '--w' in msg.args[1]:
            irc.reply("OK, I'll now check every country and try to determine lowest possible price for \x02Weapons\x02. Give me a minute or two because there are 70 countries to check.")
            with open('eRep/ERep_Countries.json', 'r') as countries:
                b = json.loads(countries.read())
                for k, v in b.items():
                    #b_items = '%s: %s' % (k, v)
                    country = k
                    try:
                        industry_base = json.load(utils.web.getUrlFd('%smarket/%s/weapons/%s/1.json' % (url, country, quality)))
                        industry_price = industry_base[0]['price']
                        list_appending = '%s - %s' % (industry_price, v)
                        country_list.append(list_appending)
                    except:
                        continue
                sorted_list = sorted(country_list, key=str)
                spliting_country = str.split(str(sorted_list[0]), ' - ')
                irc.reply("The best country to buy \x02Wepons\x02 is \x02%s\x02, price in that country is \x02%s\x02." % (spliting_country[1], spliting_country[0]))
        elif '--f' in msg.args[1]:
            irc.reply("OK, I'll now check every country and try to determine lowest possible price for \x02Food\x02. Give me a minute or two because there are 70 countries to check.")
            with open('eRep/ERep_Countries.json', 'r') as countries:
                b = json.loads(countries.read())
                for k, v in b.items():
                    #b_items = '%s: %s' % (k, v)
                    country = k
                    try:
                        industry_base = json.load(utils.web.getUrlFd('%smarket/%s/food/%s/1.json' % (url, country, quality)))
                        industry_price = industry_base[0]['price']
                        list_appending = '%s - %s' % (industry_price, v)
                        country_list.append(list_appending)
                    except:
                        continue
                sorted_list = sorted(country_list, key=str)
                spliting_country = str.split(str(sorted_list[0]), ' - ')
                irc.reply("The best country to buy \x02Food\x02 is \x02%s\x02, price in that country is \x02%s\x02." % (spliting_country[1], spliting_country[0]))
        elif '--raww' in msg.args[1]:
            irc.reply("OK, I'll now check every country and try to determine lowest possible price for \x02Weapon RAW Materials\x02. Give me a minute or two because there are 70 countries to check.")
            with open('eRep/ERep_Countries.json', 'r') as countries:
                b = json.loads(countries.read())
                for k, v in b.items():
                    #b_items = '%s: %s' % (k, v)
                    country = k
                    try:
                        industry_base = json.load(utils.web.getUrlFd('%smarket/%s/wrm/1/1.json' % (url, country)))
                        industry_price = industry_base[0]['price']
                        list_appending = '%s - %s' % (industry_price, v)
                        country_list.append(list_appending)
                    except:
                        continue
                sorted_list = sorted(country_list, key=str)
                spliting_country = str.split(str(sorted_list[0]), ' - ')
                irc.reply("The best country to buy \x02Weapon RAW Materials\x02 is \x02%s\x02, price in that country is \x02%s\x02." % (spliting_country[1], spliting_country[0]))
        elif '--rawf' in msg.args[1]:
            irc.reply("OK, I'll now check every country and try to determine lowest possible price for \x02Food RAW Materials\x02. Give me a minute or two because there are 70 countries to check.")
            with open('eRep/ERep_Countries.json', 'r') as countries:
                b = json.loads(countries.read())
                for k, v in b.items():
                    #b_items = '%s: %s' % (k, v)
                    country = k
                    try:
                        industry_base = json.load(utils.web.getUrlFd('%smarket/%s/frm/1/1.json' % (url, country)))
                        industry_price = industry_base[0]['price']
                        list_appending = '%s - %s' % (industry_price, v)
                        country_list.append(list_appending)
                    except:
                        continue
                sorted_list = sorted(country_list, key=str)
                spliting_country = str.split(str(sorted_list[0]), ' - ')
                irc.reply("The best country to buy \x02Food RAW Materials\x02 is \x02%s\x02, price in that country is \x02%s\x02." % (spliting_country[1], spliting_country[0]))
        else:
            irc.reply("You didn't gave me any industry to look for. Syntax for this command is \x02+mom \x0310--w/\x038--f/\x039--raww\x03 or \x037--rawf\x03 7-1\x02 where 7-1 means quality, if you're looking for -wrm or -frm you don't have to write quality.")
    mom = wrap(mom, ['something', optional('int')])

    def find_offer_on_market(self, irc, industry, country, quality, seller):
        url = conf.supybot.plugins.ERep.url()
        country_info = json.load(utils.web.getUrlFd('%scountry/%s/society.json' % (url, country)))
        country_id = country_info['id']
        if industry == 'weapons':
            try:
                for page in xrange(1, 150):
                    industry_base = json.load(utils.web.getUrlFd('%smarket/%s/weapons/%s/%s.json' % (url, country, quality, page)))
                    for offer in xrange(10):
                        seller_name = industry_base[offer]['seller']['name']
                        if seller_name.lower() == seller.lower():
                            offer_id = industry_base[offer]['id']
                            offer_amount = industry_base[offer]['amount']
                            offer_price = industry_base[offer]['price']
                            seller_id = industry_base[offer]['seller']['id']
                            if ' ' in seller_name:
                                splited_seller = seller_name.split(' ')
                                joined_seller = '%20'.join(splited_seller)
                                ready_url_for_print = 'http://www.erepublik.com/en/economy/market/%s/2/%s?customOffer=true&sellerId=%s&sellerName=%s&offerId=%s&offerAmount=%s&offerPrice=%s' % (country_id, quality, seller_id, joined_seller, offer_id, offer_amount, offer_price)
                                short_url = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + ready_url_for_print)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those with activated eRepublik Stuff + script\x02:%s' % (seller_name, offer_amount, offer_price, short_url))
                                url_for_none_stuff = 'http://www.erepublik.com/en/economy/market/%s/2/%s/citizen/1/price_asc/%s' % (country_id, quality, page)
                                short_url_no_script = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + url_for_none_stuff)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those without eRepublik Stuff + script\x02: %s' % (seller_name, offer_amount, offer_price, short_url_no_script))
                                return
                            else:
                                ready_url_for_print = 'http://www.erepublik.com/en/economy/market/%s/2/%s?customOffer=true&sellerId=%s&sellerName=%s&offerId=%s&offerAmount=%s&offerPrice=%s' % (country_id, quality, seller_id, seller_name, offer_id, offer_amount, offer_price)
                                short_url = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + ready_url_for_print)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those with activated eRepublik Stuff + script\x02:%s' % (seller_name, offer_amount, offer_price, short_url))
                                url_for_none_stuff = 'http://www.erepublik.com/en/economy/market/%s/2/%s/citizen/1/price_asc/%s' % (country_id, quality, page)
                                short_url_no_script = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + url_for_none_stuff)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those without eRepublik Stuff + script\x02: %s' % (seller_name, offer_amount, offer_price, short_url_no_script))
                                return
            except:
                irc.reply("Couldn't find any offer from this citizen, sorry.")
        elif industry == 'food':
            try:
                for page in xrange(1, 150):
                    industry_base = json.load(utils.web.getUrlFd('%smarket/%s/food/%s/%s.json' % (url, country, quality, page)))
                    for offer in xrange(10):
                        seller_name = industry_base[offer]['seller']['name']
                        if seller_name.lower() == seller.lower():
                            offer_id = industry_base[offer]['id']
                            offer_amount = industry_base[offer]['amount']
                            offer_price = industry_base[offer]['price']
                            seller_id = industry_base[offer]['seller']['id']
                            if ' ' in seller_name:
                                splited_seller = seller_name.split(' ')
                                joined_seller = '%20'.join(splited_seller)
                                ready_url_for_print = 'http://www.erepublik.com/en/economy/market/%s/1/%s?customOffer=true&sellerId=%s&sellerName=%s&offerId=%s&offerAmount=%s&offerPrice=%s' % (country_id, quality, seller_id, joined_seller, offer_id, offer_amount, offer_price)
                                short_url = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + ready_url_for_print)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those with activated eRepublik Stuff + script\x02:%s' % (seller_name, offer_amount, offer_price, short_url))
                                url_for_none_stuff = 'http://www.erepublik.com/en/economy/market/%s/1/%s/citizen/1/price_asc/%s' % (country_id, quality, page)
                                short_url_no_script = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + url_for_none_stuff)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those without eRepublik Stuff + script\x02: %s' % (seller_name, offer_amount, offer_price, short_url_no_script))
                                return
                            else:
                                ready_url_for_print = 'http://www.erepublik.com/en/economy/market/%s/1/%s?customOffer=true&sellerId=%s&sellerName=%s&offerId=%s&offerAmount=%s&offerPrice=%s' % (country_id, quality, seller_id, seller_name, offer_id, offer_amount, offer_price)
                                short_url = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + ready_url_for_print)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those with activated eRepublik Stuff + script\x02:%s' % (seller_name, offer_amount, offer_price, short_url))
                                url_for_none_stuff = 'http://www.erepublik.com/en/economy/market/%s/1/%s/citizen/1/price_asc/%s' % (country_id, quality, page)
                                short_url_no_script = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + url_for_none_stuff)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those without eRepublik Stuff + script\x02: %s' % (seller_name, offer_amount, offer_price, short_url_no_script))
                                return
            except:
                irc.reply("Couldn't find any offer from this citizen, sorry.")
        elif industry == 'wrm':
            try:
                for page in xrange(1, 150):
                    industry_base = json.load(utils.web.getUrlFd('%smarket/%s/wrm/1/%s.json' % (url, country, page)))
                    for offer in xrange(10):
                        seller_name = industry_base[offer]['seller']['name']
                        if seller_name.lower() == seller.lower():
                            offer_id = industry_base[offer]['id']
                            offer_amount = industry_base[offer]['amount']
                            offer_price = industry_base[offer]['price']
                            seller_id = industry_base[offer]['seller']['id']
                            if ' ' in seller_name:
                                splited_seller = seller_name.split(' ')
                                joined_seller = '%20'.join(splited_seller)
                                ready_url_for_print = 'http://www.erepublik.com/en/economy/market/%s/12/1?customOffer=true&sellerId=%s&sellerName=%s&offerId=%s&offerAmount=%s&offerPrice=%s' % (country_id, seller_id, joined_seller, offer_id, offer_amount, offer_price)
                                short_url = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + ready_url_for_print)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those with activated eRepublik Stuff + script\x02:%s' % (seller_name, offer_amount, offer_price, short_url))
                                url_for_none_stuff = 'http://www.erepublik.com/en/economy/market/%s/12/1/citizen/1/price_asc/%s' % (country_id, page)
                                short_url_no_script = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + url_for_none_stuff)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those without eRepublik Stuff + script\x02: %s' % (seller_name, offer_amount, offer_price, short_url_no_script))
                                return
                            else:
                                ready_url_for_print = 'http://www.erepublik.com/en/economy/market/%s/12/1?customOffer=true&sellerId=%s&sellerName=%s&offerId=%s&offerAmount=%s&offerPrice=%s' % (country_id, seller_id, seller_name, offer_id, offer_amount, offer_price)
                                short_url = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + ready_url_for_print)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those with activated eRepublik Stuff + script\x02:%s' % (seller_name, offer_amount, offer_price, short_url))
                                url_for_none_stuff = 'http://www.erepublik.com/en/economy/market/%s/12/1/citizen/1/price_asc/%s' % (country_id, page)
                                short_url_no_script = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + url_for_none_stuff)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those without eRepublik Stuff + script\x02: %s' % (seller_name, offer_amount, offer_price, short_url_no_script))
                                return
            except:
                irc.reply("Couldn't find any offer from this citizen, sorry.")
        elif industry == 'frm':
            try:
                for page in xrange(1, 150):
                    industry_base = json.load(utils.web.getUrlFd('%smarket/%s/frm/1/%s.json' % (url, country, page)))
                    for offer in xrange(10):
                        seller_name = industry_base[offer]['seller']['name']
                        if seller_name.lower() == seller.lower():
                            offer_id = industry_base[offer]['id']
                            offer_amount = industry_base[offer]['amount']
                            offer_price = industry_base[offer]['price']
                            seller_id = industry_base[offer]['seller']['id']
                            if ' ' in seller_name:
                                splited_seller = seller_name.split(' ')
                                joined_seller = '%20'.join(splited_seller)
                                ready_url_for_print = 'http://www.erepublik.com/en/economy/market/%s/7/1?customOffer=true&sellerId=%s&sellerName=%s&offerId=%s&offerAmount=%s&offerPrice=%s' % (country_id, seller_id, joined_seller, offer_id, offer_amount, offer_price)
                                short_url = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + ready_url_for_print)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those with activated eRepublik Stuff + script\x02:%s' % (seller_name, offer_amount, offer_price, short_url))
                                url_for_none_stuff = 'http://www.erepublik.com/en/economy/market/%s/7/1/citizen/1/price_asc/%s' % (country_id, page)
                                short_url_no_script = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + url_for_none_stuff)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those without eRepublik Stuff + script\x02: %s' % (seller_name, offer_amount, offer_price, short_url_no_script))
                                return
                            else:
                                ready_url_for_print = 'http://www.erepublik.com/en/economy/market/%s/7/1?customOffer=true&sellerId=%s&sellerName=%s&offerId=%s&offerAmount=%s&offerPrice=%s' % (country_id, seller_id, seller_name, offer_id, offer_amount, offer_price)
                                short_url = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + ready_url_for_print)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those with activated eRepublik Stuff + script\x02:%s' % (seller_name, offer_amount, offer_price, short_url))
                                url_for_none_stuff = 'http://www.erepublik.com/en/economy/market/%s/7/1/citizen/1/price_asc/%s' % (country_id, page)
                                short_url_no_script = utils.web.getUrl('http://tinyurl.com/api-create.php?url=' + url_for_none_stuff)
                                irc.reply('\x02Seller Name\x02: %s, \x02Offer Amount\x02: %s, \x02Offer Price\x02: %s, \x02URL for those without eRepublik Stuff + script\x02: %s' % (seller_name, offer_amount, offer_price, short_url_no_script))
                                return
            except:
                irc.reply("Couldn't find any offer from this citizen, sorry.")

    def fmo(self, irc, msg, args, industry, country, quality, seller):
        """<industry> <country> <quality> <seller name>

        Finds market offer for given industry, seller, in given country, and with given quality. If there's no offer it won't give you anything."""
        with open('eRep/ERep_Countries.json', 'r') as countries:
            b = json.loads(countries.read())
            possible_industry = ['weapons', 'food', 'wrm', 'frm']
            possible_food_and_wep_qualities = [1, 2, 3, 4, 5, 6, 7]
            countries = b.keys()
            possible_countries = []
            for country_name, country_code in b.items():
                ready_to_append = '%s: %s' % (country_code, country_name)
                possible_countries.append(ready_to_append)
            if country.upper() not in countries:
                irc.reply("There is no such country as \x02%s\x02. And you have to use\x034 2-letter codes, not full country name.\x03" % country)
                time.sleep(3)
                irc.reply("Possible counties are: \x02%s\x02." % ', '.join(possible_countries))
            else:
                if industry in possible_industry:
                    if industry != 'wrm' and industry != 'frm':
                        if quality in possible_food_and_wep_qualities:
                            irc.reply("Ok, give me few minutes to check if this offer exist, there are many pages and I have to check every one of them. Don't spam me with this command or I'll ignore you forever.")
                            self.find_offer_on_market(irc, industry, country, quality, ' '.join(seller))
                        else:
                            irc.reply("You can't put lower quality than 1 or higher than 7 for \x02%s\x02 industry." % industry)
                    else:
                        if quality == 1:
                            irc.reply("This command takes too much CPU/MEM from server and I can run only one instance of it at a time. If you see this message it means someone has already used this command. Please try again in few minutes.")
                            self.find_offer_on_market(irc, industry, country, quality, ' '.join(seller))
                        else:
                           irc.reply("You can't put any other quality than 1 for \x02%s\x02." % industry)
                else:
                    irc.reply("There is no \x02%s\x02 in industry list yet, possible industries are: \x02weapons\x02, \x02food\x02, \x02wrm\x02 and \x02frm\x02." % industry)
    fmo = wrap(fmo, ['something', 'something', 'int', many('something')])

    def find_job_offer(self, irc, country, employer):
        check_timer = self.check_timers('fjo')
        url = conf.supybot.plugins.ERep.url()
        country_info = json.load(utils.web.getUrlFd('%scountry/%s/society.json' % (url, country)))
        country_id = country_info['id']
        try:
            for page in xrange(1, 500):
                job_offers = json.load(utils.web.getUrlFd('%sjobmarket/%s/%s.json' % (url, country, page)))
                for offer in xrange(10):
                    employer_name = job_offers[offer]['employer']['name']
                    if employer_name.lower() == employer.lower():
                        employer_id = job_offers[offer]['employer']['id']
                        offer_salary = job_offers[offer]['salary']
                        link_to_page = 'http://www.erepublik.com/en/economy/job-market/%s/%s' % (country_id, page)
                        employer_link = 'http://www.erepublik.com/en/citizen/profile/%s' % employer_id
                        ready_to_reply = '\x02Employer Name\x02: %s, \x02Employer Link\x02: %s, \x02Salary\x02: %s, \x02\x034Link To Job On Job Market\x03\x02: %s' % (employer_name, employer_link, offer_salary, link_to_page)
                        irc.reply(ready_to_reply)
                        return
        except:
            irc.reply("Couldn't find offer from \x02%s\x02." % employer)

    def fjo(self, irc, msg, args, country, employer):
        """<country> <employer name>

        Looks for <employer name> on Job Market for given <country>. If employer is not on market returns nothing."""
        with open('eRep/ERep_Countries.json', 'r') as countries:
            b = json.loads(countries.read())
            countries = b.keys()
            possible_countries = []
            for country_name, country_code in b.items():
                ready_to_append = '%s: %s' % (country_code, country_name)
                possible_countries.append(ready_to_append)
            if country.upper() not in countries:
                irc.reply("There is no such country as \x02%s\x02. And you have to use\x034 2-letter codes, not full country name.\x03" % country)
                time.sleep(3)
                irc.reply("Possible counties are: \x02%s\x02." % ', '.join(possible_countries))
            else:
                irc.reply("Ok, give me few minutes to check if this offer exist, there are many pages and I have to check every one of them. \x02Don't spam me with this command or I'll ignore you forever\x02.")
                self.find_job_offer(irc, country, ' '.join(employer))
    fjo = wrap(fjo, ['something', many('something')])

Class = ERep


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
