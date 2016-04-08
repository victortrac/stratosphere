import datetime
import importlib
import inspect
import os
import sys
import time

import click
from googleapiclient import discovery, errors
from oauth2client.client import GoogleCredentials

from resources import Template


credentials = GoogleCredentials.get_application_default()
dm = discovery.build('deploymentmanager', 'v2', credentials=credentials)


def get_deployment(project, deployment):
    try:
        result = dm.deployments().get(project=project, deployment=deployment).execute()
        return result
    except errors.HttpError as e:
        if e.resp['status'] == '404':
            return None
        else:
            raise e

def wait_for_completion(project, result):
    print('Waiting for deployment {}...'.format(result['name']))
    last_event = result
    failed = False
    while not last_event['status'] in ['DONE', ]:
        time.sleep(1)
        last_event = dm.operations().get(project=project, operation=last_event['name']).execute()
        print('{} Operation: {name}, TargetLink: {targetLink}, Progress: {progress}, Status: {status}'.
              format(datetime.datetime.now().isoformat(), **last_event))
        if last_event['status'] == 'Failed':
            failed = True
    if failed:
        print('*** Stack apply failed! ***')
    else:
        print('Stack action complete.')


def apply_deployment(project, template):
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
        deployment = get_deployment(project, template.name)
        if deployment:
            print('Deployment already exists. Updating {}...'.format(template.name))
            body['fingerprint'] = deployment.get('fingerprint')
            result = dm.deployments().update(project=project, deployment=template.name, body=body).execute()
        else:
            print('Launching a new deployment: {}...'.format(template.name))
            result = dm.deployments().insert(project=project, body=body).execute()
    except errors.HttpError as e:
        raise e

    if result:
        return wait_for_completion(project, result)


def load_template_module(module_path):
    try:
        if os.path.isfile(module_path):
            path, filename = os.path.split(os.path.abspath(module_path))
            module_name = filename.split('.')[0].lower()
            sys.path.append(os.path.dirname(module_path))
            module = importlib.import_module(module_name)
            # Discover what the template class is from a template module.
            template_class = [r[1] for r in inspect.getmembers(module, inspect.isclass)
                              if r[0] != 'Template' and issubclass(r[1], Template)][0]
            return template_class
        raise TypeError
    except TypeError:
        raise ImportError('Unable to import module: {}'.format(module_path))


@click.command()
@click.option('--project', prompt='Your GCP Project', help='GCP project where to put resources.')
@click.option('--env', prompt='Deployment env', help='Env of deployment. Used for generating the deployment name: [env]-[template]')
@click.option('--action', prompt="Deployment action", default='template',
                type=click.Choice(['apply', 'template', 'delete']), help="What you want to do with this template")
@click.argument('template_path', type=click.Path(exists=True), required=False)
def main(project, env, action, template_path):
    if action in ['apply', 'template']:
        template_class = load_template_module(template_path)
        template = template_class(env)
        if action == 'apply':
            template.__repr__()
            apply_deployment(project, template)
        elif action == 'template':
            print(template)
            sys.exit(0)


if __name__ == '__main__':
    main()
