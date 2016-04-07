import yaml
import re

class Template(object):
    TEMPLATE_TYPE = 'UNDEFINED'  # Need to override this in subclasses

    def __init__(self, env):
        self.env = env
        self._name = "{}-{}".format(env, self.TEMPLATE_TYPE)
        self.resources = []
        self.configured = False

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
        if not self.configured:
            self.configure()
            self.configured = True
        return unicode(self.asYAML())


class BaseGCPResource(object):
    NAME_REGEX = re.compile('(?:[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?)')

    def __init__(self, name, **kwargs):
        self.name = name
        self.properties = {}
        for k, v in kwargs.items():
            self._set_property(k, v)

    def _set_property(self, key, value):
        if key not in self.props.keys():
            type_name = getattr(self, 'resource_type', self.__class__.__name__)
            raise AttributeError('{} object does not support attribute {}'.format(type_name, key))

        expected_type = self.props[key][0]
        if len(self.props[key]) == 3:
            expected_values = self.props[key][2]
            if value not in expected_values:
                self._raise_value(key, value, expected_values)

        if isinstance(expected_type, list):
            if not isinstance(value, list):
                self._raise_type(key, value, expected_type)
            for v in value:
                if not isinstance(v, tuple(expected_type)):
                    self._raise_type(key, v, expected_type)
            return self.properties.__setitem__(key, value)
        elif isinstance(value, expected_type):
            return self.properties.__setitem__(key, value)
        else:
            self._raise_type(key, value, expected_type)


    def _raise_type(self, key, value, expected_type):
        raise TypeError("{}: {}.{} is {}, expected {}".format(self.__class__,
                                                              self.name,
                                                              key,
                                                              type(value),
                                                              expected_type))

    def _raise_value(self, key, value, expected_values):
        raise TypeError("{}: {} is {}, expected values {}".format(self.__class__,
                                                              key,
                                                              value,
                                                              expected_values))

    def getRef(self):
        return unicode('$(ref.{}.selfLink)'.format(self.name))

    def isValid(self):
        if isinstance(self, GCPResource) and not hasattr(self, 'resource_type'):
            raise ValueError("Resource {} requires a resource_type.".format(self.name))
        for k, v in self.props.items():
            prop_type = v[0]
            required = v[1]
            if len(v) > 2:
                allowed_values = v[2]
            if required and k not in self.properties:
                raise ValueError("Resource {} required in type {}".format(k, self.__class__))
        # Finally, run extra validators if they are defined
        if getattr(self, 'validator', None):
            self.validator()
        return True



class GCPResource(BaseGCPResource):
    def __init__(self, name, **kwargs):
        if not self.NAME_REGEX.match(name):
            raise ValueError('{}: Invalid resource name: {}. Must match {}'.format(self.__class__, name, self.NAME_REGEX.pattern))
        super(GCPResource, self).__init__(name, **kwargs)

    def asObject(self):
        if self.isValid():
            properties = {}
            for property, value in self.properties.items():
                if isinstance(value, GCPProperty):
                    properties[property] = value.asObject()
                else:
                    properties[property] = value

            return {
                'type': self.resource_type,
                'name': self.name,
                'properties': properties
            }


class GCPProperty(BaseGCPResource):
    def __init__(self, name=None, **kwargs):
        super(GCPProperty, self).__init__(name, **kwargs)

    def asObject(self):
        if self.isValid():
            _object = {}
            for k, v in self.properties.items():
                if isinstance(v, list):
                    v2 = []
                    for item in v:
                        if isinstance(item, GCPProperty):
                            v2.append(item.asObject())
                        else:
                            v2.append(item)
                    v = v2
                if isinstance(v, GCPProperty):
                    _object[k] = v.asObject()
                else:
                    _object[k] = v
            return _object

