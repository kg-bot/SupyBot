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
import random
import time
import re
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Izmeri')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Izmeri(callbacks.Plugin):
    """Add the help for "@plugin help Izmeri" here
    This should describe *how* to use this plugin."""
    pass
	
    _responses = ('ima penis od 6cm.', 'ima penis od 15cm.', 'ima penis od 24cm.', 'ima penis od 9cm.', 'ima penis od 18cm.',
                    'ima penis od 22cm.', 'ima penis od 14cm.', 'ima penis od 17cm.', 'ima penis od 4cm.', 'ima penis od 12cm.', 'ima penis od 13cm.')

    def izmeri(self, irc, msg, args, text, channel):
	    """[<nick>]
	 
        Meri velicinu necijeg penisa.
        """
        
            irc.reply(('KG-Bot vadi svoju strucnu spravu za merenje penisa, skida gace %s, meri i dolazi do zakljucka da on %s') %
                (text, utils.iter.choice(self._responses)))
    izmeri = wrap(izmeri, ['text', 'inChannel'])
	 
Class = Izmeri


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
