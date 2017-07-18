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
import mechanize
import cookielib
import urllib2
from selenium import selenium
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import supybot.schedule as schedule
import time
from lxml import etree
from xml.etree.ElementTree import ElementTree

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Tomp3')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Tomp3(callbacks.Plugin):
    """Add the help for "@plugin help Tomp3" here
    This should describe *how* to use this plugin."""
    threaded = True

    def tomp3(self, irc, msg, args, link, ime):
        """<link>

        Converts YouTube <link> to MP3 and returns mp3 download link. It can take a few minutes to convert video, depends on its size."""
        url = 'http://www.youtube-mp3.org/'
        xpaths = {'url' : "//input[@id='youtube-url']", 'convert' : "//input[@id='submit']", 'download' : "//div[@id='progress_info']"}
        binary = FirefoxBinary('F:/Program Files/Mozilla Firefox/firefox.exe')
        mydriver = webdriver.Firefox(firefox_binary=binary)
        mydriver.get(url)
        mydriver.maximize_window()
        mydriver.find_element_by_xpath(xpaths['url']).clear()
        mydriver.find_element_by_xpath(xpaths['url']).send_keys(link)
        mydriver.find_element_by_xpath(xpaths['convert']).click()
        time.sleep(20)
        k = mydriver.page_source
        with open('mp3.txt', 'wb') as f:
            f.write(k.encode('utf-8'))
        tree = etree.HTML(k)
        for e in tree.xpath("//a[2]"):
            id = e.attrib['href']
        save = urllib2.urlopen('http://www.youtube-mp3.org%s' % id).read()
        pesma = ' '.join(ime)
        with open('%s.mp3' % pesma, 'wb') as p:
            p.write(save)
        irc.reply('Done')
        #irc.reply('\x0310You can get your mp3 file here\x03: http://www.youtube-mp3.org%s' % id)
        mydriver.close()
    tomp3 = wrap(tomp3, ['url', many('something')])

    def nikovi(self, irc, msg, args, chnnel, coun):
        """asd

        ASdads"""
        channe = chnnel
        counnt = coun
        chan = irc.getCallback('Pars')
        irc.reply(chnnel)
        #irc.reply(keys)
        irc.reply(args)
        w = chan.kanali(irc, msg, args, kanal=channe, opcija=counnt)
        irc.reply(w)
    nikovi = wrap(nikovi, [optional('something'), optional('something')])


Class = Tomp3


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
