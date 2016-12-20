import os

from stratosphere.resources import Template
from stratosphere.compute import Firewall, Instance
from stratosphere.compute_properties import FirewallAllowedPorts, InstanceTemplateMetadataProperty, \
    InstanceTemplateDisksProperty, InstanceTemplateDiskInitializeParamsProperty, \
    InstanceTemplateNetworkInterfaceProperty, InstanceTemplateNetworkInterfaceAccessConfigProperty, \
    InstanceTemplateTagsProperty, MetadataProperty
from stratosphere.common import ResourceNames
from stratosphere.utils import get_latest_image, load_startup_script

import constants


name = "nfs-server"
startup_script_path = os.path.join(os.path.dirname(__file__), 'startup-scripts', '{}.sh'.format(name))

class NFSServer(Template):
    """
    This creates a new instance, attaches a disk, and runs the startup script in
    startup-scripts/nfs-server.sh on boot.

    This particular implementation expects a constants that is structured like this:

    ENV = {
        'dev': {
            'nfs-server': {
                'zone': 'us-central1-b',
                'machine_type': 'n1-standard-1',
        }
    }

    It also assumes a persistent disk in the same zone that's called the same value as `name`,
    which in this case is 'nfs-server'.
    """
    TEMPLATE_TYPE = name

    def configure(self):
        # Use ResourceNames to get names for networks and subnetworks to be consistent
        names = ResourceNames(self.project, self.env)

        config = constants.ENV[self.env][name]

        instance = Instance(
            name=name,
            canIpForward=False,
            disks=[
                InstanceTemplateDisksProperty(
                    autoDelete=True,
                    boot=True,
                    initializeParams=InstanceTemplateDiskInitializeParamsProperty(
                        sourceImage=get_latest_image(self.project, 'debian-8'),
                        diskSizeGb=10
                    ),
                    type=InstanceTemplateDisksProperty.PERSISTENT
                ),
                # This disk was created independently so that DM isn't able to delete it.
                # You'll need to manually format the persistent volume before the startup
                # script will be able to use it for the first time, since the
                # startup script tries to do a mount on boot.
                InstanceTemplateDisksProperty(
                    autoDelete=False,
                    boot=False,
                    deviceName=name + '-data',  # Shows up as /dev/disk/by-id/google-<deviceName>
                    source="projects/{project}/zones/{zone}/disks/{disk_name}".format(**{
                        'project': names.project,
                        'zone': config['zone'],
                        'disk_name': name + '-data'}),
                    type=InstanceTemplateDisksProperty.PERSISTENT,
                ),
            ],
            machineType='zones/{}/machineTypes/{}'.format(config['zone'], config['machine_type']),
            metadata=InstanceTemplateMetadataProperty(
                items=[
                    MetadataProperty(
                        key='startup-script',
                        value=load_startup_script(startup_script_path),
                    )
                ]
            ),
            networkInterfaces=[
                InstanceTemplateNetworkInterfaceProperty(
                    accessConfigs=[
                        InstanceTemplateNetworkInterfaceAccessConfigProperty(
                            name='External Access',
                            type=InstanceTemplateNetworkInterfaceAccessConfigProperty.ONE_TO_ONE_NAT
                        )
                    ],
                    network="projects/{}/global/networks/{}".format(names.project, names.networkName),
                    subnetwork='regions/{region}/subnetworks/{env}-{region}-subnetwork'.format(**{
                        'region': names.zone_to_region(config['zone']),
                        'env': self.env})
                )
            ],
            tags=InstanceTemplateTagsProperty(
                items=[
                    'nfs-server',
                    config['zone']
                ]
            ),
            zone=config['zone']
        )
        self.add_resource(instance)

        firewall_rules = [
            Firewall(
                name='{}-nfs-server'.format(self.env),
                network="projects/{}/global/networks/{}".format(names.project, names.networkName),
                allowed=[
                    FirewallAllowedPorts(
                        IPProtocol=FirewallAllowedPorts.TCP,
                        ports=[
                            "111",
                            "2049"
                        ]
                    ),
                    FirewallAllowedPorts(
                        IPProtocol=FirewallAllowedPorts.UDP,
                        ports=[
                            "111",
                            "2049"
                        ]
                    ),
                    FirewallAllowedPorts(
                        IPProtocol=FirewallAllowedPorts.ICMP
                    )
                ],
                sourceRanges=[constants.ENV[self.env]['cidr']]
            )
        ]

        for rule in firewall_rules:
            self.add_resource(rule)
