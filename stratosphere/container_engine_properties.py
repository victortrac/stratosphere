try:
    from stratosphere.common import ResourceValidators
    from stratosphere.resources import GCPProperty
except ImportError:
    # Python2
    from common import ResourceValidators
    from resources import GCPProperty


class HorizontalPodAutoscalingProperty(GCPProperty):
    """
    Configuration options for the horizontal pod autoscaling feature, which increases or
    decreases the number of replica pods a replication controller has based on the resource
    usage of the existing pods.

    https://cloud.google.com/container-engine/reference/rest/v1/projects.zones.clusters#horizontalpodautoscaling

    """
    props = {
        'disabled': (bool, True)
    }


class HttpLoadBalancingProperty(GCPProperty):
    """
    Configuration options for the HTTP (L7) load balancing controller addon,
    which makes it easy to set up HTTP load balancers for services in a cluster.

    https://cloud.google.com/container-engine/reference/rest/v1/projects.zones.clusters#httploadbalancing
    """
    props = {
        'disabled': (bool, True)
    }


class AddonsConfigProperty(GCPProperty):
    """
    Configuration for the addons that can be automatically spun up in the cluster,
    enabling additional functionality.
    """
    props = {
        'horizontalPodAutoscaling': (HorizontalPodAutoscalingProperty, False),
        'httpLoadBalancing': (HttpLoadBalancingProperty, False)
    }


class MasterAuth(GCPProperty):
    """
    The authentication information for accessing the master endpoint.
    Authentication can be done using HTTP basic auth or using client certificates.

    https://cloud.google.com/container-engine/reference/rest/v1/projects.zones.clusters#addonsconfig
    """
    props = {
        'username': (str, True),
        'password': (str, True)
    }


class NodeConfigProperty(GCPProperty):
    IMAGE_TYPES = ['CONTAINER_VM', 'gci-dev', 'gci-beta', 'gci-stable']

    props = {
        'machineType': (str, False, ResourceValidators.is_valid_machine_type),
        'diskSizeGb': (int, False),
        'oauthScopes': ([str], False),
        'serviceAccount': (str, False),
        'metadata': (dict, False),
        'imageType': (str, False, IMAGE_TYPES),
        'localSsdCount': (int, False),
        'tags': ([str], False)
    }


class NodeManagementProperty(GCPProperty):
    """
    NodeManagement defines the set of node management services turned on for the node pool.

    https://cloud.google.com/container-engine/reference/rest/v1/projects.zones.clusters.nodePools#NodePool.NodeManagement
    """
    props = {
        'autoUpgrade': (bool, False),
        'autoRepair': (bool, False)
    }


class NodePoolAutoScalingProperty(GCPProperty):
    """
    NodePoolAutoscaling contains information required by cluster autoscaler to adjust the size of the node pool to the current cluster usage.

    https://cloud.google.com/container-engine/reference/rest/v1/projects.zones.clusters.nodePools#nodepoolautoscaling
    """
    props = {
        'enabled': (bool, True),
        'minNodeCount': (int, True),
        'maxNodeCount': (int, True)
    }

    def validator(self):
        assert self.properties.get('minNodeCount') < self.properties.get('maxNodeCount'), \
            ValueError('minNodeCount must be less than maxNodeCount.')


class NodePoolProperty(GCPProperty):
    props = {
        'name': (str, True, ResourceValidators.name),
        'config': (NodeConfigProperty, True),
        'initialNodeCount': (int, True),
        'autoscaling': (NodePoolAutoScalingProperty, False),
        'management': (NodeManagementProperty, False)
    }


class ClusterProperties(GCPProperty):
    LOGGING_SERVICES = ['logging.googleapis.com', 'none']
    MONITORING_SERVICES = ['monitoring.googleapis.com', 'none']
    LOCATIONS = [
        'us-west1-a',
        'us-west1-b',
        'us-central1-a',
        'us-central1-b',
        'us-central1-c',
        'us-central1-f',
        'us-east1-b',
        'us-east1-c',
        'us-east1-d',
        'europe-west1-b',
        'europe-west1-c',
        'europe-west1-d',
        'asia-east1-a',
        'asia-east1-b',
        'asia-east1-c'
    ]

    props = {
        'addonsConfig': (AddonsConfigProperty, False),
        'clusterIpv4Cidr': (str, False, ResourceValidators.ipAddress),
        'description': (str, False),
        'initialClusterVersion': (str, False),
        'initialNodeCount': (int, False),
        'locations': ([str], False, LOCATIONS),
        'loggingService': (str, False, LOGGING_SERVICES),
        'masterAuth': (MasterAuth, False),
        'monitoringService': (str, False, MONITORING_SERVICES),
        'network': (str, False, ResourceValidators.name),  # name of the compute engine network
        'nodeConfig': (NodeConfigProperty, False),
        'nodePools': ([NodePoolProperty], False),
        'subnetwork': (str, True, ResourceValidators.name),
    }

    def validator(self):
        # Require either nodePools or (nodeConfig and initialNodeCount)
        if not (self.properties.get('nodePools') or
                (self.properties.get('initialNodeCount') and self.properties.get('nodeConfig'))):
            raise ValueError('Either nodePools or (nodeConfig and initialNodeCount) are required.')

        if (self.properties.get('initialNodeCount') or self.properties.get('nodeConfig')) \
                and self.properties.get('nodePools'):
            raise ValueError('nodePools can not be used in with initialNodeCount or nodeConfig.')
