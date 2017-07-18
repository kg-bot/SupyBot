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
import supybot.ircmsgs as ircmsgs
import random
import time
import json
import os

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('BlJack')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class BlJack(callbacks.Plugin):
    """Add the help for "@plugin help BlJack" here
    This should describe *how* to use this plugin."""
    threaded = True
    try:
        with open('G:\supybot\Bingo\private.json', 'r') as pl:
            b = json.loads(pl.read())
    except:
        b = []
        pass
    global private_list
    if b == []:
        private_list = []
    else:
        private_list = b

    def bet(self, irc, msg, args, numbers):
        """<numbers>

        Give the numbers for \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02"""
        nick = msg.nick
        nicks = ', '.join(irc.state.channels['#loto'].users)
        if nick in nicks:
            na = '%s-name' % nick
            li = '%s-nums' % nick
            try:
                with open('G:\supybot\Bingo\Bets\%s.json' % 'bets', 'r') as d:
                    b = json.loads(d.read())
                    n = b[na]
            except KeyError:
                b[na] = nick
                b[li] = ', '.join(sorted(numbers, key=int))
                x = {}
                x[na] = nick
                x[li] = numbers
                with open('G:\supybot\Bingo\Players\%s.json' % nick, 'w') as let:
                    let.write(json.dumps(x))
                with open('G:\supybot\Bingo\Bets\%s.json' % 'bets', 'w') as k:
                    k.write(json.dumps(b))
                with open('G:\supybot\Bingo\Bets\%s.json' % 'betnames', 'r') as betNames:
                    p = json.loads(betNames.read())
                p[na] = nick
                with open('G:\supybot\Bingo\Bets\%s.json' % 'betnames', 'w') as BetNames:
                    BetNames.write(json.dumps(p))
                irc.reply('You have placed your bet for the upcoming \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02. Your numbers are: %s' % (', '.join(sorted(numbers, key=int))))
                irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', "%s has placed a bet for the upcoming \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02. His numbers are: %s" % (nick, ', '.join(sorted(numbers, key=int)))))
            else:
                irc.reply("You have already placed bet for this \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02, you can't change them. You can always send a message to some of our AOPs/SOPs on #loto and tell them why you want to change your bet")
        else:
            irc.reply("You can't play \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 or place a bet unless you're on #loto . Go to #loto and read topic.")
    bet = wrap(bet, [many('something'), 'private'])

    def loto(self, irc, msg, args, channel):
        """Takes no arguments

        Plays round of \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02."""
        global badmin
        badmin = {}
        badmin['Admin-Nick'] = msg.nick
        global b_admin
        b_admin = badmin['Admin-Nick']
        #with open('bingoadmin.json', 'w') as admin:
            #admin.write(json.dumps(badmin))
        with open('G:\supybot\Bingo\Bets\%s.json' % 'betn', 'r') as n:
            bet_n = json.loads(n.read())
        global betnumber
        betnumber = bet_n.values()[0]
        global nextgame
        nextgame = betnumber++1
        global top
        top = ("Welcome to \x0310%s\x03. You can read rules at Rules-Link, you can apply for next \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 here Form-Link (please read carefully everything on it). Next game is for \x023 days at 22:00PM\x02 (Game No. \x02%s\x03). My last game admin was: \x037%s\x03" % (channel, ircutils.mircColor(nextgame, 'teal'), b_admin))
        if channel == '#loto':
            irc.reply("Starting a \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 game No. \x02%s\x02" % ircutils.mircColor(betnumber, 'red'))
            irc.queueMsg(ircmsgs.mode(channel, '+m'))
            irc.queueMsg(ircmsgs.mode(channel, '+i'))
            num = random.sample(range(39), 7)
            num1 = num[0]
            num2 = num[1]
            num3 = num[2]
            num4 = num[3]
            num5 = num[4]
            num6 = num[5]
            num7 = num[6]
            global numbers1
            numbers1 = [', '.join(['%s' % e]) for e in num]
            irc.reply('1st number is: %s' % num1)
            time.sleep(7)
            irc.reply('2nd number is: %s' % num2)
            time.sleep(7)
            irc.reply('3rd number is: %s' % num3)
            time.sleep(7)
            irc.reply('4th number is: %s' % num4)
            time.sleep(7)
            irc.reply('5th number is: %s' % num5)
            time.sleep(7)
            irc.reply('6th number is: %s' % num6)
            time.sleep(7)
            irc.reply('7th number is: %s' % num7)
            irc.reply("Current numbers are: %s" % ', '.join(sorted(numbers1, key=int)))
            irc.reply("Please be patient 'till administrators and moderators check your bets. Channel will be unmoderated once the checking finishes. Thank you very much for your understanding, and please \x034\x02don't query moderators and administrators while they work on your bets, you don't want them to make mistake\x02\x03.")
        else:
            irc.reply('\x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 is not available on this channel. Go to #loto and read topic')
    loto = wrap(loto, [("checkChannelCapability", 'op')])

    def bclear(self, irc, msg, args):
        """takes no arguments

        Clears current bet and resets all files"""
        nick = msg.nick
        next = nextgame
        channel = '#loto'
        gameTime = {}
        gameTime['time'] = next
        with open('G:\supybot\Bingo\Bets\%s.json' % 'betn', 'w') as t:
            t.write(json.dumps(gameTime))
        if nick in private_list:
            l = {}
            l['Test-name'] = None
            l['Test-nums'] = None
            checkEmpty = {}
            checkEmpty['Test-Name'] = 'Test'
            betNames = {}
            betNames['Test-name'] = 'Test'
            with open('G:\supybot\Bingo\Schecks\schecks.json', 'w') as ch:
                ch.write(json.dumps(checkEmpty))
            global numbers1
            numbers1 = []
            with open('G:\supybot\Bingo\Bets\%s.json' % 'bets', 'w') as k:
                k.write(json.dumps(l))
            with open('G:\supybot\Bingo\Bets\%s.json' % 'betnames', 'w') as BetNames:
                BetNames.write(json.dumps(betNames))
            with open('G:\supybot\Bingo\Jackpots\jackpot.json', 'w') as pot:
                pot.write(json.dumps(betNames))
            with open('G:\supybot\Bingo\Wins\win6.json', 'w') as pot:
                pot.write(json.dumps(betNames))
            with open('G:\supybot\Bingo\Wins\win5.json', 'w') as pot:
                pot.write(json.dumps(betNames))
            with open('G:\supybot\Bingo\Wins\win4.json', 'w') as pot:
                pot.write(json.dumps(betNames))
            with open('G:\supybot\Bingo\Wins\win3.json', 'w') as pot:
                pot.write(json.dumps(betNames))
            with open('G:\supybot\Bingo\Wins\win2.json', 'w') as pot:
                pot.write(json.dumps(betNames))
            with open('G:\supybot\Bingo\Wins\win1.json', 'w') as pot:
                pot.write(json.dumps(betNames))
            """with open('G:\supybot\Bingo\Wins\win8.json', 'w') as pot:
                pot.write(json.dumps(betNames))
            with open('G:\supybot\Bingo\Wins\win7.json', 'w') as pot:
                pot.write(json.dumps(betNames))
            with open('G:\supybot\Bingo\Wins\win6.json', 'w') as pot:
                pot.write(json.dumps(betNames))
            with open('G:\supybot\Bingo\Wins\win5.json', 'w') as pot:
                pot.write(json.dumps(betNames))"""
            irc.reply("Done. Everything's clear and ready for next game.")
            irc.queueMsg(ircmsgs.mode(channel, '-m'))
            irc.queueMsg(ircmsgs.mode(channel, '-i'))
            irc.queueMsg(ircmsgs.topic(channel, top))
        else:
            irc.reply("You're not \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 administrator or moderator, this will be reported to all admins, moderators and to my owner. Fuck of")
            irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has tried to do +bclear but he is not in my private list." % (nick)))
            irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', "%s has tried to do +bclear but he is not in my private list. I've notified %s about this." % (nick, b_admin)))
    bclear = wrap(bclear, [('private')])

    def chbet(self, irc, msg, args):
        """takes no arguments

        Returns bets for current game"""
        nick = msg.nick
        nicks = ', '.join(irc.state.channels['#loto'].users)
        if nick in private_list:
            with open('G:\supybot\Bingo\Bets\%s.json' % 'bets', 'r') as d:
                b = json.loads(d.read())
            it = b.items()
            it.sort()
            v = [', '.join(['%s' % v]) for k, v in it]
            irc.queueMsg(ircmsgs.privmsg(nick, '%s' % ', '.join(v)))
            irc.queueMsg(ircmsgs.privmsg(nick, 'Current bet numbers are: %s' % ', '.join(sorted(numbers1, key=int))))
            if v == ', '.join(sorted(numbers1, key=int)):
                irc.reply(nicks)
                irc.reply('We have a \x02\x038,10JACKPOT\x03\x02')
        else:
            irc.reply("You're not \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 administrator or moderator, this will be reported to all admins, moderators and to my owner. Fuck of")
            irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has tried to do +chbet but he is not in my private list." % (nick)))
            irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', "%s has tried to do +chbet but he is not in my private list. I've notified %s about this." % (nick, b_admin)))
    chbet = wrap(chbet, [('private')])

    def scheck(self, irc, msg, args):
        """takes no arguments

        Checks if you have won any price on \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02."""
        nick = msg.nick
        li = '%s-nums' % nick
        na = '%s-name' % nick
        nicks = ', '.join(irc.state.channels['#loto'].users)
        with open('G:\supybot\Bingo\Wins\win6.json', 'r') as pot14:
            po14 = json.loads(pot14.read())
        with open('G:\supybot\Bingo\Wins\win5.json', 'r') as pot13:
            po13 = json.loads(pot13.read())
        with open('G:\supybot\Bingo\Wins\win4.json', 'r') as pot12:
            po12 = json.loads(pot12.read())
        with open('G:\supybot\Bingo\Wins\win3.json', 'r') as pot11:
            po11 = json.loads(pot11.read())
        with open('G:\supybot\Bingo\Wins\win2.json', 'r') as pot10:
            po10 = json.loads(pot10.read())
        with open('G:\supybot\Bingo\Wins\win1.json', 'r') as pot9:
            po9 = json.loads(pot9.read())
        """with open('G:\supybot\Bingo\Wins\win8.json', 'r') as pot8:
            po8 = json.loads(pot8.read())
        with open('G:\supybot\Bingo\Wins\win7.json', 'r') as pot7:
            po7 = json.loads(pot7.read())
        with open('G:\supybot\Bingo\Wins\win6.json', 'r') as pot6:
            po6 = json.loads(pot6.read())
        with open('G:\supybot\Bingo\Wins\win5.json', 'r') as pot5:
            po5 = json.loads(pot5.read())"""
        with open('G:\supybot\Bingo\Jackpots\jackpot.json', 'r') as pot:
            po = json.loads(pot.read())
        with open('G:\supybot\Bingo\Schecks\schecks.json', 'r') as checks:
            b = json.loads(checks.read())
        b[na] = nick
        with open('G:\supybot\Bingo\Schecks\schecks.json', 'w') as checks:
            checks.write(json.dumps(b))
        try:
            with open('G:\supybot\Bingo\Players\%s.json' % nick, 'r') as let:
                try:
                    x = json.loads(let.read())
                except ValueError:
                    irc.reply("You haven't placed any bet for this \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02. More luck next time")
                    return
        except IOError:
            irc.queueMsg(ircmsgs.privmsg(nick, "You haven't ever placed any bet for this \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02, more luck next time"))
            return
        else:
            numes = x[li]
            numes_list = sorted(numes, key=int)
            numes1 = ', '.join(numes_list[0:1])
            try:
                numes1_1 = numes_list[0] # first bet number
                numes1_2 = numes_list[1] # second bet number
                numes1_3 = numes_list[2] # 3th bet number
                numes1_4 = numes_list[3] # 4th bet number
                numes1_5 = numes_list[4] # 5th bet number
                numes1_6 = numes_list[5] # 6th bet number
                numes1_7 = numes_list[6] # 7th bet number
            except IndexError:
                irc.reply("Sorry but you have placed bet with less then 7 numbers, you must give me exactly 7 numbers for loto")
            else:
                # End of one number check, below is two numbers check
                # End of two numbers check, below is three numbers check
                # End of three numbers check, below is four numbers check
                # End of four numbers check. below is five numbers check
                # End of six numbers check, below is seven numbers check (jackpot)
                jackpot = ', '.join(numes_list)
                #numes12 = ', '.join(numes_list[0:12])
                #numes13 = ', '.join(numes_list[0:13])
                #numes14 = ', '.join(numes_list[0:14])
                #numes15 = ', '.join(numes_list[0:15])
                win_sort = sorted(numbers1, key=int)
                win1 = ', '.join(win_sort[0:1])
                win2 = ', '.join(win_sort[0:2])
                win3 = ', '.join(win_sort[0:3])
                win4 = ', '.join(win_sort[0:4])
                win5 = ', '.join(win_sort[0:5])
                win6 = ', '.join(win_sort[0:6])
                win6_1 = ', '.join(win_sort[1:7])
                win7 = ', '.join(win_sort)
                #win12 = ', '.join(win_sort[0:12])
                #win13 = ', '.join(win_sort[0:13])
                #win14 = ', '.join(win_sort[0:14])
                #win15 = ', '.join(win_sort[0:15])
                nunka = numes_list + win_sort
                irc.reply(nunka)
                irc.reply("Current \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 numbers are: %s." % ', '.join(win_sort))
                irc.reply("Your ticket numbers are: %s" % ', '.join(numes_list))
                irc.reply("Now lets check if you got any prize this time. You need at least 5 correct numbers to get some price.")
                if jackpot == win7:
                    irc.queueMsg(ircmsgs.privmsg(nick, '\x02\x038C\x03\x0310O\x03\x039N\x03\x037G\x03\x034R\x03\x0311A\x03\x0312T\x03\x0313S\x03!\x02 you have won a fucking \x038\x02JACKPOT!\x02\x03.'))
                    irc.queueMsg(ircmsgs.privmsg('#loto', nicks))
                    irc.queueMsg(ircmsgs.privmsg('#loto', ("We have a \x038\x02JACKPOT!\x02\x03 in this game Ladies and Gentlemen, say \x02\x038C\x03\x0310O\x03\x039N\x03\x037G\x03\x034R\x03\x0311A\x03\x0312T\x03\x0313S\x03!\x02 to %s" % nick)))
                    po[na] = nick
                    with open('G:\supybot\Bingo\Jackpots\jackpot.json', 'w') as pot:
                        pot.write(json.dumps(po))
                    return
                elif numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort:
                    irc.queueMsg(ircmsgs.privmsg(nick, "You have 6 correct numbers, this is already been reported to admins and mods, please be patient while we check if everything was regular, you will be contacted from some of our admins about receiving your prize"))
                    irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has checked win6 and he won it, please check if everything was correct and speak with him about his prize" % nick))
                    po14[na] = nick
                    with open('G:\supybot\Bingo\Wins\win6.json', 'w') as pot:
                        pot.write(json.dumps(po14))
                elif numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[3] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort:
                    irc.queueMsg(ircmsgs.privmsg(nick, "You have 13 correct numbers, this is already been reported to admins and mods, please be patient while we check if everything was regular, you will be contacted from some of our admins about receiving your prize"))
                    irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has checked win13 and he won it, please check if everything was correct and speak with him about his prize" % nick))
                    po13[na] = nick
                    with open('G:\supybot\Bingo\Wins\win5.json', 'w') as pot:
                        pot.write(json.dumps(po13))
                elif numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[4] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[3] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[3] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort and numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[3] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[5] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[6] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[1] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[1] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[1] in win_sort and numes_list[3] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[1] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[2] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort:
                    irc.queueMsg(ircmsgs.privmsg(nick, "You have 12 correct numbers, this is already been reported to admins and mods, please be patient while we check if everything was regular, you will be contacted from some of our admins about receiving your prize"))
                    irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has checked win12 and he won it, please check if everything was correct and speak with him about his prize" % nick))
                    po12[na] = nick
                    with open('G:\supybot\Bingo\Wins\win4.json', 'w') as pot:
                        pot.write(json.dumps(po12))
                elif numes_list[0] in win_sort and numes_list[1] and numes_list[2] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[3] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[4] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[1] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort and numes_list[4] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort or \
                        numes_list[0] in win_sort and numes_list[3] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[3] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[0] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[3] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[4] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[5] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort and numes_list[6] in win_sort or \
                        numes_list[1] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort or \
                        numes_list[1] in win_sort and numes_list[3] in win_sort and numes_list[5] in win_sort or \
                        numes_list[1] in win_sort and numes_list[3] in win_sort and numes_list[6] in win_sort or \
                        numes_list[1] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[1] in win_sort and numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[1] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[4] in win_sort or \
                        numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[5] in win_sort or \
                        numes_list[2] in win_sort and numes_list[3] in win_sort and numes_list[6] in win_sort or \
                        numes_list[2] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[2] in win_sort and numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[2] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[3] in win_sort and numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[3] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort or \
                        numes_list[4] in win_sort and numes_list[5] in win_sort and numes_list[6] in win_sort:
                    irc.queueMsg(ircmsgs.privmsg(nick, "You have 11 correct numbers, this is already been reported to admins and mods, please be patient while we check if everything was regular, you will be contacted from some of our admins about receiving your prize"))
                    irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has checked win11 and he won it, please check if everything was correct and speak with him about his prize" % nick))
                    po11[na] = nick
                    with open('G:\supybot\Bingo\Wins\win3.json', 'w') as pot:
                        pot.write(json.dumps(po11))
                elif numes_list[0] in win_sort and numes_list[1] in win_sort or \
                        numes_list[0] in win_sort and numes_list[2] in win_sort or \
                        numes_list[0] in win_sort and numes_list[3] in win_sort or \
                        numes_list[0] in win_sort and numes_list[4] in win_sort or \
                        numes_list[0] in win_sort and numes_list[5] in win_sort or \
                        numes_list[0] in win_sort and numes_list[6] in win_sort or \
                        numes_list[1] in win_sort and numes_list[2] in win_sort or \
                        numes_list[1] in win_sort and numes_list[3] in win_sort or \
                        numes_list[1] in win_sort and numes_list[4] in win_sort or \
                        numes_list[1] in win_sort and numes_list[5] in win_sort or \
                        numes_list[1] in win_sort and numes_list[6] in win_sort or \
                        numes_list[2] in win_sort and numes_list[3] in win_sort or \
                        numes_list[2] in win_sort and numes_list[4] in win_sort or \
                        numes_list[2] in win_sort and numes_list[5] in win_sort or \
                        numes_list[2] in win_sort and numes_list[6] in win_sort or \
                        numes_list[3] in win_sort and numes_list[4] in win_sort or \
                        numes_list[3] in win_sort and numes_list[5] in win_sort or \
                        numes_list[3] in win_sort and numes_list[6] in win_sort or \
                        numes_list[4] in win_sort and numes_list[5] in win_sort or \
                        numes_list[4] in win_sort and numes_list[6] in win_sort or \
                        numes_list[5] in win_sort and numes_list[6] in win_sort:
                    irc.queueMsg(ircmsgs.privmsg(nick, "You have 10 correct numbers, this is already been reported to admins and mods, please be patient while we check if everything was regular, you will be contacted from some of our admins about receiving your prize"))
                    irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has checked win10 and he won it, please check if everything was correct and speak with him about his prize" % nick))
                    po10[na] = nick
                    with open('G:\supybot\Bingo\Wins\win2.json', 'w') as pot:
                        pot.write(json.dumps(po10))
                elif numes_list[0] in win_sort or \
                        numes_list[1] in win_sort or \
                        numes_list[2] in win_sort or \
                        numes_list[3] in win_sort or \
                        numes_list[4] in win_sort or \
                        numes_list[5] in win_sort or \
                        numes_list[6] in win_sort:
                    irc.queueMsg(ircmsgs.privmsg(nick, "You have 9 correct numbers, this is already been reported to admins and mods, please be patient while we check if everything was regular, you will be contacted from some of our admins about receiving your prize"))
                    irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has checked win9 and he won it, please check if everything was correct and speak with him about his prize" % nick))
                    po9[na] = nick
                    with open('G:\supybot\Bingo\Wins\win1.json', 'w') as pot:
                        pot.write(json.dumps(po9))
                #elif numes8 == win8:
                    #irc.queueMsg(ircmsgs.privmsg(nick, "You have 8 correct numbers, this is already been reported to admins and mods, please be patient while we check if everything was regular, you will be contacted from some of our admins about receiving your prize"))
                    #irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has checked win8 and he won it, please check if everything was correct and speak with him about his prize" % nick))
                    #po8[na] = nick
                    #with open('G:\supybot\Bingo\Wins\win8.json', 'w') as pot:
                        #pot.write(json.dumps(po8))
                # elif numes7 == win7:
                    # irc.queueMsg(ircmsgs.privmsg(nick, "You have 7 correct numbers, this is already been reported to admins and mods, please be patient while we check if everything was regular, you will be contacted from some of our admins about receiving your prize"))
                    # irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has checked win7 and he won it, please check if everything was correct and speak with him about his prize" % nick))
                    # po7[na] = nick
                    # with open('G:\supybot\Bingo\Wins\win7.json', 'w') as pot:
                        # pot.write(json.dumps(po7))"""
                    # """irc.queueMsg(ircmsgs.privmsg(nick, "You haven't got any of our Consolation prizes, but we will now check if you have any other Status prize"))
                    # irc.queueMsg(ircmsgs.privmsg(b_admin, "%s didn't got any of our Consolation prizes, now checking for Status prizes" % nick))
                    # if numes6 == win6:
                        # irc.queueMsg(ircmsgs.privmsg(nick, "You have 6 correct numbers, this is already been reported to admins and mods, please be patient while we check if everything was regular, you will be contacted from some of our admins about receiving your prize"))
                        # irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has checked win6 and he won it, please check if everything was correct and speak with him about his prize" % nick))
                        # po6[na] = nick
                        # with open('G:\supybot\Bingo\Wins\win6.json', 'w') as pot:
                           #  pot.write(json.dumps(po6))
                    # elif numes5 == win5:
                        # irc.queueMsg(ircmsgs.privmsg(nick, "You have 5 correct numbers, this is already been reported to admins and mods, please be patient while we check if everything was regular, you will be contacted from some of our admins about receiving your prize"))
                        # irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has checked win5 and he won it, please check if everything was correct and speak with him about his prize" % nick))
                        # po5[na] = nick
                        # with open('G:\supybot\Bingo\Wins\win5.json', 'w') as pot:
                           #  pot.write(json.dumps(po5))
                    # else:
                       #  irc.queueMsg(ircmsgs.privmsg(nick, "Sorry but this time you haven't got any of our 13 possible prizes, but that doesn't mean you can't win it next time. See you in 3 days."))
                       #  irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has checked every possible prize and he didn't won anything. Finished checking for him, you can clear his bets with !clearbet %s" % (nick, nick)))
                else:
                    irc.queueMsg(ircmsgs.privmsg(nick, "You have 0 correct numbers and you've got our Consolation price. Admins where informed about this, please be patient."))
                    irc.queueMsg(ircmsgs.privmsg(b_admin, '%s has got 0 correct numbers and he won Consolation price, please check if he already has some status on #loto channel and give him his prize.' % nick))
    scheck = wrap(scheck, ['private'])

    def clearbet(self, irc, msg, args, name):
        """<name>

        Clears bets file for given <name>"""
        nick = msg.nick
        if nick in private_list:
            try:
                with open('G:\supybot\Bingo\Players\%s.json' % name, 'w') as delete:
                    irc.reply("Bets are cleared for %s" % name)
                    quit()
            except IOError:
                irc.reply("There is no bet file for this player, maybe you have made a mistake in his nick or he didn't even had any bet file")
        else:
            irc.reply("You're not \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 administrator or moderator, this will be reported to all admins, moderators and to my owner. Fuck of")
            irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has tried to do +clearbet %s but he is not in my private list." % (nick, name)))
            irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', "%s has tried to do +clearbet %s but he is not in my private list. I've notified %s about this." % (nick, name, b_admin)))
    clearbet = wrap(clearbet, ['something', 'private'])

    def checks(self, irc, msg, args):
        """takes no arguments

        Gives list of all players who have done +scheck in this \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02"""
        nick = msg.nick
        if nick in private_list:
            with open('G:\supybot\Bingo\Schecks\schecks.json', 'r') as ch:
                b = json.loads(ch.read())
            nicks = b.values()
            irc.reply("Current players in this \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 that are done +scheck are: %s" % ', '.join(nicks))
        else:
            irc.reply("You're not \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 administrator or moderator, this will be reported to all admins, moderators and to my owner. Fuck of")
            irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has tried to do +checks but he is not in my private list." % (nick)))
            irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', "%s has tried to do +checks but he is not in my private list. I've notified %s about this." % (nick, b_admin)))
    checks = wrap(checks, ['private'])

    def plcheck(self, irc, msg, args):
        """takes no arguments

        Returns every player that placed bet for upcoming \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02"""
        nick = msg.nick
        if nick in private_list:
            with open('G:\supybot\Bingo\Bets\%s.json' % 'betnames', 'r') as betNames:
                b = json.loads(betNames.read())
            nicks = b.values()
            irc.reply("Players who placed bet for upcoming \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 are: %s" % ', '.join(nicks))
        else:
            irc.reply("You're not \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 administrator or moderator, this will be reported to all admins, moderators and to my owner. Fuck of")
            irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has tried to do +plcheck but he is not in my private list." % (nick)))
            irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', "%s has tried to do +plcheck but he is not in my private list. I've notified %s about this." % (nick, b_admin)))
    plcheck = wrap(plcheck, ['private'])

    def jackpot(self, irc, msg, args):
        """takes no arguments

        Checks current \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 for Jackpots"""
        nick = msg.nick
        if nick in private_list:
            with open('G:\supybot\Bingo\Jackpots\jackpot.json', 'r') as jack:
                b = json.loads(jack.read())
            nicks = b.values()
            irc.reply("Jackpot winners for this \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 are: %s" % (', '.join(nicks)))
        else:
            irc.reply("You're not \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 administrator or moderator, this will be reported to all admins, moderators and to my owner. Fuck of")
            irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has tried to do +jackpot but he is not in my private list." % (nick)))
            irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', "%s has tried to do +jackpot but he is not in my private list. I've notified %s about this." % (nick, b_admin)))
    jackpot = wrap(jackpot, ['private'])

    def win(self, irc, msg, args, bet):
        """<number from 6 to 1>

        Gives list of winners for selected numbers for current \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02"""
        nick = msg.nick
        if nick in private_list:
            with open('G:\supybot\Bingo\Wins\win%s.json' % bet, 'r') as win:
                b = json.loads(win.read())
            nicks = b.values()
            irc.reply("Player(s) who has %s correct numbers is/are: %s" % (bet, ', '.join(nicks)))
        else:
            irc.reply("You're not \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 administrator or moderator, this will be reported to all admins, moderators and to my owner. Fuck of")
            irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has tried to do +win %s but he is not in my private list." % (nick, bet)))
            irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', "%s has tried to do +win %s but he is not in my private list. I've notified %s about this." % (nick, bet, b_admin)))
    win = wrap(win, ['int', 'private'])

    def acheck(self, irc, msg, args):
        """takes no arguments

        General admin command that will check every type of prize and return winners for that prize"""
        nick = msg.nick
        if nick in private_list:
            with open('G:\supybot\Bingo\Jackpots\jackpot.json', 'r') as jack:
                j = json.loads(jack.read())
            jackpots = j.values()
            with open('G:\supybot\Bingo\Wins\win6.json', 'r') as win14:
                w14 = json.loads(win14.read())
            wins6 = w14.values()
            with open('G:\supybot\Bingo\Wins\win5.json', 'r') as win13:
                w13 = json.loads(win13.read())
            wins5 = w13.values()
            with open('G:\supybot\Bingo\Wins\win4.json', 'r') as win12:
                w12 = json.loads(win12.read())
            wins4 = w12.values()
            with open('G:\supybot\Bingo\Wins\win3.json', 'r') as win11:
                w11 = json.loads(win11.read())
            wins3 = w11.values()
            with open('G:\supybot\Bingo\Wins\win2.json', 'r') as win10:
                w10 = json.loads(win10.read())
            wins2 = w10.values()
            with open('G:\supybot\Bingo\Wins\win1.json', 'r') as win9:
                w9 = json.loads(win9.read())
            wins1 = w9.values()
            """with open('G:\supybot\Bingo\Wins\win8.json', 'r') as win8:
                w8 = json.loads(win8.read())
            wins8 = w8.values()
            with open('G:\supybot\Bingo\Wins\win7.json', 'r') as win7:
                w7 = json.loads(win7.read())
            wins7 = w7.values()
            with open('G:\supybot\Bingo\Wins\win6.json', 'r') as win6:
                w6 = json.loads(win6.read())
            wins6 = w6.values()
            with open('G:\supybot\Bingo\Wins\win5.json', 'r') as win5:
                w5 = json.loads(win5.read())
            wins5 = w5.values()"""
            irc.reply("Jackpot Winners for current \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 are: %s" % ', '.join(jackpots))
            irc.reply("Win6 Winners for current \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 are: %s" % ', '.join(wins6))
            irc.reply("Win5 Winners for current \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 are: %s" % ', '.join(wins5))
            irc.reply("Win4 Winners for current \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 are: %s" % ', '.join(wins4))
            irc.reply("Win3 Winners for current \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 are: %s" % ', '.join(wins3))
            irc.reply("Win2 Winners for current \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 are: %s" % ', '.join(wins2))
            irc.reply("Win1 Winners for current \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 are: %s" % ', '.join(wins1))
            """irc.reply("Win8 Winners for current \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 are: %s" % ', '.join(wins8))
            irc.reply("Win7 Winners for current \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 are: %s" % ', '.join(wins7))
            irc.reply("Win6 Winners for current \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 are: %s" % ', '.join(wins6))
            irc.reply("Win5 Winners for current \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 are: %s" % ', '.join(wins5))"""
        else:
            irc.reply("You're not \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02 administrator or moderator, this will be reported to all admins, moderators and to my owner. Fuck of")
            irc.queueMsg(ircmsgs.privmsg(b_admin, "%s has tried to do +acheck but he is not in my private list." % (nick)))
            irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', "%s has tried to do +acheck but he is not in my private list. I've notified %s about this." % (nick, b_admin)))
    acheck = wrap(acheck, ['private'])

    def bfeed(self, irc, msg, args, message):
        """<feedback>

        You have something to tell us, leave us a user feedback, you want to give us proposal on how to improve \x02\x038B\x03\x0310I\x03\x039N\x03\x037G\x03\x034O\x03!\x02, this command does that. Write your <feedback> and we will read it. p.s. You can leave only one feedback in 7 days, if you try to leave us a new feedback your old one will be deleted."""
        nick = msg.nick
        nicks = ', '.join(irc.state.channels['#loto'].users)
        na = '%s-name' % nick
        fe = '%s-feed' % nick
        t = time.time()
        date = time.strftime("%H-%M-%S--%d-%m-%Y--", time.localtime())
        if nick in nicks:
            try:
                os.makedirs("G:\supybot\Bingo\%s\%s" % ('feeds', msg.nick))
                with open('G:\supybot\Bingo\%s\%s\%s%s.txt' % ('feeds', msg.nick, date, msg.nick), 'w') as k:
                    k.write(message)
                irc.reply("Your feedback has been saved, admins will read it and think about it, thank you for your time.")
            except:
                with open('G:\supybot\Bingo\%s\%s\%s%s.txt' % ('feeds', msg.nick, date, msg.nick), 'w') as k:
                    k.write(message)
                irc.reply("Your feedback has been saved, admins will read it and think about it, thank you for your time.")
        else:
            irc.reply("You can't leave a feedback if you're not in ##loto")
    bfeed = wrap(bfeed, [rest('something'), 'private'])

    def modpl(self, irc, msg, args, name, opcija):
        """<name> --del

        Modifies private_list, if --del is used it will delete <name> from private list, else if --del isn't used it will add <name> to private_list"""
        opcije = msg.args[1]
        users = ', '.join(irc.state.channels['#loto'].users)
        if '--del' in opcije and name not in private_list:
            irc.reply("%s is not in private_list" % name)
            return
        if msg.nick not in users:
            irc.reply("You can't modify this list because you're not in channel")
            irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', "%s has tried to do +modpl and he isn't on ##loto" % msg.nick))
        if msg.nick != 'DonVitoCorleone':
            irc.reply("You can't modify this list because you're not my owner")
            irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', "%s has tried to do +modpl and he isn't my owner" % msg.nick))
        if '--del' in opcije:
            private_list.remove(name)
            with open('G:\supybot\Bingo\private.json', 'w') as pl:
                pl.write(json.dumps(private_list))
            irc.reply("%s successfuly deleted from private_list" % name)
        if '--del' not in opcije:
            private_list.append(name)
            with open('G:\supybot\Bingo\private.json', 'w') as pl:
                pl.write(json.dumps(private_list))
            irc.reply("%s successfuly added to private_list" % name)
    modpl = wrap(modpl, ['something', optional('something')])

    def showpl(self, irc, msg, args):
        """takes no arguments

        Shows content from private_list"""
        if msg.nick != 'DonVitoCorleone':
            irc.reply("You can't see this list because you're not my owner")
        if private_list == []:
            irc.reply("Private_list is empty")
        else:
            irc.reply("My current available admins and owners are: %s" % ', '.join([', '.join(['%s' % v]) for v in private_list]))
    showpl = wrap(showpl)
                


Class = BlJack


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
