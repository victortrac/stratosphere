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


## Examples
See the examples_templates directory for how to build a template.

    # stratosphere --project [GCP Project name] --env dev --action template ./templates/networks.py
