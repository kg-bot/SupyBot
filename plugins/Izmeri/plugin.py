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

    _penis_responses = ('ima penis od 6cm.', 'ima penis od 15cm.', 'ima penis od 24cm.', 'ima penis od 9cm.', 'ima penis od 18cm.',
                    'ima penis od 22cm.', 'ima penis od 14cm.', 'ima penis od 17cm.', 'ima penis od 4cm.', 'ima penis od 12cm.', 'ima penis od 13cm.', 'ima enormno veliki penis i da se sa njim nije zajebavati, deco cuvajte se, stigo kuronja u grad')

    _sike_odgovori = ('su ove sise velicine zrna graska.', 'su ove sise velicine decije glave.', 'da su ove sise taman kako treba.', 'da ova osoba uopste nema sisa.', 'mozes jednu u usta drugu pod glavu.', 'nije nasao nista, jad i beda.', 'ova osoba ima rak desne dojke.')

    def penis(self, irc, msg, args, text, channel):
        """<nick>

        Meri velicinu necijeg penisa.
        """

        irc.reply(('KG-Bot vadi svoju strucnu spravu za merenje penisa, skida gace \x02%s\x02, meri i dolazi do zakljucka da ova osoba \x02%s\x02') %
        (text, utils.iter.choice(self._penis_responses)))
    penis = wrap(penis, ['nickInChannel', 'channel'])

    def sike(self, irc, msg, args, name, channel):
        """<nick>

        Meri velicinu siki. xD"""
        irc.reply("KG-Bot vadi svoju strucnu spravu za merenje sisica, zaviruje \x02%s\x02 u grudjnak i zakljucuje da \x02%s\x02" % (name, utils.iter.choice(self._sike_odgovori)))
    sike = wrap(sike, ['nickInChannel', 'channel'])
     
Class = Izmeri


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
