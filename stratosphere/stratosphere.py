import datetime
import importlib
import inspect
import logging
import os
import pprint
import sys
import time

import click
from googleapiclient import errors

from resources import Template
from utils import get_google_auth


logger = logging.getLogger(__name__)

dm = get_google_auth('deploymentmanager', 'v2')

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
    while not last_event['status'] in ['DONE', ]:
        time.sleep(1)
        last_event = dm.operations().get(project=project, operation=last_event['name']).execute()
        logger.info('Operation: {name}, TargetLink: {targetLink}, Progress: {progress}, Status: {status}'
                    .format(**last_event))
    if len(last_event.get('error', [])):
        logging.error('*** Stack apply failed! ***')
        logging.fatal(pprint.pprint(last_event))
        sys.exit(1)
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
            logging.info('Deployment already exists. Updating {}...'.format(template.name))
            body['fingerprint'] = deployment.get('fingerprint')
            result = dm.deployments().update(project=project, deployment=template.name, body=body).execute()
        else:
            logging.info('Launching a new deployment: {}...'.format(template.name))
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
@click.option('--env', prompt='Deployment env',
              help='Env of deployment. Used for generating the deployment name: [env]-[template]')
@click.option('--action', prompt="Deployment action", default='template',
              type=click.Choice(['apply', 'template', 'delete']), help="What you want to do with this template")
@click.option('-v', '--verbose', required=False, default=0, count=True,
              help="Enable verbose logging, supply multiple for more logging")
@click.argument('template_path', type=click.Path(exists=True), required=False)
def main(project, env, action, verbose, template_path):

    if verbose >= 2:
        level = 5
    elif verbose == 1:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.addLevelName(5, "TRACE")

    logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', level=level)

    logger.debug('Debug log enabled')
    logger.info("Log level: {}".format(level))

    if action in ['apply', 'template']:
        template_class = load_template_module(template_path)
        template = template_class(project, env)
        if action == 'apply':
            template.__repr__()
            apply_deployment(project, template)
        elif action == 'template':
            t = template.__repr__()
            logger.info('Template successfully rendered, printing to stdout...')
            print(t)
            sys.exit(0)


if __name__ == '__main__':
    main()
