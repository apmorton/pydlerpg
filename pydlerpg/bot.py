import shelve

from twisted.internet import reactor
from twisted.python import log

from pydlerpg import util


class PydleBot(object):
    irc = None
    _state = None

    def __init__(self, config):
        self.tick = util.TickClock(config.tick_interval)
        self.config = config
        self.signals = {}
        self.namespaces = {}
        self.plugins = {}

        self.hook_signal('core:sync', self.sync_state)

    @property
    def state(self):
        return self._state['root']

    def load_state_from_config(self):
        self._state = shelve.open(self.config.state, flag='c',
                                  protocol=2, writeback=True)

        if not self._state:
            s = util.init_root_state_from_config(self.config)
            self._state['root'] = s
        else:
            util.update_root_state_from_config(self.state, self.config)

        self.sync_state()

    def sync_state(self):
        self._state.sync()

    def load_plugins_from_config(self):
        for plugin in self.config.plugins.keys():
            config = self.config.plugins[plugin]
            state = self._state.get(plugin, None)
            self.load_plugin(plugin, config, state)

    def load_plugin(self, name, config=None, state=None):
        if name in self.plugins.keys():
            raise ValueError('plugin {} already loaded'.format(name))

        plugin = util.get_plugin_by_name(name)
        if plugin is None:
            raise ValueError('plugin {} not found'.format(name))

        plugin.load(self, config, state)
        self.plugins[name] = plugin

    def unload_plugin(self, name):
        try:
            plugin = self.plugins.pop(name)
        except KeyError:
            raise ValueError('plugin {} not loaded'.format(name))

        plugin.unload()

    def hook_signal_namespace(self, namespace, f):
        """hook an entire signal namespace"""
        if namespace not in self.namespaces.keys():
            self.namespaces[namespace] = []

        self.namespaces[namespace].append(f)

    def unhook_signal_namespace(self, namespace, f):
        """unhook an entire signal namespace"""
        if namespace not in self.namespaces.keys():
            msg = 'the namespace "{}" does not have any registered hooks'
            raise ValueError(msg.format(namespace))

        if f not in self.namespaces[namespace]:
            msg = 'the function "{}" is not registered to namespace "{}"'
            raise ValueError(msg.format(f, namespace))

        self.namespaces[namespace].remove(f)

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
        handlers = self.signals.get(signal, [])
        nshandlers = []

        ns = signal.split(':')
        while len(ns) > 1:
            ns.pop()
            namespace = ':'.join(ns)
            nshandlers.extend(self.namespaces.get(namespace, []))

        if not (handlers or nshandlers):
            log.msg("signal ignored: {}".format(signal))
            return

        log.msg('signal raised: {}'.format(signal))

        for handler in handlers:
            reactor.callLater(0, handler, *args, **kwargs)

        for handler in nshandlers:
            reactor.callLater(0, handler, signal, *args, **kwargs)
