# -*- coding: utf-8 -*-
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
import re
import string

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('SahadHelp')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class SahadHelp(callbacks.Plugin):
    """Add the help for "@plugin help SahadHelp" here
    This should describe *how* to use this plugin."""
    threaded = True

    def doJoin(self, irc, msg):
        t = msg.prefix
        nick_split = string.split(t, '!')
        nick = nick_split[0]
        big_nick = nick_split[0]
        channel = msg.args[0]
        if channel == '#e-sim.secura.support':
            nicks = ', '.join(irc.state.channels['#e-sim.secura.support'].users)
            if nick in nicks:
                irc.queueMsg(ircmsgs.notice(nick, 'Hi, %s. State your issue and wait patiently.' % big_nick))

    def doPrivmsg(self, irc, msg):
        nick = msg.nick
        channel = msg.args[0]
        message = msg.args[1]
        if channel == '#e-sim.secura.support':
            nicks = ', '.join(irc.state.channels['#e-sim.secura.support'].users)
            if nick in nicks:
                if message == '!rules':
                    irc.reply('You can use following arguments: \x034acc, bots, bugs, exploiting, password, trading, hts, pi, tat, eps, sp, f, responsibility, spam\x03 = For example: \x034+rules acc\x03')
                if message == '!commands':
                    irc.reply('>>> \x02Commands\x02: = \x02!rules\x02 & \x02!ts\x02 & \x02!ts help\x02 & \x02!wiki\x02 & \x02!ip form\x02 & \x02!forum\x02 & \x02!esim laws\x02')
                if message == '!ts':
                    irc.reply('http://tickets.e-sim.org/')
                if message == '!ts help':
                    irc.reply('http://secura.e-sim.org/article.html?id=16595')
                if message == '!wiki':
                    irc.reply('http://wiki.e-sim.org/index.php/Category:Tutorials')
                if message == '!ip form':
                    irc.reply('http://tinyurl.com/d9e23a')
                if message == '!forum':
                    irc.reply('http://forum.e-sim.org/')
                if message == '!esim laws':
                    irc.reply('http://secura.e-sim.org/laws.html')
            if channel != '#e-sim.secura.support':
                irc.queueMsg(ircmsgs.notice(nick, "This command is available only on one channel, this channel is set to +s (secret) and I'm not going to tell you channel name, sorry."))

    class rules(callbacks.Commands):

        def acc(self, irc, msg, args):
            """takes no arguments

            Displays Account rules"""
            nick = msg.nick
            message = ('You are only allowed to have one citizen account. Violating this law may result in a permanent ban of all your accounts.If you have declared your shared IP with other accounts, you are still not allowed to be together in the same military unit, work for eachother nor any sorts of transactions. It is only allowed to have a total amount of 4 accounts on the shared IP or PC. It is forbidden to have any transactions (beside referral gold) with anyone sharing your IP or PC.')
            if msg.args[0].lower() == '#e-sim.secura.support':
                nicks = ', '.join(irc.state.channels['#e-sim.secura.support'].users)
                if nick in nicks:
                    irc.reply(message)
            else:
                irc.reply("This command is available only on one channel, this channel is set to +s (secret) and I'm not going to tell you channel name, sorry.")
        acc = wrap(acc)

        def bots(self, irc, msg, args):
            """takes no arguments

            Displays Bots rules"""
            nick = msg.nick
            message = ('Using bots or automated software to play the game is strictly forbidden.Procedure: Using any kind of automated software or bots (auto-fighting scripts, mass message scripts, auto subscribe scripts, monetary market scripts and others) to play the game will instantly lead to a Permanent ban of that Citizen without any warning. A User is allowed to use automated software to play the game ONLY if the software is approved by Amepton Management Ltd.')
            if msg.args[0].lower() == '#e-sim.secura.support':
                nicks = irc.state.channels['#e-sim.secura.support'].users
                if nick in nicks:
                    irc.reply(message)
            else:
                irc.reply("This command is available only on one channel, this channel is set to +s (secret) and I'm not going to tell you channel name, sorry.")
        bots = wrap(bots)

        def bugs(self, irc, msg, args):
            """takes no arguments

            Displays Bugs rules"""
            nick = msg.nick
            message = ('Exploiting bugs will result in a permanent ban. If a player finds a bug in-game and utilises it in order to cause damage to, or gain an advantage over other players, they will be penalised depending on the scale of the offence. The penalty can vary from a temporary ban to permanent ban.Note: With reporting a Bug to e-Sim Team through the ticket system that is resolved, you will be rewarded with 5 Gold and a Tester Medal.')
            if msg.args[0].lower() == '#e-sim.secura.support':
                nicks = ', '.join(irc.state.channels['#e-sim.secura.support'].users)
                if nick in nicks:
                    irc.reply(message)
            else:
                irc.reply("This command is available only on one channel, this channel is set to +s (secret) and I'm not going to tell you channel name, sorry.")
        bugs = wrap(bugs)

        def exploiting(self, irc, msg, args):
            """takes no arguments

            Displays Exploiting rules"""
            nick = msg.nick
            message = ('Exploiting other players and being exploited is forbidden. Having players work for a low wage (under the average salary for the concerned skill) in the country where the company is located, without any transaction in return equivalent to this salary. This includes account boosting. Meaning that one/several accounts are used to send their assets/work for free for another user to gain resources even if it’s by the citizens own will.')
            if msg.args[0].lower() == '#e-sim.secura.support':
                nicks = ', '.join(irc.state.channels['#e-sim.secura.support'].users)
                if nick in nicks:
                    irc.reply(message)
            else:
                irc.reply("This command is available only on one channel, this channel is set to +s (secret) and I'm not going to tell you channel name, sorry.")
        exploiting = wrap(exploiting)

        def password(self, irc, msg, args):
            """takes no arguments

            Displays Password rules"""
            nick = msg.nick
            message = ('If Your password appears to have been shared with another player and you declare account theft, the staff team will not take action to return the account, and the account might be permanently banned. Account-sitting requires you to share your account information and is therefore forbidden. Each player is allowed to control one account. Controlling more then one accounts may lead to temporary or permanent ban of all accounts controlled by the player.')
            if msg.args[0].lower() == '#e-sim.secura.support':
                nicks = ', '.join(irc.state.channels['#e-sim.secura.support'].users)
                if nick in nicks:
                    irc.reply(message)
            else:
                irc.reply("This command is available only on one channel, this channel is set to +s (secret) and I'm not going to tell you channel name, sorry.")
        password = wrap(password)

        def trading(self, irc, msg, args):
            """takes no arguments

            Displays Trading rules"""
            nick = msg.nick
            message = ('Exchanging, selling or buying any content of E-sim (accounts, gold, items, currencies, companies etc) that is traded with anything in another game is forbidden and may result in a permanent ban (of all concerned accounts).')
            if msg.args[0].lower() == '#e-sim.secura.support':
                nicks = ', '.join(irc.state.channels['#e-sim.secura.support'].users)
                if nick in nicks:
                    irc.reply(message)
            else:
                irc.reply("This command is available only on one channel, this channel is set to +s (secret) and I'm not going to tell you channel name, sorry.")
        trading = wrap(trading)

        def hts(self, irc, msg, args):
            """takes no arguments

            Displays HTS (HTS stands for - Hiring Transferring Stealing) rules"""
            nick = msg.nick
            message = ('It is illegal to fraud investor’s money from Public Companies or national military units. \x034H\x03iring yourself in public companies to work for high salary is forbidden. \x034T\x03ransferring Money/Gold through Monetary Market at inappropriate ratios is forbidden. \x034S\x03tealing any gold/currency/items etc for your own interests is forbidden.')
            if msg.args[0].lower() == '#e-sim.secura.support':
                nicks = ', '.join(irc.state.channels['#e-sim.secura.support'].users)
                if nick in nicks:
                    irc.reply(message)
            else:
                irc.reply("This command is available only on one channel, this channel is set to +s (secret) and I'm not going to tell you channel name, sorry.")
        hts = wrap(hts)

        def pl(self, irc, msg, args):
            """takes no arguments

            Displays Personal Informations rules"""
            nick = msg.nick
            message = ('Publishing \x034p\x03ersonal \x034i\x03nformation* about any E-sim citizen without permission is forbidden. Personal information: Real names, addresses, pictures, e-mails, phone numbers, and other information that are clarified by the Staff as personal information. Procedure: Breaking this law will result with warning / temporary or permanent ban of the publisher.')
            if msg.args[0].lower() == '#e-sim.secura.support':
                nicks = ', '.join(irc.state.channels['#e-sim.secura.support'].users)
                if nick in nicks:
                    irc.reply(message)
            else:
                irc.reply("This command is available only on one channel, this channel is set to +s (secret) and I'm not going to tell you channel name, sorry.")
        pl = wrap(pl)

        def tat(self, irc, msg, args):
            """takes no arguments

            Displays TAT (TAT stands for - abuse Towards the Administration Team) rules"""
            nick = msg.nick
            message = ('Any type of abuse \x034t\x03owards the \x034a\x03dministration \x034t\x03eam will be penalised.Insulting, threatening, provoking, abusing, or petitioning the administration team or any of its members with false or trivial issues is forbidden and will result in permanent ban.Impersonating in any kind of way, any member of the Staff, is strictly prohibited. Using a nickname almost identical to a Staff member is not allowed.')
            if msg.args[0].lower() == '#e-sim.secura.support':
                nicks = ', '.join(irc.state.channels['#e-sim.secura.support'].users)
                if nick in nicks:
                    irc.reply(message)
            else:
                irc.reply("This command is available only on one channel, this channel is set to +s (secret) and I'm not going to tell you channel name, sorry.")
        tat = wrap(tat)

        def eps(self, irc, msg, args):
            """takes no arguments

            Displays EPS (EPS stands for - External Phishing Sites) rules"""
            nick = msg.nick
            message = ('It is forbidden to convince people to click on adverts or \x034e\x03xternal \x034p\x03hising \x034s\x03ites. Convincing or forcing other players to click on any external link that lead to an advert or any other external site may lead to a permanent ban.')
            if msg.args[0].lower() == '#e-sim.secura.support':
                nicks = ', '.join(irc.state.channels['#e-sim.secura.support'].users)
                if nick in nicks:
                    irc.reply(message)
            else:
                irc.reply("This command is available only on one channel, this channel is set to +s (secret) and I'm not going to tell you channel name, sorry.")
        eps = wrap(eps)

        def sp(self, irc, msg, args):
            """takes no arguments

            Displays SP (SP stands for - Stealing Properties) rules"""
            nick = msg.nick
            message = ('\x034S\x03tealing \x034p\x03roperties from national organisations is illegal and may result in a permanent ban.')
            if msg.args[0].lower() == '#e-sim.secura.support':
                nicks = ', '.join(irc.state.channels['#e-sim.secura.support'].users)
                if nick in nicks:
                    irc.reply(message)
            else:
                irc.reply("This command is available only on one channel, this channel is set to +s (secret) and I'm not going to tell you channel name, sorry.")
        sp = wrap(sp)

        def f(self, irc, msg, args):
            """takes no arguments

            Displays F (F stands for - Fraud) rules"""
            nick = msg.nick
            message = ('Any \x034f\x03raud of money/properties from stock companies is illegal.')
            if msg.args[0].lower() == '#e-sim.secura.support':
                nicks = ', '.join(irc.state.channels['#e-sim.secura.support'].users)
                if nick in nicks:
                    irc.reply(message)
            else:
                irc.reply("This command is available only on one channel, this channel is set to +s (secret) and I'm not going to tell you channel name, sorry.")
        f = wrap(f)

        def responsibility(self, irc, msg, args):
            """takes no arguments

            Displays Responsibility rules"""
            nick = msg.nick
            message = ('The Staff does not take any \x034responsibility\x03 for lost items, gold, currency, military units, stock companies etc in the game that is lost. This includes belongings that have been lost through scams, trades done outside the game, external website phising, false contracts and more.')
            if msg.args[0].lower() == '#e-sim.secura.support':
                nicks = ', '.join(irc.state.channels['#e-sim.secura.support'].users)
                if nick in nicks:
                    irc.reply(message)
            else:
                irc.reply("This command is available only on one channel, this channel is set to +s (secret) and I'm not going to tell you channel name, sorry.")
        responsibility = wrap(responsibility)

        def spam(self, irc, msg, args):
            """takes no arguments

            Displays Responsibility rules"""
            nick = msg.nick
            message = ('All contents published by users cannot contain spam, pornography, racism, flaming, insulting content, nazism, external advertising, vulgarity, violations of any real life law or anything that the Staff team will consider as highly abusive.')
            if msg.args[0].lower() == '#e-sim.secura.support':
                nicks = ', '.join(irc.state.channels['#e-sim.secura.support'].users)
                if nick in nicks:
                    irc.reply(message)
            else:
                irc.reply("This command is available only on one channel, this channel is set to +s (secret) and I'm not going to tell you channel name, sorry.")
        spam = wrap(spam)

Class = SahadHelp


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
