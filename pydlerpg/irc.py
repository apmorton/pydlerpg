from random import choice

from twisted.internet import protocol, reactor
from twisted.words.protocols import irc


class PydleIRCBotFactory(protocol.ReconnectingClientFactory, object):
    """A singleton factory for PydleIRCBot"""

    def __init__(self, irc):
        self.irc = irc
        self.irc.factory = self

    def buildProtocol(self, addr):
        return self.irc

    def getRandomServer(self):
        server = choice(self.irc.bot.config.servers).split('/')
        return (server[0], int(server[1]))

    def retry(self, connector=None):
        if connector is None:
            if self.connector is None:
                raise ValueError("no connector to retry")
            else:
                connector = self.connector

        (host, port) = self.getRandomServer()
        connector.host = host
        connector.port = port

        super(PydleIRCBotFactory, self).retry(connector)

calls_to_signal = dict(
    # server actions
    created='irc:server:created',
    yourHost='irc:server:host',
    myInfo='irc:server:my',
    luserClient='irc:server:user-count',
    bounce='irc:server:bounce',
    isupport='irc:server:isupport',
    luserChannels='irc:server:channel-count',
    luserOp='irc:server:op-count',
    luserMe='irc:server:me',

    # actions directly related to this client
    privmsg='irc:me:privmsg',
    joined='irc:me:joined',
    left='irc:me:left',
    noticed='irc:me:noticed',
    modeChanged='irc:me:mode-changed',
    pong='irc:me:pong',
    signedOn='irc:me:signed-on',
    kickedFrom='irc:me:kicked',
    nickChanged='irc:me:nick',

    # actions observed that target others
    userJoined='irc:user:joined',
    userLeft='irc:user:left',
    userQuit='irc:user:quit',
    userKicked='irc:user:kicked',
    action='irc:user:action',
    userRenamed='irc:user:nick',


    topicUpdated='irc:chan:topic'
)


class PydleIRCBot(irc.IRCClient, object):
    """IRC bot for PydleRPG"""

    def __init__(self, bot):
        self.bot = bot
        self.bot.irc = self

        # set parameters from config
        self.nickname = bot.config.nickname

        # setup all the signal calls
        for call, signal in calls_to_signal.iteritems():
            self._raise_signal_call(call, signal)

        self._namescallback = {}

    def _raise_signal_call(self, call, signal):
        old_func = getattr(self, call)

        def inner_func(*args, **kwargs):
            old_func(*args, **kwargs)
            self.bot.raise_signal(signal, *args, **kwargs)
        setattr(self, call, inner_func)

    def names(self, channel):
        channel = channel.lower()
        if channel not in self._namescallback:
            self._namescallback[channel] = []

        self.sendLine('NAMES {}'.format(channel))

    def signedOn(self):
        self.factory.resetDelay()
        reactor.callLater(1, self.bot.tick.start)

    def irc_RPL_NAMREPLY(self, prefix, params):
        channel = params[2].lower()
        nicklist = params[3].split(' ')

        if channel not in self._namescallback:
            return

        self._namescallback[channel].extend(nicklist)

    def irc_RPL_ENDOFNAMES(self, prefix, params):
        channel = params[1].lower()
        if channel not in self._namescallback:
            return

        nicklist = self._namescallback[channel]
        self.bot.raise_signal('irc:chan:nicks', channel, nicklist)

        self._namescallback.remove(channel)
