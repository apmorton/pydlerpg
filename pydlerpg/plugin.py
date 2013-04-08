from twisted.plugin import IPlugin
from zope.interface import implements

from pydlerpg.ipydlerpg import IPydlePlugin
from pydlerpg.mixins.attrdict import AttrDict, DefaultsMixin, RequiredsMixin
from pydlerpg.state import StateDict


class PydlePluginConfig(DefaultsMixin, RequiredsMixin, AttrDict):
    """Config dict for plugins"""
    pass


class PydlePluginState(StateDict):
    """State dict for plugins"""
    pass


class PydleBasePlugin(object):
    _loaded = False
    bot = None

    def load(self, bot, config=None, state=None):
        if self._loaded:
            raise RuntimeError('already loaded!')

        if not state:
            state = self._init_state()
        self.state = state
        if self.state is not None:
            self.bot._state[self.name] = self.state
            self.bot.sync_state()

        self.config = self._init_config(config)

        self._loaded = True
        self.bot = bot

        self.loaded()

    def unload(self):
        if not self._loaded:
            raise RuntimeError('not loaded!')

        self.unloading()

        self._loaded = False
        self.bot = None

    def loaded(self):
        """Called after plugin load"""
        pass

    def unloading(self):
        """Called just before plugin unload"""
        pass

    def _init_state(self):
        state_class = getattr(self, 'state_class', None)
        if state_class:
            return state_class()
        return None

    def _init_config(self, config):
        config_class = getattr(self, 'config_class', None)
        if not config:
            config = {}
        if config_class:
            return config_class(config)
        return None


class PydleIRCPlugin(PydleBasePlugin):
    """Pydle IRC Plugin

    Generate signals for the game logic by
    listening to irc events and commands
    """
    implements(IPlugin, IPydlePlugin)
    plugin_type = 'IRC'


class PydleGamePlugin(PydleBasePlugin):
    """Pydle Game plugin

    Handle the game logic by listening for
    signals sent by the core and other plugins
    """
    implements(IPlugin, IPydlePlugin)
    plugin_type = 'GAME'
