from common import ResourceValidators
from resources import GCPResource
from compute_properties import InstanceTemplateProperty, InstanceGroupNamedPort, AutoscalingPolicy, \
    FirewallAllowedPorts


class Address(GCPResource):
    '''
    A Regional Reserved IP Address
    '''
    resource_type = 'compute.v1.address'
    props = {
        'description': (basestring, False),
        'name': (basestring, True, ResourceValidators.name),
        'region': (basestring, True)
    }


class Autoscaler(GCPResource):
    resource_type = 'compute#autoscaler'

    POLICY_TYPES = ['cpuUtilization', 'customMetricUtilizations', 'loadBalancingUtilization']
    props = {
        'autoscalingPolicy': (AutoscalingPolicy, False),
        'description': (basestring, False),
        'name': (basestring, True),
        'target': (basestring, True)  # URL
    }


class Firewall(GCPResource):
    resource_type = 'compute.v1.firewall'
    props = {
        'name': (basestring, True),
        'allowed': ([FirewallAllowedPorts], True),
        'description': (basestring, False),
        'network': (basestring, True),
        'sourceRanges': ([basestring], False),
        'sourceTags': ([basestring], False),
        'targetTags': ([basestring], False)
    }

    def validator(self):
        if not (bool(self.properties.get('sourceRanges')) != bool(self.properties.get('sourceTags'))):
            raise ValueError('Either sourceRanges or sourceTags must be defined')


class InstanceGroup(GCPResource):
    resource_type = 'compute.v1.instanceGroup'
    props = {
        'description': (basestring, False),
        'name': (basestring, True, ResourceValidators.name),
        'namedPorts': ([InstanceGroupNamedPort], False),
        'network': (basestring, True),  # URL
        'subnetwork': (basestring, False)  # URL
    }


class TargetPool(GCPResource):
    pass


class InstanceGroupManager(GCPResource):
    resource_type = 'compute.v1.instanceGroupManager'
    props = {
        'baseInstanceName': (basestring, True, ResourceValidators.base_instance_name),
        'description': (basestring, False),
        'instanceTemplate': (basestring, True),  # URL
        'name': (basestring, True, ResourceValidators.name),
        'namedPorts': ([InstanceGroupNamedPort], False),
        'targetPools': ([TargetPool], False),
        'targetSize': (int, True),
        'zone': (basestring, True, ResourceValidators.zone)
    }


class InstanceTemplate(GCPResource):
    resource_type = 'compute.v1.instanceTemplate'
    props = {
        'description': (basestring, False),
        'name': (basestring, True, ResourceValidators.name),
        'properties': (InstanceTemplateProperty, True),
    }


class Network(GCPResource):
    resource_type = 'compute.v1.network'
    props = {
        'IPv4Range': (basestring, False),
        'autoCreateSubnetworks': (bool, False),
        'description': (basestring, False),
        'gatewayIPv4': (basestring, False),
        'name': (basestring, True, ResourceValidators.name),
    }


class RegionInstanceGroupManager(GCPResource):
    resource_type = 'compute.alpha.regionInstanceGroupManagers'
    props = {
        'baseInstanceName': (basestring, True, ResourceValidators.base_instance_name),
        'description': (basestring, False),
        'instanceTemplate': (basestring, True),  # URL
        'name': (basestring, True, ResourceValidators.name),
        'namedPorts': ([InstanceGroupNamedPort], False),
        'targetPools': ([TargetPool], False),
        'targetSize': (int, True),
        'zone': (basestring, False, ResourceValidators.zone)
    }



class Route(GCPResource):
    resource_type = 'compute.v1.route'
    props = {
        'description': (basestring, False),
        'destRange': (basestring, True, ResourceValidators.ipAddress),
        'name': (basestring, True, ResourceValidators.name),
        'network': (basestring, True),  # URL
        'nextHopGateway': (basestring, False),  # URL
        'nextHopInstance': (basestring, False),  # URL
        'nextHopIp': (basestring, False, ResourceValidators.ipAddress),
        'nextHopVpnTunnel': (basestring, False),  # URL
        'priority': (int, False, range(0, 65536)),
        'tags': ([basestring], True),
    }

    def validator(self):
        # Must have one and only one of nextHopGateway, nextHopInstance, nextHopIp, nextHopVpnTunnel
        if len(filter(lambda x: self.properties.get(x, False),
                      ['nextHopGateway', 'nextHopInstance', 'nextHopIp', 'nextHopVpnTunnel'])) != 1:
            raise ValueError('Must define one and only one of nextHopGateway, nextHopInstance, nextHopIp, nextHopVpnTunnel.')


class Subnetwork(GCPResource):
    resource_type = 'compute.v1.subnetworks'
    props = {
        'description': (basestring, False),
        'region': (basestring, True),
        'ipCidrRange': (basestring, True, ResourceValidators.ipAddress),
        'name': (basestring, True, ResourceValidators.name),
        'network': (basestring, True)
    }




class VpnTunnel(GCPResource):
    resource_type = 'compute.v1.vpnTunnel'
    props = {
        'description': (basestring, False),
        'ikeVersion': (int, False, [1, 2]),
        'localTrafficSelector': ([basestring], True, ResourceValidators.ipAddress),
        'name': (basestring, True, ResourceValidators.name),
        'peerIp': (basestring, True, ResourceValidators.ipAddress),
        'sharedSecret': (basestring, True),
        'sharedSecretHash': (basestring, False),
        'targetVpnGateway': (basestring, False)  # URL
    }
