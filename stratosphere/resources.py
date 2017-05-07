import hashlib
import inspect
import logging
import yaml
import json

logger = logging.getLogger(__name__)

class Template(object):
    TEMPLATE_TYPE = None  # Need to override this in subclasses

    def __init__(self, project, env):
        self.project = project
        self.env = env
        self._name = "{}-{}".format(env, self.TEMPLATE_TYPE)
        self.resources = []
        self.configured = False
        self.formatter = self.asYAML

        if self.TEMPLATE_TYPE is None:
            raise NotImplementedError('Must set constant TEMPLATE_TYPE in Template Subclass. Example: network')

    @property
    def name(self):
        return str(self._name)

    def add_resource(self, resource):
        self.resources.append(resource)

    def configure(self):
        raise NotImplementedError("Subclass Template and override configure()!")

    def asYAML(self):
        return yaml.safe_dump({'resources': [r.asObject() for r in self.resources]})

    def asJSON(self):
        return json.dumps({'resources': [r.asObject() for r in self.resources]})

    def __repr__(self):
        if not self.configured:
            self.configure()
            self.configured = True
        return str(self.formatter())


class BaseGCPResource(object):
    # The cluster API is different from the other GCP APIs.  Doesn't accept a 'name' field
    # as a property field. Sigh google.
    INCLUDE_NAME_PROPERTY = True

    def __init__(self, **kwargs):
        self.properties = {}
        for k, v in kwargs.items():
            logger.debug("Setting property {}".format(k))
            logger.log(5, "Property value: {}".format(v))
            self._set_property(k, v)

    @property
    def name(self):
        return self.properties.get('name')

    @property
    def Ref(self):
        return str('$(ref.{}.selfLink)'.format(self.name))

    def __hash__(self):
        # Make a unique name for the resource
        hasher = hashlib.md5()
        hasher.update(''.join([v for v in self.asObject().values() if
                               isinstance(v, str)]).encode('utf-8'))
        return hasher.hexdigest()

    def _set_property(self, key, value):
        if value is None: return
        if key not in self.props.keys():
            type_name = getattr(self, 'resource_type', self.__class__.__name__)
            raise AttributeError('{} object does not support attribute {}'.format(type_name, key))
        expected_type = self.props[key][0]
        # The third field in a property is a validator function or a valid list of values
        if len(self.props[key]) == 3:
            allowed_values = self.props[key][2]
            # We turn the string into a set of 1 so we can do set comparison below
            _value_set = set([value]) if isinstance(value, str) else set(value)
            # allowed_values is a validator function
            if hasattr(allowed_values, '__call__'):
                if isinstance(value, list):
                    # validate a list of items (if item is a list)
                    logger.debug("Validating list of items for key={}".format(key))
                    for v in value:
                        logger.log(5, "Validating key='{}', value='{}' against validator function:\n{}"\
                            .format(key, v, inspect.getsource(allowed_values)))
                        if not allowed_values(v):
                            self._raise_value(key, v, allowed_values)
                else:
                    # validate single item
                    logger.debug("Validating item for key={}".format(key))
                    logger.log(5, "Validating key='{}', value='{}' against validator function:\n{}"\
                        .format(key, value,inspect.getsource(allowed_values)))
                    if not allowed_values(value):
                        self._raise_value(key, value, allowed_values)
            # allowed_values is a set of valid strings
            elif not (_value_set <= set(allowed_values)):
                self._raise_value(key, value, allowed_values)
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

    def _raise_value(self, key, value, allowed_values):
        if hasattr(allowed_values, '__call__'):
            allowed_values = 'defined in function:\n{}'.format(inspect.getsource(allowed_values))
        raise TypeError("{}: Property \'{}\' is set to \'{}\', expected values {}".format(self.__class__,
                                                                                          key,
                                                                                          value,
                                                                                          allowed_values))

    def _toObject(self):
        if self.isValid():
            _object = {}
            for k, v in self.properties.items():
                if self.INCLUDE_NAME_PROPERTY is False and k == 'name':
                    continue
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
    def asObject(self):
        return {
            'type': self.resource_type,
            'name': self.name,
            'properties': self._toObject()
        }

    def asUrl(self):
        """
        Tries to turn a self.resource_type into a Google Cloud Platform API URL
        """
        api, version, resource_type = self.resource_type.split('.')
        pass


class GCPProperty(BaseGCPResource):
    """
    GCPProperty is inherited to define properties of resources. 
    
    Classes contain at least a props={} that looks something like this:
    
    props = {
        'prop1': (<type>, <required bool>, <optional object or list containining valid values>)
        ...
    }
    """
    def asObject(self):
        return self._toObject()

