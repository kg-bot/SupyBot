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
import json
import string

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Gimg')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Gimg(callbacks.Plugin):
    """Add the help for "@plugin help Gimg" here
    This should describe *how* to use this plugin."""
    threaded = True

    def img(self, irc, msg, args, word):
        """<keyword>

        Queries images\x0310dot\x03google\x0310dot\x03com for desired \x02<keyword>\x02 and returns first 3 results"""
        request = json.load(utils.web.getUrlFd('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=%s' % '%20'.join(word)))
        if request['responseData']['results'] == []:
            irc.reply('Noone')
        else:
            title = request['responseData']['results'][0]['titleNoFormatting']
            link = request['responseData']['results'][0]['unescapedUrl']
            site = request['responseData']['results'][0]['originalContextUrl']
            title1 = request['responseData']['results'][1]['titleNoFormatting']
            link1 = request['responseData']['results'][1]['unescapedUrl']
            site1 = request['responseData']['results'][1]['originalContextUrl']
            title2 = request['responseData']['results'][2]['titleNoFormatting']
            link2 = request['responseData']['results'][2]['unescapedUrl']
            site2 = request['responseData']['results'][2]['originalContextUrl']
            total = request['responseData']['cursor']['estimatedResultCount']
            stri1 = '1'
            stri2 = '2'
            stri3 = '3'
            irc.reply('Estimated images count is: %s. Displaying first 3 images below.' % ircutils.mircColor(total, 'red'))
            irc.reply('%s.) \x0310Title\x03: \x02%s\x02 - \x0310Image Link\x03: %s - \x0310Image Site\x03: %s' % (ircutils.mircColor(stri1, 'orange'), title, link, site))
            irc.reply('%s.) \x0310Title\x03: \x02%s\x02 - \x0310Image Link\x03: %s - \x0310Image Site\x03: %s' % (ircutils.mircColor(stri2, 'orange'), title1, link1, site1))
            irc.reply('%s.) \x0310Title\x03: \x02%s\x02 - \x0310Image Link\x03: %s - \x0310Image Site\x03: %s' % (ircutils.mircColor(stri3, 'orange'), title2, link2, site2))
    img = wrap(img, [many('something')])


Class = Gimg


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
