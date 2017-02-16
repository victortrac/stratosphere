try:
    from stratosphere.common import ResourceValidators
    from stratosphere.resources import GCPResource
    from stratosphere.compute_properties import BackendServiceBackend, InstanceTemplateProperty, \
            InstanceGroupNamedPort, AutoHealingPolicy, AutoscalingPolicy, FirewallAllowedPorts, \
            UrlMapHostRule, UrlMapPathMatcher, UrlMapTests, InstanceTemplateDisksProperty, \
            InstanceTemplateMetadataProperty, InstanceTemplateNetworkInterfaceProperty, \
            InstanceTemplateSchedulingProperty, InstanceTemplateServiceAccountsProperty, \
            InstanceTemplateTagsProperty
except ImportError:
    from common import ResourceValidators
    from resources import GCPResource
    from compute_properties import BackendServiceBackend, InstanceTemplateProperty, \
        InstanceGroupNamedPort, AutoHealingPolicy, AutoscalingPolicy, FirewallAllowedPorts, \
        UrlMapHostRule, UrlMapPathMatcher, UrlMapTests, InstanceTemplateDisksProperty, \
        InstanceTemplateMetadataProperty, InstanceTemplateNetworkInterfaceProperty, \
        InstanceTemplateSchedulingProperty, InstanceTemplateServiceAccountsProperty, \
        InstanceTemplateTagsProperty


class Address(GCPResource):
    resource_type = 'compute.v1.address'
    props = {
        'description': (str, False),
        'name': (str, True, ResourceValidators.name),
        'region': (str, True)
    }


class GlobalAddress(GCPResource):
    resource_type = 'compute.v1.globalAddress'
    props = {
        'description': (str, False),
        'name': (str, True, ResourceValidators.name)
    }


class Autoscaler(GCPResource):
    resource_type = 'compute#autoscaler'

    POLICY_TYPES = ['cpuUtilization', 'customMetricUtilizations', 'loadBalancingUtilization']
    props = {
        'autoscalingPolicy': (AutoscalingPolicy, False),
        'description': (str, False),
        'name': (str, True),
        'target': (str, True)  # URL
    }


class Disk(GCPResource):
    resource_type = 'compute.v1.disk'
    props = {
        'description': (str, False),
        'name': (str, True),
        'sizeGb': (int, True),
        'sourceImage': (str, False),
        'sourceSnapshot': (str, False),
        'type': (str, True),
        'zone': (str, True)
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
        'description': (str, False),
        'healthChecks': ([str], True),
        'name': (str, True, ResourceValidators.name),
        'port': (int, True),
        'portName': (str, True),
        'protocol': (str, True, ALLOWED_PROTOCOLS)
    }


class TargetHttpProxy(GCPResource):
    resource_type = 'compute.v1.targetHttpProxy'
    props = {
        'description': (str, False),
        'name': (str, True, ResourceValidators.name),
        'urlMap': (str, True)
    }


class TargetHttpsProxy(GCPResource):
    resource_type = 'compute.v1.targetHttpsProxy'
    props = {
        'description': (str, False),
        'name': (str, True, ResourceValidators.name),
        'urlMap': (str, True),
        'sslCertificates': ([str], True)
    }


class Firewall(GCPResource):
    resource_type = 'compute.v1.firewall'
    props = {
        'name': (str, True, ResourceValidators.name),
        'allowed': ([FirewallAllowedPorts], True),
        'description': (str, False),
        'network': (str, True),
        'sourceRanges': ([str], False),
        'sourceTags': ([str], False),
        'targetTags': ([str], False)
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
        'name': (str, True, ResourceValidators.name),
        'description': (str, False),
        'IPAddress': (str, False),
        'IPProtocol': (str, True, ALLOWED_PROTOCOLS),
        'portRange': (str, False),
        'target': (str, True),
        'region': (str, True)
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
        'name': (str, True, ResourceValidators.name),
        'description': (str, False),
        'IPAddress': (str, False),
        'IPProtocol': (str, True, ALLOWED_PROTOCOLS),
        'portRange': (str, False),
        'target': (str, True)
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
        'description': (str, False),
        'healthyThreshold': (int, False),
        'host': (str, False),
        'name': (str, True, ResourceValidators.name),
        'port': (int, False),
        'requestPath': (str, False),
        'timeoutSec': (int, False),
        'unhealthyThreshold': (int, False)
    }


class InstanceGroup(GCPResource):
    resource_type = 'compute.v1.instanceGroup'
    props = {
        'description': (str, False),
        'name': (str, True, ResourceValidators.name),
        'namedPorts': ([InstanceGroupNamedPort], False),
        'network': (str, True),  # URL
        'subnetwork': (str, False)  # URL
    }


