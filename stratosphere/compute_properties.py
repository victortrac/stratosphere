try:
    from stratosphere.common import ResourceValidators
    from stratosphere.resources import GCPProperty
except ImportError:
    # Python2
    from common import ResourceValidators
    from resources import GCPProperty


class AutoHealingPolicy(GCPProperty):
    props = {
        'healthCheck': (str, True),  # URL for healthcheck that signals autohealing
        'initialDelaySec': (int, True)  # Number in seconds the IG waits before recreating instance
    }


class AutoscalingPolicyCpuUtilization(GCPProperty):
    props = {
        'utilizationTarget': (float, False)
    }


class AutoscalingPolicyCustomMetricUtilizations(GCPProperty):
    UTILIZATION_TARGET_TYPE = ['GAUGE', 'DELTA_PER_SECOND', 'DELTA_PER_MINUTE']

    props = {
        'metric': (str, True),
        'utilizationTarget': (float, False),
        'utilizationTargetType': (str, False, UTILIZATION_TARGET_TYPE),
    }


class AutoscalingPolicyLoadBalancingUtilization(GCPProperty):
    props = {
        'utilizationTarget': (float, False)
    }


class AutoscalingPolicy(GCPProperty):
    props = {
        'coolDownPeriodSec': (int, False),  # Defaults to 60s
        'cpuUtilization': (AutoscalingPolicyCpuUtilization, False),
        'customMetricUtilizations': ([AutoscalingPolicyCustomMetricUtilizations], False),
        'loadBalancingUtilization': (AutoscalingPolicyLoadBalancingUtilization, False),
        'maxNumReplicas': (int, True),
        'minNumReplicas': (int, False),
        'description': (str, False),
        'name': (str, True, ResourceValidators.name),
        'target': (str, True)  # URL
    }


class BackendServiceBackend(GCPProperty):
    UTILIZATION = "UTILIZATION"
    RATE = "RATE"
    BALANCING_MODES = [UTILIZATION, RATE]

    props = {
        'balancingMode': (str, True, BALANCING_MODES),
        'capacityScaler': (float, False),
        'description': (str, False),
        'group': (str, True),
        'maxRate': (int, False),
        'maxRatePerInstance': (float, False),
        'maxUtilization': (float, False)
    }

    def validator(self):
        if self.properties.get('balancingMode') == self.RATE:
            if not self.properties.get('maxRate') or not self.properties.get('maxRatePerInstance'):
                raise ValueError('{} maxRate or maxRatePerInstance must be set if using RATE mode'
                                 .format(self.__class__))


class FirewallAllowedPorts(GCPProperty):
    TCP = 'tcp'
    UDP = 'udp'
    ICMP = 'icmp'
    ESP = 'esp'
    AH = 'ah'
    SCTP = 'sctp'
    ALLOWED_PROTOCOLS = [TCP, UDP, ICMP, ESP, AH, SCTP]

    props = {
        'IPProtocol': (str, True, ALLOWED_PROTOCOLS),
        'ports': ([str], False)
    }

    def validator(self):
        if self.properties.get('IPProtocol') in (self.TCP, self.UDP):
            if not self.properties.get('ports'):
                raise ValueError('Ports must be defined for TCP or UDP firewall rules')


class MetadataProperty(GCPProperty):
    props = {
        'key': (str, True),
        'value': (str, True)
    }


class InstanceTemplateDiskInitializeParamsProperty(GCPProperty):
    LOCAL = 'local-ssd'
    SSD = 'pd-ssd'
    STANDARD = 'pd-standard'
    DISK_TYPES = [LOCAL, SSD, STANDARD]

    props = {
        'diskName': (str, False),
        'diskSizeGb': (int, True),
        'diskType': (str, False, DISK_TYPES),
        'sourceImage': (str, False)
    }


class InstanceTemplateDisksProperty(GCPProperty):
    SCRATCH = 'SCRATCH'
    PERSISTENT = 'PERSISTENT'
    VALID_TYPES = [SCRATCH, PERSISTENT]
    props = {
        'autoDelete': (bool, False),
        'boot': (bool, True),
        'deviceName': (str, False),
        'index': (int, False),
        'initializeParams': (InstanceTemplateDiskInitializeParamsProperty, False),
        'interface': (str, False),
        'mode': (str, False),
        'source': (str, False),
        'sizeGb': (int, False),
        'type': (str, True, VALID_TYPES)
    }

    def validator(self):
        # Must provide initializeParams or source, not both
        if not (bool(self.properties.get('initializeParams')) != bool(self.properties.get('source'))):
            raise ValueError('Must provide initializeParams or source, not both.')
        if self.properties.get('boot', False) == True:
            # Boot disks require an initializeParams or source property
            return True
        else:
            # non-boot disks can't have an initializeParams property
            if self.properties.get('initializeParams'):
                raise ValueError('Non-boot disks should not have an initializeParams property')


