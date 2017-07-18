###
# Copyright (c) 2014, KG-Bot
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
import supybot.ircmsgs as ircmsgs
import random
import supybot.schedule as schedule

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('NoSleep')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class NoSleep(callbacks.Plugin):
    """Add the help for "@plugin help NoSleep" here
    This should describe *how* to use this plugin."""
    threaded = True

    def izreke(self, irc, msg, args):
        """Takes no arguments

        Starts quotes on NoSleep"""
        nick = msg.nick
        channel = '#NoSleep'
        quotes = 'NoSleep/Quotes.json'
        if nick == "DonVitoCorleone":
            def _quotes():
                with open(quotes, 'r') as latin_quotes:
                    quotes_list = json.loads(latin_quotes.read())
                    random_quote = random.choice(quotes_list)
                    irc.reply('\x02%s\x02' % random_quote)
            schedule.addPeriodicEvent(_quotes, 600, 'quote_spam')
        else:
            irc.reply("You can't start quotes replying.")
    izreke = wrap(izreke)

    def sizreke(self, irc, msg, args):
        """Takes no arguments

        Stops quotes on NoSleep"""
        nick = msg.nick
        if nick == "DonVitoCorleone":
            try:
                schedule.removeEvent('quote_spam')
                irc.reply("Quotes stoped.")
            except:
                irc.reply("There are no quotes running right now.")
        else:
            irc.reply("You can't stop quotes.")
    sizreke = wrap(sizreke)


Class = NoSleep


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
