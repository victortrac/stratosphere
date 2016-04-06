import yaml

class BaseGCPResource(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.properties = {}
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def __getattr__(self, key):
        try:
            return self.properties.__getitem__(key)
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key in self.__dict__.keys() or \
                        'name' not in self.__dict__ or \
                        'properties' not in self.__dict__:
            return dict.__setattr__(self, key, value)
        elif key in self.props.keys():
            expected_type = self.props[key][0]
            if isinstance(value, expected_type):
                return self.properties.__setitem__(key, value)
            else:
                self._raise_type(key, value, expected_type)
        type_name = getattr(self, 'resource_type', self.__class__.__name__)
        raise AttributeError("%s object does not support attribute %s" %
                             (type_name, key))

    def __repr__(self):
        return self.asYAML()

    def _raise_type(self, key, value, expected_type):
        raise TypeError("{}: {}.{} is {}, expected {}".format(self.__class__,
                                                              self.name,
                                                              key,
                                                              type(value),
                                                              expected_type))

    def getRef(self):
        return unicode('$(ref.{}.selfLink)'.format(self.name))

    def isValid(self):
        if hasattr(self, 'resource_type'):
            for k, (_, required) in self.props.items():
                if required and k not in self.properties:
                    rtype = getattr(self, 'resource_type', "<unknown type>")
                    raise ValueError("Resource {} required in type {}".format(k, rtype))
        return True

    def asObject(self):
        if self.isValid():
            return {
                'type': self.resource_type,
                'name': self.name,
                'properties': self.properties
            }

    def asYAML(self):
        if self.isValid():
            return yaml.safe_dump(self.asObject())


class Template(object):
    TEMPLATE_TYPE = 'UNDEFINED'  # Need to override this in subclasses

    def __init__(self, env):
        self.env = env
        self._name = "{}-{}".format(env, self.TEMPLATE_TYPE)
        self.resources = []

    @property
    def name(self):
        return unicode(self._name)

    def add_resource(self, resource):
        self.resources.append(resource)

    def configure(self):
        raise NotImplementedError("Subclass Template and override configure()!")

    def asYAML(self):
        return yaml.safe_dump({'resources': [r.asObject() for r in self.resources]})

    def __repr__(self):
        self.configure()
        return self.asYAML()


