from stratosphere.resources import Template
from stratosphere.compute import Firewall, Network, Subnetwork
from stratosphere.compute_properties import FirewallAllowedPorts

from . import constants


class Networks(Template):
    TEMPLATE_TYPE = 'networks'

    def configure(self):
        network = Network(
            name='{}-network'.format(self.env),
            description='{} - Multi-region Network'.format(self.name),
            autoCreateSubnetworks=False,
        )

        self.add_resource(network)

        for subnetwork in constants.ENV[self.env]['subnetworks']:
            self.add_resource(
                Subnetwork(
                    name='{}-{}-subnetwork'.format(self.env, subnetwork['region']),
                    region=subnetwork['region'],
                    description='{} - {} Subnetwork'.format(self.env, subnetwork['region']),
                    ipCidrRange=subnetwork['cidr'],
                    network=network.Ref
                )
            )

        firewall_rules = [
            Firewall(
                name='{}-internal-ssh'.format(network.name),
                network=network.Ref,
                allowed=[
                    FirewallAllowedPorts(
                        IPProtocol=FirewallAllowedPorts.TCP,
                        ports=['22']
                    ),
                    FirewallAllowedPorts(
                        IPProtocol=FirewallAllowedPorts.ICMP
                    )
                ],
                sourceRanges=[
                    constants.ENV[self.env]['cidr']
                ]
            )
        ]

        [self.add_resource(f) for f in firewall_rules]

