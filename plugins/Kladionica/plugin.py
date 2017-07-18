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
import supybot.conf as conf
import supybot.ircmsgs as ircmsgs
import datetime as dt

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Kladionica')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

_admins = ['DonVitoCorleone']
_channels = ['#b365']
_lista = 'Kladionica/Lista.json'
_winers = 'Kladionica/Winers.json'
_ban = 'Kladionica/Ban.json'
_winers_backup = 'Kladionica/Backup/Backup_Winers.json'
_url = conf.supybot.plugins.ERep.url()
_registrator = 'Kladionica/Registar.json'
_allowed_quotas = ['1', 'x', '2']
_allowed_games = ['soccer', 'basketball', 'tennis', 'handball']
_bets = 'Kladionica/Bets.json'

class Kladionica(callbacks.Plugin):
    """Add the help for "@plugin help Kladionica" here
    This should describe *how* to use this plugin."""
    threaded = True

    ### Reading list/games database here ###
    def read_bets(self):
        """Citanje liste mogucih utakmica"""
        with open(_lista, 'r') as lista:
            lista = json.loads(lista.read())
            return lista

    ### Writing new games here, using when I'm adding new games to list ###
    def write_bets(self, irc, lista):
        """Upisivanje liste"""
        with open(_lista, 'w') as lista1:
            lista1.write(json.dumps(lista))
            irc.reply("New game is added to the list.")

    ### Creating new list of games that will be sent to self.write_bets(irc, lista) ###
    def add_game_to_list(self, irc, kec, iks, dvica, date, hour, tim1, tim2, game):
        """Dodavanje nove utakmice na listu"""
        trenutna_lista = self.read_bets() # Reading of already added games, I don't want to overwrite existing games
        upisi = []
        if trenutna_lista != {}:
            if len(trenutna_lista.keys()) == 13:
                irc.reply("There's already 13 games in list, you can't add new games.") # 13 games is maximum, if there's already 13 games in list nothing will be added
            else:
                for game1 in trenutna_lista.keys():
                    ekipa1 = trenutna_lista[game1]['tim 1']
                    ekipa2 = trenutna_lista[game1]['tim 2']
                    if tim1 == ekipa1:
                        if tim2 == ekipa2:
                            irc.reply("You can't add this game to list because it's already in the list.") # Again, I don't want to overwrite existing game
                            return
                        else:
                            upisi.append(1)
                    else:
                        upisi.append(1)
                if upisi == []:
                    return
                else:
                    broj_utakmice = len(trenutna_lista.keys()) + 1
                    broj_utakmice = int(broj_utakmice)
                    kvote = {}
                    kvote[1] = kec
                    kvote['x'] = iks
                    kvote[2] = dvica
                    trenutna_lista[broj_utakmice] = {}
                    trenutna_lista[broj_utakmice]['date'] = date
                    trenutna_lista[broj_utakmice]['hour'] = hour
                    trenutna_lista[broj_utakmice]['tim 1'] = tim1
                    trenutna_lista[broj_utakmice]['tim 2'] = tim2
                    trenutna_lista[broj_utakmice]['kvote'] = kvote
                    trenutna_lista[broj_utakmice]['tip igre'] = game
                    trenutna_lista[broj_utakmice]['sifra'] = broj_utakmice
                    self.write_bets(irc, trenutna_lista)
        else:
            broj_utakmice = len(trenutna_lista.keys()) + 1
            kvote = {}
            kvote[1] = kec
            kvote['x'] = iks
            kvote[2] = dvica
            trenutna_lista[broj_utakmice] = {}
            trenutna_lista[broj_utakmice]['date'] = date
            trenutna_lista[broj_utakmice]['hour'] = hour
            trenutna_lista[broj_utakmice]['tim 1'] = tim1
            trenutna_lista[broj_utakmice]['tim 2'] = tim2
            trenutna_lista[broj_utakmice]['kvote'] = kvote
            trenutna_lista[broj_utakmice]['tip igre'] = game
            trenutna_lista[broj_utakmice]['sifra'] = broj_utakmice
            self.write_bets(irc, trenutna_lista)

    ### Reading database of registered profiles, because you can't bet if you're not registered or you don't meet requirements ###
    def read_registrator(self):
        with open(_registrator, 'r') as registars:
            registrator = json.loads(registars.read())
            return registrator

    ### Here's the function for registering new profile ###
    def register_profile(self, irc, msg, name, data, ajdi):
        registar = self.read_registrator() # Read registar database, again, I don't want to overwrite existing profiles
        if registar != {}:
            if name in registar.keys():
                irc.reply("You can't register again because you already have profile.") # Your nick is already registered ;), and you can't use someone else nick because of +R channel mode
            else:
                profiles = []
                for profile in registar:
                    profile_id = registar[profile]['id']
                    if profile_id == ajdi:
                        profiles.append(1)
                if profiles == []:
                    registar[name] = data
                    with open(_registrator, 'w') as registrator:
                        registrator.write(json.dumps(registar))
                    irc.reply("You are now registered and you can place bets.")
                    irc.queueMsg(ircmsgs.privmsg('ChanServ', 'access add %s 3' % name))
                    irc.queueMsg(ircmsgs.privmsg('ChanServ', 'sync #b365'))
                else:
                    irc.reply("There is already profile with this id and you can't use it again, if this is your profile and you didn't used it to register please contact someone of admins.")
        else:
            registar[name] = data
            with open(_registrator, 'w') as registrator:
                registrator.write(json.dumps(registar))
            irc.reply("You are now registered and you can place bets.")
            irc.queueMsg(ircmsgs.privmsg('ChanServ', 'access add %s 3' % name))
            irc.queueMsg(ircmsgs.privmsg('ChanServ', 'sync #b365'))

    ### Reading placed bets with this ###
    def read_player_bets(self):
        """Reads list of current bets."""
        with open(_bets, 'r') as bet_list:
            current_bets = json.loads(bet_list.read())
            return current_bets

    ### Writing new bet for player ###
    def add_player_bet(self, irc, new_game):
        with open(_bets, 'w') as bet_list:
            bet_list.write(json.dumps(new_game))

    def addgame(self, irc, msg, args, kec, iks, dvica, date, hour, tim1, tim2, game):
        """<kvota 1> <kvota x> <kvota 2> <datum> <vreme> <tim 1> <tim 2> <tip igre>

        Adding new game to the list."""
        nick = msg.nick
        channel = msg.args[0]
        if channel not in _channels:
            irc.reply("You can't use this command here, please go to \x02#b365\x02.")
        elif nick not in _admins:
            irc.reply("You can't use this command because you're not in admin list.")
        elif game not in _allowed_games:
            irc.reply("You can't add this game, possible games are: \x02%s\x02." % ', '.join(_allowed_games))
        else:
            self.add_game_to_list(irc, kec, iks, dvica, date, hour, tim1, tim2, game)
    addgame = wrap(addgame, ['something', 'something', 'something', 'something', 'something', 'something', 'something', 'something'])

    def seegames(self, irc, msg, args):
        """Takes no arguments

        Returns list of possible games."""
        games = self.read_bets()
        if games != {}:
            key_list = list(games.iterkeys())
            for game in sorted(key_list, key=int):
                tim1 = games[game]['tim 1']
                tim2 = games[game]['tim 2']
                tip_igre = games[game]['tip igre']
                datum = games[game]['date']
                sat = games[game]['hour']
                kvota1 = games[game]['kvote']['1']
                kvotax = games[game]['kvote']['x']
                kvota2 = games[game]['kvote']['2']
                sifra = games[game]['sifra']
                irc.reply("\x02%s\x02.) \x02%s - %s\x02, Quotas:\x034 1-\x03 \x02%s\x02, \x037x-\x03 \x02%s\x02,\x039 2-\x03 \x02%s\x02, Time: \x02%s - %s\x02, Game: \x02%s\x02." % (sifra, tim1, tim2, kvota1, kvotax, kvota2, datum, sat, tip_igre))
        else:
            irc.reply("List is currently empty, it will be updated as soon as possible.")
    seegames = wrap(seegames)

    def reqme(self, irc, msg, args, ajdi):
        """<profile id>

        Register so you can place bets, you have to be lvl 28 or higher."""
        nick = msg.nick
        channel = msg.args[0]
        banned_ids = self.read_ban_list()
        if channel not in _channels:
            irc.reply("You can't use this command here, please go to \x02#b365\x02.")
        elif ajdi in banned_ids:
            irc.reply("This ID is banned and you can't use it to register.")
        else:
            try:
                data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (_url, ajdi)))
                if 'level' in data:
                    level = data['level']
                    if level >= 28:
                        link = 'http://www.erepublik.com/en/citizen/profile/%s' % ajdi
                        donate = 'http://www.erepublik.com/en/economy/donate-money/%s' % ajdi
                        new_data = {}
                        new_data['nick'] = nick
                        new_data['id'] = ajdi
                        new_data['profile'] = link
                        new_data['donate'] = donate
                        name = nick.lower()
                        self.register_profile(irc, msg, name, new_data, ajdi)
                    else:
                        irc.reply("You can't register because your lvl is not 28 or higher.")
                else:
                    irc.reply("You didn't provide valid profile ID.")
            except:
                irc.reply("You didn't provide valid profile ID, or maybe API is currently unavailable, please try again in few seconds, if error persists please notify somebody from admin team.")
    reqme = wrap(reqme, ['int'])

    def betgame(self, irc, msg, args, quota, quota1, quota2, quota3, quota4, quota5, quota6, quota7, quota8, quota9, quota10, quota11, quota12):
        """<1st game quota> <2nd game quota> <3rd game quota> ....... <13th game quota>

        Place bet for current games."""
        nick = msg.nick.lower()
        channel = msg.args[0]
        if channel not in _channels:
            irc.reply("You can't use this command here, please go to \x02#b365\x02.")
        else:
            profiles = self.read_registrator() # Check if this player is registered or not
            if nick not in profiles.keys():
                irc.reply("You're not registered and you can't place bet.")
            else:
                lista = self.read_bets() # If there's no games, or not enough games you can't place bet
                if len(lista.keys()) != 13:
                    irc.reply("You can't place bet right now because list is not up do date.")
                else:
                    ### Here I'm validating quotes (1, x, 2)
                    if quota not in _allowed_quotas:
                        irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota, ', '.join(_allowed_quotas)))
                    elif quota1 not in _allowed_quotas:
                        irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota1, ', '.join(_allowed_quotas)))
                    elif quota2 not in _allowed_quotas:
                        irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota2, ', '.join(_allowed_quotas)))
                    elif quota3 not in _allowed_quotas:
                        irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota3, ', '.join(_allowed_quotas)))
                    elif quota4 not in _allowed_quotas:
                        irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota4, ', '.join(_allowed_quotas)))
                    elif quota5 not in _allowed_quotas:
                        irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota5, ', '.join(_allowed_quotas)))
                    elif quota6 not in _allowed_quotas:
                        irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota6, ', '.join(_allowed_quotas)))
                    elif quota7 not in _allowed_quotas:
                        irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota7, ', '.join(_allowed_quotas)))
                    elif quota8 not in _allowed_quotas:
                        irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota8, ', '.join(_allowed_quotas)))
                    elif quota9 not in _allowed_quotas:
                        irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota9, ', '.join(_allowed_quotas)))
                    elif quota10 not in _allowed_quotas:
                        irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota10, ', '.join(_allowed_quotas)))
                    elif quota11 not in _allowed_quotas:
                        irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota11, ', '.join(_allowed_quotas)))
                    elif quota12 not in _allowed_quotas:
                        irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota12, ', '.join(_allowed_quotas)))
                    else:
                        current_bets = self.read_player_bets() # Checking if someone is already placed bet, they can't change it
                        if nick in current_bets.keys():
                            irc.reply("You can't place another bet because you've already placed bet for upcoming drawing, if you think that you've made some mistake please contact someone from admin team.")
                        else:
                            donate_link = profiles[nick]['donate']
                            ### I don't really need this anymore but I'm not in a mood to delete it
                            sifra = lista['1']['sifra']
                            sifra2 = lista['2']['sifra']
                            sifra3 = lista['3']['sifra']
                            sifra4 = lista['4']['sifra']
                            sifra5 = lista['5']['sifra']
                            sifra6 = lista['6']['sifra']
                            sifra7 = lista['7']['sifra']
                            sifra8 = lista['8']['sifra']
                            sifra9 = lista['9']['sifra']
                            sifra10 = lista['10']['sifra']
                            sifra11 = lista['11']['sifra']
                            sifra12 = lista['12']['sifra']
                            sifra13 = lista['13']['sifra']
                            game_quotas = {}
                            game_quotas[sifra] = quota
                            game_quotas[sifra2] = quota1
                            game_quotas[sifra3] = quota2
                            game_quotas[sifra4] = quota3
                            game_quotas[sifra5] = quota4
                            game_quotas[sifra6] = quota5
                            game_quotas[sifra7] = quota6
                            game_quotas[sifra8] = quota7
                            game_quotas[sifra9] = quota8
                            game_quotas[sifra10] = quota9
                            game_quotas[sifra11] = quota10
                            game_quotas[sifra12] = quota11
                            game_quotas[sifra13] = quota12
                            sati = dt.datetime.now().hour
                            minuta = dt.datetime.now().minute
                            sekundi = dt.datetime.now().second
                            dan = dt.datetime.now().day
                            mesec = dt.datetime.now().month
                            godina = dt.datetime.now().year
                            vreme_dodavanja = '%s/%s/%s - %s:%s:%s' % (dan, mesec, godina, sati, minuta, sekundi)
                            current_bets[nick] = {}
                            current_bets[nick]['vreme uplate'] = vreme_dodavanja
                            current_bets[nick]['donate'] = donate_link
                            current_bets[nick]['quotas'] = game_quotas
                            self.add_player_bet(irc, current_bets) # If everything's right send new bet for writing
                            irc.reply("You have successfully added bet for upcoming games, please write down your ticket informations. If you want to appeal for something you must have those informations, you have 24h for any kind of appeal.")
    betgame = wrap(betgame, ['something', 'something', 'something', 'something', 'something', 'something', 'something', 'something', 'something', 'something', 'something', 'something', 'something'])

    def clearbets(self, irc, msg, args, name):
        """[<name>]

        Clears bets list, if [<name>] is specified clears bets for this player, in other case it clears whole bets list."""
        nick = msg.nick
        channel = msg.args[0]
        if channel not in _channels:
            irc.reply("This command is not available here, please go to \x02#b365\x02.")
        elif nick not in _admins:
            irc.reply("You can't use this command because you're not in admin list.") 
        else:
            bet_list = self.read_player_bets() # Again, no overwrite will happen because of this
            if bet_list != {}:
                if name is not None:
                    name1 = name.lower() # All keys are lowercase and I have to change everything to be like that
                    if name1 in bet_list.keys():
                        del bet_list[name1] # Removing <name1> bet
                        self.add_player_bet(irc, bet_list) # Writing new bets without <name1> bet now
                        irc.reply("\x02%s\x02 successfully deleted from bets list." % name)
                    else:
                        irc.reply("\x02%s\x02 is not in bets list, can't delete it, current players are: \x02%s\x02." % (name, ','. join(bet_list.keys())))
                else:
                    ### This is used to clear whole bets database
                    new_bets = {}
                    self.add_player_bet(irc, new_bets)
                    irc.reply("Bets list is now cleared.")
            else:
                irc.reply("Bets list is empty and I can't delete anything.")
    clearbets = wrap(clearbets, [optional('nick')])

    def viewticket(self, irc, msg, args, name):
        """[<name>]

        Returns ticket for given [<nick>], if it's not specified returns all tickets."""
        nick = msg.nick
        channel = msg.args[0]
        if channel not in _channels:
            irc.reply("This command is not available here, please go to \x02#b365\x02.")
        elif nick not in _admins:
            irc.reply("You can't view tickets because you're not in admin team.")
        else:
            bet_list = self.read_player_bets()
            if bet_list != {}:
                if name is not None:
                    name1 = name.lower()
                    if name1 in bet_list.keys():
                        clear_bet_list = []
                        vreme_uplate = bet_list[name1]['vreme uplate']
                        donate = bet_list[name1]['donate']
                        quotas = sorted(bet_list[name1]['quotas'].iterkeys(), key=int)
                        for bet in quotas:
                            bet = str(bet)
                            bet = bet_list[name1]['quotas'][bet]
                            clear_bet_list.append(bet)
                        irc.reply("\x02%s\x02, Time placed: \x02%s\x02, Donate link: \x02%s\x02, Quotas: 1.) \x02%s\x02, 2.) \x02%s\x02, 3.) \x02%s\x02, 4.) \x02%s\x02, 5.) \x02%s\x02, 6.) \x02%s\x02, 7.) \x02%s\x02, 8.) \x02%s\x02, 9.) \x02%s\x02, 10.) \x02%s\x02, 11.) \x02%s\x02, 12.) \x02%s\x02, 13.) \x02%s\x02." % (name1, vreme_uplate, donate, clear_bet_list[0], clear_bet_list[1], clear_bet_list[2], clear_bet_list[3], clear_bet_list[4], clear_bet_list[5], clear_bet_list[6], clear_bet_list[7], clear_bet_list[8], clear_bet_list[9], clear_bet_list[10], clear_bet_list[11], clear_bet_list[12]))
                    else:
                        irc.reply("\x02%s\x02 is not in bets list." % name)
                else:
                    for name1 in bet_list.keys():
                        clear_bet_list = []
                        vreme_uplate = bet_list[name1]['vreme uplate']
                        donate = bet_list[name1]['donate']
                        quotas = sorted(bet_list[name1]['quotas'].iterkeys(), key=int)
                        for bet in quotas:
                            bet = str(bet)
                            bet = bet_list[name1]['quotas'][bet]
                            clear_bet_list.append(bet)
                        irc.reply("\x02%s\x02, Time placed: \x02%s\x02, Donate link: \x02%s\x02, Quotas: 1.) \x02%s\x02, 2.) \x02%s\x02, 3.) \x02%s\x02, 4.) \x02%s\x02, 5.) \x02%s\x02, 6.) \x02%s\x02, 7.) \x02%s\x02, 8.) \x02%s\x02, 9.) \x02%s\x02, 10.) \x02%s\x02, 11.) \x02%s\x02, 12.) \x02%s\x02, 13.) \x02%s\x02." % (name1, vreme_uplate, donate, clear_bet_list[0], clear_bet_list[1], clear_bet_list[2], clear_bet_list[3], clear_bet_list[4], clear_bet_list[5], clear_bet_list[6], clear_bet_list[7], clear_bet_list[8], clear_bet_list[9], clear_bet_list[10], clear_bet_list[11], clear_bet_list[12]))
            else:
                irc.reply("Bets list is empty.")
    viewticket = wrap(viewticket, [optional('nick')])

    ### Ok, this was most annoying part of code, I don't even want to comment this -.- ###
    ### Baaah, fine, if I really have to, I'm reading winners database here, tada, you couldn't guess that from code ha????!!!! ###
    def read_winers(self):
        with open(_winers, 'r') as winers:
            winers = json.loads(winers.read())
            return winers

    ### Hmmm, what do you think I'm doing here, yes you're right, I'm writing new winners to database ###
    def write_winers(self, irc, msg, winers):
        with open(_winers, 'w') as wins:
            wins.write(json.dumps(winers))

    ### Now 13 almost identical functions (4 words are different) ###
    ### Comparing first game quota here, and if it's same as correct one adding +1 to the players winners ticket ###
    def check_first_game(self, irc, msg, name, correct_quotes, player_quotes):
        first_game = correct_quotes[0]
        player_first_game = player_quotes[0]
        if first_game == player_first_game:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 1 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_second_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_second_game(irc, msg, name, correct_quotes, player_quotes)
        else:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 0 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_second_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_second_game(irc, msg, name, correct_quotes, player_quotes)

    ### Comparing 2nd game quota here, and if it's same as correct one adding +1 to the players winners ticket ###
    def check_second_game(self, irc, msg, name, correct_quotes, player_quotes):
        second_game = correct_quotes[1]
        player_second_game = player_quotes[1]
        if second_game == player_second_game:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 1 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_third_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_third_game(irc, msg, name, correct_quotes, player_quotes)
        else:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 0 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_third_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_third_game(irc, msg, name, correct_quotes, player_quotes)

    ### Comparing 3rd game quota here, and if it's same as correct one adding +1 to the players winners ticket ###
    def check_third_game(self, irc, msg, name, correct_quotes, player_quotes):
        third_game = correct_quotes[2]
        player_third_game = player_quotes[2]
        if third_game == player_third_game:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 1 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_fourth_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_fourth_game(irc, msg, name, correct_quotes, player_quotes)
        else:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 0 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_fourth_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_fourth_game(irc, msg, name, correct_quotes, player_quotes)

    ### Comparing 4th game quota here, and if it's same as correct one adding +1 to the players winners ticket ###
    def check_fourth_game(self, irc, msg, name, correct_quotes, player_quotes):
        fourth_game = correct_quotes[3]
        player_fourth_game = player_quotes[3]
        if fourth_game == player_fourth_game:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 1 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_fifth_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_fifth_game(irc, msg, name, correct_quotes, player_quotes)
        else:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 0 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_fifth_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_fifth_game(irc, msg, name, correct_quotes, player_quotes)

    ### Comparing 5th game quota here, and if it's same as correct one adding +1 to the players winners ticket ###
    def check_fifth_game(self, irc, msg, name, correct_quotes, player_quotes):
        fifth_game = correct_quotes[4]
        player_fifth_game = player_quotes[4]
        if fifth_game == player_fifth_game:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 1 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_sixth_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_sixth_game(irc, msg, name, correct_quotes, player_quotes)
        else:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 0 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_sixth_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_sixth_game(irc, msg, name, correct_quotes, player_quotes)

    ### Comparing 6th game quota here, and if it's same as correct one adding +1 to the players winners ticket ###
    def check_sixth_game(self, irc, msg, name, correct_quotes, player_quotes):
        sixth_game = correct_quotes[5]
        player_sixth_game = player_quotes[5]
        if sixth_game == player_sixth_game:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 1 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_seventh_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_seventh_game(irc, msg, name, correct_quotes, player_quotes)
        else:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 0 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_seventh_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_seventh_game(irc, msg, name, correct_quotes, player_quotes)

    ### Comparing 7th game quota here, and if it's same as correct one adding +1 to the players winners ticket ###
    def check_seventh_game(self, irc, msg, name, correct_quotes, player_quotes):
        seventh_game = correct_quotes[6]
        player_seventh_game = player_quotes[6]
        if seventh_game == player_seventh_game:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 1 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_eight_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_eight_game(irc, msg, name, correct_quotes, player_quotes)
        else:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 0 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_eight_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_eight_game(irc, msg, name, correct_quotes, player_quotes)

    ### Comparing 8th game quota here, and if it's same as correct one adding +1 to the players winners ticket ###
    def check_eight_game(self, irc, msg, name, correct_quotes, player_quotes):
        eight_game = correct_quotes[7]
        player_eight_game = player_quotes[7]
        if eight_game == player_eight_game:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 1 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_nineth_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_nineth_game(irc, msg, name, correct_quotes, player_quotes)
        else:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 0 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_nineth_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_nineth_game(irc, msg, name, correct_quotes, player_quotes)

    ### Comparing 9th game quota here, and if it's same as correct one adding +1 to the players winners ticket ###
    def check_nineth_game(self, irc, msg, name, correct_quotes, player_quotes):
        nineth_game = correct_quotes[8]
        player_nineth_game = player_quotes[8]
        if nineth_game == player_nineth_game:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 1 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_tenth_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_tenth_game(irc, msg, name, correct_quotes, player_quotes)
        else:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 0 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_tenth_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_tenth_game(irc, msg, name, correct_quotes, player_quotes)

    ### Comparing 10th game quota here, and if it's same as correct one adding +1 to the players winners ticket ###
    def check_tenth_game(self, irc, msg, name, correct_quotes, player_quotes):
        tenth_game = correct_quotes[9]
        player_tenth_game = player_quotes[9]
        if tenth_game == player_tenth_game:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 1 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_eleventh_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_eleventh_game(irc, msg, name, correct_quotes, player_quotes)
        else:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 0 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_eleventh_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_eleventh_game(irc, msg, name, correct_quotes, player_quotes)

    ### Comparing 11th game quota here, and if it's same as correct one adding +1 to the players winners ticket ###
    def check_eleventh_game(self, irc, msg, name, correct_quotes, player_quotes):
        eleventh_game = correct_quotes[10]
        player_eleventh_game = player_quotes[10]
        if eleventh_game == player_eleventh_game:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 1 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_twelvth_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_twelvth_game(irc, msg, name, correct_quotes, player_quotes)
        else:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 0 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_twelvth_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_twelvth_game(irc, msg, name, correct_quotes, player_quotes)

    ### Comparing 12th game quota here, and if it's same as correct one adding +1 to the players winners ticket ###
    def check_twelvth_game(self, irc, msg, name, correct_quotes, player_quotes):
        twelvth_game = correct_quotes[11]
        player_twelvth_game = player_quotes[11]
        if twelvth_game == player_twelvth_game:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 1 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_thirteenth_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_thirteenth_game(irc, msg, name, correct_quotes, player_quotes)
        else:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 0 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_thirteenth_game(irc, msg, name, correct_quotes, player_quotes)
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                self.check_thirteenth_game(irc, msg, name, correct_quotes, player_quotes)

    ### Ok, this one is little different because I have to respond something to channel right? ###
    def check_thirteenth_game(self, irc, msg, name, correct_quotes, player_quotes):
        thirteenth_game = correct_quotes[12]
        player_thirteenth_game = player_quotes[12]
        if thirteenth_game == player_thirteenth_game:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 1 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                ### After checking all games I'm reading that new winners db to see numbers of correct games
                new_winers = self.read_winers()
                ### Taking "vreme uplate" and "donate" from this one
                bets = self.read_player_bets()
                vreme_uplate = bets[name]['vreme uplate']
                donate = bets[name]['donate']
                players_results = new_winers[name]['result'] # This is the last number of correct games
                ### Because we're giving prize for 11, 12 and 13 correct numbers (for now) here's the part for checking that
                if players_results >= 11:
                    irc.reply("\x02%s\x02 has \x02%s\x02 correct bets. He placed his bet on \x02%s\x02 and his donate link is \x02%s\x02" % (name, players_results, vreme_uplate, donate))
                else:
                    irc.reply("\x02%s\x02 has \x02%s\x02 correct bets which is not enough for any prize." % (name, players_results))
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                new_winers = self.read_winers()
                bets = self.read_player_bets()
                vreme_uplate = bets[name]['vreme uplate']
                donate = bets[name]['donate']
                players_results = new_winers[name]['result']
                if players_results >= 11:
                    irc.reply("\x02%s\x02 has \x02%s\x02 correct bets. He placed his bet on \x02%s\x02 and his donate link is \x02%s\x02" % (name, players_results, vreme_uplate, donate))
                else:
                    irc.reply("\x02%s\x02 has \x02%s\x02 correct bets which is not enough for any prize." % (name, players_results))
        else:
            winers = self.read_winers()
            if name in winers.keys():
                current_result = winers[name]['result']
                new_result = 0 + current_result
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                new_winers = self.read_winers()
                bets = self.read_player_bets()
                vreme_uplate = bets[name]['vreme uplate']
                donate = bets[name]['donate']
                players_results = new_winers[name]['result']
                if players_results >= 11:
                    irc.reply("\x02%s\x02 has \x02%s\x02 correct bets. He placed his bet on \x02%s\x02 and his donate link is \x02%s\x02" % (name, players_results, vreme_uplate, donate))
                else:
                    irc.reply("\x02%s\x02 has \x02%s\x02 correct bets which is not enough for any prize." % (name, players_results))
            else:
                new_result = 1
                winers[name] = {}
                winers[name]['result'] = new_result
                self.write_winers(irc, msg, winers)
                new_winers = self.read_winers()
                bets = self.read_player_bets()
                vreme_uplate = bets[name]['vreme uplate']
                donate = bets[name]['donate']
                players_results = new_winers[name]['result']
                if players_results >= 11:
                    irc.reply("\x02%s\x02 has \x02%s\x02 correct bets. He placed his bet on \x02%s\x02 and his donate link is \x02%s\x02" % (name, players_results, vreme_uplate, donate))
                else:
                    irc.reply("\x02%s\x02 has \x02%s\x02 correct bets which is not enough for any prize." % (name, players_results))

    def chwin(self, irc, msg, args, quota, quota1, quota2, quota3, quota4, quota5, quota6, quota7, quota8, quota9, quota10, quota11, quota12):
        """<1st game quota> <2nd game quota> <3rd game quota> ....... <13th game quota>

        Checks profitable tickets."""
        nick = msg.nick
        channel = msg.args[0]
        if channel not in _channels:
            irc.reply("You can't use this command here, please go to \x02#b365\x02.")
        elif nick not in _admins:
            irc.reply("You're not allowed to use this command because you're not in admins list.")
        else:
            if quota not in _allowed_quotas:
                irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota, ', '.join(_allowed_quotas)))
            elif quota1 not in _allowed_quotas:
                irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota1, ', '.join(_allowed_quotas)))
            elif quota2 not in _allowed_quotas:
                irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota2, ', '.join(_allowed_quotas)))
            elif quota3 not in _allowed_quotas:
                irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota3, ', '.join(_allowed_quotas)))
            elif quota4 not in _allowed_quotas:
                irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota4, ', '.join(_allowed_quotas)))
            elif quota5 not in _allowed_quotas:
                irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota5, ', '.join(_allowed_quotas)))
            elif quota6 not in _allowed_quotas:
                irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota6, ', '.join(_allowed_quotas)))
            elif quota7 not in _allowed_quotas:
                irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota7, ', '.join(_allowed_quotas)))
            elif quota8 not in _allowed_quotas:
                irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota8, ', '.join(_allowed_quotas)))
            elif quota9 not in _allowed_quotas:
                irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota9, ', '.join(_allowed_quotas)))
            elif quota10 not in _allowed_quotas:
                irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota10, ', '.join(_allowed_quotas)))
            elif quota11 not in _allowed_quotas:
                irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota11, ', '.join(_allowed_quotas)))
            elif quota12 not in _allowed_quotas:
                irc.reply("You can't use this type of quota (\x02%s\x02), possible quotas are: \x02%s\x02." % (quota12, ', '.join(_allowed_quotas)))
            else:
                bet_list = self.read_player_bets()
                if bet_list == {}:
                    irc.reply("There are no bets to check.")
                else:
                    ### This code below took me 2 days to invent xD and now I don't even need it but I won't delete it because I can always comment it and leave for later notices
                    win_list = [quota, quota1, quota2, quota3, quota4, quota5, quota6, quota7, quota8, quota9, quota10, quota11, quota12]
                    for name1 in bet_list.keys():
                        clear_bet_list = []
                        vreme_uplate = bet_list[name1]['vreme uplate']
                        donate = bet_list[name1]['donate']
                        ### Because dict keys are strings and I want to sort them from first to last, and there's 13 keys, if there's no this line below it would go like 1, 10, 11, 12, 13, 2, 3 etc. STRING not INT ###
                        quotas = sorted(bet_list[name1]['quotas'].iterkeys(), key=int)
                        for bet in quotas:
                            ### Now I have to format this into string again because I won't be able to compare this with correct results because they are string because of wrap par, and it must be 'something' instead of 'int' because of quota x
                            bet = str(bet)
                            bet = bet_list[name1]['quotas'][bet]
                            clear_bet_list.append(bet)
                        self.check_first_game(irc, msg, name1, win_list, clear_bet_list) # I'm starting with checking correct numbers here
    chwin = wrap(chwin, ['something', 'something', 'something', 'something', 'something', 'something', 'something', 'something', 'something', 'something', 'something', 'something', 'something'])

    def read_backup(self):
        with open(_winers_backup, 'r') as backup:
            win_backup = json.loads(backup.read())
            return win_backup

    def clearwins(self, irc, msg, args):
        """Takes no arguments

        Clears winners database, makes backup of it of course."""
        nick = msg.nick
        channel = msg.args[0]
        if channel not in _channels:
            irc.reply("You can't use this command here, please go to \x02#b365\x02.")
        elif nick not in _admins:
            irc.reply("You're not allowed to use this command because you're not in admins list.")
        else:
            sati = dt.datetime.now().hour
            minuta = dt.datetime.now().minute
            sekundi = dt.datetime.now().second
            dan = dt.datetime.now().day
            mesec = dt.datetime.now().month
            godina = dt.datetime.now().year
            dan_mesec_godina = '%s/%s/%s' % (dan, mesec, godina)
            vreme_brisanja = '%s/%s/%s - %s:%s:%s' % (dan, mesec, godina, sati, minuta, sekundi)
            winers = self.read_winers()
            current_backup = self.read_backup()
            if dan_mesec_godina in current_backup.keys():
                irc.reply("Backup for this date already exist, you can't make more than 1 backup for one date.")
            else:
                new_backup = {}
                new_backup['nick'] = nick
                new_backup['vreme'] = vreme_brisanja
                new_backup['winers'] = winers
                current_backup[dan_mesec_godina] = new_backup
                clear_winers = {}
                self.write_winers(irc, msg, clear_winers)
                with open(_winers_backup, 'w') as add_new_backup:
                    add_new_backup.write(json.dumps(current_backup))
                irc.reply("New backup is added.")
    clearwins = wrap(clearwins)

    def delgame(self, irc, msg, args, game):
        """[<game>]

        Removes [<game>] from list database, if [<game>] is not provided clears whole list database."""
        nick = msg.nick
        channel = msg.args[0]
        if channel not in _channels:
            irc.reply("You can't use this command here, please go to \x02#b365\x02.")
        elif nick not in _admins:
            irc.reply("You're not allowed to use this command because you're not in admins list.")
        else:
            if game is None:
                lista = self.read_bets()
                new_lista = {}
                with open(_lista, 'w') as new_list:
                    new_list.write(json.dumps(new_lista))
                irc.reply("Lista database is cleared.")
            else:
                lista = self.read_bets()
                if str(game) in lista.keys():
                    del lista[str(game)]
                    with open(_lista, 'w') as new_lista:
                        new_lista.write(json.dumps(lista))
                    irc.reply("Game \x02%s\x02 deleted from lista database." % game)
                else:
                    irc.reply("There is no game number \x02%s\x02." % game)
    delgame = wrap(delgame, [optional('int')])

    def fix_game(self, irc, msg, broj, kec, iks, dvica, date, hour, tim1, tim2, game):
        trenutna_lista = self.read_bets()
        broj_utakmice = broj
        kvote = {}
        kvote[1] = kec
        kvote['x'] = iks
        kvote[2] = dvica
        trenutna_lista[broj_utakmice] = {}
        trenutna_lista[broj_utakmice]['date'] = date
        trenutna_lista[broj_utakmice]['hour'] = hour
        trenutna_lista[broj_utakmice]['tim 1'] = tim1
        trenutna_lista[broj_utakmice]['tim 2'] = tim2
        trenutna_lista[broj_utakmice]['kvote'] = kvote
        trenutna_lista[broj_utakmice]['tip igre'] = game
        trenutna_lista[broj_utakmice]['sifra'] = broj_utakmice
        self.write_bets(irc, trenutna_lista)

    def fixgame(self, irc, msg, args, broj, kec, iks, dvica, date, hour, tim1, tim2, game):
        """<number of game> <kvota 1> <kvota x> <kvota 2> <datum> <vreme> <tim 1> <tim 2> <tip igre>

        Adding new game to the list."""
        nick = msg.nick
        channel = msg.args[0]
        if channel not in _channels:
            irc.reply("You can't use this command here, please go to \x02#b365\x02.")
        elif nick not in _admins:
            irc.reply("You can't use this command because you're not in admin list.")
        elif game not in _allowed_games:
            irc.reply("You can't add this game, possible games are: \x02%s\x02." % ', '.join(_allowed_games))
        else:
            if broj <= 13:
                self.fix_game(irc, msg, broj, kec, iks, dvica, date, hour, tim1, tim2, game)
            else:
                irc.reply("<number of game> can't be higher than 13.")
    fixgame = wrap(fixgame, ['int', 'something', 'something', 'something', 'something', 'something', 'something', 'something', 'something'])

    def banid(self, irc, msg, args, profile_id):
        """<profile id>

        Adds <profile id> to the ban list."""
        current_bans = self.read_ban_list()
        nick = msg.nick
        channel = msg.args[0]
        if channel not in _channels:
            irc.reply("You can't use this command here, please go to \x02#b365\x02.")
        elif nick not in _admins:
            irc.reply("You can't use this command because you're not in admin list.")
        else:
            if profile_id in current_bans:
                irc.reply("\x02%s\x02 is already banned.")
            else:
                current_bans.append(profile_id)
                self.write_ban(irc, msg, current_bans)
    banid = wrap(banid, ['int'])

    def unbanid(self, irc, msg, args, profile_id):
        """<profile id>

        Unbans <profile id>."""
        current_bans = self.read_ban_list()
        nick = msg.nick
        channel = msg.args[0]
        if channel not in _channels:
            irc.reply("You can't use this command here, please go to \x02#b365\x02.")
        elif nick not in _admins:
            irc.reply("You can't use this command because you're not in admin list.")
        else:
            if profile_id in current_bans:
                current_bans.remove(profile_id)
                with open(_ban, 'w') as bans:
                    bans.write(json.dumps(current_bans))
                irc.reply("\x02%s\x02 removed from banned ids." % profile_id)
            else:
                irc.reply("\x02%s\x02 is not in ban list and I can't remove it." % profile_id)
    unbanid = wrap(unbanid, ['int'])

    def seebanns(self, irc, msg, args):
        """Takes no arguments

        Returns ban list."""
        bans = self.read_ban_list()
        nick = msg.nick
        channel = msg.args[0]
        if channel not in _channels:
            irc.reply("You can't use this command here, please go to \x02#b365\x02.")
        elif nick not in _admins:
            irc.reply("You can't use this command because you're not in admin list.")
        else:
            if bans == []:
                irc.reply("List is empty.")
            else:
                irc.reply(', '.join(map(str, bans)))
    seebanns = wrap(seebanns)

    def rmprofile(self, irc, msg, args, name):
        """<nick>

        Removes profile from registered profiles."""
        nick = msg.nick
        channel = msg.args[0]
        if channel not in _channels:
            irc.reply("You can't use this command here, please go to \x02#b365\x02.")
        elif nick not in _admins:
            irc.reply("You can't use this command because you're not in admin list.")
        else:
            register = self.read_registrator()
            if register != {}:
                if name.lower() in register.keys():
                    del register[name.lower()]
                    with open(_registrator, 'w') as regs:
                        regs.write(json.dumps(register))
                    irc.reply("\x02%s\x02 successfully removed." % name)
                else:
                    irc.reply("\x02%s\x02 is not in the registered profiles database." % name)
            else:
                irc.reply("Registered profiles database is empty.")
    rmprofile = wrap(rmprofile, ['nick'])

    def read_ban_list(self):
        with open(_ban, 'r') as ban_lista:
            bans = json.loads(ban_lista.read())
            return bans

    def write_ban(self, irc, msg, lista):
        with open(_ban, 'w') as bans:
            bans.write(json.dumps(lista))
        irc.reply("Successfully added to the ban list.")

Class = Kladionica


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
