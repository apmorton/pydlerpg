from pydlerpg.plugin import PydleIRCPlugin
from pydlerpg.mixins.plugin import SignalHookMixin


class IRCMainPlugin(SignalHookMixin, PydleIRCPlugin):
    name = 'irc:main'
    description = 'parse irc events into game events'

    def loaded(self):
        self.hook_signal('irc:me:joined', self._handle_me_joined)

    def _handle_me_joined(self, channel):
        if channel == self.bot.config.channel:
            self.raise_signal('game:chan:join')

plugin = IRCMainPlugin()
