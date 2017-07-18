###
# Copyright (c) 2013, KG-Bot
# All rights reserved.
#
#
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Mass')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Mass(callbacks.Plugin):
    """Add the help for "@plugin help Mass" here
    This should describe *how* to use this plugin."""
    pass

    def mass(self, irc, msg, args, poruka):
        """<message>

        This will ping everyone on channel with desired message."""
        poruka = poruka or None
        nick = msg.nick
        channel = msg.args[0]
        try:
            opovi = irc.state.channels[channel].ops
            users = ', '.join(irc.state.channels[channel].users)
            pr = poruka or users
        except KeyError:
            irc.reply("This command is available only in channel, not in my private list, I won't hasittate to disable this command for you if you try to use it in my PM again.")
            return
        if channel.startswith('#'):
            if nick not in opovi:
                irc.reply("You can't use this command because you don't have OP in this channel")
                return
            if poruka is None:
                irc.reply(users)
                return
            else:
                irc.reply('%s' % (users))
                irc.reply('\x0310>>>>\x03\x02\x034%s\x03\x02\x0310<<<<\x03' % (poruka))
        else:
            irc.reply("This command is available only in channel, not in my private list, I won't hasittate to disable this command for you if you try to use it in my PM again.")
    mass = wrap(mass, [optional('text')])

    def sayme(self, irc, msg, args, chan):
        """None

        Nooo"""
        usrs = irc.state.channels[chan].users
        irc.reply(usrs)
    sayme = wrap(sayme, ['something'])


Class = Mass


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
