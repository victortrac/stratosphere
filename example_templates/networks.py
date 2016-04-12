from stratosphere.resources import Template
from stratosphere.compute import Network, Subnetwork

import constants


class Networks(Template):
    TEMPLATE_TYPE = 'networks'

    def configure(self):
        network = Network(
            name='{}-network'.format(self.env),
            description='{} - MultiAZ Network'.format(self.name),
            autoCreateSubnetworks=False,
        )

        self.add_resource(network)

        for subnetwork in constants.ENV[self.env]['subnetworks']:
            self.add_resource(
                Subnetwork(
                    name='{}-{}-subnetwork'.format(self.env, subnetwork['zone']),
                    region=subnetwork['zone'][:subnetwork['zone'].rfind('-')],
                    description='{} - {} Subnetwork'.format(self.env, subnetwork['zone']),
                    ipCidrRange=subnetwork['cidr'],
                    network=network.Ref
                )
            )


def GenerateConfig(context):
    return unicode(Networks(context.env['name']))

