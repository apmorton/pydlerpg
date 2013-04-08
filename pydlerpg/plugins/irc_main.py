from twisted.python import log

from pydlerpg.plugin import PydleIRCPlugin
from pydlerpg.mixins.plugin import SignalHookMixin


class IRCMainPlugin(SignalHookMixin, PydleIRCPlugin):
    name = 'irc:main'
    description = 'parse irc events into game events'

    def loaded(self):
        users = {}
        self.hook_signal('irc:me:joined', self._handle_me_joined)
        self.hook_signal('irc:chan:names', self._handle_chan_names)

    def _handle_chan_names(self, channel, nicks):
        if channel != self.bot.config.channel:
            return

        log.msg(nicks)

    def _handle_me_joined(self, channel):
        if channel == self.bot.config.channel:
            self.bot.irc.names(channel)
            self.raise_signal('game:chan:join')

plugin = IRCMainPlugin()
