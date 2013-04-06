from pydlerpg.util import AttrDict, DefaultsMixin

class StateDict(DefaultsMixin, AttrDict):
    """AttrDict with defaults"""
    pass

class PydleUserState(StateDict):
    """Pydle user state
    
    represents the state of a single user in the game
    """
    _defaults = dict(
        name="",
        hostmask="*!*@*",
        admin=False,
        online=False,
        last_login=None,
        date_registered=None,
    )

class PydleRootState(StateDict):
    """Root Pydle state object
    
    Top of the state hierarchy
    """
    _defaults = dict(
        users=StateDict,
        
    )