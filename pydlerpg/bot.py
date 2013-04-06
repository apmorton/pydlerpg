from pydlerpg import util

class PydleBot(object):
    def __init__(self, config):
        self.tick = util.TickClock(config.tick_interval)
        self.config = config
        self.signals = {}
        self.plugins = {}
    
    def load_plugins_from_config(self):
        for plugin in self.config.plugins:
            self.load_plugin(plugin)
    
    def load_plugin(self, name):
        if name in self.plugins.keys():
            raise ValueError('plugin {} already loaded'.format(name))
        
        plugin = util.get_plugin_by_name(name)
        if plugin is None:
            raise ValueError('plugin {} not found'.format(name))
        
        plugin.load(self)
        self.plugins[name] = plugin
    
    def unload_plugin(self, name):
        try:
            plugin = self.plugins.pop(name)
        except KeyError:
            raise ValueError('plugin {} not loaded'.format(name))
        
        plugin.unload()
    
    def hook_signal(self, signal, f):
        """hook a signal"""
        if signal not in self.signals.keys():
            self.signals[signal] = []
        
        self.signals[signal].append(f)
    
    def unhook_signal(self, signal, f):
        """unhook a signal"""
        if signal not in self.signals.keys():
            msg = 'the signal "{}" does not have any registered hooks'
            raise ValueError(msg.format(signal))
        
        if f not in self.signals[signal]:
            msg = 'the function "{}" is not registered to signal "{}"'
            raise ValueError(msg.format(f, signal))
        
        self.signals[signal].remove(f)
    
    def raise_signal(self, signal, *args, **kwargs):
        """raise a signal for all registered hooks"""
        try:
            handlers = self.signals[signal]
        except KeyError:
            return
        
        for handler in handlers:
            handler(*args, **kwargs)