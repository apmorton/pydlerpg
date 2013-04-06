from twisted.internet.task import LoopingCall

class TickHookMixin(object):
    """Add functions to schedule based on ticks
    """
    __lcs = None
    __dcs = None
    
    def every(self, interval, f, *args, **kwargs):
        """Call f every interval ticks"""
        if not self.__lcs:
            self.__lcs = []
        
        call = LoopingCall(f, *args, **kwargs)
        call.clock = self.bot.tick
        call.start(interval, False)
        
        self.__lcs.append(call)
        
        return call
    
    def after(self, n, f, *args, **kwargs):
        """Call f after n ticks"""
        if not self.__dcs:
            self.__dcs = []
            
        call = self.bot.tick.callLater(n, f, *args, **kwargs)
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