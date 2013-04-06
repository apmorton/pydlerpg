from pydlerpg.util import AttrDict, DefaultsMixin, RequiredsMixin

class ConfigDict(DefaultsMixin, RequiredsMixin, AttrDict):
    """AttrDict with defaults and requireds"""

    _requireds = dict(
        servers=list,
        admins=dict,
        state=basestring,
        plugins=list,
    )

    _defaults = dict(
        nickname='PydleRPG',
        channel='#PydleRPG',
        additional_channels=list,
        tick_interval=1.0,
    )