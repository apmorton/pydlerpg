from pydlerpg.mixins.attrdict import AttrDict, DefaultsMixin, RequiredsMixin


class ConfigDict(DefaultsMixin, RequiredsMixin, AttrDict):
    """AttrDict with defaults and requireds"""

    _requireds = dict(
        servers=list,
        admins=dict,
        state=basestring,
        plugins=dict,
    )

    _defaults = dict(
        nickname='PydleRPG',
        channel='#PydleRPG',
        additional_channels=list,
        tick_interval=1.0,
        msg_length=400,
    )
