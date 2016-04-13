from common import ResourceValidators
from resources import GCPResource
from compute_properties import InstanceTemplateProperty, InstanceGroupNamedPort, AutoscalingPolicy


class Autoscaler(GCPResource):
    POLICY_TYPES = ['cpuUtilization', 'customMetricUtilizations', 'loadBalancingUtilization']

    resource_type = 'compute#autoscaler'
    props = {
        'autoscalingPolicy': (AutoscalingPolicy, False),
        'description': (basestring, False),
        'name': (basestring, True),
        'target': (basestring, True)  # URL
    }


class TargetPool(GCPResource):
    pass


class InstanceGroup(GCPResource):
    resource_type = 'compute.v1.instanceGroup'
    props = {
        'description': (basestring, False),
        'name': (basestring, True, ResourceValidators.name),
        'namedPorts': ([InstanceGroupNamedPort], False),
        'network': (basestring, True),  # URL
        'subnetwork': (basestring, False)  # URL
    }


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