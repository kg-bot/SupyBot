###
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012, nyuszika7h <nyuszika7h@cadoth.net>
#
# Licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0
# Unported License <https://creativecommons.org/licenses/by-nc-sa/3.0/>.
###

# Supybot imports
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

# Standard library imports
import time
import random

class SpinBottle(callbacks.Plugin):
    """This plugin is for spinning bottles! ;)"""

    def __init__(self, irc):
        self.__parent = super(SpinBottle, self)
        self.__parent.__init__(irc)

    def getNicks(self, irc, channel):
        """Returns a list of people who are currently joined to a channel."""
        return list(irc.state.channels[channel].users)

    def randomNick(self, irc, channel):
        """Returns a random nick from a channel."""
        # This might give more random numbers.
        random.seed(time.ctime())
        return random.choice(self.getNicks(irc, channel))

    def spin(self, irc, msg, args):
        """takes no arguments

        Spins a bottle from you.
        """
        channel = msg.args[0]

        source = msg.nick
        target = self.randomNick(irc, channel)

        irc.reply(('%s spins the bottle and it lands on... %s! Enjoy. ;)') %
            (source, target))
    spin = wrap(spin)

    def randspin(self, irc, msg, args):
        """takes no arguments

        Makes the bot spin a bottle for a random person.
        """
        channel = msg.args[0]
        target = self.randomNick(irc, channel)

        irc.reply(('I spin the bottle and it lands on... %s! YES!!!! :D <3') %
            target)
    randspin = wrap(randspin)

    def forcespin(self, irc, msg, args, source):
        """<source nick>

        Forces <source nick> to spin a bottle.
        """
        channel = msg.args[0]
        target = self.randomNick(irc, channel)

        irc.reply(('%s spins the bottle and it lands on... %s! Enjoy. ;)') %
            (source, target))
    forcespin = wrap(forcespin, ['nickInChannel'])

    def forcebottle(self, irc, msg, args, source, target):
        """<source nick> <target nick>

        Forces <source nick> to spin a bottle which will land on <target nick>.
        """
        irc.reply(('%s spins the bottle and it lands on... %s! Enjoy. ;)') %
            (source, target))
    forcebottle = wrap(forcebottle, ['nickInChannel', 'nickInChannel'])
        
Class = SpinBottle


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
