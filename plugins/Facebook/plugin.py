###
# Copyright (c) 2013, KG-Bot
# All rights reserved.
#
#
###
import re
import json

import string

import supybot.conf as conf
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    from supybot.i18n import internationalizeDocstring
    _ = PluginInternationalization('Facebook')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x
    internationalizeDocstring = lambda x:x

def flatten_subdicts(dicts, flat=None):
    """Change dict of dicts into a dict of strings/integers. Useful for
    using in string formatting."""
    if flat is None:
        flat = {}
    if isinstance(dicts, list):
        for key, value in dicts.items():
            if isinstance(value, dict):
                value = dict(flatten_subdicts(values))
                for subkey, subvalue in value.items():
                    flat['%s__%s' % (key, value)] = subvalue
            else:
                flat[key] = value
        return flat
    else:
        return dicts

class Template(string.Template):
    idpattern = r'[_a-z0-9]+'

class Facebook(callbacks.Plugin):
    """Add the help for "@plugin help Facebook" here
    This should describe *how* to use this plugin."""
    threaded = True

    def _get(self, irc, name):
        token = conf.supybot.plugins.Facebook.token()
        if not token:
            irc.error(_('There is no token, ask the owner to add one'),
                    Raise=True)
        try:
            base = 'https://graph.facebook.com/%s?fields=id,link,name&access_token=%s'
            data = json.load(utils.web.getUrlFd(base %
                (name, token)))
            return data
        except:
            irc.error(_('No cush user exist'), Raise=True)

    def _advinfo(self, irc, msg, args, format_, name):
        """<format> <name>

        Returns info about <name>"""
        mu = flatten_subdicts(self._get(irc, name), flat={
                'favorite__teams': 'None',
                'favorite__teams__name': 'None',
                })
        repl = lambda x:Template(x).safe_substitute(mu)
        irc.replies(map(repl, format_.split('\\n')))
    advinfo = wrap(_advinfo, ['something', 'something'])

    def _gen(format_, name, doc):
        format_ = re.sub('[ \n]+', ' ', format_)
        def f(self, irc, msg, args, *ids):
            self._advinfo(irc, msg, args, format_, *ids)
        f.__doc__ = """<name>

        %s""" % doc
        return wrap(f, ['something'], name=name)

    info = _gen("""Name: $name, ID: $id, Middle name: $middle__name, Teams: $favorite__teams__name. """,
    'info',
    'Gives <name> name and id.')


Class = Facebook


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
