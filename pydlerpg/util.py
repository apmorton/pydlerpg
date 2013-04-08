from datetime import datetime

from twisted.internet import task
from twisted.plugin import getPlugins

from pydlerpg.ipydlerpg import IPydlePlugin
from pydlerpg.state import PydleRootState, PydleUserState

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
    return [p for p in all_plugins() if p.plugin_type == plugin_type]


def update_root_state_from_config(s, config):
    for admin, mask in config.admins.iteritems():
        if admin not in s.users:
            s.users[admin] = PydleUserState(name=admin, hostmask=mask,
                                            admin=True,
                                            date_registered=datetime.now())
        elif s.users[admin].hostmask != mask:
            s.users[admin].hostmask = mask


def init_root_state_from_config(config):
        s = PydleRootState()
        update_root_state_from_config(s, config)

        return s


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
