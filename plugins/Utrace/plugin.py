###
# Copyright (c) 2013, nyuszika7h
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
    _ = PluginInternationalization('Utrace')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Utrace(callbacks.Plugin):
    """Add the help for "@plugin help Utrace" here
    This should describe *how* to use this plugin."""
    pass


Class = Utrace


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
