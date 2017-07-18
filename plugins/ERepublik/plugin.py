###
# Copyright (c) 2010, KG-Bot
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
# this list of conditions, and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions, and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# * Neither the name of the author of this software nor the name of
# contributors to this software may be used to endorse or promote products
# derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import re
import json
import math
import supybot.ircmsgs as ircmsgs
import supybot.schedule as schedule

import string

import supybot.conf as conf
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    from supybot.i18n import internationalizeDocstring
    _ = PluginInternationalization('ERepublik')
except:
    # This are useless functions that's allow to run the plugin on a bot
    # without the i18n plugin
    _ = lambda x:x
    internationalizeDocstring = lambda x:x

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

class ERepublik(callbacks.Plugin):
    threaded = True


    ##############################################################
    # Battle
    ##############################################################

    class battle(callbacks.Commands):
        def _get(self, irc, name):
            key = conf.supybot.plugins.ERepublik.apikey()
            url = conf.supybot.plugins.ERepublik.url()
            if not key:
                irc.error(_('No API key set. Ask the owner to add one.'),
                        Raise=True)
            try:
                base = '%sbattle/%s.json'
                data = json.load(utils.web.getUrlFd(base % (url, name)))
                return data
            except:
                irc.error(_('This battle does not exist.'), Raise=True)

        def _advinfo(self, irc, msg, args, format_, name):
            """<format> <id>

            Returns informations about a battle with advanced formating."""
            battle = flatten_subdicts(self._get(irc, name))
            repl = lambda x:Template(x).safe_substitute(battle)
            irc.replies(map(repl, format_.split('\\n')))
        advinfo = wrap(_advinfo, ['something', 'int'])

        def active(self, irc, msg, args):
            """takes no arguments

            Returns list of active battles."""
            url = conf.supybot.plugins.ERepublik.url()
            key = conf.supybot.plugins.ERepublik.apikey()
            base = '%sbattle/active.json'
            data = json.load(utils.web.getUrlFd(base % (url)))
            irc.reply(format('%L', map(str, data)))
        active = wrap(active)

        def calc(self, irc, msg, args, name):
            """<name|id>

            Calculates how much damage you can make in one hit."""
            citizen = ERepublik.citizen()._get(irc, name)
            rank = citizen['military']['rank']['level']
            strength = citizen['military']['strength']
            base = citizen['military']['base_hit']
            q1 = base * 1.2000373204
            q2 = q1 * 1.1666925828
            q3 = q2 * 1.14287618286
            q4 = q3 * 1.12501457726
            q5 = q4 * 1.1111226288
            q6 = q5 * 1.10000932923
            q7 = q6 * 1.36358239335
            irc.reply('\x02\x0310Q0:\x02\x03 %s, \x02\x0312Q1\x02\x03: %s, \x02\x0303Q2\x02\x03: %s, \x02\x0309Q3\x02\x03: %s, \x02\x0307Q4\x02\x03: %s, \x02\x0305Q5\x02\x03: %s, \x02\x0311Q6\x02\x03: %s, \x02\x0304Q7\x02\x03: %s' % ('{:,}'.format(base), '{:,}'.format(int(q1)), '{:,}'.format(int(q2)), '{:,}'.format(int(q3)), '{:,}'.format(int(q4)), '{:,}'.format(int(q5)), '{:,}'.format(int(q6)), '{:,}'.format(int(q7))))
        calc = wrap(calc, ['text'])

        def dmg(self, irc, msg, args, name, hit):
            """<name|id> <hits>
            
            Calculates how much damage you can make with <hits> (number of hits) with q7 weapon."""
            citizen = ERepublik.citizen()._get(irc, name)
            base = citizen['military']['base_hit']
            na = citizen['name']
            con = base * 3.00015689556
            coun = con * int(hit)
            irc.reply('%s can make \x02%s\02 of damage with q7 weapon.' % (na, '{:,}'.format(int(coun))))
        dmg = wrap(dmg, ['anything', 'something'])
            

        def _gen(format_, name, doc):
            format_ = re.sub('[ \n]+', ' ', format_)
            def f(self, irc, msg, args, *ids):
                self._advinfo(irc, msg, args, format_, *ids)
            f.__doc__ = """<id>

            %s""" % doc
            return wrap(f, ['int'], name=name)
            
        battle = _gen("""Region: \x02\x0309$region__name\x02\x03 .::. (URL: $url) .::. Attacker total points: \x02\x0304$attacker__points\x02\x03 .::. Attacker name: \x02\x0304$attacker__country__name\x02\x03 .::. Attacker domination by DIV -s \x0307<====>\x03 \x0309DIV 1\x03: \x02\x0304$attacker__divisions__1__domination\x02\x03 .::. \x0309DIV 2\x03: \x02\x0304$attacker__divisions__2__domination\x02\x03 .::.
        \x0309DIV 3\x03: \x02\x0304$attacker__divisions__3__domination\x02\x03 .::. \x0309DIV 4\x03: \x02\x0304$attacker__divisions__4__domination\x02\x03 .::. 
        Defender points: \x02\x0310$defender__points\x02\x03 .::. Defender name: \x02\x0310$defender__country__name.\x02\x03 .::. Defender domination by DIV -s \x0307<====>\x03 \x0309DIV 1\x03: \x02\x0310$defender__divisions__1__domination\x02\x03 .::. \x0309DIV 2\x03: \x02\x0310$defender__divisions__2__domination\x02\x03 .::. \x0309DIV 3\x03: \x02\x0310$defender__divisions__3__domination\x02\x03 .::.
        \x0309DIV 4\x03: \x02\x0310$defender__divisions__4__domination""",
        'battle',
        'Returns general informations about a battle.')

    ##############################################################
    # Citizen
    ##############################################################

    class citizen(callbacks.Commands):
        def _get(self, irc, name):
            url = conf.supybot.plugins.ERepublik.url()
            try:
                if name.isdigit():
                    base = '%scitizen/profile/%s.json'
                    data = json.load(utils.web.getUrlFd(base % (url, name)))
                    color = 3 if data['online'] else 4
                    data['name'] = '\x030%i%s\x0f' % (color, data['name'])
                    return data
                else:
                    base = '%scitizen/search/%s/1.json'
                    data = json.load(utils.web.getUrlFd(base % (url, name)))
                    return self._get(irc, str(data[0]['id']))
            except:
                irc.error(_('This citizen does not exist.'), Raise=True)

        def _advinfo(self, irc, msg, args, format_, name):
            """<format> <name|id>

            Returns informations about a citizen with advanced formating."""
            citizen = flatten_subdicts(self._get(irc, name), flat={
                    'party__name': 'None',
                    'party__id': 0,
                    'party__role': 'N/A',
                    'army__name': 'None',
                    'army__id': 0,
                    'army__role': 'N/A',
                    })
            repl = lambda x:Template(x).safe_substitute(citizen)
            irc.replies(map(repl, format_.split('\\n')))
        advinfo = wrap(_advinfo, ['something', 'text'])

        def _gen(format_, name, doc):
            format_ = re.sub('[ \n]+', ' ', format_)
            def f(self, irc, msg, args, *ids):
                self._advinfo(irc, msg, args, format_, *ids)
            f.__doc__ = """<name|id>

            %s""" % doc
            return wrap(f, ['text'], name=name)

        info = _gen("""\x02Name: %s (ID:\x0310 $id\x03)\x0310,\x03 Level: \x0310$level\x03(XP: \x0310$experience\x03),\x03 Strength:\x0310 $military__strength,\x03 Residence:
        \x0310$residence__region__name, $residence__country__name,\x03 Citizenship:
        \x0310$citizenship__name,\x03 Rank: \x0310$military__rank__name\x03, Rank points: \x0310$military__rank__points\x03, Points to next rank: \x0310$military__rank__toNext\x03, Party: \x0310$party__name - \x0304$party__role\x03 MU:
        \x0310$military__unit__name - \x0304$military__unit__role\x03, Top damage: \x0310$top_damage__damage\x03 achieved on \x0310$top_damage__date\x03, \x0310$top_damage__message\x03, True patriot: \x0310'{:,}'.format($true_patriot__damage)\x03 since \x0310$true_patriot__since\x03.
        """,
        'info',
        'Returns general informations about a citizen.')

        link = _gen("""\x02$name's link\x0310 <->\x03 http://www.erepublik.com/en/citizen/profile/$id """,
        'link',
        'Returns link informations about a citizen.')

        donate = _gen("""\x02$name's donate link\x0310 <->\x03 http://www.erepublik.com/en/economy/donate-items/$id """,
        'donate',
        'Returns link to danate.')

        avatar = _gen("""\x02$name's avatar link\x0310 <->\x03 $avatar """,
        'avatar',
        'Returns avatar link of citizen.')

        @internationalizeDocstring
        def medals(self, irc, msg, args, name):
            """<name|id>

            Displays the citizens medals."""
            citizen = self._get(irc, name)
            medals = ['%s (%i)' % x for x in citizen['medals'].items() if x[1]]
            irc.reply(_('\x02%s\x02 has the following medal(s): \x0310%s\x03, %s') %
                      (name, ', '.join(medals)))
        medals = wrap(medals, ['text'])


    ##############################################################
    # Country
    ##############################################################

    class country(callbacks.Commands):
        def _get(self, irc, name):
            key = conf.supybot.plugins.ERepublik.apikey()
            url = conf.supybot.plugins.ERepublik.url()
            if not key:
                irc.error(_('No API key set. Ask the owner to add one.'),
                        Raise=True)
            try:
                base = '%scountry/%s/%s.json'
                data = json.load(utils.web.getUrlFd(base %
                    (url, name, 'economy')))
                data.update(json.load(utils.web.getUrlFd(base %
                    (name, 'society'))))
                return data
            except:
                irc.error(_('This country does not exist.'), Raise=True)

        def _advinfo(self, irc, msg, args, format_, name):
            """<format> <code>

            Returns informations about a country with advanced formatting."""
            country = flatten_subdicts(self._get(irc, name))
            repl = lambda x:Template(x).safe_substitute(country)
            irc.replies(map(repl, format_.split('\\n')))
        advinfo = wrap(_advinfo, ['something', 'something'])

        def _gen(format_, name, doc):
            format_ = re.sub('[ \n]+', ' ', format_)
            def f(self, irc, msg, args, *ids):
                self._advinfo(irc, msg, args, format_, *ids)
            f.__doc__ = """<code>

            %s""" % doc
            return wrap(f, ['something'], name=name)
            
        society = _gen("""\x02Country: \x0310$name \x03(URL:\x0310 http://www.erepublik.com/en/country/society/$name\x03) \\n\x02\x03Active citizens \x0310$active_citizens,000\x03, \x03Online now \x0310$online_now\x03, \x03New citizens today \x0310$new_citizens_today\x03. """,
        'society',
        'Returns general informations about a society.')

        economy = _gen("""\x02Country: \x0310$name \x03(URL:\x0310 http://www.erepublik.com/en/country/economy/$name\x03) \\n\x02\x03Economy \x0310$treasury__gold Gold - $treasury__cc CC \x03, \x03Taxes import: -Food \x0310$taxes__food__import\x03, -Weapons \x0310$taxes__weapons__import\x03, -Tickets \x0310$taxes__tickets__import\x03, -Frm \x0310$taxes__frm__import\x03, -Wrm \x0310$taxes__wrm__import\x03, -Hospital \x0310$taxes__hospital__import\x03, -Defense \x0310$taxes__defense__import\x03. """,
        'society',
        'Returns general informations about economy.')


    ##############################################################
    # Job market
    ##############################################################

    class jobmarket(callbacks.Commands):
        def _get(self, irc, country, page):
            page = page or 1
            key = conf.supybot.plugins.ERepublik.apikey()
            url = conf.supybot.plugins.ERepublik.url()
            if not key:
                irc.error(_('No API key set. Ask the owner to add one.'),
                        Raise=True)
            try:
                base = '%sjobmarket/%s.json'
                ids = '/'.join((country, str(page)))
                data = json.load(utils.web.getUrlFd(base % (url, ids)))
                return data
            except:
                irc.error(_('This job market does not exist.'), Raise=True)

        def _advinfo(self, irc, msg, args, format_,
                country, page):
            """<format> <country> [<page>]

            Returns informations about a job market with advanced formating."""
            jobmarket = flatten_subdicts(self._get(irc, country, page))
            repl = lambda x:Template(x).safe_substitute(jobmarket)
            irc.replies(map(repl, format_.split('\\n')))
        advinfo = wrap(_advinfo, ['something', 'something', optional('int')])

        def _gen(format_, name, doc):
            format_ = re.sub('[ \n]+', ' ', format_)
            def f(self, irc, msg, args, *ids):
                self._advinfo(irc, msg, args, format_, *ids)
                medals = [', '.join(['%s: %s' % x for x in d.items()]) for d in data]
            f.__doc__ = """<format> <country> [<page>]

            %s""" % doc
            return wrap(f, ['something', optional('int')], name=name)
			
        def emlo(self, irc, msg, args, country, page):
            """<country> [<page>]

            Gives info about emplos"""
            page = page or 1
            url = conf.supybot.plugins.ERepublik.url()
            base = ('%sjobmarket/%s/%s.json'	% (country, page))
            data = json.load(utils.web.getUrlFd(base % (url)))
            emplos = [', '.join(['%s: %s' % x for x in d.items()]) for d in data]
            irc.reply(_('has the following medal(s): \x0310%s\x03') %
                    (', '.join(emplos)))
        emlo = wrap(emlo, ['something', optional('int')])


    ##############################################################
    # Market
    ##############################################################

    class market(callbacks.Commands):
        def _get(self, irc, country, industry, quality, page):
            page = page or 1
            key = conf.supybot.plugins.ERepublik.apikey()
            url = conf.supybot.plugins.ERepublik.url()
            if not key:
                irc.error(_('No API key set. Ask the owner to add one.'),
                        Raise=True)
            try:
                base = '%smarket/%s.json'
                ids = '/'.join((country, industry, str(quality), str(page)))
                data = json.load(utils.web.getUrlFd(base % (url, ids)))
                return data
            except:
                irc.error(_('This market does not exist.'), Raise=True)

        def _advinfo(self, irc, msg, args, format_, *ids):
            """<format> <country> <industry> <quality> [<page>]

            Returns informations about a market with advanced formating."""
            market = flatten_subdicts(self._get(irc, *ids))
            repl = lambda x:Template(x).safe_substitute(market)
            irc.replies(map(repl, format_.split('\\n')))
        advinfo = wrap(_advinfo, ['something', 'something', 'something',
            'int', optional('int')])

        def _gen(format_, name, doc):
            format_ = re.sub('[ \n]+', ' ', format_)
            def f(self, irc, msg, args, *ids):
                self._advinfo(irc, msg, args, format_, *ids)
            f.__doc__ = """<format> <country> <industry> <quality> [<page>]

            %s""" % doc
            return wrap(f, ['something', 'something', 'int', optional('int')],
                    name=name)


    ##############################################################
    # Mu
    ##############################################################

    class mu(callbacks.Commands):
        def _get(self, irc, name):
            key = conf.supybot.plugins.ERepublik.apikey()
            url = conf.supybot.plugins.ERepublik.url()
            if not key:
                irc.error(_('No API key set. Ask the owner to add one.'),
                        Raise=True)
            try:
                base = '%sunit/%s.json'
                data = json.load(utils.web.getUrlFd(base % (url, name)))
                return data
            except:
                irc.error(_('This Military Unit does not exist.'), Raise=True)

        def _advinfo(self, irc, msg, args, format_, name):
            """<format> <id>

            Returns informations about a Military Unit with advanced formating."""
            mu = flatten_subdicts(self._get(irc, name))
            repl = lambda x:Template(x).safe_substitute(mu)
            irc.replies(map(repl, format_.split('\\n')))
        advinfo = wrap(_advinfo, ['something', 'int'])

        def _gen(format_, name, doc):
            format_ = re.sub('[ \n]+', ' ', format_)
            def f(self, irc, msg, args, *ids):
                self._advinfo(irc, msg, args, format_, *ids)
            f.__doc__ = """<id>

            %s""" % doc
            return wrap(f, ['int'], name=name)


    ##############################################################
    # Party
    ##############################################################

    class party(callbacks.Commands):
        def _get(self, irc, name):
            key = conf.supybot.plugins.ERepublik.apikey()
            url = conf.supybot.plugins.ERepublik.url()
            if not key:
                irc.error(_('No API key set. Ask the owner to add one.'),
                        Raise=True)
            try:
                base = '%sparty/%s.json'
                data = json.load(utils.web.getUrlFd(base % (name)))
                return data
            except:
                irc.error(_('This party does not exist.'), Raise=True)

        def _advinfo(self, irc, msg, args, format_, name):
            """<format> <id>

            Returns informations about a party with advanced formating."""
            party = flatten_subdicts(self._get(irc, name))
            repl = lambda x:Template(x).safe_substitute(party)
            irc.replies(map(repl, format_.split('\\n')))
        advinfo = wrap(_advinfo, ['something', 'int'])

        def _gen(format_, name, doc):
            format_ = re.sub('[ \n]+', ' ', format_)
            def f(self, irc, msg, args, *ids):
                self._advinfo(irc, msg, args, format_, *ids)
            f.__doc__ = """<id>

            %s""" % doc
            return wrap(f, ['int'], name=name)

ERepublik = internationalizeDocstring(ERepublik)
Class = ERepublik


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79: