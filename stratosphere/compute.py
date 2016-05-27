from common import ResourceValidators
from resources import GCPResource
from compute_properties import BackendServiceBackend, InstanceTemplateProperty, InstanceGroupNamedPort, AutoscalingPolicy, \
    FirewallAllowedPorts, UrlMapHostRule, UrlMapPathMatcher, UrlMapTests, InstanceTemplateDisksProperty, \
    InstanceTemplateMetadataProperty, InstanceTemplateNetworkInterfaceProperty, InstanceTemplateSchedulingProperty, \
    InstanceTemplateServiceAccountsProperty, InstanceTemplateTagsProperty


class Address(GCPResource):
    resource_type = 'compute.v1.address'
    props = {
        'description': (basestring, False),
        'name': (basestring, True, ResourceValidators.name),
        'region': (basestring, True)
    }


class GlobalAddress(GCPResource):
    resource_type = 'compute.v1.globalAddress'
    props = {
        'description': (basestring, False),
        'name': (basestring, True, ResourceValidators.name)
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


class Disk(GCPResource):
    resource_type = 'compute.v1.disk'
    props = {
        'description': (basestring, False),
        'name': (basestring, True),
        'sizeGb': (long, True),
        'sourceImage': (basestring, False),
        'sourceSnapshot': (basestring, False),
        'type': (basestring, True),
        'zone': (basestring, True)
    }

    def validator(self):
        if self.properties.get('sourceImage') and self.properties.get('sourceSnapshot'):
            raise ValueError('{} unable to specify both sourceImage and sourceSnapshot.'.format(self.__class__))


class BackendService(GCPResource):
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    HTTP2 = "HTTP2"
    TCP = "TCP"
    SSL = "SSL"
    ALLOWED_PROTOCOLS = [HTTP, HTTPS, HTTP2, TCP, SSL]

    resource_type = 'compute.v1.backendService'
    props = {
        'backends': ([BackendServiceBackend], True),
        'description': (basestring, False),
        'healthChecks': ([basestring], True),
        'name': (basestring, True, ResourceValidators.name),
        'port': (int, True),
        'portName': (basestring, True),
        'protocol': (basestring, True, ALLOWED_PROTOCOLS)
    }


class TargetHttpProxy(GCPResource):
    resource_type = 'compute.v1.targetHttpProxy'
    props = {
        'description': (basestring, False),
        'name': (basestring, True, ResourceValidators.name),
        'urlMap': (basestring, True)
    }


class TargetHttpsProxy(GCPResource):
    resource_type = 'compute.v1.targetHttpsProxy'
    props = {
        'description': (basestring, False),
        'name': (basestring, True, ResourceValidators.name),
        'urlMap': (basestring, True),
        'sslCertificates': ([basestring], True)
    }


class Firewall(GCPResource):
    resource_type = 'compute.v1.firewall'
    props = {
        'name': (basestring, True, ResourceValidators.name),
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


class ForwardingRule(GCPResource):
    TCP = 'TCP'
    UDP = 'UDP'
    ESP = 'ESP'
    AH = 'AH'
    SCTP = 'SCTP'
    ALLOWED_PROTOCOLS = [TCP, UDP, ESP, AH, SCTP]

    resource_type = 'compute.v1.forwardingRule'
    props = {
        'name': (basestring, True, ResourceValidators.name),
        'description': (basestring, False),
        'IPAddress': (basestring, False),
        'IPProtocol': (basestring, True, ALLOWED_PROTOCOLS),
        'portRange': (basestring, False),
        'target': (basestring, True),
        'region': (basestring, True)
    }

    def validator(self):
        protos = (self.TCP, self.UDP, self.SCTP)
        if self.properties.get('IPProtocol') in protos:
            if not self.properties.get('portRange'):
                raise ValueError('PortRange must be set if protocol is: {}'.format(",".join(protos)))


class GlobalForwardingRule(GCPResource):
    TCP = 'TCP'
    UDP = 'UDP'
    ESP = 'ESP'
    AH = 'AH'
    SCTP = 'SCTP'
    ALLOWED_PROTOCOLS = [TCP, UDP, ESP, AH, SCTP]

    resource_type = 'compute.v1.globalForwardingRule'
    props = {
        'name': (basestring, True, ResourceValidators.name),
        'description': (basestring, False),
        'IPAddress': (basestring, False),
        'IPProtocol': (basestring, True, ALLOWED_PROTOCOLS),
        'portRange': (basestring, False),
        'target': (basestring, True)
    }

    def validator(self):
        protos = (self.TCP, self.UDP, self.SCTP)
        if self.properties.get('IPProtocol') in protos:
            if not self.properties.get('portRange'):
                raise ValueError('PortRange must be set if protocol is: {}'.format(",".join(protos)))


class HttpHealthCheck(GCPResource):
    resource_type = 'compute.v1.httpHealthCheck'
    props = {
        'checkIntervalSec': (int, False),
        'description': (basestring, False),
        'healthyThreshold': (int, False),
        'host': (basestring, False),
        'name': (basestring, True, ResourceValidators.name),
        'port': (int, False),
        'requestPath': (basestring, False),
        'timeoutSec': (int, False),
        'unhealthyThreshold': (int, False)
    }


class InstanceGroup(GCPResource):
    resource_type = 'compute.v1.instanceGroup'
    props = {
        'description': (basestring, False),
        'name': (basestring, True, ResourceValidators.name),
        'namedPorts': ([InstanceGroupNamedPort], False),
        'network': (basestring, True),  # URL
        'subnetwork': (basestring, False)  # URL
    }


class Instance(GCPResource):
    resource_type = 'compute.v1.instance'
    props = {
        'name': (basestring, True, ResourceValidators.name),
        'description': (basestring, False),
        'canIpForward': (bool, False),
        'disks': ([InstanceTemplateDisksProperty], True),
        'machineType': (basestring, True),
        'metadata': (InstanceTemplateMetadataProperty, False),
        'networkInterfaces': ([InstanceTemplateNetworkInterfaceProperty], True),
        'scheduling': (InstanceTemplateSchedulingProperty, False),
        'serviceAccounts': ([InstanceTemplateServiceAccountsProperty], False),
        'tags': (InstanceTemplateTagsProperty, False),
        'zone': (basestring, True)
    }

    def validator(self):
        # at least one disk must be marked as boot
        boot_count = 0
        for disk in self.properties.get('disks'):
            if disk.properties['boot'] == True:
                boot_count += 1
                # Boot disks must be persistent
                if not disk.properties['type'] == InstanceTemplateDisksProperty.PERSISTENT:
                    raise ValueError('{} - Boot disks must be persistent!'.format(disk))
                # Boot disks must have a source
                if not disk.properties.get('initializeParams') and not disk.properties.get('source'):
                    raise ValueError('{} - Boot disks without initializeParams must have source!'.format(disk))
        if not boot_count == 1:
            raise ValueError('{} - One disk must be marked as bootable!'.format(self.__class__))


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
        'priority': (int, False, range(1, 65536)),
        'tags': ([basestring], True),  # Bug in GCP: requires at least an empty list
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


class TargetVpnGateway(GCPResource):
    resource_type = 'compute.v1.targetVpnGateway'
    props = {
        'description': (basestring, False),
        'name': (basestring, True, ResourceValidators.name),
        'network': (basestring, True),
        'region': (basestring, True),
    }


class UrlMap(GCPResource):
    resource_type = 'compute.v1.urlMap'
    props = {
        'name': (basestring, True, ResourceValidators.name),
        'defaultService': (basestring, True),
        'description': (basestring, False),
        'hostRules': ([UrlMapHostRule], True),
        'pathMatchers': ([UrlMapPathMatcher], True),
        'tests': ([UrlMapTests], False)
    }


class VpnTunnel(GCPResource):
    resource_type = 'compute.v1.vpnTunnel'
    props = {
        'description': (basestring, False),
        'ikeVersion': (int, False, [1, 2]),
        'localTrafficSelector': ([basestring], True, ResourceValidators.ipAddress),
        'name': (basestring, True, ResourceValidators.name),
        'peerIp': (basestring, True, ResourceValidators.ipAddress),
        'region': (basestring, True),
        'sharedSecret': (basestring, True),
        'sharedSecretHash': (basestring, False),
        'targetVpnGateway': (basestring, True)  # URL
    }
