from stratosphere.common import ResourceValidators
from stratosphere.resources import GCPResource
from stratosphere.container_engine_properties import ClusterProperties, NodeConfigProperty, NodePoolAutoScalingProperty



class Cluster(GCPResource):
    """
    A Google Container Engine Cluster

    https://cloud.google.com/container-engine/reference/rest/v1/projects.zones.clusters#resource-cluster
    """
    resource_type = 'container.v1.cluster'

    # The cluster API is different from the other GCP APIs.  Doesn't accept a 'name' field
    # as a property field. Sigh google.
    INCLUDE_NAME_PROPERTY = False

    props = {
        'name': (str, True, ResourceValidators.name),
        'zone': (str, True),
        'cluster': (ClusterProperties, True)
    }

    def validator(self):
        locations = self.properties.get('cluster').properties.get('locations')
        if locations:
            if not set([self.properties.get('zone')]) <= set(locations):
                raise ValueError('zone property must be included in locations.')
