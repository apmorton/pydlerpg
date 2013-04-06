from twisted.plugin import IPlugin
from zope.interface import implements

from pydlerpg.ipydlerpg import IPydlePlugin

class PydleBasePlugin(object):
    _loaded = False
    bot = None
    
    def load(self, bot):
        if self._loaded:
            raise RuntimeError('already loaded!')
        
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