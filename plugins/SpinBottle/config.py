###
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012, nyuszika7h <nyuszika7h@cadoth.net>
#
# Licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0
# Unported License <https://creativecommons.org/licenses/by-nc-sa/3.0/>.
###

import supybot.conf as conf
import supybot.registry as registry

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('SpinBottle', True)


SpinBottle = conf.registerPlugin('SpinBottle')
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(SpinBottle, 'someConfigVariableName',
#     registry.Boolean(False, _("""Help for someConfigVariableName.""")))
conf.registerGroup(SpinBottle, 'spin')
conf.registerGlobalValue(conf.supybot.plugins.SpinBottle.spin,
    'requireCapability', registry.String('', ("""Determines what capability
    (if any) the bot should require people trying to use this command to
    have.""")))

conf.registerGroup(SpinBottle, 'randspin')
conf.registerGlobalValue(conf.supybot.plugins.SpinBottle.randspin,
    'requireCapability', registry.String('', ("""Determines what
    capability (if any) the bot should require people trying to use this command
    to have.""")))

conf.registerGroup(SpinBottle, 'forcespin')
conf.registerGlobalValue(conf.supybot.plugins.SpinBottle.forcespin,
    'requireCapability', registry.String('', ("""Determines what
    capability (if any) the bot should require people trying to use this
    command to have.""")))

conf.registerGroup(SpinBottle, 'forcebottle')
conf.registerGlobalValue(conf.supybot.plugins.SpinBottle.forcebottle,
    'requireCapability', registry.String('', ("""Determines what
    capability (if any) the bot should require people trying to use this
    command to have.""")))


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
