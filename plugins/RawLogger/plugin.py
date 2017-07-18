###
# Copyright (c) 2002-2005, Jeremiah Fincher
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

import supybot.conf as conf
import supybot.world as world
import supybot.irclib as irclib

###
# RawLogger: Logs the *raw* IRC messages.
###
class RawLogger(irclib.IrcCallback):
    """Logs raw IRC messages.  This was useful back when Supybot was
    originally being written, and the developers needed a corpus of raw IRC
    messages for their tests, but now it's less than useful."""
    def __init__(self, irc):
        self.fd = file(conf.supybot.directories.log.dirize('raw.log'), 'a')
        self._flush = self.fd.flush
        world.flushers.append(self._flush)

    def die(self):
        if self._flush in world.flushers:
            world.flushers.remove(self._flush)
        self.fd.close()

    def inFilter(self, irc, msg):
        self.fd.write(str(msg))
        return msg

    def outFilter(self, irc, msg):
        self.fd.write(str(msg))
        return msg


Class = RawLogger
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