class InstanceTemplateMetadataProperty(GCPProperty):
    props = {
        'fingerprint': (bytes, False),
        'items': ([MetadataProperty, ], False)
    }


class InstanceTemplateNetworkInterfaceAccessConfigProperty(GCPProperty):
    ONE_TO_ONE_NAT = 'ONE_TO_ONE_NAT'
    VALID_TYPES = [ONE_TO_ONE_NAT, ]

    props = {
        'name': (str, True),
        'natIP': (str, False),
        'type': (str, True, VALID_TYPES)
    }


class InstanceTemplateNetworkInterfaceProperty(GCPProperty):
    props = {
        'accessConfigs': ([InstanceTemplateNetworkInterfaceAccessConfigProperty], True),
        'network': (str, False),  # URL of network
        'subnetwork': (str, False),  # URL of subnetwork
    }

    def validator(self):
        if self.properties.get('network') and not self.properties.get('subnetwork'):
            raise ValueError('A custom network requires a subnetwork')


class InstanceTemplateSchedulingProperty(GCPProperty):
    MIGRATE = 'MIGRATE'
    TERMINATE = 'TERMINATE'
    VALID_ONHOSTSMAINTENANCE = [MIGRATE, TERMINATE]

    props = {
        'automaticRestart': (bool, False),
        'onHostMaintenance': (str, False, VALID_ONHOSTSMAINTENANCE),
        'preemptible': (bool, False)
    }


class InstanceTemplateServiceAccountsProperty(GCPProperty):
    props = {
        'email': (str, False),
        'scopes': ([str], True)
    }


class InstanceTemplateTagsProperty(GCPProperty):
    props = {
        'fingerprint': (bytes, False),
        'items': ([str], False)
    }


class InstanceTemplateProperty(GCPProperty):
    props = {
        'description': (str, False),
        'canIpForward': (bool, False),
        'disks': ([InstanceTemplateDisksProperty], True),
        'machineType': (str, True, ResourceValidators.is_valid_machine_type),
        'metadata': (InstanceTemplateMetadataProperty, False),
        'networkInterfaces': ([InstanceTemplateNetworkInterfaceProperty], True),
        'scheduling': (InstanceTemplateSchedulingProperty, False),
        'serviceAccounts': ([InstanceTemplateServiceAccountsProperty], False),
        'tags': (InstanceTemplateTagsProperty, False)
    }

    def validator(self):
        # at least one disk must be marked as boot
        boot_count = 0
        for disk in self.properties.get('disks'):
            if disk.properties.get('boot') == True:
                boot_count += 1
                # Boot disks must be persistent
                if not disk.properties['type'] == InstanceTemplateDisksProperty.PERSISTENT:
                    raise ValueError('{} - Boot disks must be persistent!'.format(disk))
                # Boot disks must have a source
                if not disk.properties.get('initializeParams') and not disk.properties.get('source'):
                    raise ValueError('{} - Boot disks without initializeParams must have source!'.format(disk))
        if not boot_count == 1:
            raise ValueError('{} - One disk must be marked as bootable!'.format(self.__class__))


class InstanceGroupNamedPort(GCPProperty):
    props = {
        'name': (str, True, ResourceValidators.name),
        'port': (int, True)
    }


class UrlMapHostRule(GCPProperty):
    props = {
        'description': (str, False),
        'hosts': ([str], True),
        'pathMatcher': (str, True)
    }


class UrlMapPathMatcherPathRule(GCPProperty):
    props = {
        'paths': ([str], True),
        'service': (str, True)
    }


class UrlMapPathMatcher(GCPProperty):
    props = {
        'defaultService': (str, True),
        'description': (str, False),
        'name': (str, True),
        'pathRules': ([UrlMapPathMatcherPathRule], False)
    }


class UrlMapTests(GCPProperty):
    props = {
        'description': (str, False),
        'host': (str, True),
        'path': (str, True),
        'service': (str, True)
    }
