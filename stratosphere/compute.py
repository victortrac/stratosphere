from resources import BaseGCPResource


class Network(BaseGCPResource):
    resource_type = "compute.v1.network"
    props = {
        'IPv4Range': (basestring, False),
        'autoCreateSubnetworks': (bool, False),
        'description': (basestring, False),
        'gatewayIPv4': (basestring, False),
    }


class Subnetwork(BaseGCPResource):
    resource_type = 'compute.v1.subnetworks'
    props = {
        'description': (basestring, False),
        'region': (basestring, True),
        'ipCidrRange': (basestring, True),
        'network': (basestring, True)
    }