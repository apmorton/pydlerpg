from zope.interface import Interface, Attribute

class IPydlePlugin(Interface):
    name = Attribute('unique identifier for plugin')
    description = Attribute('short description of plugin function')
    plugin_type = Attribute('game or irc plugin')
    _loaded = Attribute('Whether or not the plugin is loaded')
    
    def load(self, bot):
        """Load the plugin into the bot
        """
    
    def unload(self):
        """Unload the plugin from the bot
        """