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
import json
import urllib2
import urllib
import datetime
import supybot.schedule as schedule

import string

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('BDPing')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Template(string.Template):
    # Original string.Template does not accept variables starting with a
    # number.
    idpattern = r'[_a-z0-9]+'

class BDPing(callbacks.Plugin):
    """Add the help for "@plugin help BDPing" here
    This should describe *how* to use this plugin."""
    threaded = True

    def batt5(self, irc, msg, args, server, battle, round):
        """<server> <battle>

        Will keep track of battle time and it will ping everyone on channel if there is 2 minutes 'till the end"""
        base = 'http://api.cscpro.org/esim/%s/battle/%s/%s.json'
        data = json.load(utils.web.getUrlFd(base % (server, battle, round)))
        durationh = data['time']['hour']
        durationm = data['time']['minute']
        channel = msg.args[0]
        users = ' '.join(irc.state.channels[channel].users)
        msg = ("There is 5 more minutes 'till the end of battle, fight here http://%s.e-sim.org/battle.html?id=%s" % (server, battle))
    batt5 = wrap(batt5, [("checkChannelCapability", 'op'), 'something', 'something', optional('int')])
        


Class = BDPing


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
