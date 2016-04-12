from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def get_google_auth(service, version='v2'):
    credentials = GoogleCredentials.get_application_default()
    dm = discovery.build(service, version, credentials=credentials)
    return dm


def get_latest_image(project, name):
    '''
    This attempts to return the latest image based on an search string.
    '''
    dm = get_google_auth('compute', 'v1')
    result = dm.images().list(project=project).execute()
    newest_image = None
    for image in result.get('items'):
        if image['name'].find(name):
            if not newest_image:
                newest_image = image
            else:
                if image['creationTimestamp'] > newest_image['creationTimestamp']:
                    newest_image = image
    return newest_image
