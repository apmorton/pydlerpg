from twisted.internet import task
from twisted.plugin import getPlugins

from pydlerpg.ipydlerpg import IPydlePlugin
import pydlerpg.plugins

def all_plugins():
    plugins = getPlugins(IPydlePlugin, pydlerpg.plugins)
    return list(plugins)

def get_plugin_by_name(name):
    for plugin in all_plugins():
        if plugin.name == name:
            return plugin
    return None

def get_plugins_by_type(plugin_type):
    return [ p for p in all_plugins() if p.plugin_type == plugin_type ]

class AttrDict(dict):
    """Dictionary that allows attribute access"""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError
    
    def __setattr__(self, name, value):
        try:
            super(AttrDict, self).__setattr__(name, value)
        except AttributeError:
            self[name] = value

class TickClock(task.Clock, object):
    """A custom clock for plugin ticks
    """
    
    def __init__(self, interval=1):
        super(TickClock, self).__init__()
        self.interval = interval
        self.update_loop = task.LoopingCall(self.advance, 1)
    
    def start(self):
        self.update_loop.start(self.interval, False)
    
    def stop(self):
        self.update_loop.stop()