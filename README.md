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

Instead of ```--action template```, ```--action create``` can be used instead to actually insert
the template into Google Deployment Manager via API.



## License

Apache 2.0 - See [LICENSE](LICENSE) for more information.