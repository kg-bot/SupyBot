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
import requests
from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.shelve_store import ShelveJobStore
import uuid
from platform import *
import sysconfig as sc
from pyDes import *
import urllib
import supybot.plugin as plugin
import gc
import dropbox
import urllib2
import re
import os
from lxml import html
from lxml import etree
from bs4 import *
from xml.etree.ElementTree import ElementTree
from operator import itemgetter
import mechanize
import cookielib
import supybot.ircmsgs as ircmsgs
import simplejson
import httplib2
from twitter import *
import supybot
import supybot.schedule as schedule
import random
import string
import time
import sys
import json
import supybot.conf as conf
import supybot.ircdb as ircdb
import supybot.questions as qs
#from supybot.Channel import nicks
import datetime
import html2text
import adminsowners

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Pars')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x
a = 1
channels = []
p = 0

class Pars(callbacks.Plugin):
    """Add the help for "@plugin help Pars" here
    This should describe *how* to use this plugin."""
    threaded = True
    _whois = {}

    def __init__(self, irc):
        self.__parent = super(Pars, self)
        self.__parent.__init__(irc)
        self.owners = []
        self.admins = []
        self.owners = []
        self.whois = 0
        self.irc = None
        self.eventName = None
        self.eventNumber = 0

    def dt(self, irc, msg, args):
        """Nothing

        None"""
        today_date = datetime.date.today().strftime('%d/%m/%Y') # datetime.date.today().strftime('%d')
        today_hour = datetime.datetime.now().hour
        today = '%s_%s' % (today_date, today_hour)
        irc.reply(today)
    dt = wrap(dt)

    def do353(self, irc, msg):
        broken_nicks = msg.args[3].split(' ')
        for name in broken_nicks:
            if '&' in name:
                splited_name = name.split('&')
                if splited_name[1] not in self.admins:
                    self.admins.append(splited_name[1])
            elif '~' in name:
                splited_name = name.split('~')
                if splited_name[1] not in self.owners:
                    self.owners.append(splited_name[1])
    
    def par(self, irc, msg, args):
        """<takes no arguments>

        Gives pages title names"""
        import dropbox

        # Get your app key and secret from the Dropbox developer website

        # Have the user sign in and authorize this token
        irc.reply('1. Go to:')
        irc.reply('2. Click "Allow" (you might have to log in first)')
        irc.reply('3. Copy the authorization code.')
        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.open('http://www.dropbox.com/login')
        br.select_form(nr=0)
        br.form['login_email'] = 'ja1994@krstarica.com'
        br.form['login_password'] = 'nino1994'
        br.submit()
        #br.open(authorize_url)
        #br.select_form(nr=0)
        #br.submit()
        #submit = br.response().read()
        #with open('submit.html', 'w') as s:
            #s.write(str(submit))
        # This will fail if the user enters an invalid authorization code
        access_token = '4y6fCq-1vsEAAAAAAAAAAUJ5ShlHDTS_RBQ6YpDI9u8'

        client = dropbox.client.DropboxClient()
        #irc.reply('linked account: %s' % client.account_info())

        f = open('pesma.mp3')
        response = client.put_file('/KgBot/pesma.mp3', f)
        irc.reply('uploaded: %s' % response)

        #folder_metadata = client.metadata('/')
        #print 'metadata: ', folder_metadata

        #f, metadata = client.get_file_and_metadata('/magnum-opus.txt')
        #out = open('magnum-opus.txt', 'w')
        #out.write(f.read())
        #out.close()
        #print metadata
    par = wrap(par)

    #def do353(self, irc, msg):
        #"""Takes no arguments

        #Returns channel admins."""
        #nick = user.lstrip('@%+&~!')
        #if not nick:
            #return
        # & is used to denote protected users in UnrealIRCd
        # ~ is used to denote channel owner in UnrealIRCd
        # ! is used to denote protected users in UltimateIRCd
        #while user and user[0] in '@%+&~!':
            #(marker, user) = (user[0], user[1:])
            #assert user, 'Looks like my caller is passing chars, not nicks.'
            #if marker == '&':
                #admin.append(nick)
            #elif marker == '%':
                #self.halfops.add(nick)
            #elif marker == '+':
                #self.voices.add(nick)
        #self.users.add(nick)
        #admin = irc.state.channels[channel].admin
        #irc.reply(msg.user)

    def kklk(self, irc, msg, args, chan):
        """None

        Nooone"""
        if self.whois == 0:
            irc.queueMsg(ircmsgs.IrcMsg('NAMES %s' % chan))
            self.whois = 1
            time.sleep(1)
            admines = self.admins
            irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', 'Admins in \x02%s\x02 are: \x02%s\x02.' % (chan, ', '.join(admines))))
            irc.reply('Admins in \x02%s\x02 are: \x02%s\x02.' % (chan, ', '.join(admines)))
            self.admins = []
        else:
            time.sleep(1)
            irc.queueMsg(ircmsgs.IrcMsg('NAMES %s' % chan))
            time.sleep(1)
            admines = self.admins
            irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', 'Admins in \x02%s\x02 are: \x02%s\x02.' % (chan, ', '.join(admines))))
            irc.reply('Admins in \x02%s\x02 are: \x02%s\x02.' % (chan, ', '.join(admines)))
            self.admins = []
            self.whois = 0
    kklk = wrap(kklk, ['channel'])

    def modappend(self, irc, msg, args, location):
        """<location>

        Adds <location> to sys.path and starts searching for modules in that location"""
        owner = 'DonVitoCorleone'
        if msg.nick == owner:
            sys.path.append('%s' % location)
            irc.replySuccess()
    modappend = wrap(modappend, ['something'])

    #def inFilter(self, irc, msg):
        #if crone_job == 1:
            #irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', "Hello world"))
        #irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', 'Prefix: \x02%s\x02, Command: \x02%s\x02, Nick: \x02%s\x02, Args: \x02%s\x02' % (msg.prefix, msg.command, msg.nick, str(msg.args))))
        #return msg

    #def outFilter(self, irc, msg):
        #if str(msg.args[0]) != 'DonVitoCorleone':
            #irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', '\x033outFilter\x03 \x0313:::\x03 Nick: \x02%s\x02, Command: \x02%s\x02, Args: \x02%s\x02' % (msg.args[0], msg.command, str(msg.args))))
        #return msg

    def do319(self, irc, msg):
        if a == 1:
            broken_channels = msg.args[2].split(' ')
            #channels = []
            for chan in broken_channels:
                self.channels.append(chan)
            #irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', ', '.join(channels)))

    def do317(self, irc, msg):
        if a == 1:
            p = str(msg.args)

    def whomightbe(self, irc, msg, args, name):
        """<name>

        Checks WHOIS info, advanced."""
        try:
            irc.queueMsg(ircmsgs.IrcMsg('WHOIS %s' % name))
            irc.reply('WHOIS sent')
            nick = msg.nick
            time.sleep(5)
            irc.reply(', '.join(self.channels))
            self.channels = []
        except Exception, e:
            irc.reply(str(e))
    whomightbe = wrap(whomightbe, ['nick'])

    def recia(self, irc, msg, args):
        """None

        No."""
        irc.reply(self.channels)
    recia = wrap(recia)

    def _checkTime(self, irc):
        url = conf.supybot.plugins.ERep.url()
        bata = json.load(utils.web.getUrlFd('%scitizen/search/Digital_Lemon/1.json' % (url)))
        id = str(bata[0]['id'])
        irc.reply(id)
        if id == '3876733':
            irc.reply(id)
            #irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', '\x02 Link\x02: http://www.erepublik.com/en/citizen/profile/'))
        #return data #except:
            #irc.reply('Nooooo')
    def spammer(self, irc, msg, args):
        """<none

        Spamming!!!"""
        #global lines
        #lines = []
        #irc.reply('asdsad')
        #with open('C:\\KAVIRC\\11-14-2013-SasaIka.txt', 'r') as k:
        #b = k.readlines()
        #reg = re.match('(.*)(Z|z)naci(.*)', b)
        #url = conf.supybot.plugins.ERep.url()
        #bata = json.load(utils.web.getUrlFd('%scitizen/search/Digital_Lemon/1.json' % (url)))
        #id = str(bata[0]['id'])
        #irc.reply(id)
        #if id == '3876733':
            #irc.reply('\x02 Link\x02: http://www.erepublik.com/en/citizen/profile/%s' % id)
        #else:
            #return
        #for line in b:
            #lines.append(line)
        #for l in lines:
            #time.sleep(5)
            #irc.reply(l)
        #t = time.time() + 7
        #schedule.addPeriodicEvent(self._checkTime, 7, 'MyFirstEvent')
        def _checkTime():
            url = conf.supybot.plugins.ERep.url()
            bata = json.load(utils.web.getUrlFd('%scitizen/search/Crazy_Hospy/1.json' % (url)))
            id = str(bata[0]['id'])
            irc.reply(id)
            if id == '3876733':
                irc.reply(id)
            if id == '4693953':
                irc.reply('ADsddad')
        schedule.addPeriodicEvent(_checkTime, 7, 'ms')
    spammer = wrap(spammer)

    def stopspam(self, irc, msg, args, event):
        """None
    
        Stop spam"""
        #del lines[:]
        try:
            schedule.removeEvent(event)
            irc.reply('Spam stop')
        except:
            irc.reply('No spamer')
            pass
    stopspam = wrap(stopspam, ['something'])

    def cpar(self, irc, msg, args):
        """<no args>

        Nonono lololo"""
        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        br.open('http://www.weather2umbrella.com/')
        br.select_form(nr=14)
        br.form['keyword'] = 'Belgrade'
        br.submit()
        zz = br.response().read()
        with open('lm.html', 'w') as klk:
            klk.write(zz)
        #irc.reply("Done looking for Belgrade, let's code next part, we must read info about Belgrade and give it to our users, right?")
        for e in br.links(url_regex='belgrade'):
            br.follow_link(e)
        dif = br.response().read()
        soup = BeautifulSoup(zz)
        dif = str(soup.findAll('belgrade'))
        irc.reply(dif)
        #parser = etree.HTML(br.response().read())
        #inf = parser.xpath('/html/body/div[3]/div/div/div/div/div/div/div/div[2]')
        #ll = [', '.join(['%s' % e.get('href')]) for e in inf]
        irc.reply("I've got this link o-O %s" % (dif))
        #consumer_key = '3lAITOLX069DxsxOZFwxEg' as
        #consumer_secret = 'gAzhx5TgfrUjNFhwnALcPbT8Iq4QwEG773K787Jyg'
        #access_token_key = '760308402-SdbNHdNDYiDzcX8YSexPkvMFGQnKTogrYm5CKI'
        #access_token_secret = 'RGNl0Cp3lv9iBGb5Q28k3p4WKpKi9XDifdfSUEtio'
        #api = Twitter(auth=OAuth(access_token_key, access_token_secret, consumer_key, consumer_secret))
        #api.statuses.update(status='Helooooooo')
        #irc.reply('Done')
        #do = br.form.find_control('status')
        #qo = do.disabled = False
        #irc.reply(do)
        #br.form.set_all_readonly(False)
        #br['tweet[text]'] = 'Sta se radi'
        #br.submit()
        #kl = br.response().read()
        #irc.reply(kl)
    cpar = wrap(cpar)
        #irc.reply(br.title())
        #for f in br.forms(): /html/body/div/div[4]/div/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/ol/li
            #continue
        #br.select_form(nr=0)
        #br.form['name'] = 'erepublik'
        #br["locations"] = "Hollywood and Vine, Hollywood CA"
        #k = br.submit()
        #irc.reply(br.response().read())
        #for l in br.links():
        #p = k.read()
        #with open('gres.html', 'w') as f:
        #    f.write(p)
        #for k in p[0:1]:
            #irc.reply(k)
        #req = br.click_link(text="*")
        #br.open(req)
        #br.response().read()
        #irc.reply(br.geturl())
            #siteMatch = re.compile( 'www.erepublik.com' ).search( l.url )
            #if siteMatch:
                #irc.reply(l.url) #resp = br.follow_link( l )
                #break
        #content = resp.get_data()
        #irc.reply(content)

    def libs(self, irc, msg, args):
        """<name>

        Sets dict"""
        py_path = sys.path
        irc.reply("I'm looking for modules in those dirs right now")
        for k in py_path:
            time.sleep(3)
            irc.reply(k)
    libs = wrap(libs)

    def modrm(self, irc, msg, args, location):
        """<location>

        Adds <location> to sys.path and starts searching for modules in that location"""
        owner = 'DonVitoCorleone'
        if msg.nick == owner:
            sys.path.remove('%s' % location)
            irc.replySuccess()
    modrm = wrap(modrm, ['something'])

    """def inFilter(self, irc, msg):
        channel = msg.args[0]
        ms = 'You have new PM.'
        y ='yes'
        if channel == '#supy-testing':
            if 'My name is' in msg.args[1]:
                irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', 'Right'))
            else:
                return
        else:
            return"""

    def us(self, irc, msg, args, chnnel, optlist):
        """asd

        ASdads"""
        channe = chnnel or '#supy-testing'
        counnt = False
        chan = irc.getCallback('Channel')
        irc.reply(chnnel)
        irc.reply(optlist)
        #irc.reply(keys)
        irc.reply(args)
        w = chan.nicks(irc, msg, args, channel=chnnel, count='--count')
        irc.reply(w)
    us = wrap(us, [optional('something'), getopts({'count':''})])

    """def toto(self, irc, msg, args, channel, dict, link):
        "<name>

        PMs <name>"
        a = {}
        a['dict'] = dict
        a['on'] = link
        to = ('I hope this will work: %s, %s' % (a['dict'], a['on']))
        topic = irc.queueMsg(ircmsgs.topic(channel, to))
        #irc.queueMsg(ircmsgs.topic(channel, a)
        #nick = string.split(a, '!')
        #topic = irc.state.channels[channel].topic
        #if nick[0] in topic:
            #irc.reply('You are %s' % nick[1])
        #else:
        irc.reply('You are not %s' % a)
    toto = wrap(toto, ['inChannel', 'something', 'something'])

    def off(self, irc, msg, args, channel):
        "<no arguments>

       Close"
        a = {}
        a['dict'] = ' '
        a['on'] = ' '
        to = ('I hope this will work also %s %s' % (a['dict'], a['on']))
        topic = irc.queueMsg(ircmsgs.topic(channel, to))
    off = wrap(off, [("checkChannelCapability", 'op')])

    def request(self, irc, msg, args, channel, name, ff, link):
        "<name> <ff> <link>

        Request sup"
        nic = msg.prefix
        nicc = string.split(nic, '!')
        nick = nicc[0]
        dict = name
        msg = ('%s has requested supplies on %s, he has %s FF, and his link is %s' % (nick, channel, ff, link))
        to = irc.state.channels[channel].topic
        if dict in to:
            irc.queueMsg(ircmsgs.privmsg(name, msg))
        else:
            irc.reply(nick)
    request = wrap(request, ['inChannel', 'something', 'int', 'something'])"""

    def ops(self, irc, msg, args, link):
        """<no arguments>

        Gives list of channel ops"""
        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        br.open('http://www.modesr.info/kompanije')
        br.select_form(name='youtubeForm')
        br.form['url'] = link
        br.submit()
        time.sleep(120)
        info = br.response().read()
        with open('mp3.txt', 'w') as l:
            l.write(info)
    ops = wrap(ops, ['url'])

    def kanali(self, irc, msg, args, kanal, opcija):
        """[<kanal>] [--count]

        Modifikovani kanali, --count moze a i ne mora"""
        if kanal is not None:
            error = 'KeyError: %s' % kanal
        try:
            if kanal is not None:
                irc.state.channels[kanal].users
        except KeyError:
            irc.reply("I'm not on %s" % kanal)
            return
        try:
            opcije = msg.args[1]
        except IndexError:
            return
        if kanal is None and opcija is None:
            nick = msg.nick
            kanal = msg.args[0]
            mod = irc.state.channels[kanal].modes
            imena = irc.state.channels[kanal].users
            if 's' in mod and nick not in imena:
                irc.reply('Ne dam imena i ne mozes mi nista')
            else:
                irc.reply('%s' % ', '.join(imena))
        elif '--count' in opcije and '#' not in opcije:
                kanal = msg.args[0]
                imena = irc.state.channels[kanal].users
                irc.reply(len(imena))
        elif '--count' in opcije and '#' in opcije:
            nick = msg.nick
            kanal = kanal
            mod = irc.state.channels[kanal].modes
            imena = irc.state.channels[kanal].users
            if 's' in mod and nick not in imena:
                irc.reply('Ne dam imena i ne mozes mi nista')
            else:
                irc.reply('%s' % len(imena))
        elif '--count' not in opcije and '#' not in opcije:
            nick = msg.nick
            kanal = msg.args[0]
            mod = irc.state.channels[kanal].modes
            imena = irc.state.channels[kanal].users
            if 's' in mod and nick not in imena:
                irc.reply('Ne dam imena, duvaj kitu')
            else:
                irc.reply(', '.join(imena))
        elif '--count' not in opcije and '#' in opcije:
            nick = msg.nick
            kanal = kanal
            mod = irc.state.channels[kanal].modes
            imena = irc.state.channels[kanal].users
            if 's' in mod and nick not in imena:
                irc.reply('Ne dam imena, duvaj kitu')
            else:
                irc.reply(', '.join(imena))
        else:
            irc.reply('Sta hoces bre')
    kanali = wrap(kanali, [optional('something'), optional('something')])

    def opers(self, irc, msg, args):
        """none

        Ops list"""
        kanal = msg.args[0]
        mreza = 'Rizon'
        opovi = ', '.join(irc.state.channels[kanal].ops)
        irc.reply(opovi)
    opers = wrap(opers)

    def geet(self, irc, msg ,args):
        """asd

        asd"""
        lin = 'YouPorn - ORGASMS Sex tape boyfriend has huge cock girlfriend loves.3gp?nvb=20131116153618&nva=20131117153618&ir=1200&sr=6000&hash=0d045bbfffe3482a7e054'
        linq = urllib.quote(lin)
        irc.reply(linq)
        ir = etree.HTML(urllib2.urlopen('http://www.youporn.com/watch/8884451/orgasms-sex-tape-boyfriend-has-huge-cock-girlfriend-loves').read())
        mo = ir.xpath('/html/body/div[6]/ul/li[4]/a')
        irc.reply(mo)
        get_link = [', '.join(['%s' % e.get('href')]) for e in mo]
        irc.reply(get_link)
        link = urllib2.urlopen('%s' % get_link[0]).read()
        with open('pornic.3gp', 'w') as k:
            k.write(link)
    geet = wrap(geet)

    def rr(self, irc, msg, args):
        """assda

        ASdasd"""
        url = conf.supybot.plugins.ERep.url()
        li = ['35-pl', '2-pl', '24-kl']
        sorli = sorted(li, key=str, reverse=False)
        splili_0 = sorli[0].split('-')
        irc.reply(splili_0[0])
    rr = wrap(rr)

    def passgen(self, irc, msg, args, length):
        """<length>
    
        Generates password for desired <length>"""
        chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '{', '}', ':', '>', '<', '?', '|', '@', '!', '#', '$', '%', '*', '(', ')', '-', '+']  #'u', 'v'] # 'w'] # 'x', 'y', 'z'] '1', '2'] #, '3', '4', '5', '6', '7', '8', '9', '{', ':', '>'] #, '?', '}', '|', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+']
        pswrd = []
        for i in xrange(length):
            pswrd.append(random.choice(chars))
        irc.reply("Your password is %s" % ''.join(pswrd))
    passgen = wrap(passgen, ['int'])

    def rsa(self, irc, msg, args):
        """<key>

        Returns private and public key"""
        ciphertext = des('ja199459')
        irc.reply(ciphertext)
    rsa = wrap(rsa, ['private'])

    def getk(self, irc, msg, args):
        """takes no arguments

        Returns your Public and Private key"""
        try:
            with open('G:\\supybot\\RSA-keys\\%s-keys.json' % msg.nick, 'r') as pk:
                b = json.loads(pk.read())
            publ_key = b[pub_key]
            prive_key = b[priv_key]
            irc.queueMsg(ircmsgs.notice(msg.nick, "Your keys are: %s, %s" % (publ_key, prive_key)))
        except:
            irc.reply("You havent generated any Public Keys so far")
    getk = wrap(getk, ['private'])

    def getpass(self, irc, msg, args, password):
        """<password>

        This will encrypt your password with RSA encryption, store it in my database for later use, and return you password suitable for desired web site"""
        with open('G:\\supybot\\RSA-keys\\%s-keys.json' % msg.nick, 'r') as pk:
            b = json.loads(pk.read())
        (bob_pub, bob_priv) = rsa.newkeys(512)
        irc.reply(bob_pub)
        m = 5, 3
        p_key = b[priv_key]
        irc.reply(p_key)
        publ_key = str(b[pub_key])
        split_pub_key = publ_key.split('(')
        #irc.reply(split_pub_key[1])
        pub_key_to_encrypt = '(%s' % split_pub_key[1]
        pu_key = 'PublicKey%s' % pub_key_to_encrypt
        irc.reply(pu_key)
        prive_key = b[priv_key]
        #irc.reply(publ_key)
        pass1 = ('%s, %s' % (str(password), publ_key))
        pass_encrypt = rsa.encrypt(password, publ_key)
        irc.reply(pass_encrypt)
    getpass = wrap(getpass, ['something'])

    def ytub(self, irc, msg, args, name):
        """<name>

        Yt info"""
        channe = '#supy-testing'
        counnt = False
        chan = irc.getCallback('Yt')
        #irc.reply(chnnel)
        #irc.reply(optlist)
        #irc.reply(keys)
        #irc.reply(args)
        w = chan.yt(irc, msg, args, name='Ne koci')
        irc.reply(w)
    ytub = wrap(ytub, [many('anything')])

    def startyt(self, irc, msg, args):
        """Takes no argumnets

        Gives link totot"""
        channel = '#suoy'
        b = self.ytub(irc, msg, channel)
    startyt = wrap(startyt)

    def pin(self, irc, msg, args, name):
        """<name>

        PINGS <name> and return reply"""
        v = irc.queueMsg(ircmsgs.ping(name))
        irc.reply(v)
        m = conf.supybot.directories.plugins
        irc.reply(m)
        k = sys.modules[name]
        irc.reply(k)
    pin = wrap(pin, ['something'])

    def loguj(self, irc, msg, args):
        """Takes no arguments

        Loges info from e-sim until it's stopped"""
        global sched
        sched = Scheduler()
        sched.start()
        def logger():
            url = 'http://www.cscpro.org/secura/damage/136-1.json'
            data = json.load(utils.web.getUrlFd(url))
            members = data['members']
            memlen = len(members)
            for i in xrange(memlen):
                soldier = members[i]['id']
                url = 'http://cscpro.org/secura/citizen/%s.json'
                data = data = json.load(utils.web.getUrlFd(url % soldier))
                name = data['name']
                exp = data['experience']
                strength = data['strength']
                cp = data['medal'][1]['president']
                congr = data['medal'][0]['congressman']
                x = {}
                x['name'] = name
                x['experience'] = exp
                x['strength'] = strength
                x['cp'] = cp
                x['congress'] = congr
                with open('G:\supybot\eRep\prva\%s.json' % name, 'w') as erep:
                    erep.write(json.dumps(x))
            irc.reply('Finished logging MU 136')
            url = 'http://www.cscpro.org/secura/damage/128-1.json'
            data = json.load(utils.web.getUrlFd(url))
            members = data['members']
            memlen = len(members)
            for i in xrange(memlen):
                soldier = members[i]['id']
                url = 'http://cscpro.org/secura/citizen/%s.json'
                data = data = json.load(utils.web.getUrlFd(url % soldier))
                name = data['name']
                exp = data['experience']
                strength = data['strength']
                cp = data['medal'][1]['president']
                congr = data['medal'][0]['congressman']
                x = {}
                x['name'] = name
                x['experience'] = exp
                x['strength'] = strength
                x['cp'] = cp
                x['congress'] = congr
                with open('G:\supybot\eRep\druga\%s.json' % name, 'w') as erep:
                    erep.write(json.dumps(x))
            irc.reply('Finished logging MU 128')
        global job
        job = sched.add_cron_job(logger, second='10')
    loguj = wrap(loguj)

    def pisanje(self, fajl):
        a = []
        with open("%s" % fajl, "w") as krm:
            krm.write(json.dumps(a))
            resp = "Done"
            return "Pisanje"
            return resp
            
    def citanje(self, fajl):
        with open("%s" % fajl, 'r') as krm:
            b = json.loads(krm.read())
            return "Citanje, %s" % b
        
    def provera(self, irc, msg, args, fajl):
        """<fajl>
        
        I/O"""
        try:
            b = self.citanje(fajl)
            irc.reply(b)
        except:
            resp = self.pisanje(fajl)
            irc.reply(resp)
    provera = wrap(provera, ['something'])

    def hos(self, irc, msg, args):
        """takes no arguments

        Starts collecting eSim info"""
        global sched
        sched = Scheduler()
        sched.start()
        def job_function():
            irc.queueMsg(ircmsgs.privmsg('DonVitoCorleone', "Hello World"))
        global job
        job = sched.add_cron_job(job_function, second='25')
        #sched.remove_jobstore('file')
    hos = wrap(hos)

    def jobs(self, irc, msg, args):
        """takes no arguments

        Gives info about jobs"""
        advanced = sched.get_jobs()
        name = str(advanced[0]).split('(')[0]
        split = str(advanced[0]).split('(')[1].split('=')
        split0 = str(split).split('[')[2]
        split1 = str(split0).split(']')[0]
        split = str(split1).split(',')[1]
        seconds = str(split).split('"')[1]
        seconds = str(seconds).split("'")[1]
        run = str(split0).split(',')[2]
        irc.reply("Job name: %s, Job timer: %s, %s" % (name, seconds, str(run).split(')')[0]))
    jobs = wrap(jobs)

    def rmjob(self, irc, msg, args):
        """takes no arguments

        Removes jobs"""
        sched.unschedule_job(job)
    rmjob = wrap(rmjob)
    
    def prenos(self, irc, msg, args):
        """Takes no arguments
        
        Gives info about results"""
        uplata = 8081
        prethodni_fond = 5026
        f = prethodni_fond + 0.8 * uplata * 50
        tacno3 = 783
        tacno4 = 75
        tacno5 = 7
        tacno6 = 1
        tacno7 = 0
        f567 = f - tacno3 * 50 - tacno4 * 500
        prenos5 = prenos6 = 0.25 * f567
        prenos7 = 0.50 * f567
        nagrada5 = prenos5 / tacno5
        nagrada6 = prenos6 / tacno6
        try:
            nagrada7 = prenos7 / tacno7
            irc.reply("There was %s tickets, last game fond was: %s. There is %s winners with 3 correct numbers, %s winers with 4 correct numbers, %s winners with 5 correct numbers, %s winers with 6 correct numbers and %s winners with 7 numbers. Prize for 5 numbers is: %s, for 6 numbers is: %s, for 7 numbers is: %s" % (uplata, prethodni_fond, tacno3, tacno4, tacno5, tacno6, tacno7, nagrada5, nagrada6, nagrada7))
        except:
            irc.reply("There was %s tickets, last game fond was: %s. There is %s winners with 3 correct numbers, %s winers with 4 correct numbers, %s winners with 5 correct numbers, %s winers with 6 correct numbers and %s winners with 7 numbers. Prize for 5 numbers is: %s, for 6 numbers is: %s, and there was no winers with 7 correct numbers this time." % (uplata, prethodni_fond, tacno3, tacno4, tacno5, tacno6, tacno7, nagrada5, nagrada6))
    prenos = wrap(prenos)

    def dvd(self, irc, msg, args, number, stuff):
        """<number> <stuff>

        Writes down a DVD <number> and all <stuff> on it to json file, structured in list."""
        nick = msg.nick
        dvd_content = '%s' % number
        if nick == "DonVitoCorleone" or nick == "Corleone_Michael":
            with open('Dvds/Dvds.json', 'r') as dvd:
                dv = json.loads(dvd.read())
                try:
                    irc.reply("DVD with this number is already added, and its content is: \x02%s\x02" % dv[dvd_content])
                except:
                    dv[dvd_content] = stuff
                    with open('Dvds/Dvds.json', 'w') as dvd:
                        dvd.write(json.dumps(dv))
                        irc.reply("Done")
        else:
            irc.reply("You don't have permission to write any DVDs info, fuck off!!!")
    dvd = wrap(dvd, ['int', rest('something')])

    def rmdvd(self, irc, msg, args, number):
        """<dvd_number>

        Removes DVD from list."""
        nick = msg.nick
        dvd_content = '%s' % number
        if nick == "DonVitoCorleone" or nick == "Corleone_Michael":
            with open('Dvds/Dvds.json', 'r') as dvd:
                dv = json.loads(dvd.read())
                try:
                    irc.reply("There is a DVD with this number, it's content is: \x02%s\x02 and it is going to be removed now." % dv[dvd_content])
                    dv.pop(dvd_content)
                    with open('Dvds/Dvds.json', 'w') as dvd:
                        dvd.write(json.dumps(dv))
                        irc.reply("Successfully removed")
                except:
                    irc.reply("There is no DVD \x02#%s\x02" % number)
        else:
            irc.reply("You don't have permission to remove any DVDs info, fuck off!!!")
    rmdvd = wrap(rmdvd, ['int'])

    def readdvd(self, irc, msg, args, number, option):
        """[<dvd_number>]

        Returns data about this [<dvd_number>] if specified, if not it will return info about all DVDs."""
        nick = msg.nick
        dvd_content = '%s' % number
        if nick == "DonVitoCorleone" or nick == "Corleone_Michael":
            if option == "-len":
                with open('Dvds/Dvds.json', 'r') as dvd:
                    dvds = json.loads(dvd.read())
                    if len(dvds) >= 1:
                        numbers = ', '.join('%s' % k for k in dvds)
                        irc.reply("There is/are %s DVD(s) in list. And their numbers are: \x02%s\x02" % (len(dvds), numbers))
                    else:
                        irc.reply("There are no DVDs in list, yet.")
            elif number is not None:
                try:
                    with open('Dvds/Dvds.json', 'r') as dvd:
                        dv = json.loads(dvd.read())
                        irc.reply("Data for DVD \x02#%s\x02 is : \x02%s\x02." % (number, dv[dvd_content]))
                except:
                    irc.reply("There is no data for DVD \x02#%s\x02." % number)
            else:
                with open('Dvds/Dvds.json', 'r') as dvd:
                    dv = json.loads(dvd.read())
                    if len(dv) == 1:
                        key = dv.keys()
                        data = dv.values()
                        irc.reply("There is just one DVD in list, with \x02#%s\x02, and its data is: \x02%s\x02." % (', '.join(key), ', '.join(data)))
                    elif len(dv) < 1:
                        irc.reply("There are no DVDs in list, yet.")
                    else:
                        irc.reply("There are \x02%s\x02 DVDs in list and I'm going to give you data for everyone of them, starting from first to last." % len(dv))
                        for k in dv:
                            irc.reply("DVD #%s data: %s" % (k, dv[k]))
        else:
            irc.reply("You are not allowed to view DVD data, fuck off!!!")
    readdvd = wrap(readdvd, [optional('int'), optional('something')])

    def cjob(self, irc, msg, args):
        """Takes no argument

        Switches crone_job to 0"""
        global crone_job
        crone_job = 0
        irc.reply("done")
    cjob = wrap(cjob)

    def jobc(self, irc, msg, args):
        """Takes no arguments

        Sets global crone_job to 1"""
        global crone_job
        crone_job = 1
        irc.reply("Done")
    jobc = wrap(jobc)

    def erlogin(self, irc, msg, args, id):
        """ Takes no arguments

        Loges in eRepublik."""
        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        url = ('http://www.erepublik.com/en/economy/donate-items/%s' % id)
        br.set_cookiejar(cj)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0')]
        br.open(url)
        url_check = br.geturl()
        irc.reply(url_check)
        if url_check == url:
            br.find_link(text='Corleone Michael')
            req = br.click_link(text='Corleone Michael')
            br.open(req)
            irc.reply(br.geturl())
        else:
            br.open('http://erepublik.com/en')
            br.select_form(nr=0)
            br.form['citizen_email'] = 'ja1994@krstarica.com'
            br.form['citizen_password'] = 'ja1994'
            br.submit()
            br.open('http://www.erepublik.com/en/economy/donate-items/%s' % id)
            #br.find_link(text='Corleone Michael')
            #req = br.click_link(text='Corleone Michael')
            #br.open(req)
            #irc.reply(br.geturl())
            loged_in_url = br.geturl()
            irc.reply("I've just logged in, and url is: %s" % loged_in_url)
        #b = br.response().readlines()
        """for line in b:
            if '_token' in line:
                irc.reply(line)
                new_line = string.split(line, 'value="')
                first_token = string.split(new_line[1], '"')
                token_to_use = first_token[0]
                irc.reply(token_to_use)
        irc.reply("Finished")
        br.select_form(nr=1)
        br.form.set_all_readonly(False)
        br.form['amount'] = '5'
        br.form['industry_id'] = '2'
        br.form['quality'] = '7'
        br.submit()
        response = br.response().read()
        irc.reply(response)"""
    erlogin = wrap(erlogin, ['int'])

    def myua(self, irc, msg, args):
        """Takes no arguments

        Returns my UA."""
        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0')]
        br.open('http://whatsmyuseragent.com/')
        a = br.response().readlines()
        for line in a:
            if '<span id="body_lbUserAgent">' in line:
                first_strip = string.split(line, '>')
                second_strip = string.split(first_strip[2], '<')
                irc.reply("My user agent is: %s" % second_strip[0])
        irc.reply("Done checking.")
    myua = wrap(myua)

    def naked(self, irc, msg, args):
        """Takes no arguments

        Lets get fucking naked!!!!"""
        women = r"""         __                              ___   __        .ama     ,
      ,d888a                                 ,d88888888888ba.  ,88"I)   d
     a88']8i                                a88".8"8)   `"8888:88  " _a8'
   .d8P' PP                             .d8P'.8  d)      "8:88:baad8P'
  ,d8P' ,ama,   .aa,  .ama.g ,mmm       d8P' 8  .8'        88):888P'
 ,d88' d8[ "8..a8"88 ,8I"88[ I88'       d88   ]IaI"        d8[         
 a88' dP "bm8mP8'(8'.8I  8[             d88'    `"         .88          
,88I ]8'  .d'.8     88' ,8' I[          ,88P ,ama    ,ama,  d8[  .ama.g
[88' I8, .d' ]8,  ,88B ,d8 aI           (88',88"8)  d8[ "8. 88 ,8I"88[
]88  `888P'  `8888" "88P"8m"            I88 88[ 8[ dP "bm8m88[.8I  8[
]88,          _,,aaaaaa,_               I88 8"  8 ]P'  .d' 88 88' ,8' I[
`888a,.  ,aadd88888888888bma.           )88,  ,]I I8, .d' )88a8B ,d8 aI
  "888888PP"'        `8""""""8          "888PP'  `888P'  `88P"88P"8m"""
        for line in women.split('\n'):
            irc.reply(ircutils.mircColor(line, 'orange', 'white'))
    naked = wrap(naked)

    def ice(self, irc, msg, args, profile):
        """Takes no arguments

        Tries to login to IceApple and find profile link."""
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0')]
        urllib2.install_opener(opener)
        authentication_url = 'http://ice-apple.com/game/index.php/en/login'
        payload = {
            'citizen_email': 'ja1994@krstarica.com',
            'password': 'ja1994',
            }
        data = urllib.urlencode(payload)
        req = urllib2.Request(authentication_url, data)
        resp = urllib2.urlopen(req)
        search_form = 'http://ice-apple.com/game/index.php/en/search'
        payload = {
            'searchword': profile,
            'task': 'search',
            'option': 'com_search',
            }
        data = urllib.urlencode(payload)
        req = urllib2.Request(search_form, data)
        resp = urllib2.urlopen(req)
        read_response = resp.readlines()
        for line in read_response:
            if profile in line:
                split_line = line.split('/en/profile/')
                #break
                second_split = split_line[1].split('">')
                third_split = second_split[0].split('"')
                irc.reply("\x02%s\x02 profile link is: \x02http://ice-apple.com/game/index.php/en/profile/%s\x02." % (profile, third_split[0]))
                break
    ice = wrap(ice, ['something'])

    def iinfo(self, irc, msg, args, profile):
        """<profile>

        Gives basic info about <profile>."""
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0')]
        urllib2.install_opener(opener)
        authentication_url = 'http://ice-apple.com/game/index.php/en/login'
        payload = {
            'citizen_email': 'ja1994@krstarica.com',
            'password': 'ja1994',
            }
        data = urllib.urlencode(payload)
        req = urllib2.Request(authentication_url, data)
        resp = urllib2.urlopen(req)
        search_form = 'http://ice-apple.com/game/index.php/en/search'
        payload = {
            'searchword': profile,
            'task': 'search',
            'option': 'com_search',
            }
        data = urllib.urlencode(payload)
        req = urllib2.Request(search_form, data)
        resp = urllib2.urlopen(req)
        read_response = resp.readlines()
        for line in read_response:
            if profile in line:
                split_line = line.split('/en/profile/')
                #break
                second_split = split_line[1].split('">')
                third_split = second_split[0].split('"')
                link = "http://ice-apple.com/game/index.php/en/profile/%s\x02" % third_split[0]
                profil = urllib2.urlopen(link)
                read_profile = profil.readlines()
                for line in read_profile:
                    if "Location:" in line:
                        location_country_split1 = line.split('title="')
                        location_country_split = location_country_split1[1].split('"')
                        country = location_country_split[0] # this is country
                        region_split = line.split('en/country/region')
                        region_split2 = region_split[1].split('</a')
                        region_split3 = region_split2[0].split('> ')
                        region = region_split3[1] # this is region
                        citizenship_split1 = line.split('Citizenship: <a href="http://ice-apple.com/game/index.php/en/country/society/')
                        citizenship_split2 = citizenship_split1[1].split('"><')
                        citizenship_split3 = citizenship_split2[0].split('title="')
                        citizenship = citizenship_split3[1]
                        #citizenship_split = citizenship_split[1].split('"')
                        #citizenship = citizenship_split[0]
                        irc.reply("Link: \x02%s\x02, Country: \x02%s - %s\x02, Citizenship: \x02%s\x02." % (link, country, region, citizenship))
                        """if 'Joined on' in line:
                            birth1 = line.split('</span')
                            birth2 = birth1[0].split('on ')
                            birth = birth2[1]
                            irc.reply("Joined found.")
                            if 'a href="http://ice-apple.com/game/index.php/en/rankings/' in line:
                                rank1 = line.split('<strong>')
                                rank2 = rank1[1].split('</strong>')
                                rank = rank2[0]
                                irc.reply("Rank found.")
                                if 'Level' in line:
                                    level1 = line.split('style="margin-left:30px">')
                                    level2 = level1[1].split('</div>')
                                    level = level2[0]
                                    irc.reply("Level found.")
                                    if 'Energy' in line:
                                        energy1 = line.split('style="margin-left:30px">')
                                        energy2 = energy1[1].split('</div>')
                                        energy = energy2[0]
                                        irc.reply("Energy found.")
                                        if 'Strength' in line:
                                            str1 = line.split('style="margin-left:30px">')
                                            str2 = str1[1].split('</div>')
                                            strength = str2[0]
                                            irc.reply("Strength found.")
                                            if 'Military Rank' in line:
                                                rank_lvl1 = line.split('style="margin-left:30px">')
                                                rank_lvl2 = rank_lvl1[1].split('</div>')
                                                rank_lvl = rank_lvl2[0]
                                                irc.reply("MU rank lvl found.")
                                                if 'src="http://ice-apple.com/game/public/game/rank/' in line:
                                                    rank_name1 = line.split('src="http://ice-apple.com/game/public/game/rank/')
                                                    rank_name2 = rank_name1[1].split('</div>')
                                                    rank_name3 = rank_name2[0].split('.png">')
                                                    rank_name = rank_name3[1]
                                                    irc.reply("\x02%s\x02's link: \x02%s \x02, Country: \x02%s - %s\x02, Citizenship: \x02%s\x02, Birth: \x02%s\x02, Rank Points: \x02%s\x02, Level: \x02%s\x02, Energy: \x02%s\x02, Strength: \x02%s\x02, Rank Level: \x02%s\x02, Rank Name: \x02%s\x02." % (profile, link, country, region, citizenship, birth, rank, level, energy, strength, rank_lvl, rank_name))"""
    iinfo = wrap(iinfo, ['something'])
    
    def sayirc(self, irc, msg, args):
        """takes no arguments
        
        Prints irc object."""
        users = []
        for user in irc.state.channels["#BorgiaFamily"].users:
            users.append(user)
        irc.reply(', '.join(users))
    sayirc = wrap(sayirc)
    
    def printjobs(self, irc, msg, args):
        """ Nothing"""
        irc.reply(schedule.schedule.events.keys())
    printjobs = wrap(printjobs)
    
    def read_timer_number(self):
        with open("plugins/Pars/local/timerNumbers.json", "r") as timerTimes:
            number = json.loads(timerTimes.read())
            return number
        
    def write_timer_number(self):
        timers = self.read_timer_number()
        number = timers["n"] + 1
        timers["n"] = number
        with open("plugins/Pars/local/timerNumbers.json", "w") as writeTimer:
            writeTimer.write(json.dumps(timers))
    
    def _sayHello(self):
        irc = self.irc
        irc.queueMsg(ircmsgs.privmsg("DonVitoCorleone", "Function _sayHello is called"))
        eventN = self.eventNumber
        eventName = self.eventName
        if eventN <= 5:
            print "Current i before ++ is %s" % str(eventN)
            self.eventNumber = eventN + 1
            print "I after ++ is %s" % str(eventN)
            irc.queueMsg(ircmsgs.privmsg("DonVitoCorleone", "Hello World"))
        else:
            print schedule.schedule.events.keys()
            self._stopTimers(eventName)
            print "Going to remove event %s" % eventName
            
    def _delhello(self, eventName):
        schedule.removeEvent(eventName)
        
    def starthello(self, irc, msg, args):
        """Nothing"""
        channel = msg.args[0]
        eventName = "%s_sayhello" % channel
        def sayHello():
            irc.queueMsg(ircmsgs.privmsg("DonVitoCorleone", "Function _sayHello is called"))
            eventNumber = self.read_timer_number()
            eventNumber = eventNumber["n"]
            irc.queueMsg(ircmsgs.privmsg("DonVitoCorleone", "eventN is %i" % eventNumber))
            if eventNumber <= 1:
                irc.queueMsg(ircmsgs.privmsg("DonVitoCorleone", "It's diferent"))
                self.write_timer_number()
            """if eventNumber <= 5:
                irc.sendMsg(ircmsgs.privmsg("DonVitoCorleone", "Current i before is %i" % eventNumber))
                eventNumber += 1
                irc.queueMsg(ircmsgs.privmsg("DonVitoCorleone", "I after is %i" % eventNumber))
                irc.queueMsg(ircmsgs.privmsg("DonVitoCorleone", "Hello World"))
            else:
                irc.queueMsg(ircmsgs.privmsg("DonVitoCorleone", schedule.schedule.events.keys()))
                schedule.removeEvent(eventName)
                irc.queueMsg(ircmsgs.privmsg("DonVitoCorleone", "Going to remove event %s" % eventName))"""
        schedule.addPeriodicEvent(sayHello, 60, eventName, now=False)
        def stopHello():
            print "Going to stop %s" % eventName
            try:
                schedule.removeEvent(eventName)
                print "Event %s stopped" % eventName
            except Exception as e:
                print e
        schedule.addEvent(stopHello, time.time() + 100)
    starthello = wrap(starthello)
    
    def delhello(self, irc, msg, args):
        """Nothing"""
        try:
            schedule.removeEvent("#starttv_sayhello")
        except:
            pass
        try:
            schedule.removeEvent("#supy-testing_sayhello")
        except:
            pass
        try:
            schedule.removeEvent("#loto_sayhello")
        except:
            pass
    delhello = wrap(delhello)
    
Class = Pars


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
