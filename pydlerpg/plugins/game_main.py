from twisted.python import log

from pydlerpg.plugin import PydleGamePlugin, PydlePluginConfig
from pydlerpg.mixins.plugin import SignalHookMixin, TickHookMixin


class GameConfig(PydlePluginConfig):
    _defaults = dict(
        level_base=600,
        level_factor=1.16
    )


class GamePlugin(SignalHookMixin, TickHookMixin, PydleGamePlugin):
    name = 'game:main'
    description = 'the main game plugin'

    config_class = GameConfig

    def loaded(self):
        self.hook_signal('game:user:level', self._handle_user_level)
        self.hook_signal('game:user:penalize', self._handle_user_penalize)
        self.every(1, self._handle_ttl_ticks)
        # sync every 10 seconds (not ticks)
        self.every(10, self.raise_signal, 'core:sync', tick=False)

    def _handle_user_level(self, user):
        user.level += 1
        # TODO: use configuration options
        user.ttl += int(self.config.level_base *
                        (self.config.level_factor ** user.level))

    def _handle_user_penalize(self, user, time, message):
        user.ttl += time

    def _handle_ttl_ticks(self):
        for user in self.bot.state.users.values():
            if user.online:
                user.ttl -= 1
                # log.msg('{} {}'.format(user.name, user.ttl))
                if user.ttl == 0:
                    self.raise_signal('game:user:level', user)

plugin = GamePlugin()
