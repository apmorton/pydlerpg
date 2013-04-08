from datetime import timedelta

from pydlerpg.mixins.attrdict import AttrDict, DefaultsMixin


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
        online=True,
        last_login=None,
        date_registered=None,
        ttl=600,
        level=0
    )

    @property
    def pretty_ttl(self):
        td = timedelta(seconds=self.ttl)
        return str(td)


class PydleRootState(StateDict):
    """Root Pydle state object

    Top of the state hierarchy
    """
    _defaults = dict(
        users=StateDict,

    )
