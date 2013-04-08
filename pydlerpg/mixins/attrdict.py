from inspect import isclass


class AttrDict(dict):
    """Dictionary that allows attribute access"""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError

    def __setattr__(self, name, value):
        try:
            super(AttrDict, self).__setattr__(name, value)
        except AttributeError:
            self[name] = value


class DefaultsMixin(object):
    """Mixin to initialize default values for a dictionary"""

    _defaults = None

    def __init__(self, *args, **kwargs):
        if self._defaults is not None:
            # update self with default values
            self.update(self._defaults)

            # create instances of any classes referenced in defaults
            for k, v in self._defaults.iteritems():
                if isclass(v):
                    self[k] = v()

        super(DefaultsMixin, self).__init__(*args, **kwargs)


class RequiredsMixin(object):
    """Mixin to validate specific items exist in a dictionary"""

    _requireds = None

    def __init__(self, *args, **kwargs):
        super(RequiredsMixin, self).__init__(*args, **kwargs)

        if self._requireds is not None:
            for attr, type_ in self._requireds.items():
                try:
                    val = self[attr]
                    if not isinstance(val, type_):
                        msg = 'Required item is the wrong type: {} -> {}'
                        raise ValueError(msg.format(attr, type_))
                except KeyError:
                    msg = 'Required item is not specified: {}'
                    raise ValueError(msg.format(attr))
