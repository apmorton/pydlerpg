from twisted.python import log

from pydlerpg.plugin import PydleIRCPlugin
from pydlerpg.mixins.plugin import SignalHookMixin

RESP = {
    'user:level': '{0.name} has reached level {0.level}! next level in {0.pretty_ttl}',
}


class IRCChatterPlugin(SignalHookMixin, PydleIRCPlugin):
    name = 'irc:chatter'
    description = 'announce events in the game to the main channel'

    def loaded(self):
        self.bot.hook_signal_namespace('game', self._handle_game_signal)

    def _handle_game_signal(self, signal, *args, **kwargs):
        signal = signal.split(':', 1).pop()
        responses = RESP.get(signal, [])
        if isinstance(responses, basestring):
            responses = [responses]

        for resp in responses:
            msg = resp.format(*args, **kwargs)
            self.bot.irc.say(self.bot.config.channel, msg,
                             length=self.bot.config.msg_length)

plugin = IRCChatterPlugin()