class Instance(GCPResource):
    resource_type = 'compute.v1.instance'
    props = {
        'name': (str, True, ResourceValidators.name),
        'description': (str, False),
        'canIpForward': (bool, False),
        'disks': ([InstanceTemplateDisksProperty], True),
        'machineType': (str, True),
        'metadata': (InstanceTemplateMetadataProperty, False),
        'networkInterfaces': ([InstanceTemplateNetworkInterfaceProperty], True),
        'scheduling': (InstanceTemplateSchedulingProperty, False),
        'serviceAccounts': ([InstanceTemplateServiceAccountsProperty], False),
        'tags': (InstanceTemplateTagsProperty, False),
        'zone': (str, True)
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
        'baseInstanceName': (str, True, ResourceValidators.base_instance_name),
        'description': (str, False),
        'instanceTemplate': (str, True),  # URL
        'name': (str, True, ResourceValidators.name),
        'namedPorts': ([InstanceGroupNamedPort], False),
        'targetPools': ([TargetPool], False),
        'targetSize': (int, True),
        'zone': (str, True, ResourceValidators.zone)
    }


class InstanceTemplate(GCPResource):
    resource_type = 'compute.v1.instanceTemplate'
    props = {
        'description': (str, False),
        'name': (str, True, ResourceValidators.name),
        'properties': (InstanceTemplateProperty, True),
    }


class Network(GCPResource):
    resource_type = 'compute.v1.network'
    props = {
        'IPv4Range': (str, False),
        'autoCreateSubnetworks': (bool, False),
        'description': (str, False),
        'gatewayIPv4': (str, False),
        'name': (str, True, ResourceValidators.name),
    }


class RegionInstanceGroupManager(GCPResource):
    resource_type = 'compute.beta.regionInstanceGroupManager'

    FAILOVER_ACTIONS = ['NO_FAILOVER']
    props = {
        'autoHealingPolicies': ([AutoHealingPolicy], False),
        'region': (str, True),
        'baseInstanceName': (str, True, ResourceValidators.base_instance_name),
        'description': (str, False),
        'failoverAction': (str, False, FAILOVER_ACTIONS),
        'instanceTemplate': (str, True, ResourceValidators.is_url),
        'name': (str, True, ResourceValidators.name),
        'namedPorts': ([InstanceGroupNamedPort], False),
        'targetPools': ([TargetPool], False),
        'targetSize': (int, True),
        'zone': (str, False, ResourceValidators.zone)
    }

    def validator(self):
        if len(self.properties.get('autoHealingPolicies', [])) > 1:
            raise ValueError('Only one AutoHealingPolicy is allowed')


class Route(GCPResource):
    resource_type = 'compute.v1.route'
    props = {
        'description': (str, False),
        'destRange': (str, True, ResourceValidators.ipAddress),
        'name': (str, True, ResourceValidators.name),
        'network': (str, True),  # URL
        'nextHopGateway': (str, False),  # URL
        'nextHopInstance': (str, False),  # URL
        'nextHopIp': (str, False, ResourceValidators.ipAddress),
        'nextHopVpnTunnel': (str, False),  # URL
        'priority': (int, False, range(1, 65536)),
        'tags': ([str], True),  # Bug in GCP: requires at least an empty list
    }

    def validator(self):
        # Must have one and only one of nextHopGateway, nextHopInstance, nextHopIp, nextHopVpnTunnel
        if len(filter(lambda x: self.properties.get(x, False),
                      ['nextHopGateway', 'nextHopInstance', 'nextHopIp', 'nextHopVpnTunnel'])) != 1:
            raise ValueError('Must define one and only one of nextHopGateway, nextHopInstance, nextHopIp, nextHopVpnTunnel.')


class Subnetwork(GCPResource):
    resource_type = 'compute.v1.subnetworks'
    props = {
        'description': (str, False),
        'region': (str, True),
        'ipCidrRange': (str, True, ResourceValidators.ipAddress),
        'name': (str, True, ResourceValidators.name),
        'network': (str, True)
    }


class TargetVpnGateway(GCPResource):
    resource_type = 'compute.v1.targetVpnGateway'
    props = {
        'description': (str, False),
        'name': (str, True, ResourceValidators.name),
        'network': (str, True),
        'region': (str, True),
    }


class UrlMap(GCPResource):
    resource_type = 'compute.v1.urlMap'
    props = {
        'name': (str, True, ResourceValidators.name),
        'defaultService': (str, True),
        'description': (str, False),
        'hostRules': ([UrlMapHostRule], True),
        'pathMatchers': ([UrlMapPathMatcher], True),
        'tests': ([UrlMapTests], False)
    }


class VpnTunnel(GCPResource):
    resource_type = 'compute.v1.vpnTunnel'
    props = {
        'description': (str, False),
        'ikeVersion': (int, False, [1, 2]),
        'localTrafficSelector': ([str], True, ResourceValidators.ipAddress),
        'name': (str, True, ResourceValidators.name),
        'peerIp': (str, True, ResourceValidators.ipAddress),
        'region': (str, True),
        'sharedSecret': (str, True),
        'sharedSecretHash': (str, False),
        'targetVpnGateway': (str, True)  # URL
    }
