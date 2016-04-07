from resources import GCPResource
from compute_properties import InstanceTemplateProperty


class InstanceTemplate(GCPResource):
    resource_type = 'compute.v1.instanceTemplate'
    props = {
        'description': (basestring, False),
        'properties': (InstanceTemplateProperty, True),
    }


class Network(GCPResource):
    resource_type = 'compute.v1.network'
    props = {
        'IPv4Range': (basestring, False),
        'autoCreateSubnetworks': (bool, False),
        'description': (basestring, False),
        'gatewayIPv4': (basestring, False),
    }


class Subnetwork(GCPResource):
    resource_type = 'compute.v1.subnetworks'
    props = {
        'description': (basestring, False),
        'region': (basestring, True),
        'ipCidrRange': (basestring, True),
        'network': (basestring, True)
    }