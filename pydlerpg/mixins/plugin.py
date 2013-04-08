from twisted.internet import reactor
from twisted.internet.task import LoopingCall


class SignalHookMixin(object):
    """Keep track of signal hooks and destroy them on unload
    """
    __sig = None

    def raise_signal(self, signal, *args, **kwargs):
        """proxy to easily raise signal"""
        self.bot.raise_signal(signal, *args, **kwargs)

    def hook_signal(self, signal, f):
        """hook a signal"""
        if not self.__sig:
            self.__sig = []

        self.__sig.append((signal, f))
        return self.bot.hook_signal(signal, f)

    def unhook_signal(self, signal, f):
        """unhook a signal"""
        if not self.__sig:
            self.__sig = []

        if (signal, f) in self.__sig:
            self.__sig.remove((signal, f))

        return self.bot.unhook_signal(signal, f)

    def unloading(self):
        """unhook any remaining signals"""
        if self.__sig:
            for (signal, f) in self.__sig:
                try:
                    self.bot.unhook_signal(signal, f)
                except ValueError:
                    pass
        super(SignalHookMixin, self).unloading()


class TickHookMixin(object):
    """Add functions to schedule based on ticks
    """
    __lcs = None
    __dcs = None

    def every(self, interval, f, *args, **kwargs):
        """Call f every interval ticks"""
        if not self.__lcs:
            self.__lcs = []

        tick = kwargs.pop('tick', True)
        call = LoopingCall(f, *args, **kwargs)

        if tick:
            call.clock = self.bot.tick

        call.start(interval, False)

        self.__lcs.append(call)

        return call

    def after(self, n, f, *args, **kwargs):
        """Call f after n ticks"""
        if not self.__dcs:
            self.__dcs = []

        tick = kwargs.pop('tick', True)
        if tick:
            func = self.bot.tick.callLater
        else:
            func = reactor.callLater

        call = func(n, f, *args, **kwargs)
        self.__dcs.append(call)

        return call

    def unloading(self):
        """Stop any pending calls"""
        if self.__lcs:
            for c in [c for c in self.__lcs if c.running]:
                c.stop()

        if self.__dcs:
            for c in [c for c in self.__dcs if not (c.cancelled or c.called)]:
                c.cancel()
        super(TickHookMixin, self).unloading()
