###
# Copyright (c) 2010, Julian Aloofi
#
#    This file is part of supybot-werewolf.
#
#    supybot-werewolf is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    supybot-werewolf is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with supybot-werewolf.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
###

import supybot.conf as conf
import supybot.registry as registry

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Werewolf', True)
    Werewolf = conf.registerPlugin('Werewolf')
    
    #conf.registerGlobalValue(Werewolf, 'manage_voices',
    #registry.Boolean('', """Determines whether the bot should handle voices"""))

    # This is where your configuration variables (if any) should go.  For example:
    # conf.registerGlobalValue(Werewolf, 'someConfigVariableName',
    #     registry.Boolean(False, """Help for someConfigVariableName."""))

    #if yn("""If the bot is operator in a channel, he can manage voices of the 
    #participating players, so they can't speak when they're dead.
    #Would you like the bot to manage voices when he can?""", default=False):
    #    Werewolf.manage_voices.setValue(True)

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
