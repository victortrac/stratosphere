import imp
import os
import sys

import click
from googleapiclient import discovery, errors
from oauth2client.client import GoogleCredentials

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

credentials = GoogleCredentials.get_application_default()
dm = discovery.build('deploymentmanager', 'v2', credentials=credentials)


def is_deployment(project, name):
    deployments = dm.deployments().list(project=project).execute().get('deployments')
    if deployments and name in [d['name'] for d in deployments]:
        return True
    return False


def create_deployment(project, template):
    # context = Context(project, name)
    # deployment_yaml = template.GenerateConfig(context)
    template.configure()
    body = {
        'name': template.name,
        'description': 'project: {}, name: {}'.format(project, template.name),
        'target': {
            'config': {
                'content': unicode(template)
            }
        }
    }
    try:
        result = dm.deployments().insert(project=project, body=body).execute()
    except errors.HttpError as e:
        raise e


def update_deployment(project, name, template):
    pass


def load_template_module(module_path):
    try:
        if os.path.isfile(module_path):
            path, filename = os.path.split(os.path.abspath(module_path))
            module_name = filename.split('.')[0].lower()
            sys.path.append(os.path.dirname(module_path))
            return imp.load_source(module_name, module_path).get_class()
        raise TypeError
    except TypeError:
        raise ImportError('Unable to import module: {}'.format(module_path))


@click.command()
@click.option('--project', prompt='Your GCP Project', help='GCP project where to put resources.')
@click.option('--env', prompt='Deployment env', help='Env of deployment. Used for generating the deployment name: [env]-[template]')
@click.option('--action', prompt="Deployment action", default='create',
                type=click.Choice(['create', 'update', 'template', 'delete']), help="What you want to do with this template")
@click.argument('template_path', type=click.Path(exists=True), required=False)
def main(project, env, action, template_path):
    if action in ['create', 'update', 'template']:
        template_class = load_template_module(template_path)
        template = template_class(env)
        if action == 'create':
            if is_deployment(project, template.name):
                click.echo('Deployment {} already exists. Exiting..'.format(template.name))
                sys.exit(1)
            else:
                create_deployment(project, template)
        elif action == 'update':
            if is_deployment(project, template.name):
                update_deployment(project, template)
            else:
                click.echo('Deployment {} does not exist'.format(template.name))
                sys.exit(1)
        elif action == 'template':
            print(template)
            sys.exit(0)


if __name__ == '__main__':
    main()
