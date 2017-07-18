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
import random
import supybot.ircmsgs as ircmsgs

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('IceDice')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class IceDice(callbacks.Plugin):
    """Add the help for "@plugin help IceDice" here
    This should describe *how* to use this plugin."""
    threaded = True

    def citanje_zetona(self, channel):
        with open('IceDice/%s/Zetoni.json' % channel, 'r') as citanje_zetona:
            procitani_zetoni = json.loads(citanje_zetona.read())
            return procitani_zetoni

    def dodavanje_zetona(self, irc, upisivac, nick, zetoni, channel):
        citanje_zetona = self.citanje_zetona(channel)
        if nick in citanje_zetona.keys():
            postojeci_zetoni = citanje_zetona[nick]['zetoni']
            novi_zetoni = postojeci_zetoni + zetoni
            citanje_zetona[nick]['zetoni'] = novi_zetoni
            with open('IceDice/%s/Zetoni.json' % channel, 'w') as pisanje_zetona:
                pisanje_zetona.write(json.dumps(citanje_zetona))
                irc.reply("Successfully added \x02%s\x02 chips to \x02%s\x02. He's chips account is now \x02%s\x02." % (zetoni, nick, novi_zetoni))
        else:
            sati = datetime.datetime.now().hour
            minuta = datetime.datetime.now().minute
            sekundi = datetime.datetime.now().second
            dan = datetime.datetime.now().day
            mesec = datetime.datetime.now().month
            godina = datetime.datetime.now().year
            vreme_dodavanja = '%s/%s/%s - %s:%s:%s' % (dan, mesec, godina, sati, minuta, sekundi)
            nick_za_upisati = {}
            nick_za_upisati['nick'] = nick
            nick_za_upisati['zetoni'] = zetoni
            nick_za_upisati['upisao'] = upisivac
            nick_za_upisati['vreme'] = vreme_dodavanja
            citanje_zetona[nick] = nick_za_upisati
            with open('IceDice/%s/Zetoni.json' % channel, 'w') as upisivanje_zetona:
                upisivanje_zetona.write(json.dumps(citanje_zetona))
                irc.reply("Successfully added \x02%s\x02 chips to \x02%s\x02. He's chips account is now \x02%s\x02." % (zetoni, nick, zetoni))

    def oduzimanje_zetona(self, irc, nick, zetoni, channel):
        citanje_zetona = self.citanje_zetona(channel)
        citanje_zetona[nick]['zetoni'] = zetoni
        with open('IceDice/%s/Zetoni.json' % channel, 'w') as pisanje_zetona:
                pisanje_zetona.write(json.dumps(citanje_zetona))

    def chips(self, irc, msg, args, nick, zetoni):
        """<nick> <schips>

        Adds <chips> to <nick> account."""
        upisivac = msg.nick
        channel = msg.args[0]
        achannels = ['#dice', '#Happy.tree.friends']
        ops = irc.state.channels[channel].ops
        if channel in achannels:
            if upisivac in ops:
                self.dodavanje_zetona(irc, upisivac, nick, zetoni, channel)
            else:
                irc.reply("You're not allowed to add chips because you're not OP here.")
        else:
            irc.reply("This command is not available on this channel.")
    chips = wrap(chips, ['something', 'int'])

    def spin(self, irc, msg, args, game, nick1, chips1, nick2, chips2, nick3, chips3, nick4, chips4, nick5, chips5):
        """<game type> <nick> <chips> [<nick>] [<chips>] [<nick>] [<chips>] [<nick>] [<chips>] [<nick>] [<chips>]

        Plays game of type <game type> for given nicks. There can be min 1 nick and max 5 nicks."""
        pokretac = msg.nick
        channel = msg.args[0]
        achannels = ['#dice', '#Happy.tree.friends']
        ops = irc.state.channels[channel].ops
        if channel in achannels:
            if pokretac in ops:
                if game == 'c':
                    if nick2 is None:
                        read_chips = self.citanje_zetona(channel)
                        if nick1 in read_chips.keys():
                            nick_account = read_chips[nick1]['zetoni']
                            if nick_account - chips1 < 0:
                                irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account." % (nick1, nick_account))
                            else:
                                take_chips = nick_account - chips1
                                self.oduzimanje_zetona(irc, nick1, take_chips, channel)
                                colors = ['red', 'black']
                                select_random_color = random.choice(colors)
                                irc.queueMsg(ircmsgs.action(channel, 'rolls \x02%s\x02 colour.' % select_random_color))
                        else:
                            irc.reply("\x02%s\x02 doesn't even have account." % nick1)
                    elif nick2 is not None and nick3 is None:
                        read_chips = self.citanje_zetona(channel)
                        if nick1 in read_chips.keys() and nick2 in read_chips.keys():
                            nick1_account = read_chips[nick1]['zetoni']
                            nick2_account = read_chips[nick2]['zetoni']
                            if nick1_account - chips1 < 0:
                                irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick1, nick1_account))
                            elif nick2_account - chips2 < 0:
                                irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick2, nick2_account))
                            else:
                                take_chips_nick1 = nick1_account - chips1
                                take_chips_nick2 = nick2_account - chips2
                                self.oduzimanje_zetona(irc, nick1, take_chips_nick1, channel)
                                self.oduzimanje_zetona(irc, nick2, take_chips_nick2, channel)
                                colors = ['red', 'black']
                                select_random_color = random.choice(colors)
                                irc.queueMsg(ircmsgs.action(channel, 'rolls \x02%s\x02 colour.' % select_random_color))
                        else:
                            irc.reply("Some of those players doesn't even have account yet.")
                    elif nick3 is not None and nick4 is None:
                        read_chips = self.citanje_zetona(channel)
                        if nick1 in read_chips.keys() and nick2 in read_chips.keys():
                            if nick3 in read_chips.keys():
                                nick1_account = read_chips[nick1]['zetoni']
                                nick2_account = read_chips[nick2]['zetoni']
                                nick3_account = read_chips[nick3]['zetoni']
                                if nick1_account - chips1 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick1, nick1_account))
                                elif nick2_account - chips2 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick2, nick2_account))
                                elif nick3_account - chips3 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick3, nick3_account))
                                else:
                                    take_chips_nick1 = nick1_account - chips1
                                    take_chips_nick2 = nick2_account - chips2
                                    take_chips_nick3 = nick3_account - chips3
                                    self.oduzimanje_zetona(irc, nick1, take_chips_nick1, channel)
                                    self.oduzimanje_zetona(irc, nick2, take_chips_nick2, channel)
                                    self.oduzimanje_zetona(irc, nick3, take_chips_nick3, channel)
                                    colors = ['red', 'black']
                                    select_random_color = random.choice(colors)
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls \x02%s\x02 colour.' % select_random_color))
                            else:
                                irc.reply("Some of those players doesn't even have account yet.")
                        else:
                            irc.reply("Some of those players doesn't even have account yet.")
                    elif nick4 is not None and nick5 is None:
                        read_chips = self.citanje_zetona(channel)
                        if nick1 in read_chips.keys() and nick2 in read_chips.keys():
                            if nick3 in read_chips.keys() and nick4 in read_chips.keys():
                                nick1_account = read_chips[nick1]['zetoni']
                                nick2_account = read_chips[nick2]['zetoni']
                                nick3_account = read_chips[nick3]['zetoni']
                                nick4_account = read_chips[nick4]['zetoni']
                                if nick1_account - chips1 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick1, nick1_account))
                                elif nick2_account - chips2 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick2, nick2_account))
                                elif nick3_account - chips3 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick3, nick3_account))
                                elif nick4_account - chips4 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick4, nick4_account))
                                else:
                                    take_chips_nick1 = nick1_account - chips1
                                    take_chips_nick2 = nick2_account - chips2
                                    take_chips_nick3 = nick3_account - chips3
                                    take_chips_nick4 = nick4_account - chips4
                                    self.oduzimanje_zetona(irc, nick1, take_chips_nick1, channel)
                                    self.oduzimanje_zetona(irc, nick2, take_chips_nick2, channel)
                                    self.oduzimanje_zetona(irc, nick3, take_chips_nick3, channel)
                                    self.oduzimanje_zetona(irc, nick4, take_chips_nick4, channel)
                                    colors = ['red', 'black']
                                    select_random_color = random.choice(colors)
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls \x02%s\x02 colour.' % select_random_color))
                            else:
                                irc.reply("Some of those players doesn't even have account yet.")
                        else:
                            irc.reply("Some of those players doesn't even have account yet.")
                    elif nick5 is not None and chips5 is not None:
                        read_chips = self.citanje_zetona(channel)
                        if nick1 in read_chips.keys() and nick2 in read_chips.keys():
                            if nick3 in read_chips.keys() and nick4 in read_chips.keys():
                                if nick5 in read_chips.keys():
                                    nick1_account = read_chips[nick1]['zetoni']
                                    nick2_account = read_chips[nick2]['zetoni']
                                    nick3_account = read_chips[nick3]['zetoni']
                                    nick4_account = read_chips[nick4]['zetoni']
                                    nick5_account = read_chips[nick5]['zetoni']
                                    if nick1_account - chips1 < 0:
                                        irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick1, nick1_account))
                                    elif nick2_account - chips2 < 0:
                                        irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick2, nick2_account))
                                    elif nick3_account - chips3 < 0:
                                        irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick3, nick3_account))
                                    elif nick4_account - chips4 < 0:
                                        irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick4, nick4_account))
                                    elif nick5_account - chips5 < 0:
                                        irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick5, nick5_account))
                                    else:
                                        take_chips_nick1 = nick1_account - chips1
                                        take_chips_nick2 = nick2_account - chips2
                                        take_chips_nick3 = nick3_account - chips3
                                        take_chips_nick4 = nick4_account - chips4
                                        take_chips_nick5 = nick5_account - chips5
                                        self.oduzimanje_zetona(irc, nick1, take_chips_nick1, channel)
                                        self.oduzimanje_zetona(irc, nick2, take_chips_nick2, channel)
                                        self.oduzimanje_zetona(irc, nick3, take_chips_nick3, channel)
                                        self.oduzimanje_zetona(irc, nick4, take_chips_nick4, channel)
                                        self.oduzimanje_zetona(irc, nick5, take_chips_nick5, channel)
                                        colors = ['red', 'black']
                                        select_random_color = random.choice(colors)
                                        irc.queueMsg(ircmsgs.action(channel, 'rolls \x02%s\x02 colour.' % select_random_color))
                                else:
                                    irc.reply("Some of those players doesn't even have account yet.")
                            else:
                                irc.reply("Some of those players doesn't even have account yet.")
                        else:
                            irc.reply("Some of those players doesn't even have account yet.")
                elif game == 'hn':
                    if nick2 is None:
                        read_chips = self.citanje_zetona(channel)
                        if nick1 in read_chips.keys():
                            nick_account = read_chips[nick1]['zetoni']
                            if nick_account - chips1 < 0:
                                irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account." % (nick1, nick_account))
                            else:
                                take_chips = nick_account - chips1
                                self.oduzimanje_zetona(irc, nick1, take_chips, channel)
                                numbers = random.sample(range(1000), 1)
                                number = numbers[0]
                                irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number, nick1)))
                        else:
                            irc.reply("\x02%s\x02 doesn't even have account." % nick1)
                    elif nick2 is not None and nick3 is None:
                        read_chips = self.citanje_zetona(channel)
                        if nick1 in read_chips.keys() and nick2 in read_chips.keys():
                            nick1_account = read_chips[nick1]['zetoni']
                            nick2_account = read_chips[nick2]['zetoni']
                            if nick1_account - chips1 < 0:
                                irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick1, nick1_account))
                            elif nick2_account - chips2 < 0:
                                irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick2, nick2_account))
                            else:
                                take_chips_nick1 = nick1_account - chips1
                                take_chips_nick2 = nick2_account - chips2
                                self.oduzimanje_zetona(irc, nick1, take_chips_nick1, channel)
                                self.oduzimanje_zetona(irc, nick2, take_chips_nick2, channel)
                                numbers = random.sample(range(1000), 2)
                                number1 = numbers[0]
                                number2 = numbers[1]
                                irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number1, nick1)))
                                irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number2, nick2)))
                        else:
                            irc.reply("Some of those players doesn't even have account yet.")
                    elif nick3 is not None and nick4 is None:
                        read_chips = self.citanje_zetona(channel)
                        if nick1 in read_chips.keys() and nick2 in read_chips.keys():
                            if nick3 in read_chips.keys():
                                nick1_account = read_chips[nick1]['zetoni']
                                nick2_account = read_chips[nick2]['zetoni']
                                nick3_account = read_chips[nick3]['zetoni']
                                if nick1_account - chips1 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick1, nick1_account))
                                elif nick2_account - chips2 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick2, nick2_account))
                                elif nick3_account - chips3 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick3, nick3_account))
                                else:
                                    take_chips_nick1 = nick1_account - chips1
                                    take_chips_nick2 = nick2_account - chips2
                                    take_chips_nick3 = nick3_account - chips3
                                    self.oduzimanje_zetona(irc, nick1, take_chips_nick1, channel)
                                    self.oduzimanje_zetona(irc, nick2, take_chips_nick2, channel)
                                    self.oduzimanje_zetona(irc, nick3, take_chips_nick3, channel)
                                    numbers = random.sample(range(1000), 3)
                                    number1 = numbers[0]
                                    number2 = numbers[1]
                                    number3 = numbers[2]
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number1, nick1)))
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number2, nick2)))
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number3, nick3)))
                            else:
                                irc.reply("Some of those players doesn't even have account yet.")
                        else:
                            irc.reply("Some of those players doesn't even have account yet.")
                    elif nick4 is not None and nick5 is None:
                        read_chips = self.citanje_zetona(channel)
                        if nick1 in read_chips.keys() and nick2 in read_chips.keys():
                            if nick3 in read_chips.keys() and nick4 in read_chips.keys():
                                nick1_account = read_chips[nick1]['zetoni']
                                nick2_account = read_chips[nick2]['zetoni']
                                nick3_account = read_chips[nick3]['zetoni']
                                nick4_account = read_chips[nick4]['zetoni']
                                if nick1_account - chips1 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick1, nick1_account))
                                elif nick2_account - chips2 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick2, nick2_account))
                                elif nick3_account - chips3 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick3, nick3_account))
                                elif nick4_account - chips4 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick4, nick4_account))
                                else:
                                    take_chips_nick1 = nick1_account - chips1
                                    take_chips_nick2 = nick2_account - chips2
                                    take_chips_nick3 = nick3_account - chips3
                                    take_chips_nick4 = nick4_account - chips4
                                    self.oduzimanje_zetona(irc, nick1, take_chips_nick1, channel)
                                    self.oduzimanje_zetona(irc, nick2, take_chips_nick2, channel)
                                    self.oduzimanje_zetona(irc, nick3, take_chips_nick3, channel)
                                    self.oduzimanje_zetona(irc, nick4, take_chips_nick4, channel)
                                    numbers = random.sample(range(1000), 4)
                                    number1 = numbers[0]
                                    number2 = numbers[1]
                                    number3 = numbers[2]
                                    number4 = numbers[3]
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number1, nick1)))
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number2, nick2)))
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number3, nick3)))
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number4, nick4)))
                            else:
                                irc.reply("Some of those players doesn't even have account yet.")
                        else:
                            irc.reply("Some of those players doesn't even have account yet.")
                    elif nick5 is not None and chips5 is not None:
                        read_chips = self.citanje_zetona(channel)
                        if nick1 in read_chips.keys() and nick2 in read_chips.keys():
                            if nick3 in read_chips.keys() and nick4 in read_chips.keys():
                                if nick5 in read_chips.keys():
                                    nick1_account = read_chips[nick1]['zetoni']
                                    nick2_account = read_chips[nick2]['zetoni']
                                    nick3_account = read_chips[nick3]['zetoni']
                                    nick4_account = read_chips[nick4]['zetoni']
                                    nick5_account = read_chips[nick5]['zetoni']
                                    if nick1_account - chips1 < 0:
                                        irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick1, nick1_account))
                                    elif nick2_account - chips2 < 0:
                                        irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick2, nick2_account))
                                    elif nick3_account - chips3 < 0:
                                        irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick3, nick3_account))
                                    elif nick4_account - chips4 < 0:
                                        irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick4, nick4_account))
                                    elif nick5_account - chips5 < 0:
                                        irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick5, nick5_account))
                                    else:
                                        take_chips_nick1 = nick1_account - chips1
                                        take_chips_nick2 = nick2_account - chips2
                                        take_chips_nick3 = nick3_account - chips3
                                        take_chips_nick4 = nick4_account - chips4
                                        take_chips_nick5 = nick5_account - chips5
                                        self.oduzimanje_zetona(irc, nick1, take_chips_nick1, channel)
                                        self.oduzimanje_zetona(irc, nick2, take_chips_nick2, channel)
                                        self.oduzimanje_zetona(irc, nick3, take_chips_nick3, channel)
                                        self.oduzimanje_zetona(irc, nick4, take_chips_nick4, channel)
                                        self.oduzimanje_zetona(irc, nick5, take_chips_nick5, channel)
                                        numbers = random.sample(range(1000), 5)
                                        number1 = numbers[0]
                                        number2 = numbers[1]
                                        number3 = numbers[2]
                                        number4 = numbers[3]
                                        number5 = numbers[4]
                                        irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number1, nick1)))
                                        irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number2, nick2)))
                                        irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number3, nick3)))
                                        irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number4, nick4)))
                                        irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number5, nick5)))
                                else:
                                    irc.reply("Some of those players doesn't even have account yet.")
                            else:
                                irc.reply("Some of those players doesn't even have account yet.")
                        else:
                            irc.reply("Some of those players doesn't even have account yet.")
                elif game == 'sn':
                    if nick2 is None:
                        read_chips = self.citanje_zetona(channel)
                        if nick1 in read_chips.keys():
                            nick_account = read_chips[nick1]['zetoni']
                            if nick_account - chips1 < 0:
                                irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account." % (nick1, nick_account))
                            else:
                                take_chips = nick_account - chips1
                                self.oduzimanje_zetona(irc, nick1, take_chips, channel)
                                numbers = random.sample(range(36), 1)
                                number = numbers[0]
                                irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number, nick1)))
                        else:
                            irc.reply("\x02%s\x02 doesn't even have account." % nick1)
                    elif nick2 is not None and nick3 is None:
                        read_chips = self.citanje_zetona(channel)
                        if nick1 in read_chips.keys() and nick2 in read_chips.keys():
                            nick1_account = read_chips[nick1]['zetoni']
                            nick2_account = read_chips[nick2]['zetoni']
                            if nick1_account - chips1 < 0:
                                irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick1, nick1_account))
                            elif nick2_account - chips2 < 0:
                                irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick2, nick2_account))
                            else:
                                take_chips_nick1 = nick1_account - chips1
                                take_chips_nick2 = nick2_account - chips2
                                self.oduzimanje_zetona(irc, nick1, take_chips_nick1, channel)
                                self.oduzimanje_zetona(irc, nick2, take_chips_nick2, channel)
                                numbers = random.sample(range(36), 2)
                                number1 = numbers[0]
                                number2 = numbers[1]
                                irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number1, nick1)))
                                irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number2, nick2)))
                        else:
                            irc.reply("Some of those players doesn't even have account yet.")
                    elif nick3 is not None and nick4 is None:
                        read_chips = self.citanje_zetona(channel)
                        if nick1 in read_chips.keys() and nick2 in read_chips.keys():
                            if nick3 in read_chips.keys():
                                nick1_account = read_chips[nick1]['zetoni']
                                nick2_account = read_chips[nick2]['zetoni']
                                nick3_account = read_chips[nick3]['zetoni']
                                if nick1_account - chips1 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick1, nick1_account))
                                elif nick2_account - chips2 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick2, nick2_account))
                                elif nick3_account - chips3 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick3, nick3_account))
                                else:
                                    take_chips_nick1 = nick1_account - chips1
                                    take_chips_nick2 = nick2_account - chips2
                                    take_chips_nick3 = nick3_account - chips3
                                    self.oduzimanje_zetona(irc, nick1, take_chips_nick1, channel)
                                    self.oduzimanje_zetona(irc, nick2, take_chips_nick2, channel)
                                    self.oduzimanje_zetona(irc, nick3, take_chips_nick3, channel)
                                    numbers = random.sample(range(36), 3)
                                    number1 = numbers[0]
                                    number2 = numbers[1]
                                    number3 = numbers[2]
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number1, nick1)))
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number2, nick2)))
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number3, nick3)))
                            else:
                                irc.reply("Some of those players doesn't even have account yet.")
                        else:
                            irc.reply("Some of those players doesn't even have account yet.")
                    elif nick4 is not None and nick5 is None:
                        read_chips = self.citanje_zetona(channel)
                        if nick1 in read_chips.keys() and nick2 in read_chips.keys():
                            if nick3 in read_chips.keys() and nick4 in read_chips.keys():
                                nick1_account = read_chips[nick1]['zetoni']
                                nick2_account = read_chips[nick2]['zetoni']
                                nick3_account = read_chips[nick3]['zetoni']
                                nick4_account = read_chips[nick4]['zetoni']
                                if nick1_account - chips1 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick1, nick1_account))
                                elif nick2_account - chips2 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick2, nick2_account))
                                elif nick3_account - chips3 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick3, nick3_account))
                                elif nick4_account - chips4 < 0:
                                    irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick4, nick4_account))
                                else:
                                    take_chips_nick1 = nick1_account - chips1
                                    take_chips_nick2 = nick2_account - chips2
                                    take_chips_nick3 = nick3_account - chips3
                                    take_chips_nick4 = nick4_account - chips4
                                    self.oduzimanje_zetona(irc, nick1, take_chips_nick1, channel)
                                    self.oduzimanje_zetona(irc, nick2, take_chips_nick2, channel)
                                    self.oduzimanje_zetona(irc, nick3, take_chips_nick3, channel)
                                    self.oduzimanje_zetona(irc, nick4, take_chips_nick4, channel)
                                    numbers = random.sample(range(36), 4)
                                    number1 = numbers[0]
                                    number2 = numbers[1]
                                    number3 = numbers[2]
                                    number4 = numbers[3]
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number1, nick1)))
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number2, nick2)))
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number3, nick3)))
                                    irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number4, nick4)))
                            else:
                                irc.reply("Some of those players doesn't even have account yet.")
                        else:
                            irc.reply("Some of those players doesn't even have account yet.")
                    elif nick5 is not None and chips5 is not None:
                        read_chips = self.citanje_zetona(channel)
                        if nick1 in read_chips.keys() and nick2 in read_chips.keys():
                            if nick3 in read_chips.keys() and nick4 in read_chips.keys():
                                if nick5 in read_chips.keys():
                                    nick1_account = read_chips[nick1]['zetoni']
                                    nick2_account = read_chips[nick2]['zetoni']
                                    nick3_account = read_chips[nick3]['zetoni']
                                    nick4_account = read_chips[nick4]['zetoni']
                                    nick5_account = read_chips[nick5]['zetoni']
                                    if nick1_account - chips1 < 0:
                                        irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick1, nick1_account))
                                    elif nick2_account - chips2 < 0:
                                        irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick2, nick2_account))
                                    elif nick3_account - chips3 < 0:
                                        irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick3, nick3_account))
                                    elif nick4_account - chips4 < 0:
                                        irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick4, nick4_account))
                                    elif nick5_account - chips5 < 0:
                                        irc.reply("\x02%s\x02 doesn't have enough chips for this bet. He has \x02%s\x02 chips in his account. Please start roulette again without this player or after he pays some credit." % (nick5, nick5_account))
                                    else:
                                        take_chips_nick1 = nick1_account - chips1
                                        take_chips_nick2 = nick2_account - chips2
                                        take_chips_nick3 = nick3_account - chips3
                                        take_chips_nick4 = nick4_account - chips4
                                        take_chips_nick5 = nick5_account - chips5
                                        self.oduzimanje_zetona(irc, nick1, take_chips_nick1, channel)
                                        self.oduzimanje_zetona(irc, nick2, take_chips_nick2, channel)
                                        self.oduzimanje_zetona(irc, nick3, take_chips_nick3, channel)
                                        self.oduzimanje_zetona(irc, nick4, take_chips_nick4, channel)
                                        self.oduzimanje_zetona(irc, nick5, take_chips_nick5, channel)
                                        numbers = random.sample(range(36), 5)
                                        number1 = numbers[0]
                                        number2 = numbers[1]
                                        number3 = numbers[2]
                                        number4 = numbers[3]
                                        number5 = numbers[4]
                                        irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number1, nick1)))
                                        irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number2, nick2)))
                                        irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number3, nick3)))
                                        irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number4, nick4)))
                                        irc.queueMsg(ircmsgs.action(channel, 'rolls number \x02%s\x02 for \x02%s\x02.' % (number5, nick5)))
                                else:
                                    irc.reply("Some of those players doesn't even have account yet.")
                            else:
                                irc.reply("Some of those players doesn't even have account yet.")
                        else:
                            irc.reply("Some of those players doesn't even have account yet.")
                else:
                    irc.reply("We don't have this game type yet, possible game types are: \x02color (c), high number (hn), small number (sn)\x02.")
            else:
                irc.reply("You can't start roulette because you're not OP.")
        else:
            irc.reply("This command is not available on this channel.")
    spin = wrap(spin, ['something', 'something', 'int', optional('something'), optional('int'), optional('something'), optional('int'), optional('something'), optional('int'), optional('something'), optional('int')])

    def seechips(self, irc, msg, args, name):
        """[<name>]

        Returns info about chips accounts. If you specify [<nick>] it will return info just for that player."""
        nick = msg.nick
        channel = msg.args[0]
        ops = irc.state.channels[channel].ops
        achannels = ['#dice', '#Happy.tree.friends']
        if channel in achannels:
            if nick in ops:
                zetoni = self.citanje_zetona(channel)
                if name is None:
                    if len(zetoni.keys()) >= 1:
                        for player in zetoni.keys():
                            player_chips = zetoni[player]['zetoni']
                            player_time = zetoni[player]['vreme']
                            player_added_by = zetoni[player]['upisao']
                            irc.reply("\x02%s\x02 is added on \x02%s\x02 by \x02%s\x02 and he has \x02%s\x02 chips." % (player, player_time, player_added_by, player_chips))
                    else:
                        irc.reply("There are no accounts in my database yet.")
                else:
                    if zetoni[name]:
                        player_chips = zetoni[name]['zetoni']
                        player_time = zetoni[name]['vreme']
                        player_added_by = zetoni[name]['upisao']
                        irc.reply("\x02%s\x02 is added on \x02%s\x02 by \x02%s\x02 and he has \x02%s\x02 chips." % (name, player_time, player_added_by, player_chips))
                    else:
                        irc.reply("\x02%s\x02 is not in my database yet." % name)
            else:
                irc.reply("You can use this command because you're not OP.")
        else:
            irc.reply("This command is not avaialbe on this channel.")
    seechips = wrap(seechips, [optional('something')])
                        

Class = IceDice


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
