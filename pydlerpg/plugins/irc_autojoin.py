from pydlerpg.plugin import PydleIRCPlugin
from pydlerpg.mixins.plugin import SignalHookMixin


class AutoJoinPlugin(SignalHookMixin, PydleIRCPlugin):
    name = 'irc:auto-join'
    description = 'automatically join and rejoin main channel'

    def loaded(self):
        self.hook_signal('irc:me:signed-on', self.signedOn)

    def signedOn(self):
        self.joinChannel(self.bot.config.channel)

    def joinChannel(self, channel, key=None, verify=True):
        # TODO: verify we actually join
        self.bot.irc.join(channel, key)

plugin = AutoJoinPlugin()
