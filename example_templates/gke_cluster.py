from stratosphere.resources import Template
from stratosphere.container_engine import Cluster
from stratosphere.container_engine_properties import AddonsConfigProperty, ClusterProperties, \
    HorizontalPodAutoscalingProperty, HttpLoadBalancingProperty, \
    NodeManagementProperty, NodePoolProperty, NodePoolAutoScalingProperty, NodeConfigProperty

import constants


class GKECluster(Template):
    """
    Creates a Container Engine cluster.  This template, as written, assumes
    that constants contains a structure like this:

    ENV = {
        "dev": {
            'gke_clusters': [
                {
                    'name': 'my-cluster',
                    'zone': 'us-central1-b',  #  Primary zone
                    'subnetwork': 'us-central1',
                    'locations': ['us-central1-a', 'us-central1-b', 'us-central1-c'], #  Additional zones. Not required.
                    'nodepools': [
                        {
                            'name': 'pool-1',
                            'node_count': 1,
                            'machine_type': 'f1-micro',
                            'disk_size': 20,
                        }
                    ]
                }
            ]
        }
    }

    https://cloud.google.com/container-engine/reference/rest/v1/projects.zones.clusters/create
    """
    TEMPLATE_TYPE = 'gke-cluster'

    def configure(self):
        for cluster in constants.ENV[self.env]['gke_clusters']:
            _cluster = Cluster(
                name='{}-{}-cluster'.format(self.env, cluster.get('name')),
                zone=cluster.get('zone'),
                cluster=ClusterProperties(
                    addonsConfig=AddonsConfigProperty(
                        horizontalPodAutoscaling=HorizontalPodAutoscalingProperty(disabled=False),
                        httpLoadBalancing=HttpLoadBalancingProperty(disabled=False)
                    ),
                    description='{} {} GKE Cluster'.format(self.env, cluster.get('name')),
                    initialClusterVersion='1.6.2',
                    network='{}-network'.format(self.env),
                    nodePools=[
                        NodePoolProperty(
                            name='{}-{}'.format(cluster.get('name'), nodepool.get('name')),
                            autoscaling=NodePoolAutoScalingProperty(
                                enabled=True,
                                minNodeCount=1,
                                maxNodeCount=20
                            ),
                            config=NodeConfigProperty(
                                machineType=nodepool.get('machine_type'),
                                diskSizeGb=nodepool.get('disk_size'),
                                # see https://developers.google.com/identity/protocols/googlescopes
                                oauthScopes=[
                                    "https://www.googleapis.com/auth/userinfo.email",
                                    "https://www.googleapis.com/auth/compute",
                                    "https://www.googleapis.com/auth/devstorage.read_write",
                                    "https://www.googleapis.com/auth/taskqueue",
                                    "https://www.googleapis.com/auth/bigquery",
                                    "https://www.googleapis.com/auth/datastore",
                                    "https://www.googleapis.com/auth/logging.write",
                                    "https://www.googleapis.com/auth/monitoring",
                                    "https://www.googleapis.com/auth/cloud-platform",
                                    "https://www.googleapis.com/auth/bigtable.data",
                                    "https://www.googleapis.com/auth/pubsub",
                                    "https://www.googleapis.com/auth/servicecontrol",
                                    "https://www.googleapis.com/auth/service.management",
                                    "https://www.googleapis.com/auth/trace.append",
                                    "https://www.googleapis.com/auth/source.read_write"
                                ]
                            ),
                            initialNodeCount=nodepool.get('node_count'),
                            management=NodeManagementProperty(
                                autoUpgrade=True,
                                autoRepair=True
                            )
                        )
                        for nodepool in cluster.get('nodepools')
                    ],
                    subnetwork='{}-{}-subnetwork'.format(self.env, cluster.get('subnetwork')),
                    locations=cluster.get('locations')
                )
            )

            self.add_resource(_cluster)


