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

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

import urllib

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Paste')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Paste(callbacks.Plugin):
    """Add the help for "@plugin help Paste" here
    This should describe *how* to use this plugin."""
    threaded = True

    def paste(self, irc, msg, args, channel, text, name, time, syntax):
        """<text> <name> [<time>] [<syntax>]

        Create new paste on pastebin.com, this is for public pastes only, you must contact my owner for private pastes. <text> is text you want to paste, put the text in quotes "", <name> will be name of that paste, [<time>] is expiration time, if it's not specified it will expire in 10m, you can view available times here: http://pastebin.com/RFqqCqt9, [<syntax>] is optional and you can view list of available syntaxes here: http://pastebin.com/api#5"""
        time = time or '10M'
        syntax = syntax or 'text'
        api = self.registryValue('api', channel)
        cred = {'api_dev_key':api,'api_option':'paste','api_paste_code':text, 'api_paste_name':name, 'api_paste_expire_date':time, 'api_paste_format':syntax}
        req = urllib.urlopen('http://pastebin.com/api/api_post.php', urllib.urlencode(cred))
        url = req.read()
        irc.reply('You can find your new paste here %s' % url)
    paste = wrap(paste, [("checkChannelCapability", 'op'), 'something', 'something', optional('something'), optional('text')])

    def ppaste(self, irc, msg, args, channel, text, name, time, syntax, private):
        """<text> <name> [<time>] [<syntax>] [<private>]

        Create new private paste on pastebin.com, this is for private pastes only, for public pastes use paste command. <text> is text you want to paste, put the text in quotes "", <name> will be name of that paste, [<time>] is expiration time, if it's not specified it will expire in 10m, you can view available times here: http://pastebin.com/RFqqCqt9 [<syntax>] is optional and you can view list of available syntaxes here: http://pastebin.com/api#5 [<private>] is optional, default is private, you can set different with giving option number, numbers are: 0 - Public paste, 1 - Unlisted paste"""
        private = private or '2'
        time = time or 'N'
        syntax = syntax or 'text'
        api = self.registryValue('api', channel)
        api_user_name = self.registryValue('apiun', channel)
        api_user_pass = self.registryValue('apiup', channel)
        loginc = {'api_dev_key':api, 'api_user_name':api_user_name, 'api_user_password':api_user_pass}
        login = urllib.urlopen('http://pastebin.com/api/api_login.php', urllib.urlencode(loginc))
        logink = login.read()
        cred = {'api_dev_key':api, 'api_option':'paste', 'api_paste_code':text, 'api_paste_name':name, 'api_paste_expire_date':time, 'api_paste_format':syntax, 'api_user_key':logink, 'api_paste_private':private}
        req = urllib.urlopen('http://pastebin.com/api/api_post.php', urllib.urlencode(cred))
        url = req.read()
        irc.reply('You can find your paste here %s' % url)
    ppaste = wrap(ppaste, [("checkChannelCapability", 'op'), 'something', 'something', optional('something'), optional('something'), optional('something')])


Class = Paste


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
