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
import datetime
import time
import supybot.schedule as schedule
import supybot.ircmsgs as ircmsgs
import supybot.conf as conf

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Misc1')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x
_timers = 'plugins/Misc1/Stopwatch_Timers.json'
allowed_channels = ['#CorleoneFamily']

class Misc1(callbacks.Plugin):
    """Add the help for "@plugin help Misc1" here
    This should describe *how* to use this plugin."""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Misc1, self)
        self.__parent.__init__(irc)
        self.owners = []
        self.admins = []
        self.ops = []
        self.hops = []
        self.voices = []
        self.users = []
        self.whois = 0
        self.names = 0

    def linux(self, irc, msg, args):
        """Takes no arguments

        Prints nice Linux Pingu."""
        message = u"""\x0311,11@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
\x0311,11@@@@@@@@@@@@@@@@@\x031,1@@@@@@@@@@@\x0311,11@@@@@@@@@@@@@@@@@@
\x0311,11@@@@@@@@@@@@@@@@\x031,1@@@@@@@@@@@@@@@\x0311,11@@@@@@@@@@@@@@@
\x0311,11@@@@@@@@@@@@@@\x031,1@@@@@@@@@@@@@@@@@@\x0311,11@@@@@@@@@@@@@@
\x0311,11@@@@@@@@@@@@@@\x031,1@@@@@@@@@@@@@@@@@@\x0311,11@@@@@@@@@@@@@@
\x0311,11@@@@@@@@@@@@@@\x031,1@@\x030,0@@@@\x031,1@@\x030,0@@@@@\x031,1@@@@@\x0311,11@@@@@@@@@@@@@@
\x0311,11@@@@@@@@@@@@@@\x031,1@@\x030,0@\x031,1@@\x030,0@\x031,1@@\x030,0@\x031,1@@\x030,0@@\x031,1@@@@@\x0311,11@@@@@@@@@@@@@@
\x0311,11@@@@@@@@@@@@@@\x031,1@@\x030,0@\x031,1@@\x030,0@\x031,1@@\x030,0@\x031,1@@\x030,0@\x031,1@@@@@@\x0311,11@@@@@@@@@@@@@@
\x0311,11@@@@@@@@@@@@@@\x031,1@@\x038,8@@@@@@@@@@@@\x031,1@@@@\x0311,11@@@@@@@@@@@@@@
\x0311,11@@@@@@@@@@@@@@\x031,1@@\x030,0@\x038,8@@@@@@@@@@\x030,0@\x031,1@@@@\x0311,11@@@@@@@@@@@@@@
\x0311,11@@@@@@@@@@@@@\x031,1@@@\x030,0@@\x038,8@@@@@@\x030,0@@@@\x031,1@@@@@\x0311,11@@@@@@@@@@@@@
\x0311,11@@@@@@@@@@@@\x031,1@@@@\x030,0@@@@@@@@@@@@\x031,1@@@@@@@\x0311,11@@@@@@@@@@@
\x0311,11@@@@@@@@@@\x031,1@@@@@@\x030,0@@@@@@@@@@@@@\x031,1@@@@@@@@\x0311,11@@@@@@@@@
\x0311,11@@@@@@@@@\x031,1@@@@@\x0315,15@@@\x030,0@@\x0315,15@@@@\x030,0@@\x0315,15@@@@@\x031,1@@@@@@@@@\x0311,11@@@@@@@
\x0311,11@@@@@@@@\x031,1@@@@@@\x0315,15@\x030,0@@@@@\x0315,15@@\x030,0@@@@@\x0315,15@@@@@\x031,1@@@@@@@@\x0311,11@@@@@@
\x0311,11@@@@@@@\x031,1@@@@@\x030,0@@@@@@@@\x0315,15@\x030,0@@@@@@@@@\x0315,15@\x031,1@@@@@@@@@@\x0311,11@@@@@
\x0311,11@@@@@@\x031,1@@@@@\x030,0@@@@@@@@@\x0315,15@\x030,0@@@@@@@@@@@\x031,1@@@@@@@@@\x0311,11@@@@@
\x0311,11@@@@\x031,1@@@@@@@\x030,0@@@@@@@@\x0315,15@@\x030,0@@@@@@@@@@@\x031,1@@@@@@@@@@\x0311,11@@@@
\x0311,11@@@@\x031,1@@@@@@@@\x030,0@@@@@@@\x0315,15@@\x030,0@@@@@@@@@@@\x031,1@@@@@@@@@\x0311,11@@@@@
\x0311,11@@@@\x038,8@@@@@\x031,1@@@@\x030,0@@@@@@\x0315,15@@\x030,0@@@@@@@@@@\x031,1@@@@@@@@@\x0311,11@@@@@@
\x0311,11@@@\x038,8@@@@@@@@\x031,1@@@@\x030,0@@@@\x0315,15@@\x030,0@@@@@@@@@\x038,8@@@\x031,1@@@@@@\x038,8@@@\x0311,11@@@@
\x0311,11@@\x038,8@@@@@@@@@@@\x031,1@@@\x030,0@@@\x0315,15@\x030,0@@@@@@@@@\x038,8@@@@@@@@@@@@@\x0311,11@@@@
\x0311,11@@\x038,8@@@@@@@@@@@@@\x031,1@\x030,0@@@@\x0315,15@\x030,0@@@@@@\x031,1@@@\x038,8@@@@@@@@@@@@@\x0311,11@@@
\x0311,11@\x038,8@@@@@@@@@@@@@@@@\x030,0@@@@@@@@\x031,1@@@@@\x038,8@@@@@@@@@@@@@\x0311,11@@@
\x0311,11@\x038,8@@@@@@@@@@@@@@@\x031,1@@@@@@@@@@@@@@\x038,8@@@@@@@@@@@@\x0311,11@@@@
\x0311,11@@\x038,8@@@@@@@@@@@@@@\x031,1@@@@@@@@@@@@@@\x038,8@@@@@@@@@@\x0311,11@@@@@@
\x0311,11@@@@@@@@\x038,8@@@@@@@@\x0311,11@\x031,1@@@@@@@@@@@@@\x038,8@@@@@@@@\x0311,11@@@@@@@@
\x0311,11@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""
        for line in message.split('\n'):
            irc.reply(line)
    linux = wrap(linux, ['owner'])

    def procitaj_svetca(self):
        try:
            with open('Misc1/Svetci.json', 'r') as svetci:
                kalendar = json.loads(svetci.read())
                return kalendar
        except:
            return 0

    def upisi_svetca(self, database):
        try:
            with open('Misc1/Svetci.json', 'w') as svetci:
                kalendar = svetci.write(json.dumps(database))
                return kalendar
        except:
            return 0

    def svadd(self, irc, msg, args, channel, dan, mesec, godina, svetac):
        """<dan> <mesec> <godina> <svetac>

        Dodaje Svetca na listu svetaca za <dan>/<mesec>/<godina>."""
        nick = msg.nick
        channel = msg.args[0]
        provera_svetaca = self.procitaj_svetca()
        if dan is not None:
            danasnji_datum = '%s/%s/%s' % (str(dan), str(mesec), str(godina))
            if danasnji_datum in provera_svetaca.keys():
                irc.reply("\x02%s\x02 se vec nalazi u listi Svetaca, nije moguce duplo upisivanje." % ' '.join(svetac))
            else:
                svetac_dict = {}
                svetac_dict['dodao'] = nick
                svetac_dict['svetac'] = ' '.join(svetac)
                provera_svetaca[danasnji_datum] = svetac_dict
                pisanje_svetaca = self.upisi_svetca(provera_svetaca)
                if pisanje_svetaca == 0:
                    irc.reply("Nije uspelo upisivanje, GRESKA!!!")
                else:
                    irc.reply("\x02%s\x02 uspesno upisan za datum: \x02%s\x02." % (' '.join(svetac), danasnji_datum))
        else:
            irc.reply("Morate da stavite datum za koji ce biti upisan svetac, primer za stavljanje datuma je +svadd 8 1 2014 Bozic.")
    svadd = wrap(svadd, [("checkChannelCapability", 'op'), 'int', 'int', 'int', many('something')])

    def svsee(self, irc, msg, args, dan, mesec, godina):
        """<dan> <mesec> <godina>

        Radi pretragu baze po datom datumu, ukoliko ne pronadje svetca vraca erro poruku. <dan> i <mesec> se upisuju bez 0, recimo ako je datum 24/01/2014 upisujete +svsee 24 1 2014."""
        svetci = self.procitaj_svetca()
        datum = '%s/%s/%s' % (dan, mesec, godina)
        if datum in svetci.keys():
            svetac = svetci[datum]['svetac']
            dodao = svetci[datum]['dodao']
            irc.reply("\x02%s\x02, u bazu ga dodao/la: \x02%s\x02." % (svetac, dodao))
        else:
            irc.reply("Jos uvek nije unesen svetac za \x02%s\x02." % datum)
    svsee = wrap(svsee, ['int', 'int', 'int'])

    def read_stopwatch_timers(self):
        with open(_timers, 'r') as timers:
            current_timers = json.loads(timers.read())
            return current_timers

    def write_stopwatch_timers(self, irc, msg):
        current_time = time.time()
        nick = msg.nick
        channel = msg.args[0]
        timer_name = '%s-%s' % (channel, nick)
        timers = self.read_stopwatch_timers()
        if timer_name in timers.keys():
            irc.reply("You've already scheduled timer and you can't schedule new one before you stop currentlly started or wait until it stops itself (24h).")
        else:
            timers[timer_name] = {}
            timers[timer_name]['nick'] = nick
            timers[timer_name]['channel'] = channel
            timers[timer_name]['timer'] = current_time
            with open(_timers, 'w') as timers1:
                timers1.write(json.dumps(timers))
            irc.reply("Timer successfully added.")
            schedule.addEvent(self.clear_stopwatch_timers, time.time() + 86400, timer_name, args=(irc, timer_name))

    def clear_stopwatch_timers(self, irc, timer):
        timers = self.read_stopwatch_timers()
        if timer not in timers:
            return
        else:
            now_time = time.time()
            elapsed_time = now_time - timers[timer]['timer']
            elapsed_time = '%.f' % elapsed_time
            nick = timers[timer]['nick']
            del timers[timer]
            with open(_timers, 'w') as timers1:
                timers1.write(json.dumps(timers))
            #try:
            schedule.removeEvent(timer)
            irc.reply("Timer for \x02%s\x02 successfully stopped. Time elapsed \x02%s\x02s." % (nick, elapsed_time))
            #except:
                #return

    def stopwatch(self, irc, msg, args, channel):
        """Takes no arguments

        Starts stopwatch until you stop it with \x02+sstopwatch\x02."""
        self.write_stopwatch_timers(irc, msg)
    stopwatch = wrap(stopwatch, ['channel'])

    def sstopwatch(self, irc, msg, args, channel):
        """Takes no arguments

        Stops previously started timer."""
        chan = msg.args[0]
        nick = msg.nick
        timer = '%s-%s' % (channel, nick)
        self.clear_stopwatch_timers(irc, timer)
    sstopwatch = wrap(sstopwatch, ['channel'])

    def do353(self, irc, msg):
        if self.names == 1:
            broken_nicks = msg.args[3].split(' ')
            for name in broken_nicks:
                if '&' in name:
                    splited_name = name.split('&')
                    if splited_name[1].lower() not in self.admins:
                        self.admins.append(splited_name[1].lower())
                    if splited_name[1].lower() not in self.users:
                        self.users.append(splited_name[1].lower())
                elif '~' in name:
                    splited_name = name.split('~')
                    if splited_name[1].lower() not in self.owners:
                        self.owners.append(splited_name[1].lower())
                    if splited_name[1].lower() not in self.users:
                        self.users.append(splited_name[1].lower())
                elif '@' in name:
                    splited_name = name.split('@')
                    if splited_name[1].lower() not in self.ops:
                        self.ops.append(splited_name[1].lower())
                    if splited_name[1].lower() not in self.users:
                        self.users.append(splited_name[1].lower())
                elif '%' in name:
                    splited_name = name.split('%')
                    if splited_name[1].lower() not in self.hops:
                        self.hops.append(splited_name[1].lower())
                    if splited_name[1].lower() not in self.users:
                        self.users.append(splited_name[1].lower())
                elif '+' in name:
                    splited_name = name.split('+')
                    if splited_name[1].lower() not in self.voices:
                        self.voices.append(splited_name[1].lower())
                    if splited_name[1].lower() not in self.users:
                        self.users.append(splited_name[1].lower())
                else:
                    if name.lower() not in self.users:
                        self.users.append(name.lower())
    
    def count_users(self, irc, channel, owner):
        irc.queueMsg(ircmsgs.join(channel))
        time.sleep(4)
        irc.queueMsg(ircmsgs.IrcMsg('NAMES %s' % channel))
        time.sleep(5)
        useres = self.users
        self.discount_invalid_users(irc, useres, channel, owner)

    def discount_invalid_users(self, irc, users, channel, owner):
        if owner.lower() not in self.owners and owner.lower() not in self.admins:
            irc.queueMsg(ircmsgs.privmsg(channel, "You can't request bot because you're not owner or admin on this channel."))
            self.owners = []
            self.admins = []
            self.ops = []
            self.hops = []
            self.voices = []
            self.users = []
            self.names = 0
            irc.queueMsg(ircmsgs.part(channel))
        else:
            valid_nicks = 0
            dissalowed_nicks = ['erepublik', 'internets', 'limitserv', 'quotes', 'chanstat', 'trivia', 'e-sim', 'f9', 'foobar', 'gamblebot', 'nini', 'kugelblitz', 'thinkbot', 'weedle', 'youtube', '[th]runescript', 'barkeep', 'macbot', 'merzbot', 'cccc', 'visitor', 'alisa', 'e-bot', 'erepbot', 'g-bot', 'evento', 'fishbot', 'expl0it', 'esclavo', 'merc', 'wharrgarbl', '[0sec]-bot', '[420]', '[4warez]', '[^_^]', '[ax]enforcer', '[basement]', '[chihiro]', '[crazy]', '[doki]', '[off]', '[ksn]kirino', '[leet]', '[retarded]', '[rori]', '[sgkk]', '[utw]', '[zero-raws]', 'agito', 'aishwarya', 'alegria', 'anime-keep', 'animehq', 'animezx', 'athena', 'atlantis', 'ayakok', 'ayu', 'ayuda', 'baka', 'bakabt', 'bakakozou', 'bakemonogatari', 'bettyboop', 'billgates', 'blazn', 'canuck', 'carmen', 'cccp', 'cell', 'chat', 'coalbot', 'comiket', 'complex', 'consoiezx', 'cool', 'creepybot', 'cro-warrior', 'cyber', 'd-s', 'darkbot', 'db', 'devbox', 'die', 'disorder', 'distro', 'donarudo', 'doujin-world', 'draze', 'dreamie', 'dso-nl', 'dvd', 'e-hentai', 'elite', 'elite-gamer', 'empire', 'endorphine', 'eon', 'eurovision', 'ewan', 'exploits', 'fansubber', 'fapfire', 'fusion', 'fx', 'gabbermp3', 'gamezx', 'gengstah', 'ganondorf', 'gatekeeper', 'gayserv', 'georgewashington', 'gijoe', 'ginp', 'glados', 'glock', 'godroo', 'guardianangel', 'hell', 'hfdhdef', 'hisouten', 'hoe', 'hug', 'hwbot', 'icebot', 'icecold', 'illiteratemonkey', 'imperatori', 'internet2', 'itrade', 'izdaja', 'jnet', 'juped', 'kami-sama', 'ken', 'kickassanime', 'kim_II-sung', 'kittehbot', 'kk', 'kohakuren', 'kyuu', 'l33t', 'luftwaffe', 'lunar', 'madokami', 'meltyblood', 'merc', 'mi5', 'mihajlo', 'moelicious', 'mp3passion', 'mustafakemalataturk', 'myspace', 'nanashi', 'nba', 'nds', 'nhs', 'nibl', 'nipponsei', 'oink', 'onee-chan', 'onigiri-bot', 'opertits', 'paffu', 'papaille', 'penis', 'ph34rb0t', 'pheer', 'phx', 'pixiv-tan', 'pomozx', 'protector', 'raawr', 'radio', 'recruitx', 'redmoon', 'reinforce', 'rizon', 'rizonfm', 'rsbot', 'scene-bot', 'sereti', 'sexy', 'sgtrock', 'shancerv', 'shitstorm', 'shouko-chan', 'slime_ball', 'snoopdogg', 'sobermonkey', 'somebot', 'sonchou', 'source', 'special_bot', 'sporeserv', 'starcraft', 'static-subs', 'stronk', 'supersnow800', 'sverige', 'swizzle', 'taiwan', 'teacher', 'tek9', 'the_matrix', 'thekey', 'therocksays', 'thoreenforcer', 'tickleweasel', 'tnt', 'tomgreen', 'tradersnetwork', 'trinity', 'triviax', 'tx', 'valentine', 'vibez0r', 'vincentbot', 'w000t', 'wannabe', 'war', 'warden', 'warez', 'wasted', 'wickedhelp', 'wobbuffet', 'wtfs', 'wx', 'x-bot', 'xdcc', 'xdccz', 'xmas', 'yoroshiku', 'yugioh', 'zangola', '|[daw]|', '|f-`|f', '|glorious_failure|', '}o{', owner, irc.nick]
            for user in users:
                if user.lower() not in dissalowed_nicks:
                    valid_nicks += 1
            if valid_nicks >= 15:
                try:
                    networkGroup = conf.supybot.networks.get(irc.network)
                    networkGroup.channels().add(channel)
                    modes = irc.state.channels[channel].modes
                    if 'c' not in modes and 'C' not in modes:
                        irc.queueMsg(ircmsgs.privmsg(channel, "I've been assigned to this channel on \x02%s\x02's initiative, to see some info about me use \x0310+help\x03, if you have any other questions come to \x039#KG-Bot\x03 and ask. There are \x02%s\x02 valid users here." % (owner, valid_nicks)))
                        self.owners = []
                        self.admins = []
                        self.ops = []
                        self.hops = []
                        self.voices = []
                        self.users = []
                        self.names = 0
                    else:
                        irc.queueMsg(ircmsgs.privmsg(channel, "I've been assigned to this channel on %s's initiative, to see some info about me use +help, if you have any other questions come to #KG-Bot and ask." % owner))
                        self.owners = []
                        self.admins = []
                        self.ops = []
                        self.hops = []
                        self.voices = []
                        self.users = []
                        self.names = 0
                except:
                    modes = irc.state.channels[channel].modes
                    if 'c' not in modes and 'C' not in modes:
                        irc.queueMsg(ircmsgs.privmsg(channel, "I've been assigned to this channel on \x02%s\x02's initiative, to see some info about me use \x0310+help\x03, if you have any other questions come to \x039#KG-Bot\x03 and ask. There are \x02%s\x02 valid users here." % (owner, valid_nicks)))
                        self.owners = []
                        self.admins = []
                        self.ops = []
                        self.hops = []
                        self.voices = []
                        self.users = []
                        self.names = 0
                    else:
                        irc.queueMsg(ircmsgs.privmsg(channel, "I've been assigned to this channel on %s's initiative, to see some info about me use +help, if you have any other questions come to #KG-Bot and ask." % owner))
                        self.owners = []
                        self.admins = []
                        self.ops = []
                        self.hops = []
                        self.voices = []
                        self.users = []
                        self.names = 0
            else:
                irc.queueMsg(ircmsgs.part(channel, 'This channel does not meat our requirements.'))

    def requestchan(self, irc, msg, args, chan):
        """<channel name (with #)>

        Request channel."""
        channel = msg.args[0]
        nick = msg.nick
        if channel not in allowed_channels:
            irc.reply("You can't use this command here, please go to #KG-Bot")
        else:
            if chan.startswith('#'):
                banovi = self.read_bans()
                if banovi != {}:
                    if chan.lower() not in banovi.keys():
                        if self.names == 0:
                            self.names = 1
                            self.count_users(irc, chan, nick)
                        else:
                            irc.reply("I'm already adding another channel, please wait until I finish that (30s aprox.), after that I'll process your request.")
                            time.sleep(25)
                            self.names = 1
                            self.count_users(irc, chan, nick)
                    else:
                        irc.reply("This channel is banned, you can't request for it.")
                else:
                    if self.names == 0:
                            self.names = 1
                            self.count_users(irc, chan, nick)
                    else:
                        irc.reply("I'm already adding another channel, please wait until I finish that (15s aprox.), after that I'll process your request.")
                        time.sleep(25)
                        self.names = 1
                        self.count_users(irc, chan, nick)
            else:
                irc.reply("Invalid channel name.")
    requestchan = wrap(requestchan, ['channel'])

    def read_bans(self):
        with open('Kanali/Banovani_kanali.json', 'r') as citanje_banova:
            banovi = json.loads(citanje_banova.read())
            return banovi

Class = Misc1


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
