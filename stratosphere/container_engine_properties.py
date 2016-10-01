from stratosphere.common import ResourceValidators
from stratosphere.resources import GCPProperty


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
        'httpLoadBalancing': (HttpLoadBalancingProperty, False),
        'horizontalPodAutoscaling': (HorizontalPodAutoscalingProperty, False)
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
    IMAGE_TYPES = ['container_vm', 'gci-dev', 'gci-beta', 'gci-stable']

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
    resource_type = 'container.v1.cluster'

    props = {
        'name': (str, True, ResourceValidators.name),
        'config': (NodeConfigProperty, True),
        'initialNodeCount': (int, True),
        'autoscaling': (NodePoolAutoScalingProperty, False)
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
        'description': (str, False),
        'initialNodeCount': (int, True),
        'nodeConfig': (NodeConfigProperty, False),
        'masterAuth': (MasterAuth, False),
        'loggingService': (str, False, LOGGING_SERVICES),
        'monitoringService': (str, False, MONITORING_SERVICES),
        'network': (str, False, ResourceValidators.name),  # name of the compute engine network
        'clusterIpv4Cidr': (str, False, ResourceValidators.ipAddress),
        'addonsConfig': (AddonsConfigProperty, False),
        'subnetwork': (str, True, ResourceValidators.name),
        'nodePools': ([NodePoolProperty], False),
        'locations': ([str], True, LOCATIONS),
    }

    def validator(self):
        # Must only specific initialNodeCount or nodePool
        if (self.properties.get('initialNodeCount') or self.properties.get('nodeConfig')) \
                and self.properties.get('nodePools'):
            raise ValueError('nodePools can not be used in with initialNodeCount or nodeConfig')

