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
Let's say you want to programmatically create a GCP network with custom ranges (example is if the default range
conflicts with other networks).  You can write a constants file that looks like this:

    $ cat example_templates/constants.py
    ENV = {
        "dev": {
            "cidr": "10.128.0.0/14",
            "subnetworks": [
                {
                    "region": "us-central1",
                    "cidr": "10.128.0.0/20"
                },
                {
                    "region": "us-west1",
                    "cidr": "10.128.32.0/20"
                },
                {
                    "region": "us-east1",
                    "cidr": "10.128.64.0/20"
                },
                {
                    "region": "europe-west1",
                    "cidr": "10.128.96.0/20"
                },
                {
                    "region": "asia-east1",
                    "cidr": "10.128.128.0/20"
                }
            ]
        }
    }

Then write a stratosphere template that looks like this:

    $ cat example_templates/networks.py
    from stratosphere.resources import Template
    from stratosphere.compute import Firewall, Network, Subnetwork
    from stratosphere.compute_properties import FirewallAllowedPorts

    import constants


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


Use stratosphere to validate and generate YAML:

    $ stratosphere --project [MyGCPProject] --env dev --action template ./example_templates/networks.py
    2016-09-29 13:09:04 INFO:stratosphere.stratosphere:Log level: 20
    2016-09-29 13:09:04 INFO:stratosphere.stratosphere:Template successfully rendered, printing to stdout...
    resources:
    - name: dev-network
      properties: {autoCreateSubnetworks: false, description: dev-networks - MultiAZ Network,
        name: dev-network}
      type: compute.v1.network
    - name: dev-us-central1-subnetwork
      properties: {description: dev - us-central1 Subnetwork, ipCidrRange: 10.128.0.0/20,
        name: dev-us-central1-subnetwork, network: $(ref.dev-network.selfLink), region: us-central1}
      type: compute.v1.subnetworks
    - name: dev-us-west1-subnetwork
      properties: {description: dev - us-west1 Subnetwork, ipCidrRange: 10.128.32.0/20,
        name: dev-us-west1-subnetwork, network: $(ref.dev-network.selfLink), region: us-west1}
      type: compute.v1.subnetworks
    - name: dev-us-east1-subnetwork
      properties: {description: dev - us-east1 Subnetwork, ipCidrRange: 10.128.64.0/20,
        name: dev-us-east1-subnetwork, network: $(ref.dev-network.selfLink), region: us-east1}
      type: compute.v1.subnetworks
    - name: dev-europe-west1-subnetwork
      properties: {description: dev - europe-west1 Subnetwork, ipCidrRange: 10.128.96.0/20,
        name: dev-europe-west1-subnetwork, network: $(ref.dev-network.selfLink), region: europe-west1}
      type: compute.v1.subnetworks
    - name: dev-asia-east1-subnetwork
      properties: {description: dev - asia-east1 Subnetwork, ipCidrRange: 10.128.128.0/20,
        name: dev-asia-east1-subnetwork, network: $(ref.dev-network.selfLink), region: asia-east1}
      type: compute.v1.subnetworks


This reads the networks.py template and generates a valid Google Compute Engine Deployment Manager YAML
config, reading values from a constants.py that is shared across your deployments.

If you want to create the network, instead of `--action template`, you would run `--action apply`:

    $ stratosphere --project [MyGCPProject] --env dev --action apply ./example_templates/networks.py
    2016-09-29 13:10:59 INFO:stratosphere.stratosphere:Log level: 20
    2016-09-29 13:10:59 INFO:root:Generated template:
    resources:
    - name: dev-network
      properties: {autoCreateSubnetworks: false, description: dev-networks - MultiAZ Network,
        name: dev-network}
      type: compute.v1.network
    - name: dev-us-central1-subnetwork
      properties: {description: dev - us-central1 Subnetwork, ipCidrRange: 10.128.0.0/20,
        name: dev-us-central1-subnetwork, network: $(ref.dev-network.selfLink), region: us-central1}
      type: compute.v1.subnetworks
    - name: dev-us-west1-subnetwork
      properties: {description: dev - us-west1 Subnetwork, ipCidrRange: 10.128.32.0/20,
        name: dev-us-west1-subnetwork, network: $(ref.dev-network.selfLink), region: us-west1}
      type: compute.v1.subnetworks
    - name: dev-us-east1-subnetwork
      properties: {description: dev - us-east1 Subnetwork, ipCidrRange: 10.128.64.0/20,
        name: dev-us-east1-subnetwork, network: $(ref.dev-network.selfLink), region: us-east1}
      type: compute.v1.subnetworks
    - name: dev-europe-west1-subnetwork
      properties: {description: dev - europe-west1 Subnetwork, ipCidrRange: 10.128.96.0/20,
        name: dev-europe-west1-subnetwork, network: $(ref.dev-network.selfLink), region: europe-west1}
      type: compute.v1.subnetworks
    - name: dev-asia-east1-subnetwork
      properties: {description: dev - asia-east1 Subnetwork, ipCidrRange: 10.128.128.0/20,
        name: dev-asia-east1-subnetwork, network: $(ref.dev-network.selfLink), region: asia-east1}
      type: compute.v1.subnetworks


    2016-09-29 13:10:59 INFO:root:Launching a new deployment: dev-networks

    Continue? (yes/no) yes
    Running in 5...4...3...2...1...
    Waiting for deployment operation-1475172676856-53da96762e8c0-ce3bcf31-fb776453...
    2016-09-29 13:11:18 INFO:stratosphere.stratosphere:Operation: operation-1475172676856-53da96762e8c0-ce3bcf31-fb776453, TargetLink: https://www.googleapis.com/deploymentmanager/v2/projects/MyGCPProject/global/deployments/dev-networks, Progress: 0, Status: RUNNING
    ...
    2016-09-29 13:12:18 INFO:stratosphere.stratosphere:Operation: operation-1475172676856-53da96762e8c0-ce3bcf31-fb776453, TargetLink: https://www.googleapis.com/deploymentmanager/v2/projects/MyGCPProject/global/deployments/dev-networks, Progress: 100, Status: DONE
    Stack action complete.

Let's now say you want to add some firewall rules. Modify `networks.py` to include this:
    
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

Run `--action apply` again and see a diff:

    $ stratosphere --project [MyGCPProject] --env dev --action apply ./example_templates/networks.py
    2016-09-29 13:59:58 INFO:stratosphere.stratosphere:Log level: 20
    2016-09-29 13:59:58 INFO:root:Deployment already exists. Getting changes for dev-networks...
    --- Existing template

    +++ Proposed template

    @@ -23,3 +23,13 @@

       properties: {description: dev - asia-east1 Subnetwork, ipCidrRange: 10.128.128.0/20,
         name: dev-asia-east1-subnetwork, network: $(ref.dev-network.selfLink), region: asia-east1}
       type: compute.v1.subnetworks
    +- name: dev-network-internal-ssh
    +  properties:
    +    allowed:
    +    - IPProtocol: tcp
    +      ports: ['22']
    +    - {IPProtocol: icmp}
    +    name: dev-network-internal-ssh
    +    network: $(ref.dev-network.selfLink)
    +    sourceRanges: [10.128.0.0/14]
    +  type: compute.v1.firewall

    Continue? (yes/no)


Simply enter 'yes' and you'll have some firewall rules.

See the [example_templates](example_templates) directory for more template examples.

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
