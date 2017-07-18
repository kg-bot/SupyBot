###
# coding=utf-8
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
import random
import supybot.ircmsgs as ircmsgs
import smtplib
from email.mime.text import MIMEText
import supybot.schedule as schedule
import time

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('BitMine')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class BitMine(callbacks.Plugin):
    """Add the help for "@plugin help BitMine" here
    This should describe *how* to use this plugin."""
    threaded = True

    def order(self, irc, msg, args, name, surname, username, email):
        """<name> <surname> <username> <email>

        You can order a BitcoinMining application with this command."""
        channel = msg.args[0]
        if channel == "#ACCMS_REQUEST":
            pass_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '{', '}', ':', '>', '<', '?', '|', '@', '!', '#', '$', '%', '*', '(', ')', '-', '+']
            ##### ID characters list and empty list which is ready for appending #####
            id_chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
            id = []
            ##### Confirmation list which is ready for appending (using same characters like in ID but different randomization #####
            confirm_order = []
            ##### Password list ready for appending (using pass_chars for randomization) #####
            password = []
            ##### File locations, those files are used in WITH OPEN() statement #####
            buyers = 'Bitcoin/Buyers.json'
            email_folder = 'Bitcoin/Email.txt'
            waiting_confirm = 'Bitcoin/Waiting_confirmation.json'
            confirmed_emails = 'Bitcoin/Confirmed_orders.json'
            hostname = msg.host
            nick = msg.nick
            ##### Randomizing password and appending password = [] #####
            for pass_char in xrange(125):
                password.append(random.choice(pass_chars))
            ##### Randomizing ID and appending id = [] #####
            for id_char in xrange(10):
                id.append(random.choice(id_chars))
            ##### Randomizing confirmation code and appending confirm_order =[] #####
            for id_char in xrange(15):
                confirm_order.append(random.choice(id_chars))
            ##### Preparing customer dictionary for customers file #####
            buyer_dict = {}
            buyer_dict['ime'] = name
            buyer_dict['prezime'] = surname
            buyer_dict['sifra'] = ''.join(password)
            buyer_dict['hostname'] = hostname
            buyer_dict['username'] = username
            buyer_dict['id'] = ''.join(id)
            buyer_dict['nick'] = nick
            buyer_dict['email'] = email
            ##### Preparing dictionary for email confirmation #####
            email_confirm = {}
            email_confirm['username'] = username
            email_confirm['email'] = email
            email_confirm['code'] = ''.join(confirm_order)
            email_confirm['password'] = ''.join(password)
            email_confirm['hostname'] = hostname
            email_confirm['name'] = name
            email_confirm['surname'] = surname
            email_confirm['nick'] = nick
            email_confirm['id'] = ''.join(id)
            ##### Opening and reading customers file #####
            with open(buyers, 'r') as read_buyers:
                customers = json.loads(read_buyers.read())
                ##### Checking if customer has already ordered application #####
                try:
                    customers[username]['hostname']
                    irc.queueMsg(ircmsgs.privmsg(channel, "You have already bought this product \x02%s\x02. If you think this is some kind of error, or maybe you want to buy it again for the first time go to #ACCMS_HELP and state your issue." % nick))
                except:
                    try:
                        customers[username]['nick']
                        irc.queueMsg(ircmsgs.privmsg(channel, "You have already bought this product \x02%s\x02. If you think this is some kind of error, or maybe you want to buy it again for the first time go to #ACCMS_HELP and state your issue." % nick))
                    except:
                        ##### Preparing email message #####
                        email_username = "Your Username is: %s" % username
                        email_password = "Your Password is: %s" % ''.join(password)
                        email_id = "Your ID is: %s" % ''.join(id)
                        confirmation_code = "Your confirmation code is: %s" % ''.join(confirm_order)
                        bank_account = "You need to send 25 EUR on this account: \x02%s\x02, after that we will process your request and inform you weather you will get application or we will return your money back to you."
                        other_info = "Now go to IRC and in the same channel where you've requested application use command +confirm USERNAME CONFIRMATION-CODE to validate your email and confirm your order. Please write down all of those informations somewhere because you won't be able to use your application without them."
                        disclaimer = "If you didn't ordered anything please ignore this message and don't respond to it because nobody's reading those email. If you have any questions come to the #ACCMS_HELP and ask."
                        email_list = [email_username, email_password, email_id, '', '', '', confirmation_code, '', '', bank_account, '', '', other_info, '', disclaimer]
                        for option in email_list:
                            with open(email_folder, 'a') as write_email:
                                write_email.write(option)
                                write_email.write('\n')
                        ##### Creating SMTP server and sending email #####
                        ready_email = open(email_folder, 'r')
                        email_message = MIMEText(ready_email.read())
                        ready_email.close()
                        email_message['Subject'] = "Miner"
                        email_message['From'] = 'ACCMS'
                        email_message['To'] = email
                        mail_server = smtplib.SMTP()
                        mail_server.connect('smtp.krstarica.com', 25)
                        mail_server.ehlo()
                        mail_server.starttls()
                        mail_server.ehlo()
                        mail_server.login('stefanninic', 'ja1994')
                        mail_server.sendmail('stefanninic@krstarica.com', email, email_message.as_string())
                        mail_server.quit()
                        ##### Writing customer to file and replying with PM #####
                        customers[username] = buyer_dict
                        with open(buyers, 'w') as write_buyers:
                            write_buyers.write(json.dumps(customers))
                            irc.queueMsg(ircmsgs.privmsg(channel, "We have sent you confirmation email, please read it carefully and do everything what it says to do. If you have any questions come to #ACCMS_HELP and ask."))
                        ##### Clearing email message #####
                            with open(email_folder, 'w') as clear_email:
                                clear_email.write('')
                        ##### Opening and reading email confirmation dictionary #####
                            with open(waiting_confirm, 'r') as waiting_email:
                                email_validation = json.loads(waiting_email.read())
                                try:
                                    email_validation[username]['username']
                                    irc.queueMsg(ircmsgs.privmsg(channel, "You have already received email with confirmation code, use the \x02+confirm USERNAME CONFIRMATION-CODE\x02 to validate your email."))
                                except:
                                    try:
                                        email_validation[username]['email']
                                        irc.queueMsg(ircmsgs.privmsg(channel, "You have already received email with confirmation code, use the \x02+confirm USERNAME CONFIRMATION-CODE\x02 to validate your email."))
                                    except:
                                        email_validation[username] = email_confirm
                                        with open(waiting_confirm, 'w') as waiting_email:
                                            waiting_email.write(json.dumps(email_validation))
        else:
            irc.reply("You can't use this command anywhere else except on #ACCMS_REQUEST channel.")
    order = wrap(order, ['something', 'something', 'something', 'something'])

    def confirm(self, irc, msg, args, username, code):
        """<username> <code>

        Validate your email by typing username that you've used while ordering application and confirmation ID that you got in email after ordering application."""
        waiting_confirm = 'Bitcoin/Waiting_confirmation.json'
        confirmed_emails = 'Bitcoin/Confirmed_orders.json'
        channel = msg.args[0]
        if channel == '#ACCMS_REQUEST':
            ##### Reading file with waiting confirmations to check if that username is in it #####
            with open(waiting_confirm, 'r') as waiting_confirms:
                waiting_orders = json.loads(waiting_confirms.read())
                try:
                    waiting_orders[username]['code']
                    old_code = waiting_orders[username]['code']
                    if old_code == str(code):
                        ##### Reading confirmed emails and writing new entry for current user #####
                        with open(confirmed_emails, 'r') as emails_confirmed:
                            done_confirms = json.loads(emails_confirmed.read())
                            ##### Checking if this user has already confirmed his email #####
                            if username in done_confirms.keys():
                                irc.queueMsg(ircmsgs.privmsg(channel, "You have already confirmed your email. Please be patient while we process your request. If you have any questions you can always come to #ACCMS_HELP and ask."))
                            else:
                                ##### Making a new entry for done confirmations and updating this dictionary #####
                                done_confirms[username] = waiting_orders[username]
                                with open(confirmed_emails, 'w') as writing_confirmation:
                                    writing_confirmation.write(json.dumps(done_confirms))
                                    ##### Deleting username from waiting confirmations dictionary #####
                                    with open(waiting_confirm, 'r') as waiting_confirms:
                                        removing_orders = json.loads(waiting_confirms.read())
                                        del removing_orders[username]
                                        ##### Writing a new dictionary without the old username that has just confirmed his email #####
                                        with open(waiting_confirm, 'w') as updated_confirmations:
                                            updated_confirmations.write(json.dumps(removing_orders))
                                            irc.queueMsg(ircmsgs.privmsg(channel, "You have confirmed your email successfully, please be patient while we and the bank process your request/payment. If you have any questions feel free to come to #ACCMS_HELP and ask."))
                    else:
                        irc.queueMsg(ircmsgs.privmsg(channel, "You have mistyped your confirmation code, please double check it and then try again."))
                except:
                    irc.queueMsg(ircmsgs.privmsg(channel, "You didn't even ordered application, it means you can confirm anything, yet."))
        else:
            irc.queueMsg(ircmsgs.privmsg(channel, "This command is available only on #ACCMS_REQUEST channel."))
    confirm = wrap(confirm, ['something', 'int'])

    def req(self, irc, msg, args):
        """Takes no arguments

        Creates channel for you where you can request application."""
        nick = msg.nick
        irc.reply("Channel will now create and invite will be sent to you, please keep track of your Rizon tab (and every other tab, it all depends where your client sends invite message).")
        self.make_and_join_channel(irc, nick)
    req = wrap(req)

    def make_and_join_channel(self, irc, nick):
        channel_length = 15
        channel_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        channel_name_chars = []
        for character in xrange(channel_length):
            channel_name_chars.append(random.choice(channel_characters))
        channel_name = '#%s' % ''.join(channel_name_chars)
        irc.queueMsg(ircmsgs.join(channel_name))
        time.sleep(7)
        irc.queueMsg(ircmsgs.mode(channel_name, '+i'))
        self._invite(irc, nick, channel_name)

    def _invite(self, irc, nick, channel):
        irc.queueMsg(ircmsgs.invite(nick, channel))
        part_event = '%s-%s-part' % (channel, nick)
        schedule.addEvent(self._track_time_and_part, time.time() + 900, part_event, args=(irc, channel, nick))

    def _track_time_and_part(self, irc, channel, nick):
        reason = "Your time's up, for new request please contact my owner."
        irc.queueMsg(ircmsgs.kick(channel, nick, reason))
        irc.queueMsg(ircmsgs.part(channel))
Class = BitMine


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
