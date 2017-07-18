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
import string
import supybot.ircmsgs as ircmsgs
import json
import os

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Bots')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Bots(callbacks.Plugin):
    """Add the help for "@plugin help Bots" here
    This should describe *how* to use this plugin."""
    threaded = True

    def doJoin(self, irc, msg):
        t = msg.prefix
        nick_split = string.split(t, '!')
        nick = nick_split[0]
        big_nick = nick_split[0]
        channel = msg.args[0]
        if channel == '#bots':
            irc.queueMsg(ircmsgs.notice(nick, "Hello %s, welcome to \x02#BOTS\x02, type \x0310+botlist\x03 to see our available bots, and use \x0310+botdesc BOT-NAME\x03, to see description and info about some bot from \x0310+botlist\x03 list" % nick))

    def botlist(self, irc, msg, args):
        """takes no arguments

        Sends notice to you with list of our bot"""
        global channel
        channel = msg.args[0]
        global nick
        nick = msg.nick
        if channel == '#bots':
            with open('Bots/%s.json' % 'botlist', 'r') as bots:
                b = json.loads(bots.read())
                bot_names = ', '.join(v for v in b)
                irc.queueMsg(ircmsgs.notice(nick, bot_names))
        else:
            irc.queueMsg(ircmsgs.notice(nick, "This command is available only on #bots channel"))
    botlist = wrap(botlist)

    def addbot(self, irc, msg, args, bot):
        """<bot>

        Adds <bot> to bots list."""
        if nick != 'DonVitoCorleone':
            irc.queueMsg(ircmsgs.notice(nick, "You're not allowed to add bots, if \x033%s\03 is your bot please contact my owner, DonVitoCorleone"))
        else:
            with open('Bots/%s.json' % 'botlist', 'r') as bots:
                b = json.loads(bots.read())
                if bot in b:
                    irc.reply("\x02%s\x02 is already in bot list" % bot)
                else:
                    b.append(str(bot))
                    with open('Bots/%s.json' % 'botlist', 'w') as bots:
                        bots.write(json.dumps(b))
                        irc.reply("\x02%s\x02 added to bot list" % bot)
    addbot = wrap(addbot, ['something'])

    def removebot(self, irc, msg, args, bot):
        """<bot>

        Removes <bot> from bots list."""
        if nick != 'DonVitoCorleone':
            irc.queueMsg(ircmsgs.notice(nick, "You're not allowed to remove bots, if \x033%s\03 is your bot please contact my owner, DonVitoCorleone"))
        else:
            with open('Bots/%s.json' % 'botlist', 'r') as bots:
                b = json.loads(bots.read())
                if bot in b:
                    b.remove(bot)
                    with open('Bots/%s.json' % 'botlist', 'w') as bots:
                        bots.write(json.dumps(b))
                        irc.reply("\x02%s\x02 is removed from bots list" % bot)
                else:
                    irc.reply("%s is not in bots list, it means I can't delete it, use \x0310+botlist\x03 to see bots list" % bot)
    removebot = wrap(removebot, ['something'])

    def adddesc(self, irc, msg, args, bot, chan, web, owner, desc):
        """<bot> <chan> <web> <owner> <desc>

        Adds description for <bot>"""
        if nick != 'DonVitoCorleone':
            irc.reply("You're not allowed to add description for bots")
        else:
            a = {}
            a['channel'] = chan
            a['website'] = web
            a['owner'] = owner
            a['description'] = ' '.join(desc)
            with open('Bots/%s.json' % bot, 'w') as bots:
                bots.write(json.dumps(a))
                irc.reply("Description for \x02%s\x02 has been added" % bot)
    adddesc = wrap(adddesc, ['something', 'something', optional('url'), 'something', many('something')])

    def botdesc(self, irc, msg, args, bot):
        """<bot>

        Gives description about <bot>"""
        if channel != '#bots':
            irc.queueMsg(ircmsgs.notice(nick, "This command is available only on #bots channel"))
        else:
            try:
                with open('/Bots/%s.json' % bot, 'r') as bots:
                    a = json.loads(bots.read())
                    bot_channel = a['channel']
                    bot_website = a['website']
                    bot_owner = a['owner']
                    bot_description = a['description']
                    if bot_website is None:
                        irc.queueMsg(ircmsgs.notice(nick, "\x033%s\x03's channel: \x02%s\x02, \x033%s\x03's owner: \x02%s\x02, \x033%s\x03's description: \x02%s\x02" % (bot, bot_channel, bot, bot_owner, bot, bot_description)))
                    else:
                        irc.queueMsg(ircmsgs.notice(nick, "\x033%s\x03's channel: \x02%s\x02, \x033%s\x03's website: \x02%s\x02 , \x033%s\x03's owner: \x02%s\x02, \x033%s\x03's description: \x02%s\x02" % (bot, bot_channel, bot, bot_website, bot, bot_owner, bot, bot_description)))
            except IOError:
                irc.queueMsg(ircmsgs.notice(nick, "\x033%s\x03 has no description yet, if this is your bot please ping \x034@OPerater\x03 on \x02#bots\x02 to add it" % bot))
    botdesc = wrap(botdesc, ['something'])

    def rmdesc(self, irc, msg, args, bot):
        """<bot>

        Removes bots description"""
        if nick != 'DonVitoCorleone':
            irc.reply("You're not allowed to remove \x033%s\x03 description, if this is your bot please contact my owner, DonVitoCorleone" % bot)
        else:
            os.remove('/Bots/%s.json' % bot)
            irc.reply("\x033%s\x03's description is removed" % bot)
    rmdesc = wrap(rmdesc, ['something'])


Class = Bots


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
