# Stratosphere

A library and tool for creating Google Cloud Platform Deployment Manager templates.

Stratosphere is inspired by [Troposphere](https://github.com/cloudtools/troposphere) for AWS.

## Features
* Lets you write pure python
* Includes property and type validation
* Interacts directly with the GCP Deployment Manager API without having to use the clunky gcloud CLI
* Highly opinionated about naming to enforce consistent naming across deployments

## Installation
Git clone this repository, then:

    # python setup.py install

You'll need to get a valid OAuth auth JSON file to interact with the GCP DM API. This is most
easily done by just installing the [GCP API Client Library for Python](https://developers.google.com/api-client-library/python/start/get_started#setup).

## Examples
See the [example_templates](example_templates) directory for how to build a template.

    $ stratosphere --project [MyGCPProject] --env dev --action template ./example_templates/networks.py
    resources:
    - name: dev-network
      properties: {autoCreateSubnetworks: false, description: dev-networks - MultiAZ Network}
      type: compute.v1.network
    - name: dev-us-central1-b-subnetwork
      properties: {description: dev - us-central1-b Subnetwork, ipCidrRange: 10.100.0.0/20,
        network: $(ref.dev-network.selfLink), region: us-central1}
      type: compute.v1.subnetworks
    - name: dev-us-central1-c-subnetwork
      properties: {description: dev - us-central1-c Subnetwork, ipCidrRange: 10.100.16.0/20,
        network: $(ref.dev-network.selfLink), region: us-central1}
      type: compute.v1.subnetworks
    - name: dev-us-central1-f-subnetwork
      properties: {description: dev - us-central1-f Subnetwork, ipCidrRange: 10.100.32.0/20,
        network: $(ref.dev-network.selfLink), region: us-central1}
      type: compute.v1.subnetworks

This reads the networks.py template and generates a valid Google Compute Engine Deployment Manager YAML
config, reading values from a constants.py that is shared across your deployments.

### Local Validation Examples
Stratosphere resources know about required parameters, so if you define a resource that is missing a parameter
or has an invalid field, you'll get an error like this (without having to wait for the Deployment Manager error).

##### Template defining a Firewall snippet:

    Firewall(
        name='{}-ssh'.format(self.env),
        network="projects/{}/global/networks/{}".format(names.project, names.networkName),
        allowed=[
            FirewallAllowedPorts(
                IPProtocol=FirewallAllowedPorts.TCP,
                ports=[
                    '22'
                ]
            ),
        ]
    )

Results in this error:

    ValueError: Either sourceRanges or sourceTags must be defined

##### Name field validation

    for subnetwork in constants.ENV[self.env]['subnetworks']:
        self.add_resource(
            Subnetwork(
                name='SUBNETWORk-{}'.format(names.subnetworkName(subnetwork['zone'])),
                region=names.zone_to_region(subnetwork['zone']),
                description='{} - {} Subnetwork'.format(names.networkName, subnetwork['zone']),
                ipCidrRange=subnetwork['cidr'],
                network=network.Ref
            )
        )


Results in this error (only lowercase characters are allowed in names):

    TypeError: <class 'stratosphere.compute.Subnetwork'>: name is SUBNETWORk-mynetwork-us-central1-b-subnetwork, expected values defined in function:
        @staticmethod
        def name(name):
            return ResourceValidators.regex_match('^(?:[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?)$', name)



## License

Apache 2.0 - See [LICENSE](LICENSE) for more information.