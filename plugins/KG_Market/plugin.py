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
import datetime as dt
import supybot.ircmsgs as ircmsgs

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('KG_Market')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

_sellers_db = 'KG_Market/Sellers.json'
_registar = 'KG_Market/Registar.json'
_allowed_items = ['wrm', 'frm', 'weapons', 'food', 'ticket', 'gold', 'cc']
_allowed_games = ['eRep']
_allowed_channels = ['#KG_Market']
_votes_db = 'KG_Market/Votes.json'
_scamers_db = 'KG_Market/Scamers.json'
_allowed_votes = ['+', '-']
_admins = ['DonVitoCorleone']
_raw_qualities = 1
_allowed_qualities = ['1', '2', '3', '4', '5', '6', '7']

class KG_Market(callbacks.Plugin):
    """Add the help for "@plugin help KG_Market" here
    This should describe *how* to use this plugin."""
    threaded = True

    def read_sellers(self):
        with open(_sellers_db, 'r') as sellers_db:
            sellers_db = json.loads(sellers_db.read())
            return sellers_db

    def read_registar(self):
        with open(_registar, 'r') as registar:
            registar = json.loads(registar.read())
            return registar

    def register_seller(self, irc, nick, link):
        check_register = self.read_registar()
        if nick in check_register.keys():
            irc.reply("You can't register again.")
        else:
            if check_register != {}:
                for acc in check_register.keys():
                    if link == check_register[acc]['link']:
                        irc.reply("You can't register with this link because someone has already used it to register.")
                    else:
                        sati = dt.datetime.now().hour
                        minuta = dt.datetime.now().minute
                        sekundi = dt.datetime.now().second
                        dan = dt.datetime.now().day
                        mesec = dt.datetime.now().month
                        godina = dt.datetime.now().year
                        vreme_dodavanja = '%s/%s/%s - %s:%s:%s' % (dan, mesec, godina, sati, minuta, sekundi)
                        check_register[nick] = {}
                        check_register[nick]['time-registered'] = vreme_dodavanja
                        check_register[nick]['link'] = link
                        irc.queueMsg(ircmsgs.privmsg('ChanServ', 'access #KG_Market add %s 3' % nick))
                        irc.queueMsg(ircmsgs.privmsg('ChanServ', 'sync #KG_Market'))
                        with open(_registar, 'w') as registar:
                            registar.write(json.dumps(check_register))
                            irc.reply("Successfully registered as seller.")
            else:
                sati = dt.datetime.now().hour
                minuta = dt.datetime.now().minute
                sekundi = dt.datetime.now().second
                dan = dt.datetime.now().day
                mesec = dt.datetime.now().month
                godina = dt.datetime.now().year
                vreme_dodavanja = '%s/%s/%s - %s:%s:%s' % (dan, mesec, godina, sati, minuta, sekundi)
                check_register[nick] = {}
                check_register[nick]['time-registered'] = vreme_dodavanja
                check_register[nick]['link'] = link
                irc.queueMsg(ircmsgs.privmsg('ChanServ', 'access #KG_Market add %s 3' % nick))
                irc.queueMsg(ircmsgs.privmsg('ChanServ', 'sync #KG_Market'))
                with open(_registar, 'w') as registar:
                    registar.write(json.dumps(check_register))
                    irc.reply("Successfully registered as seller.")
        

    def add_seller(self, irc, msg, game, item, amount, price, quality):
        nick = msg.nick.lower()
        check_seller = self.read_sellers()
        check_registar = self.read_registar()
        quality = str(quality)
        if nick not in check_registar.keys():
            irc.reply("You can't add offer because you're not registered as seller. First you must register as one with command \x02+regseller\x02.")
        else:
            if nick in check_seller.keys():
                if game in check_seller[nick].keys():
                    if item in check_seller[nick][game].keys():
                        if quality in check_seller[nick][game][item].keys():
                            item_amount = check_seller[nick][game][item][quality]['amount']
                            new_item_amount = int(item_amount) + int(amount)
                            check_seller[nick][game][item][quality]['amount'] = new_item_amount
                            with open(_sellers_db, 'w') as sellers_db:
                                sellers_db.write(json.dumps(check_seller))
                                irc.reply("Successfully updated \x02%s\x02 amount, and it is \x02%s\x02 now." % (item, new_item_amount))
                        else:
                            new_item = {}
                            new_item['amount'] = amount
                            new_item['price'] = price
                            check_seller[nick][game][item][quality] = new_item
                            with open(_sellers_db, 'w') as sellers_db:
                                sellers_db.write(json.dumps(check_seller))
                                irc.reply("Successfully added \x02%s\x02 in the current sellers database with following data; Price: \x02%s\x02, Amount: \x02%s\x02, Quality: \x02%s\x02" % (item, price, amount, int(quality)))
                    else:
                        new_item = {}
                        new_item['amount'] = amount
                        new_item['price'] = price
                        check_seller[nick][game][item] = {}
                        check_seller[nick][game][item][quality] = new_item
                        with open(_sellers_db, 'w') as sellers_db:
                            sellers_db.write(json.dumps(check_seller))
                            irc.reply("Successfully added \x02%s\x02 in the current sellers database with following data; Price: \x02%s\x02, Amount: \x02%s\x02, Quality: \x02%s\x02." % (item, price, amount, int(quality)))
                else:
                    new_offer = {}
                    new_offer['price'] = price
                    new_offer['amount'] = amount
                    check_seller[nick][game] = {}
                    check_seller[nick][game][item] = {}
                    check_seller[nick][game][item][quality] = new_offer
                    with open(_sellers_db, 'w') as sellers_db:
                        sellers_db.write(json.dumps(check_seller))
                        irc.reply("Successfully added \x02%s\x02 in the current sellers database with following data; Price: \x02%s\x02, Amount: \x02%s\x02, Quality: \x02%s\x02." % (item, price, amount, int(quality)))
            else:
                new_item = {}
                new_item['price'] = price
                new_item['amount'] = amount
                check_seller[nick] = {}
                check_seller[nick][game] = {}
                check_seller[nick][game][item] = {}
                check_seller[nick][game][item][quality] = new_item
                with open(_sellers_db, 'w') as sellers_db:
                    sellers_db.write(json.dumps(check_seller))
                    irc.reply("Successfully added \x02%s\x02 in the sellers database with following data; Product: \x02%s\x02, Price: \x02%s\x02, Amount: \x02%s\x02, Quality: \x02%s\x02." % (nick, item, price, amount, int(quality)))

    def rm_offer(self, irc, seller, game, item, amount, quality):
        sellers = self.read_sellers()
        quality = str(quality)
        current_amount = sellers[seller][game][item][quality]['amount']
        if current_amount == amount:
            del sellers[seller][game][item]
            with open(_sellers_db, 'w') as sellers_db:
                sellers_db.write(json.dumps(sellers))
                irc.reply("Successfully removed \x02%s\x02 from your \x02%s\x02 offers." % (item, game))
        else:
            new_amount = current_amount - amount
            sellers[seller][game][item][quality]['amount'] = new_amount
            with open(_sellers_db, 'w') as sellers_db:
                sellers_db.write(json.dumps(sellers))
                irc.reply("Successfully removed \x02%s\x02 amount of \x02%s\x02 from your \x02%s\x02 offers. Current amount of \x02%s\x02 in \x02%s\x02 offers is \x02%s\x02." % (str(amount), item, game, item, game, str(new_amount)))

    def read_votes(self):
        with open(_votes_db, 'r') as votes:
            votes = json.loads(votes.read())
            return votes

    def like(self, irc, seller, vote):
        sellers = self.read_sellers()
        if seller not in sellers.keys():
            irc.reply("You can't vote for \x02%s\x02 because he's not even a seller." % seller)
        else:
            votes = self.read_votes()
            if seller in votes.keys():
                num_of_votes = votes[seller]['votes']
                new_votes = int(num_of_votes) + int((vote))
                votes[seller]['votes'] = new_votes
                with open(_votes_db, 'w') as votes1:
                    votes1.write(json.dumps(votes))
                    irc.reply("Number of \x02%s\x02's votes is \x02%s\x02." % (seller, new_votes))
            else:
                new_votes = 0 + int((vote))
                votes[seller] = {}
                votes[seller]['votes'] = new_votes
                with open(_votes_db, 'w') as votes1:
                    votes1.write(json.dumps(votes))
                    irc.reply("Number of \x02%s\x02's votes is \x02%s\x02." % (seller, new_votes))

    def read_scam_list(self):
        with open(_scamers_db, 'r') as scamers:
            scamers = json.loads(scamers.read())
            return scamers

    def scam(self, irc, name, reasone, date_time):
        scam_list = self.read_scam_list()
        if name in scam_list.keys():
            time_added = scam_list[name]['time']
            razlog = scam_list[name]['razlog']
            irc.reply("\x02%s\x02 is already in scam list, added on \x02%s\x02, with reason." % (name, time_added, razlog))
        else:
            users = irc.state.channels['#KG_Market'].users
            new_scam = {}
            new_scam['time'] = date_time
            new_scam['razlog'] = reasone
            scam_list[name] = new_scam
            with open(_scamers_db, 'w') as scamers:
                scamers.write(json.dumps(scam_list))
                irc.queueMsg(ircmsgs.privmsg('#KG_Market', ', '.join(users)))
                irc.queueMsg(ircmsgs.privmsg('#KG_Market', "Be aware of \x02%s\x02 he's added to the scam list. Reason: \x02%s\x02, Time: \x02%s\x02." % (name, reasone, date_time)))

    def remove_scam(self, irc, name):
        scammers = self.read_scam_list()
        scamer = name.lower()
        if scamer in scammers.keys():
            users = irc.state.channels['#KG_Market'].users
            del scammers[scamer]
            with open(_scamers_db, 'w') as scam_list:
                scam_list.write(json.dumps(scammers))
                irc.queueMsg(ircmsgs.privmsg('#KG_Market', ', '.join(users)))
                irc.queueMsg(ircmsgs.privmsg('#KG_Market', "\x02%s\x02 removed from scam list." % name))
        else:
            irc.reply("\x02%s\x02 is not in scam list." % scamer)

    def addoffer(self, irc, msg, args, game, item, amount, price, quality):
        """<game> <item> <amount> <price> <quality>

        Adds <item> in database for your profile."""
        channel = msg.args[0]
        quality = str(quality)
        if channel not in _allowed_channels:
            irc.reply("This command is not available here.")
        else:
            if game not in _allowed_games:
                irc.reply("This game is not yet implemented, games that we currently serve are: \x02%s\x02." % ', '.join(_allowed_games))
            else:
                if item not in _allowed_items:
                    irc.reply("This type of product is not yet implemented for this game, products that we currently support are: \x02%s\x02." % ', '.join(_allowed_items))
                elif quality not in _allowed_qualities:
                    irc.reply("This quality is not allowed, current possible qualities are: \x02%s\x02." % ', '.join(_allowed_qualities))
                else:
                    if item == 'wrm' or item == 'frm':
                        self.add_seller(irc, msg, game, item, amount, price, 1)
                    else:
                        self.add_seller(irc, msg, game, item, amount, price, quality)
    addoffer = wrap(addoffer, ['something', 'something', 'int', 'something', 'int'])

    def regseller(self, irc, msg, args, link):
        """<profile link>

        Register as seller with <link>."""
        nick = msg.nick.lower()
        channel = msg.args[0]
        if channel not in _allowed_channels:
            irc.reply("This command is not available here.")
        else:
            self.register_seller(irc, nick, link)
    regseller = wrap(regseller, ['url'])

    def viewoffer(self, irc, msg, args, item, game, quality):
        """<item> <game> <quality>

        Returns current offers of <item>."""
        channel = msg.args[0]
        quality = str(quality)
        if channel not in _allowed_channels:
            irc.reply("This command is not available here.")
        elif item not in _allowed_items:
            irc.reply("This type of product is not yet implemented for this game, products that we currently support are: \x02%s\x02." % ', '.join(_allowed_items))
        elif game not in _allowed_games:
            irc.reply("This game is not yet implemented, games that we currently serve are: \x02%s\x02." % ', '.join(_allowed_games))
        elif quality not in _allowed_qualities:
            irc.reply("This quality is not available, possible qualities are: \x02%s\x02." % ', '.join(_allowed_qualities))
        else:
            offers = self.read_sellers()
            sellers = []
            for name in offers.keys():
                if game in offers[name].keys():
                    if item in offers[name][game].keys():
                        if item == 'wrm' or item == 'frm':
                            quality = '1'
                            if quality in offers[name][game][item].keys():
                                sellers.append(name)
                                price = offers[name][game][item][quality]['price']
                                amount = offers[name][game][item][quality]['amount']
                                irc.reply("Seller: \x02%s\x02, Amount: \x02%s\x02, Price: \x02%s\x02, Quality: \x02q%s\x02" % (name, amount, price, quality))
                        else:
                            if quality in offers[name][game][item].keys():
                                sellers.append(name)
                                price = offers[name][game][item][quality]['price']
                                amount = offers[name][game][item][quality]['amount']
                                irc.reply("Seller: \x02%s\x02, Amount: \x02%s\x02, Price: \x02%s\x02, Quality: \x02q%s\x02" % (name, amount, price, quality))
            if sellers == []:
                irc.reply("Currently there are no offers for \x02%s\x02." % item)
    viewoffer = wrap(viewoffer, ['something', 'something', 'int'])

    def buyoffer(self, irc, msg, args, name, game, item, amount, quality):
        """<seller name> <game> <product> <amount> <quality>

        Marks offer as bought."""
        channel = msg.args[0]
        seller = name.lower()
        buyer = msg.nick
        quality = str(quality)
        if channel not in _allowed_channels:
            irc.reply("This command is not available here.")
        elif game not in _allowed_games:
            irc.reply("This game is not yet implemented, games that we currently serve are: \x02%s\x02." % ', '.join(_allowed_games))
        elif item not in _allowed_items:
            irc.reply("This type of product is not yet implemented for this game, products that we currently support are: \x02%s\x02." % ', '.join(_allowed_items))
        elif quality not in _allowed_qualities:
            irc.reply("This quality is not available, possible qualities are: \x02%s\x02." % ', '.join(_allowed_qualities))
        else:
            sellers = self.read_sellers()
            if seller not in sellers.keys():
                irc.reply("There is no such seller as \x02%s\x02." % name)
            else:
                if game not in sellers[seller].keys():
                    irc.reply("\x02%s\x02 doesn't have offers for \x02%s\x02." % (name, game))
                else:
                    if item not in sellers[seller][game].keys():
                        irc.reply("\x02%s\x02 doesn't have \x02%s\x02 in offers for \x02%s\x02." % (name, item, game))
                    elif quality not in sellers[seller][game][item].keys():
                        irc.reply("There is no \x02q%s\x02 for this offer." % quality)
                    else:
                        if item == 'wrm' or item == 'frm':
                            offer_amount = sellers[seller][game][item][1]['amount']
                            if offer_amount - int(amount) < 0:
                                irc.reply("You can't buy more amount of this product than it's available.")
                            else:
                                irc.queueMsg(ircmsgs.privmsg('MemoServ', "send %s \x02%s\x02 has just bought \x02%s\x02 amount of \x02q1 - %s\x02 in \x02%s\x02 from you, please remove this from your offers if it's really bought. If it's not bought please report \x02%s\x02 to admins on #KG_Market" % (name, buyer, amount, item, game, buyer)))
                                irc.reply("You have successfully bought this product. Seller has been notified about this and he will remove this offer from market next time he comes online, you should know that he can report you for false buy if you didn't really bought this.")
                        else:
                            offer_amount = sellers[seller][game][item][quality]['amount']
                            if offer_amount - int(amount) < 0:
                                irc.reply("You can't buy more amount of this product than it's available.")
                            else:
                                irc.queueMsg(ircmsgs.privmsg('MemoServ', "send %s \x02%s\x02 has just bought \x02%s\x02 amount of \x02q%s - %s\x02 in \x02%s\x02 from you, please remove this from your offers if it's really bought. If it's not bought please report \x02%s\x02 to admins on #KG_Market" % (name, buyer, quality, amount, item, game, buyer)))
                                irc.reply("You have successfully bought this product. Seller has been notified about this and he will remove this offer from market next time he comes online, you should know that he can report you for false buy if you didn't really bought this.")
    buyoffer = wrap(buyoffer, ['nick', 'something', 'something', 'int', 'int'])

    def rmoffer(self, irc, msg, args, game, item, amount, quality):
        """<game> <product> <amount> <quality>

        Removes your offer from market for given values."""
        channel = msg.args[0]
        seller = msg.nick.lower()
        quality = str(quality)
        if channel not in _allowed_channels:
            irc.reply("This command is not available here.")
        elif game not in _allowed_games:
            irc.reply("This game is not yet implemented, games that we currently serve are: \x02%s\x02." % ', '.join(_allowed_games))
        elif item not in _allowed_items:
            irc.reply("This type of product is not yet implemented for this game, products that we currently support are: \x02%s\x02." % ', '.join(_allowed_items))
        elif quality not in _allowed_qualities:
            irc.reply("This quality is not available, possible qualities are: \x02%s\x02." % ', '.join(_allowed_qualities))
        else:
            sellers = self.read_sellers()
            if seller not in sellers.keys():
                irc.reply("You are not a seller and you can't remove anything.")
            else:
                if game not in sellers[seller].keys():
                    irc.reply("\x02%s\x02 doesn't have offers for \x02%s\x02." % (seller, game))
                else:
                    if item not in sellers[seller][game].keys():
                        irc.reply("\x02%s\x02 doesn't have \x02%s\x02 in offers for \x02%s\x02." % (seller, item, game))
                    elif quality not in sellers[seller][game][item].keys():
                        irc.reply("There is no \x02q%s\x02 for this offer." % quality)
                    else:
                        if item == 'wrm' or item == 'frm':
                            offer_amount = sellers[seller][game][item]['1']['amount']
                            if offer_amount - int(amount) < 0:
                                irc.reply("You can't remove more amount of this product than it's available.")
                            else:
                                self.rm_offer(irc, seller, game, item, amount, 1)
                        else:
                            offer_amount = sellers[seller][game][item][quality]['amount']
                            if offer_amount - int(amount) < 0:
                                irc.reply("You can't remove more amount of this product than it's available.")
                            else:
                                self.rm_offer(irc, seller, game, item, amount, quality)
    rmoffer = wrap(rmoffer, ['something', 'something', 'int', 'int'])

    def mvote(self, irc, msg, args, seller, votes):
        """<seller> <votes>

        You can give + or - to the seller."""
        seller = seller.lower()
        nick = msg.nick.lower()
        if seller == nick:
            irc.reply("You can't add/remove votes for yourself.")
        elif votes not in _allowed_votes:
            irc.reply("You can't give this vote for the seller, possible votes are: \x02%s\x02." % ', '.join(_allowed_votes))
        else:
            if votes == '+':
                self.like(irc, seller, '+1')
            else:
                self.like(irc, seller, '-1')
    mvote = wrap(mvote, ['something', 'something'])

    def addscam(self, irc, msg, args, name, reason):
        """<name> <reason>

        Adds <name> to the scam list."""
        nick = msg.nick
        if nick not in _admins:
            irc.reply("You're not allowed to add someone on scam list, if you would like to do that please notify someone with the OP and above status on #KG_Market.")
        else:
            sati = dt.datetime.now().hour
            minuta = dt.datetime.now().minute
            sekundi = dt.datetime.now().second
            dan = dt.datetime.now().day
            mesec = dt.datetime.now().month
            godina = dt.datetime.now().year
            vreme_dodavanja = '%s/%s/%s - %s:%s:%s' % (dan, mesec, godina, sati, minuta, sekundi)
            self.scam(irc, name.lower(), ' '.join(reason), vreme_dodavanja)
    addscam = wrap(addscam, ['nick', many('something')])

    def scammers(self, irc, msg, args):
        """Takes no arguments

        Returns users from scam list."""
        channel = msg.args[0]
        if channel not in _allowed_channels:
            irc.reply("This command is not available here.")
        else:
            scamers = self.read_scam_list()
            if scamers == {}:
                irc.reply("Scam list is empty right now.")
            else:
                for name in scamers.keys():
                    reason = scamers[name]['razlog']
                    time_added = scamers[name]['time']
                    irc.reply("\x02%s\x02 added on \x02%s\x02 with reason: \x02%s\x02." % (name, time_added, reason))
    scammers = wrap(scammers)

    def rmscam(self, irc, msg, args, name):
        """<name>

        Removes <name> from scam list."""
        nick = msg.nick
        if nick not in _admins:
            irc.reply("You're not allowed to remove anyone from scam list, if you think that \x02%s\x02 should be removed from scam list contact someone with OP or higher status on \x02#KG_Market\x02." % name)
        else:
            self.remove_scam(irc, name)
    rmscam = wrap(rmscam, ['nick'])

Class = KG_Market


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
