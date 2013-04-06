from pydlerpg.plugin import PydleGamePlugin
from pydlerpg.mixins.plugin import TickHookMixin

class TestPlugin(PydleGamePlugin, TickHookMixin):
    name = 'test-plugin'
    description = 'test plugin'
    
    def loaded(self):
        super(TestPlugin, self).loaded()
        self.lc = self.every(3, self.every_3_ticks)
    
    def unloading(self):
        super(TestPlugin, self).unloading()
    
    def every_3_ticks(self):
        print 'every 3 ticks!'

plugin = TestPlugin()