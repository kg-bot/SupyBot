###
# Copyright (c) 2015, KG-Bot
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
import supybot.ircmsgs as ircmsgs
import supybot.schedule as schedule
import supybot.conf as conf

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('RequestBot')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class RequestBot(callbacks.Plugin):
    """Plugin is used to automate bot requests for some channel."""
    threaded = True
    
    def __init__(self):
        self.__parent = super(RequestBot, self)
        self.__parent.__init__(irc)
        self.dailyChecksInterval = conf.supybot.plugins.RequestBot.dailyCheckInterval()
        self.stopDailyCheck = conf.supybot.plugins.RequestBot.stopDailyCheck()
        self.numberOfChecks = conf.supybot.plugins.RequestBot.numberOfChecks()
        self.numberOfValidUsers = conf.supybot.plugins.RequestBot.numberOfValidUsers()
    
    def _logError(self, message):
        with open("local\log.txt", "a") as logFile:
            logFile.write("\n")
            logFile.write(message)
    
    def _checkChannelBan(self, channel):
        try:
            with open("plugins/RequestBot/local/channelBans.json", "r") as bans:
                banList = json.loads(bans.read())
                if channel.lower() not in banList.keys():
                    return "Valid"
                else:
                    return "Banned"
        except Exception as e:
            today_date = datetime.datetime.today().strftime("[%Y-%m-%d %H:%M:%S]")
            self._logError("%s - %s" % (today_date, str(e)))
            return "Error"
        
    def _checkRequesterBan(self, nick):
        try:
            with open("plugins/RequestBot/local/nickBans.json", "r") as nicks:
                banList = json.loads(nicks.read())
                if nick.lower() not in banList.keys():
                    return "Valid"
                else:
                    return "Banned"
        except Exception as e:
            today_date = datetime.datetime.today().strftime("[%Y-%m-%d %H:%M:%S]")
            self._logError("%s - %s" % (today_date, str(e)))
            return "Error"
        
    def _populateNicks(self, users):
        with open("plugins/RequestBot/local/invalidNicks.json", "r") as nicks:
            invalidNicks = json.loads(nicks.read())
        numberOfInvalidUsers = 0
        for user in users:
            for nick in invalidNicks:
                if user.lower() == nick:
                    numberOfInvalidUsers += 1
        numberOfValidUsers = len(users) - numberOfInvalidUsers
        if numberOfValidUsers >= self.numberOfValidUsers:
            return "Valid"
        else:
            return "Invalid"
        
    def _getDailyChecks(self, channel):
        with open("plugins/RequestBot/local/dailyChecks.json", "r") as dailyChecks:
            channels = json.loads(dailyChecks.read())
            if channels != "{}" and channel in channels.keys():
                return channels
            else:
                return "Error"
        
    def _dailyCheckOfUsers(self, irc, msg, adminPlugin, channel, eventName):
        numberOfChecks = self._getDailyChecks(channel)
        if numberOfChecks <= self.numberOfChecks: #TODO Change this because numberOfChecks will return dict of items
            if channel in irc.state.channels:
                users = irc.state.channels[channel].users
                validNicks = self._populateNicks(users)
                if validNicks == "Invalid":
                    adminPlugin.part(irc, msg, [channel, partMsg])
        
    def _channelState(self, irc, msg, nick, channel, adminPlugin):
        """Collects users from <channel> and determines if <nick> is owner or admin"""
        channels = irc.state.channels
        if channel in channels:
            users = irc.state.channels[channel].users
            # This checks number of valid users on channel
            validNicks = self._populateNicks(users)
            if validNicks == "Valid":
                owners = irc.state.channels[channel].owners
                # If owners are not empty that means ownermode is set and user must have +q
                # mode to request bot
                if len(owners) != 0:
                    if nick in owners:
                        eventName = "%s_RequestBot_dailyChecks" % channel
                        stopEventName = "%s_RequestBot_stopDailyChecks" % channel
                        # We must schedule it this way because we can't pass args in schedule...
                        def startDailyChecks():
                            # We are checking channel users for few days because one might try
                            # to bring a lot of users when he requests bot and later those users
                            # will part channel and never come back again
                            self._dailyCheckOfUsers(irc, msg, adminPlugin, channel, eventName)
                        # We're scheduling this to be run few times a day for few days and at the last
                        # time we're going to check if there where minimum users on the channel
                        # for most of the time
                        # TODO: Implement last check
                        schedule.addPeriodicEvent(startDailyChecks, self.dailyChecksInterval, eventName, now=False)
                        def stopDailyChecks():
                            # We must schedule it here because if we do it elswhere we won't be able to
                            # access new state of scheduler which holds reference to our scheduled event
                            schedule.removeEvent(eventName)
                        schedule.addEvent(stopDailyChecks, time.time() + self.stopDailyCheck, stopEventName)
                        greetMsg = "Hi, I've been assigned here thanks to %s. If you have any questions use +list or come to #KG-Bot and ask." % nick
                        irc.queueMsg(ircmsgs.privmsg(channel, greetMsg))
                    else:
                        partMsg = "You're not owner (with +q set) so you can't have me in here."
                        irc.queueMsg(ircmsgs.privmsg(channel, partMsg))
                        adminPlugin.part(irc, msg, [channel, partMsg])
                # If there are no owners with +q mode set we're not going to allow admins or ops
                # to request bot, we're forcing players to use ownermode and +q so only true channel owner
                # can request bot (you never know what admins can try to do)
                else:
                    partMsg = "There are no owners in here (with +q set)."
                    irc.queueMsg(ircmsgs.privmsg(channel, partMsg))
                    adminPlugin.part(irc, msg, [channel, partMsg])
            else:
                partMsg = "You don't have enough users in here."
                irc.queueMsg(ircmsgs.privmsg(channel, partMsg))
                adminPlugin.part(irc, msg, [channel, partMsg])
        # This should never happen, maybe only if bot is kicked from channel before
        # scheduled event for this command has been executed
        else:
            partMsg = "There was something strange internally. Please notify my owner about this."
            irc.queueMsg(ircmsgs.privmsg(channel, partMsg))
            adminPlugin.part(irc, msg, [channel, partMsg])
    
    
    
    def request(self, irc, msg, args, channel, reason):
        """<channel> - channel name for which you make request, <reason> - reason why do you want bot (it must be some good reason, not some bullshit)
        
        Request bot for <channel>, you must specify <reason> why do you want it."""
        # TODO: Before anything happens we should check if <channel> is valid IRC channel name
        # because if it's not we won't be able to join it, collect irc.state and our code will
        # probably brake in the unwanted manner
        
        #TODO: If we're already on channel nothing should be done and user should be
        # presented with explanation (we still have to implement that in our code)"""
        nick = msg.nick
        isChannelBanned = self._checkChannelBan(channel)
        # TODO: change this because this will probably return dict of more info about ban
        if isChannelBanned == "Valid":
            isRequesterBanned = self._checkRequesterBan(nick)
            # TODO: Change this because this will probably behave like channel ban and will return dict
            if isRequesterBanned == "Valid":
                # We're doing it this way because it's much more easier than trying to reimplement
                # admin join function with all those network, group, et. stuff
                adminPlugin = irc.getCallback("Admin")
                adminPlugin.join(irc, msg, [channel.lower()])
                # We must schedule this command because when bot joins some channel it neads few seconds
                # to collect irc.state and we can't access those right after the join
                schedule.addEvent(self._channelState, time.time() + 5, args=[irc, msg, nick, channel, adminPlugin])
            elif isRequesterBanned == "Banned":
                irc.reply("You can't request bot becuase you're on ban list.")
            else:
                irc.reply("There was some ugly internal error. Please try again and notify my owner about this.")
        elif isChannelBanned == "Banned":
            irc.reply("This channel is banned and you can't request bot for it.")
        else:
            irc.reply("There was some ugly internal error. Please try again and notify my owner about this.")
    request = wrap(request, ["channel", "something"])
    


Class = RequestBot


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
