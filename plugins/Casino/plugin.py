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
import random
import json
import supybot.ircmsgs as ircmsgs
import datetime
import supybot.schedule as schedule
import time


import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Casino')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Casino(callbacks.Plugin):
    """Add the help for "@plugin help Casino" here
    This should describe *how* to use this plugin."""
    threaded = True

    def citanje_zetona(self, channel):
        with open('IceDice/Rulet/%s/Zetoni.json' % channel, 'r') as citanje_zetona:
            procitani_zetoni = json.loads(citanje_zetona.read())
            return procitani_zetoni

    def dodavanje_zetona(self, irc, nick, zetoni, channel):
        citanje_zetona = self.citanje_zetona(channel)
        if nick in citanje_zetona.keys():
            postojeci_zetoni = citanje_zetona[nick]['zetoni']
            novi_zetoni = postojeci_zetoni + zetoni
            citanje_zetona[nick]['zetoni'] = novi_zetoni
            with open('IceDice/Rulet/%s/Zetoni.json' % channel, 'w') as pisanje_zetona:
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
            nick_za_upisati['vreme'] = vreme_dodavanja
            citanje_zetona[nick] = nick_za_upisati
            with open('IceDice/Rulet/%s/Zetoni.json' % channel, 'w') as upisivanje_zetona:
                upisivanje_zetona.write(json.dumps(citanje_zetona))
                irc.reply("Successfully added \x02%s\x02 chips to \x02%s\x02. He's chips account is now \x02%s\x02." % (zetoni, nick, zetoni))

    def oduzimanje_zetona(self, irc, nick, zetoni, channel):
        citanje_zetona = self.citanje_zetona(channel)
        trenutno_stanje = citanje_zetona[nick]['zetoni']
        update_account = int(trenutno_stanje) - int(zetoni)
        citanje_zetona[nick]['zetoni'] = update_account
        with open('IceDice/Rulet/%s/Zetoni.json' % channel, 'w') as pisanje_zetona:
            pisanje_zetona.write(json.dumps(citanje_zetona))
            irc.reply("Removed \x02%s\x02 chips from \x02%s\x02's account. He's chips account is now \x02%s\x02." % (zetoni, nick, update_account))

    def dodavanje_beta(self, irc, nick, bet, stake, channel):
        player = {}
        player['bet'] = bet
        player['stake'] = stake
        with open('IceDice/Rulet/%s/Bets.json' % channel, 'r') as citanje_betsa:
            bets = json.loads(citanje_betsa.read())
            bets[nick] = player
            with open('IceDice/Rulet/%s/Bets.json' % channel, 'w') as pisanje_betsa:
                pisanje_betsa.write(json.dumps(bets))
                irc.reply("\x02%s\x02 you have successfully placed bet for upcoming drawing." % nick)

    def citanje_beta(self, channel):
        with open('IceDice/Rulet/%s/Bets.json' % channel, 'r') as citanje_betsa:
            bets = json.loads(citanje_betsa.read())
            return bets

    def play_game(self, irc, channel):
        numbers = random.sample(range(1, 36), 1)
        number = numbers[0]
        black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        green_number_zero = [0]
        irc.queueMsg(ircmsgs.mode(channel, '+m'))
        if number in green_number_zero:
            color_number = '\x030,3 0\x03'
            response = "rolls %s, and nobody wins, stakes are returned and I'm going to spin again." % color_number
            irc.queueMsg(ircmsgs.action(channel, response))
            self.play_game(irc, channel)
        elif number in black_numbers:
            color = 'black'
            color_number = '\x030,1 %s\x03' % number
            response = "rolls %s." % color_number
            irc.queueMsg(ircmsgs.action(channel, response))
            self.check_winers(irc, color, number, channel)
        else:
            color = 'red'
            color_number = '\x030,4 %s\x03' % number
            response = "rolls %s." % color_number
            irc.queueMsg(ircmsgs.action(channel, response))
            self.check_winers(irc, color, number, channel)

    def log_schedule(self, sched, channel):
        with open('IceDice/Rulet/%s/Scheduler.json' % channel, 'r') as citaj_scheduler:
            scheduler_running = json.loads(citaj_scheduler.read())
            if sched in scheduler_running.keys():
                return 'Scheduler is running'
            else:
                scheduler_writing = {}
                scheduler_writing[sched] = 'Running'
                with open('IceDice/Rulet/%s/Scheduler.json' % channel, 'w') as pisi_scheduler:
                    pisi_scheduler.write(json.dumps(scheduler_writing))
                    return "Scheduler is not running."

    def max_boje_i_trecine(self, nick, bet, channel):
        with open('IceDice/Rulet/%s/Max_bets.json' % channel, 'r')as max_bets:
            bets = json.loads(max_bets.read())
            if nick.lower() in bets.keys():
                if bet == 'color':
                    if 'betova-boje' in bets[nick].keys():
                        current_bets_color = bets[nick]['betova-boje']
                        new_bets_color = current_bets_color + 1
                        bets[nick]['betova-boje'] = new_bets_color
                        with open('IceDice/Rulet/%s/Max_bets.json' % channel, 'w')as max_bets:
                            max_bets.write(json.dumps(bets))
                        return current_bets_color
                    else:
                        bets[nick]['betova-boje'] = 1
                        with open('IceDice/Rulet/%s/Max_bets.json' % channel, 'w') as max_bets:
                            max_bets.write(json.dumps(bets))
                        return 1
                elif bet == 'trecina':
                    if 'betova-trecine' in bets[nick].keys():
                        current_bets_trecine = bets[nick]['betova-trecine']
                        new_bets_trecine = current_bets_trecine + 1
                        bets[nick]['betova-trecine'] = new_bets_trecine
                        with open('IceDice/Rulet/%s/Max_bets.json' % channel, 'w')as max_bets:
                            max_bets.write(json.dumps(bets))
                        return current_bets_trecine
                    else:
                        bets[nick]['betova-trecine'] = 1
                        with open('IceDice/Rulet/%s/Max_bets.json' % channel, 'w') as max_bets:
                            max_bets.write(json.dumps(bets))
                        return 1
            else:
                if bet == 'color':
                    new_nick = {}
                    new_nick['betova-boje'] = 1
                    bets[nick] = new_nick
                    with open('IceDice/Rulet/%s/Max_bets.json' % channel, 'w') as max_bets:
                        max_bets.write(json.dumps(bets))
                    return 1
                else:
                    new_nick = {}
                    new_nick['betova-trecine'] = 1
                    bets[nick] = new_nick
                    with open('IceDice/Rulet/%s/Max_bets.json' % channel, 'w') as max_bets:
                        max_bets.write(json.dumps(bets))
                    return 1

    def schedule_bet_clear(self, channel):
        with open('IceDice/Rulet/%s/Schedule_max_bets_clear.json' % channel, 'r') as read_bets_time:
            bets_time = json.loads(read_bets_time.read())
            if 'bet-scheduled' in bets_time.keys():
                return
            else:
                schedule.addEvent(self.next_bets_max_clear(channel), time.time() + 86400, args=(channel))
                bets_time['bet-scheduled'] = 1
                with open('IceDice/Rulet/%s/Schedule_max_bets_clear.json' % channel, 'w') as write_bets_time:
                    write_bets_time.write(json.dumps(bets_time))

    def next_bets_max_clear(self, channel):
        new_bet_time = {}
        with open('IceDice/Rulet/%s/Schedule_max_bets_clear.json' % channel, 'w') as clear_bet_time:
            clear_bet_time.write(json.dumps(new_bet_time))

    def check_winers(self, irc, color, number, channel):
        read_bets = self.citanje_beta(channel)
        possible_bets = ['red', 'black']
        schedule.addEvent(self.close_sched, time.time() + 40, args=(irc, channel))
        irc.reply("Going to calculate your bets and clear databases for next bet, this will take 40 seconds to complete. Until then channel will be muted.")
        for player in read_bets.keys():
            player_bet = read_bets[player]['bet']
            player_stake = read_bets[player]['stake']
            if player_bet == 'red':
                if color == 'red':
                    prize = int(player_stake) * 2
                    self.dodavanje_zetona(irc, player, prize, channel)
                else:
                    self.oduzimanje_zetona(irc, player, player_stake, channel)
            elif player_bet == 'black':
                if color == 'black':
                    prize = int(player_stake) * 2
                    self.dodavanje_zetona(irc, player, prize, channel)
                else:
                    self.oduzimanje_zetona(irc, player, player_stake, channel)
            elif player_bet == '1/3':
                if number >= 1 and number <= 12:
                    prize = int(player_stake) * 3
                    self.dodavanje_zetona(irc, player, prize, channel)
                else:
                    self.oduzimanje_zetona(irc, player, player_stake, channel)
            elif player_bet == '2/3':
                if number >= 13 and number <= 24:
                    prize = int(player_stake) * 3
                    self.dodavanje_zetona(irc, player, prize, channel)
                else:
                    self.oduzimanje_zetona(irc, player, player_stake, channel)
            elif player_bet == '3/3':
                if number >= 25 and number <= 36:
                    prize = int(player_stake) * 3
                    self.dodavanje_zetona(irc, player, prize, channel)
                else:
                    self.oduzimanje_zetona(irc, player, player_stake, channel)
            elif int(player_bet) == number:
                prize = int(player_stake) * 36
                self.dodavanje_zetona(irc, player, prize, channel)
            else:
                self.oduzimanje_zetona(irc, player, player_stake, channel)

    def close_sched(self, irc, channel):
        empty_dict = {}
        with open('IceDice/Rulet/%s/Scheduler.json' % channel, 'w') as write_scheduler:
            write_scheduler.write(json.dumps(empty_dict))
        with open('IceDice/Rulet/%s/Bets.json' % channel, 'w') as clear_bets:
            clear_bets.write(json.dumps(empty_dict))
        irc.queueMsg(ircmsgs.mode(channel, '-m'))
        users = irc.state.channels[channel].users
        irc.reply(', '.join(users))
        irc.reply("Everything is ready for next game.")

    def clear_nick_max_colors(self, nick, channel):
        with open('IceDice/Rulet/%s/Max_bets.json' % channel, 'r') as max_bets:
            max_bets = json.loads(max_bets.read())
        del max_bets[nick]['betova-boje']
        with open('IceDice/Rulet/%s/Max_bets.json' % channel, 'w') as write_max_bets:
            write_max_bets.write(json.dumps(max_bets))

    def clear_nick_max_thirds(self, nick, channel):
        with open('IceDice/Rulet/%s/Max_bets.json' % channel, 'r') as max_bets:
            max_bets = json.loads(max_bets.read())
        del max_bets[nick]['betova-trecine']
        with open('IceDice/Rulet/%s/Max_bets.json' % channel, 'w') as write_max_bets:
            write_max_bets.write(json.dumps(max_bets))

    def addchips(self, irc, msg, args, nick, zetoni):
        """<nick> <schips>

        Adds <chips> to <nick> account."""
        upisivac = msg.nick
        channel = msg.args[0]
        achannels = ['#IceDice']
        ops = irc.state.channels[channel].ops
        if channel in achannels:
            if upisivac in ops:
                self.dodavanje_zetona(irc, nick.lower(), zetoni, channel)
            else:
                irc.reply("You're not allowed to add chips because you're not OP here.")
        else:
            irc.reply("This command is not available on this channel.")
    addchips = wrap(addchips, ['something', 'int'])

    def addbet(self, irc, msg, args, bet, stake):
        """<type of bet> <stake>

        Adds bet for upcoming spin."""
        nick = msg.nick.lower()
        channel = msg.args[0]
        zetoni = self.citanje_zetona(channel)
        allowed_channels = ['#IceDice']
        possible_bets = ['red', 'black', '1/3', '2/3', '3/3']
        if channel not in allowed_channels:
            irc.reply("This command is not available on this channel.")
        else:
            bank = self.view_bank(irc, channel)
            if bank == "Failed":
                irc.queueMsg(ircmsgs.privmsg(channel, "You can't bet because there is no bank yet."))
            else:
                if bet.isdigit():
                    if stake <= 150:
                        if stake >= 70:
                            if int(bet) > 0 and int(bet) <= 36:
                                if nick in zetoni.keys():
                                    broj_zetona = zetoni[nick]['zetoni']
                                    dozvoljeni_zetoni = broj_zetona - stake
                                    if dozvoljeni_zetoni < 0:
                                        irc.reply("You don't have enough chips for this stake.")
                                    else:
                                        self.dodavanje_beta(irc, nick, bet, stake, channel)
                                        sched = '%s-next-spin' % channel
                                        check_sched = self.log_schedule(sched, channel)
                                        if check_sched != "Scheduler is running":
                                            schedule.addEvent(self.play_game, time.time() + 30, sched, args=(irc, channel))
                                            irc.reply("Your bet has been added and I'll do spin in 30 seconds.")
                                        else:
                                            return
                                else:
                                    irc.reply("You don't even have account, please buy chips and then try again.")
                            else:
                                irc.reply("Your bet number must be bigger than 0 and equal or lower than 36.")
                        else:
                            irc.reply("You can't place stake lower than 70 for this type of game.")
                    else:
                        irc.reply("You can't place bet bigger then 150 for this type of bet.")
                elif bet in possible_bets:
                    if stake <= 50:
                        if stake >= 20:
                            if nick in zetoni.keys():
                                broj_zetona = zetoni[nick]['zetoni']
                                dozvoljeni_zetoni = broj_zetona - stake
                                if dozvoljeni_zetoni < 0:
                                    irc.reply("You don't have enough chips for this stake.")
                                else:
                                    self.schedule_bet_clear(channel)
                                    if bet == 'red':
                                        provera_broja_betova = self.max_boje_i_trecine(nick, 'color', channel)
                                        if provera_broja_betova < 5:
                                            self.dodavanje_beta(irc, nick, bet, stake, channel)
                                            sched = '%s-next-spin' % channel
                                            check_sched = self.log_schedule(sched, channel)
                                            if check_sched != "Scheduler is running":
                                                schedule.addEvent(self.play_game, time.time() + 30, sched, args=(irc, channel))
                                                irc.reply("Your bet has been added and I'll do spin in 30 seconds.")
                                            else:
                                                irc.reply("Your bet has been added and I'm already scheduled to spin. Please wait.")
                                                return
                                        else:
                                            irc.reply("You can play this type of bet 5 times in 24h max and you've already used those today. Please come back tomorrow or play another type of bet.")
                                            try:
                                                schedule.addEvent(self.clear_nick_max_colors, time.time() + 86400, '%s_%s_clear_color' % (nick, channel), args=(nick, channel))
                                            except:
                                                return
                                    elif bet == 'black':
                                        provera_broja_betova = self.max_boje_i_trecine(nick, 'color', channel)
                                        if provera_broja_betova < 5:
                                            self.dodavanje_beta(irc, nick, bet, stake, channel)
                                            sched = '%s-next-spin' % channel
                                            check_sched = self.log_schedule(sched, channel)
                                            if check_sched != "Scheduler is running":
                                                schedule.addEvent(self.play_game, time.time() + 30, sched, args=(irc, channel))
                                                irc.reply("Your bet has been added and I'll do spin in 30 seconds.")
                                            else:
                                                irc.reply("Your bet has been added and I'm already scheduled to spin. Please wait.")
                                                return
                                        else:
                                            irc.reply("You can play this type of bet 5 times in 24h max and you've already used those today. Please come back tomorrow or play another type of bet.")
                                            try:
                                                schedule.addEvent(self.clear_nick_max_colors, time.time() + 86400, '%s_%s_clear_color' % (nick, channel), args=(nick, channel))
                                            except:
                                                return
                                    elif bet == '1/3':
                                        provera_broja_betova = self.max_boje_i_trecine(nick, 'trecina', channel)
                                        if provera_broja_betova < 7:
                                            self.dodavanje_beta(irc, nick, bet, stake, channel)
                                            sched = '%s-next-spin' % channel
                                            check_sched = self.log_schedule(sched, channel)
                                            if check_sched != "Scheduler is running":
                                                schedule.addEvent(self.play_game, time.time() + 30, sched, args=(irc, channel))
                                                irc.reply("Your bet has been added and I'll do spin in 30 seconds.")
                                            else:
                                                irc.reply("Your bet has been added and I'm already scheduled to spin. Please wait.")
                                                return
                                        else:
                                            irc.reply("You can play this type of bet 7 times in 24h max and you've already used those today. Please come back tomorrow or play another type of bet.")
                                            try:
                                                schedule.addEvent(self.clear_nick_max_thirds, time.time() + 86400, '%s_%s_clear_color' % (nick, channel), args=(nick, channel))
                                            except:
                                                return
                                    elif bet == '2/3':
                                        provera_broja_betova = self.max_boje_i_trecine(nick, 'trecina', channel)
                                        if provera_broja_betova < 7:
                                            self.dodavanje_beta(irc, nick, bet, stake, channel)
                                            sched = '%s-next-spin' % channel
                                            check_sched = self.log_schedule(sched, channel)
                                            if check_sched != "Scheduler is running":
                                                schedule.addEvent(self.play_game, time.time() + 30, sched, args=(irc, channel))
                                                irc.reply("Your bet has been added and I'll do spin in 30 seconds.")
                                            else:
                                                irc.reply("Your bet has been added and I'm already scheduled to spin. Please wait.")
                                                return
                                        else:
                                            irc.reply("You can play this type of bet 7 times in 24h max and you've already used those today. Please come back tomorrow or play another type of bet.")
                                            try:
                                                schedule.addEvent(self.clear_nick_max_thirds, time.time() + 86400, '%s_%s_clear_color' % (nick, channel), args=(nick, channel))
                                            except:
                                                return
                                    else:
                                        provera_broja_betova = self.max_boje_i_trecine(nick, 'trecina', channel)
                                        if provera_broja_betova < 7:
                                            self.dodavanje_beta(irc, nick, bet, stake, channel)
                                            sched = '%s-next-spin' % channel
                                            check_sched = self.log_schedule(sched, channel)
                                            if check_sched != "Scheduler is running":
                                                schedule.addEvent(self.play_game, time.time() + 30, sched, args=(irc, channel))
                                                irc.reply("Your bet has been added and I'll do spin in 30 seconds.")
                                            else:
                                                irc.reply("Your bet has been added and I'm already scheduled to spin. Please wait.")
                                                return
                                        else:
                                            irc.reply("You can play this type of bet 7 times in 24h max and you've already used those today. Please come back tomorrow or play another type of bet.")
                                            try:
                                                schedule.addEvent(self.clear_nick_max_thirds, time.time() + 86400, '%s_%s_clear_color' % (nick, channel), args=(nick, channel))
                                            except:
                                                return
                            else:
                                irc.reply("You don't even have account, please buy chips and then try again.")
                        else:
                            irc.reply("You can't play stake lower than 20 for this game.")
                    else:
                        irc.reply("Biggest possible stake for this type of game is 50.")
                else:
                    irc.reply("This bet is not yet implemented. You can't use it.")
    addbet = wrap(addbet, ['something', 'int'])

    def remove_bank(self, irc, name, channel):
        with open('IceDice/Rulet/%s/Bank.json' % channel, 'r') as bank:
            current_bank = json.loads(bank.read())
            if name in current_bank.keys():
                bank_for_backup = current_bank[name]['nick']
                del current_bank[name]
                with open('IceDice/Rulet/%s/Bank.json' % channel, 'w') as add_bank:
                    add_bank.write(json.dumps(current_bank))
                    self.make_chips_backup(channel, bank_for_backup)
                    with open('IceDice/Rulet/%s/Zetoni.json' % channel, 'w') as clear_because_no_bank:
                        clear_because_no_bank.write(json.dumps(current_bank))
                        irc.reply("\x02%s\x02 removed from banks database." % name)
                        users = irc.state.channels[channel].users
                        irc.reply(', '.join(users))
                        irc.reply("No bets until new bank is added. You can ask \x02DonVitoCorleone or ZijaRiko\x02 to give you bank, but first read the House Rules.")
                        irc.queueMsg(ircmsgs.privmsg('ChanServ', 'access %s del %s' % (channel, name)))
                        try:
                            irc.queueMsg(ircmsgs.deop(channel, name))
                            schedule.removeEvent('%s-removing-bank' % channel)
                            return "Deleted"
                        except:
                            schedule.removeEvent('%s-removing-bank' % channel)
                            return "Deleted"

    def make_chips_backup(self, channel, bank):
        with open('IceDice/Rulet/%s/Zetoni.json' % channel, 'r') as zetoni_backup:
            old_chips = json.loads(zetoni_backup.read())
            with open('IceDice/Rulet/%s/Zetoni_backup_%s.json' % (channel, bank), 'w') as zapisi_backup:
                zapisi_backup.write(json.dumps(old_chips))

    def add_bank(self, irc, name, vreme, channel, nick):
        try:
            sati = datetime.datetime.now().hour
            minuta = datetime.datetime.now().minute
            sekundi = datetime.datetime.now().second
            dan = datetime.datetime.now().day
            mesec = datetime.datetime.now().month
            godina = datetime.datetime.now().year
            vreme_dodavanja = '%s/%s/%s - %s:%s:%s' % (dan, mesec, godina, sati, minuta, sekundi)
            nova_banka = {}
            nova_banka['nick'] = name
            nova_banka['dodao'] = nick
            nova_banka['vreme'] = vreme_dodavanja
            nova_banka['istice za'] = vreme
            spremna_banka = {} 
            spremna_banka[name] = nova_banka
            with open('IceDice/Rulet/%s/Bank.json' % channel, 'w') as add_bank:
                add_bank.write(json.dumps(spremna_banka))
                days_in_hours = int(vreme) * 24
                hours_in_seconds = int(days_in_hours) * 3600
                schedule.addEvent(self.remove_bank, time.time() + hours_in_seconds, '%s-removing-bank' % channel, args=(irc, name, channel))
                irc.reply("\x02%s\x02 added as bank for \x02%s\x02 days." % (name, vreme))
                irc.queueMsg(ircmsgs.privmsg('ChanServ', 'access %s add %s 5' % (channel, name)))
                irc.queueMsg(ircmsgs.privmsg('ChanServ', 'sync %s' % channel))
        except:
            return "Failed"

    def view_bank(self, irc, channel):
        try:
            with open('IceDice/Rulet/%s/Bank.json' % channel, 'r') as see_bank:
                banks = json.loads(see_bank.read())
                if banks == {}:
                    irc.reply("There is no bank yet.")
                else:
                    for player in banks:
                        nick = banks[player]['nick']
                        dodao = banks[player]['dodao']
                        vreme = banks[player]['vreme']
                        istice = banks[player]['istice za']
                        irc.reply("Current bank is \x02%s\x02, it is added on \x02%s\x02 by \x02%s\x02 and he will be bank for \x02%s\x02 days." % (nick, vreme, dodao, istice))
        except:
            return "Failed"

    def addbank(self, irc, msg, args, name, length, remove):
        """<nick> <# of days>

        Adds bank for roulette for <# of days> days."""
        nick = msg.nick
        channel = msg.args[0]
        allowed_nicks = ['ZijaRiko', 'DonVitoCorleone']
        ops = irc.state.channels[channel].ops
        allowed_channels = ['#IceDice']
        if channel in allowed_channels:
            if nick in allowed_nicks:
                if remove is not None:
                    if remove == '-r':
                        remove_bank = self.remove_bank(irc, name, channel)
                        if remove_bank == 'Deleted':
                            return
                        else:
                            irc.queueMsg(ircmsgs.notice(nick, "\x02%s\x02 is not in banks database, couldn't remove it." % name))
                    else:
                        irc.queueMsg(ircmsgs.notice(nick, "there is no \x02%s\x02 option available, just option \x02%s\x02 is available for now." % remove))
                else:
                    adding_bank = self.add_bank(irc, name, length, channel, nick)
                    if adding_bank == "Failed":
                        irc.queueMsg(ircmsgs.notice(nick, "Adding \x02%s\x02 as bank has failed with unknown reason." % name))
                    else:
                        return
            else:
                irc.reply("You're not allowed to add bank.")
        else:
            irc.reply("Command is not allowed here.")
    addbank = wrap(addbank, ['something', 'int', optional('something')])

    def viewbank(self, irc, msg, args):
        """Takes no arguments

        Outputs current Roulette bank."""
        nick = msg.nick
        channel = msg.args[0]
        ops = irc.state.channels[channel].ops
        allowed_channels = ['#IceDice']
        if channel in allowed_channels:
            if nick in ops:
                bank = self.view_bank(irc, channel)
                if bank == "Failed":
                    irc.queueMsg(ircmsgs.notice(nick, "There is no bank in database yet."))
                else:
                    return
            else:
                irc.reply("You can't view bank because you're not OP.")
        else:
            irc.reply("Command is not allowed here.")
    viewbank = wrap(viewbank)

    def viewchips(self, irc, msg, args, name):
        """[<nick>]

        Gives info about <nick> chips."""
        big_nick = msg.nick
        nick = msg.nick.lower()
        channel = msg.args[0]
        zetoni = self.citanje_zetona(channel)
        ops = irc.state.channels[channel].ops
        allowed_channels = ['#IceDice']
        if channel in allowed_channels:
            if zetoni == {}:
                irc.reply("Chips database is empty.")
            else:
                if name is not None:
                    if big_nick in ops:
                        if name.lower() in zetoni.keys():
                            zetona = zetoni[name.lower()]['zetoni']
                            irc.reply("\x02%s\x02 has \x02%s\x02 chips in account." % (name, zetona))
                        else:
                            irc.reply("\x02%s\x02 doesn't have account." % name)
                    else:
                        irc.reply("You can't view another player account if you're not OP.")
                else:
                    if big_nick in ops:
                        for player in zetoni:
                            zetona = zetoni[player]['zetoni']
                            irc.queueMsg(ircmsgs.notice(big_nick, "\x02%s\x02 has \x02%s\x02 chips." % (player, zetona)))
                    else:
                        if nick in zetoni.keys():
                            zetona = zetoni[nick]['zetoni']
                            irc.reply("You have \x02%s\x02 chips in your account." % zetona)
                        else:
                            irc.reply("You don't have account.")
        else:
            irc.reply("Command is not allowed here.")
    viewchips = wrap(viewchips, [optional('something')])
Class = Casino


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
