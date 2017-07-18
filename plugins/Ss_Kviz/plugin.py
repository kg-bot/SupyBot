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
import json

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Ss_Kviz')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Ss_Kviz(callbacks.Plugin):
    """Add the help for "@plugin help Ss_Kviz" here
    This should describe *how* to use this plugin."""
    threaded = True

    def promena(self, irc, msg, args, number):
        """<broj>

        Menja pitanja za SS kviz, <broj> oznacava grupu pitanja."""
        with open('Samosrbija/Ss%s.questions' % number, 'r') as pitanja:
            pita = pitanja.read()
            with open('data/Eureka.#samosrbija.questions', 'w') as upis_pitanja:
                upis_pitanja.write(pita)
                irc.reply("Pitanja su uspesno promenjena u grupu pitanja pod rednim brojem %s." % number)
    promena = wrap(promena, ['int'])

    def fmvoice(self, irc, msg, args, option):
        """Takes no arguments

        Podela igraca u dve grupe, voice/devoice."""
        voices_empty = []
        channel = msg.args[0]
        voices = irc.state.channels[channel].voices
        voices_length = len(voices)
        users = irc.state.channels[channel].users
        users_length = len(users)
        half_users_length = users_length / 2
        list_of_users = list(users)
        if '--first' in msg.args[1]:
            for i in xrange(half_users_length + 2): 
                nick = random.choice(list_of_users)
                if nick == "eRepublikBot" or nick == "DonVitoCorleone":
                    continue
                if nick not in voices:
                    irc.queueMsg(ircmsgs.voice(channel, nick))
        elif '--devoice' in msg.args[1]:
            for i in users:
                irc.queueMsg(ircmsgs.devoice(channel, i))
        else:
            for i in users:
                if i not in voices:
                    irc.queueMsg(ircmsgs.voice(channel, i))
                elif i == 'eRepublikBot' or i == "DonVitoCorleone" or i == "x-bot":
                    continue    
                else:
                    irc.queueMsg(ircmsgs.devoice(channel, i))
    fmvoice = wrap(fmvoice, [optional('something')])   


Class = Ss_Kviz


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
