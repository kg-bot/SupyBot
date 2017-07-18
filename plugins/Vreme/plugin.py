# -*- coding: utf8 -*-
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

import re
import json
import urllib2
from xml.dom import minidom
from xml.dom.minidom import parseString
from time import strftime
from datetime import datetime

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Vreme')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Vreme(callbacks.Plugin):
    """Add the help for "@plugin help Vreme" here
    This should describe *how* to use this plugin."""
    threaded = True

    def vreme(self, irc, msg, args, grad):
        """<city>

        Gives info about <city> weather for 3 days"""
        url = json.load(utils.web.getUrlFd('http://api.openweathermap.org/data/2.5/forecast/daily?q=%s&mode=json&units=metric&cnt=3' % (grad)))
        # Here starts first day
        t = url['list'][0]['dt']
        nam = url['city']['name']
        country = url['city']['country']
        g = datetime.fromtimestamp(int(t)).strftime('%Y-%m-%d')
        ap = url['list'][0]['pressure']
        ah = url['list'][0]['humidity']
        aoc = url['list'][0]['clouds']
        c = url['list'][0]['weather'][0]['description']
        ws = url['list'][0]['speed']
        min = url['list'][0]['temp']['min']
        max = url['list'][0]['temp']['max']
        morning = url['list'][0]['temp']['morn']
        day = url['list'][0]['temp']['day']
        evening = url['list'][0]['temp']['eve']
        night = url['list'][0]['temp']['night']
        # Here is the end of first day and below is second day
        t1 = url['list'][1]['dt']
        nam1 = url['city']['name']
        country1 = url['city']['country']
        g1 = datetime.fromtimestamp(int(t1)).strftime('%Y-%m-%d')
        ap1 = url['list'][1]['pressure']
        ah1 = url['list'][1]['humidity']
        aoc1 = url['list'][1]['clouds']
        c1 = url['list'][1]['weather'][0]['description']
        ws1 = url['list'][1]['speed']
        min1 = url['list'][1]['temp']['min']
        max1 = url['list'][1]['temp']['max']
        morning1 = url['list'][1]['temp']['morn']
        day1 = url['list'][1]['temp']['day']
        evening1 = url['list'][1]['temp']['eve']
        night1 = url['list'][1]['temp']['night']
        # Here is the end of first day and below is third day
        t2 = url['list'][2]['dt']
        nam2 = url['city']['name']
        country2 = url['city']['country']
        g2 = datetime.fromtimestamp(int(t2)).strftime('%Y-%m-%d')
        ap2 = url['list'][2]['pressure']
        ah2 = url['list'][2]['humidity']
        aoc2 = url['list'][2]['clouds']
        c2 = url['list'][2]['weather'][0]['description']
        ws2 = url['list'][2]['speed']
        min2 = url['list'][2]['temp']['min']
        max2 = url['list'][2]['temp']['max']
        morning2 = url['list'][2]['temp']['morn']
        day2 = url['list'][2]['temp']['day']
        evening2 = url['list'][2]['temp']['eve']
        night2 = url['list'][2]['temp']['night']
        # Here is the end of third day and below are some encoding stuffs
        posto = '%' # Because we can't use % in reply it's defined here
        stepen = '°C' # Encoding for supy isn't yet implemented so we must do it like this
        irc.reply("\x02Weather\x02 for \x034%s\x03, \x034%s\x03. \x02\x034Date\x03\x02: \x1F%s\x1F, \x02Air Pressure\x02: %skPa, \x02Air Humidity\x02: %s%s \x02Amount Of Clouds\x02: %s%s \x02Conditions\x02: %s, \x02Wind Speed\x02: %smps. \x02\x034Temperatures\x03\x02; \x02Min\x02: %s%s, \x02Max\x02: %s%s, \x02Morning\x02: %s%s"
            ' \x02Day\x02: %s%s, \x02Evening\x02: %s%s, \x02Night\x02: %s%s \x02\x037<===>\x03\x02 \x02\x0310Date\x03\x02: \x1F%s\x1F, \x02\x0310Air Pressure\x03\x02: %skPa, \x02\x0310Air Humidity\x03\x02: %s%s \x02\x0310Amount Of Clouds\x03\x02: %s%s \x02\x0310Conditions\x03\x02: %s, \x02\x0310Wind Speed\x03\x02: %smps. \x02\x034Temperatures\x03\x02; \x02\x0310Min\x03\x02: %s%s, \x02\x0310Max\x03\x02: %s%s, \x02\x0310Morning\x03\x02: %s%s'
            ' \x02\x0310Day\x03\x02: %s%s, \x02\x0310Evening\x03\x02: %s%s, \x02\x0310Night\x03\x02: %s%s \x02\x037<===>\x03\x02 \x02\x039Date\x03\x02: \x1F%s\x1F, \x02\x039Air Pressure\x03\x02: %skPa, \x02\x039Air Humidity\x03\x02: %s%s \x02\x039Amount Of Clouds\x03\x02: %s%s \x02\x039Conditions\x03\x02: %s, \x02\x039Wind Speed\x03\x02: %smps. \x02\x034Temperatures\x03\x02; \x02\x039Min\x03\x02: %s%s, \x02\x039Max\x03\x02: %s%s, \x02\x039Morning\x03\x02: %s%s'
            ' \x02\x039Day\x03\x02: %s%s, \x02\x039Evening\x03\x02: %s%s, \x02\x039Night\x03\x02: %s%s' % (nam, country, g, ap, ah, posto, aoc, posto, c, ws, min, stepen.decode('utf-8'), max, stepen.decode('utf-8'), morning, stepen.decode('utf-8'), day, stepen.decode('utf-8'), evening, stepen.decode('utf-8'), night, 
            stepen.decode('utf-8'), g1, ap1, ah1, posto, aoc1, posto, c1, ws1, min1, stepen.decode('utf-8'), max1, stepen.decode('utf-8'), morning1, stepen.decode('utf-8'), day1, stepen.decode('utf-8'), evening1, stepen.decode('utf-8'), night1, 
            stepen.decode('utf-8'), g2, ap2, ah2, posto, aoc2, posto, c2, ws2, min2, stepen.decode('utf-8'), max2, stepen.decode('utf-8'), morning2, stepen.decode('utf-8'), day2, stepen.decode('utf-8'), evening2, stepen.decode('utf-8'), night2, 
            stepen.decode('utf-8')))
    vreme = wrap(vreme, ['text'])


Class = Vreme


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
