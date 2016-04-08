from resources import GCPProperty


class MetadataProperty(GCPProperty):
    props = {
        'key': (basestring, True),
        'value': (basestring, True)
    }


class InstanceTemplateDiskInitializeParamsProperty(GCPProperty):
    props = {
        'diskName': (basestring, False),
        'diskSizeGb': (int, True),
        'diskType': (basestring, True),
        'sourceImage': (basestring, False)
    }


class InstanceTemplateDisksProperty(GCPProperty):
    SCRATCH = 'SCRATCH'
    PERSISTENT = 'PERSISTENT'

    VALID_TYPES = [SCRATCH, PERSISTENT]

    props = {
        'autoDelete': (bool, False),
        'boot': (bool, True),
        'deviceName': (basestring, False),
        'index': (int, False),
        'initializeParams': (InstanceTemplateDiskInitializeParamsProperty, True),
        'interface': (basestring, False),
        'mode': (basestring, False),
        'source': (basestring, False),
        'type': (basestring, True, VALID_TYPES)
    }


class InstanceTemplateMetadataProperty(GCPProperty):
    props = {
        'fingerprint': (bytes, False),
        'items': ([MetadataProperty, ], False)
    }



class InstanceTemplateNetworkInterfaceAccessConfigProperty(GCPProperty):
    ONE_TO_ONE_NAT = 'ONE_TO_ONE_NAT'
    VALID_TYPES = [ONE_TO_ONE_NAT, ]

    props = {
        'name': (basestring, False),
        'natIP': (basestring, False),
        'type': (basestring, True, VALID_TYPES)
    }


class InstanceTemplateNetworkInterfaceProperty(GCPProperty):
    props = {
        'accessConfigs': ([InstanceTemplateNetworkInterfaceAccessConfigProperty], True),
        'network': (basestring, True),  # URL of network
        'subnetwork': (basestring, False),  # URL of subnetwork
    }


class InstanceTemplateSchedulingProperty(GCPProperty):
    MIGRATE = 'MIGRATE'
    TERMINATE = 'TERMINATE'
    VALID_ONHOSTSMAINTENANCE = [MIGRATE, TERMINATE]

    props = {
        'automaticRestart': (bool, False),
        'onHostMaintenance': (basestring, False, VALID_ONHOSTSMAINTENANCE),
        'preemptible': (bool, False)
    }


class InstanceTemplateServiceAccountsProperty(GCPProperty):
    props = {
        'email': (basestring, False),
        'scopes': ([basestring], False)
    }


class InstanceTemplateTagsProperty(GCPProperty):
    props = {
        'fingerprint': (bytes, False),
        'items': ([basestring], False)
    }


class InstanceTemplateProperty(GCPProperty):
    props = {
        'description': (basestring, False),
        'canIpForward': (bool, False),
        'disks': ([InstanceTemplateDisksProperty], True),
        'machineType': (basestring, True),
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
            if disk.properties['boot'] == True:
                boot_count += 1
                # Boot disks must be persistent
                if not disk.properties['type'] == InstanceTemplateDisksProperty.PERSISTENT:
                    raise ValueError('{} - Boot disks must be persistent!'.format(disk))
                # Boot disks must have a source
                if not disk.properties.get('initializeParams'):
                    raise ValueError('{} - Boot disks must have initializeParams!'.format(disk))
        if not boot_count == 1:
            raise ValueError('{} - One disk must be marked as bootable!'.format(self.__class__))

    def update(self, current_deployment):
        # Updates to InstanceTemplates require setting a fingerprint from the current deployment
        metadataProperty = self.properties.get('metadata', None)
        if metadataProperty:
            metadataProperty.properties['fingerprint'] = current_deployment.get('fingerprint')
        else:
            self.properties['metadata'] = InstanceTemplateMetadataProperty(
                fingerprint=str(current_deployment.get('fingerprint'))
            )
