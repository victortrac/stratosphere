import re
from netaddr import IPNetwork

from utils import get_google_auth

class ResourceValidators(object):
    @classmethod
    def regex_match(cls, regex, string):
        RE = re.compile(regex)
        if RE.match(string):
            return True
        return False

    @staticmethod
    def name(name):
        return ResourceValidators.regex_match('^(?:[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?)$', name)

    @staticmethod
    def zone(zone):
        return ResourceValidators.regex_match('^(?:[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?)$', zone)

    @staticmethod
    def base_instance_name(name):
        return ResourceValidators.regex_match('^[a-z][-a-z0-9]{0,57}$', name)

    @staticmethod
    def ipAddress(network):
        try:
            IPNetwork(network)
            return True
        except:
            raise ValueError('Invalid CIDR - {}'.format(network))

    @staticmethod
    def is_valid_machine_type(project, zone, _type):
        pass


class ResourceNames(object):
    """
    Provides some helper functions to consistently name things
    """
    def __init__(self, project, env):
        self.project = project
        self.env = env

    @property
    def networkName(self):
        return '{}-network'.format(self.env)

    def subnetworkName(self, zone):
        return '{}-{}-subnetwork'.format(self.env, zone)

    def zone_to_region(self, zone):
        """Derives the region from a zone name."""
        parts = zone.split('-')
        if len(parts) != 3:
            raise Exception('Cannot derive region from zone "%s"' % zone)
        return '-'.join(parts[:2])