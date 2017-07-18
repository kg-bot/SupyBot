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
import supybot.ircmsgs as ircmsgs
import string
import json

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('War')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class War(callbacks.Plugin):
    """Add the help for "@plugin help War" here
    This should describe *how* to use this plugin."""
    threaded = True

    def set(self, irc, msg, args, channel, link, dict):
        """<name> <link>

        Sets current distributor and battle order link."""
        nick = msg.prefix
        nick = string.split(nick, '!')
        nick = nick[0]
        nick = dict or nick
        v = nick, link
        with open('%s.json' % channel, 'w') as f:
            f.write(json.dumps(v))
        to = ('Welcome to \x0310%s\x03, DISTRIBUTION: \x02\x034ON\x03\x02, DISTRIBUTOR: \x02\x034%s\x03\x02, BATTLE ORDER: \x02\x034%s\x03\x02, use command \x02+request\x02 to request your supplies.%s' % (channel, nick, link, v))
        topic = irc.queueMsg(ircmsgs.topic(channel, to))
    set = wrap(set, [("checkChannelCapability", 'op'), 'something', optional('something')])

    def off(self, irc, msg, args, channel):
        """<no arguments>

        Close distribution."""
        to = ('Welcome to \x0310%s\x03, DISTRIBUTION: \x02\x034OFF\x03\x02, DISTRIBUTOR: \x02\x034No distributor right now\x03\x02, BATTLE ORDER: \x02\x034None\x03\x02. Have a nice day untill next distribution.' % channel)
        topic = irc.queueMsg(ircmsgs.topic(channel, to))
    off = wrap(off, [("checkChannelCapability", 'op')])

    def request(self, irc, msg, args, channel, ff, link):
        """<name> <ff> <link>

        Request supplies."""
        nic = msg.prefix
        nicc = string.split(nic, '!')
        nick = nicc[0]
        with open('%s.json' % channel, 'r') as f:
            b = json.loads(f.read())
        v = b[0]
        with open('reglinks.json', 'r') as l:
            d = json.loads(l.read())
        m = '%s-link' % nick
        link = link or d[m]
        msg = ('%s has requested supplies on %s, he has %s FF, and his link is %s' % (nick, channel, ff, link))
        mssg = ('%s has requested supplies on %s, his link is %s' % (nick, channel, link))
        to = irc.state.channels[channel].topic
        #try:
        if v in to:
            if ff is None:
                irc.queueMsg(ircmsgs.privmsg(v, mssg))
            else:
                irc.queueMsg(ircmsgs.privmsg(v, msg))
        else:
            irc.reply("Don't try to cheat me, that name isn't current distributor. %s" % v)
        #except:
            #irc.reply('''Ooops! Something went wrong. You probably didn't used quotes "" for name, example of correct command: \x02+request distributr-name 150 Your-Valid-Link\x02.''')
    request = wrap(request, ['inChannel', 'int', optional('url')])

    def reglink(self, irc, msg, args, channel, name, link):
        """[<name>] <link>

        This will register your link"""
        na = '%s-name' % name
        li = '%s-link' % name
        with open('reglinks.json', 'r') as d:
            b = json.loads(d.read())
        b[na] = name
        b[li] = link
        with open('reglinks.json', 'w') as k:
            k.write(json.dumps(b))
        #with open('reglinks.json', 'a') as k:
            #k.write(json.dumps('imena': v, indent=4))
        irc.reply('You have registered successfuly. %s' % b)
    reglink = wrap(reglink, ['inChannel', 'something', 'url'])


Class = War


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
