import sys

from yaml import load
from twisted.internet import reactor
from twisted.python import log

from pydlerpg.bot import PydleBot
from pydlerpg.config import ConfigDict
from pydlerpg.irc import PydleIRCBotFactory, PydleIRCBot

if __name__ == '__main__':
    # TODO: use argparse here
    if len(sys.argv) < 2:
        print "usage: {} /path/to/config.yml".format(sys.argv[0])
        sys.exit(1)

    log.startLogging(sys.stdout)
    config = load(open(sys.argv[1], 'r'))
    config = ConfigDict(config)

    bot = PydleBot(config)
    # bot.tick.start()

    bot.load_state_from_config()
    bot.load_plugins_from_config()

    irc = PydleIRCBot(bot)

    f = PydleIRCBotFactory(irc)
    (host, port) = f.getRandomServer()

    log.msg("Connecting to {}/{}".format(host, port))
    reactor.connectTCP(host, port, f)
    reactor.run()
