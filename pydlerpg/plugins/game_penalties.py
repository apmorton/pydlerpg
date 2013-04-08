from pydlerpg.plugin import PydleGamePlugin, PydlePluginConfig
from pydlerpg.mixins.plugin import SignalHookMixin, TickHookMixin


class GamePenaltiesConfig(PydlePluginConfig):
    _defaults = dict(
        factor=1.14,
        nick=30,
        part=200,
        quit=20,
        kick=250
    )


class GamePenaltiesPlugin(SignalHookMixin, TickHookMixin, PydleGamePlugin):
    name = 'game:penalties'
    description = 'penalize users for irc actions'

    config_class = GamePenaltiesConfig

    def loaded(self):
        self.hook_signal('game:user:nick', self.nick)
        self.hook_signal('game:user:part', self.part)
        self.hook_signal('game:user:quit', self.quit)
        self.hook_signal('game:user:kick', self.kick)
        self.hook_signal('game:user:spoke', self.spoke)

    def penalize(self, user, level, message):
        time = int(level * (self.config.factor ** user.level))
        self.raise_signal('game:user:penalize', user, time, message)

    def nick(self, user):
        self.penalize(user, self.config.nick, "changing nick")

    def part(self, user):
        self.penalize(user, self.config.part, "parting")

    def quit(self, user):
        self.penalize(user, self.config.quit, "quitting")

    def kick(self, user):
        self.penalize(user, self.config.kick, "being kicked")

    def spoke(self, user, message):
        level = len(message)
        self.penalize(user, level, "speaking")

plugin = GamePenaltiesPlugin()
