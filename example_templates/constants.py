ENV = {
    "dev": {
        "cidr": "10.128.0.0/14",
        "subnetworks": [
            {
                "region": "us-central1",
                "cidr": "10.128.0.0/20"
            },
            {
                "region": "us-west1",
                "cidr": "10.128.32.0/20"
            },
            {
                "region": "us-east1",
                "cidr": "10.128.64.0/20"
            },
            {
                "region": "europe-west1",
                "cidr": "10.128.96.0/20"
            },
            {
                "region": "asia-east1",
                "cidr": "10.128.128.0/20"
            },
            {
                "region": "asia-northeast1",
                "cidr": "10.128.160.0/20"
            },
            {
                "region": "asia-southeast1",
                "cidr": "10.128.192.0/20"
            },
            {
                "region": "us-east4",
                "cidr": "10.128.224.0/20"
            }
        ],
        'gke_clusters': [
            {
                'name': 'cluster1',
                'zone': 'us-central1-b',  #  Primary zone
                'subnetwork': 'us-central1',
                'locations': ['us-central1-a', 'us-central1-b', 'us-central1-c'],  #  Additional zones. Not required.
                'nodepools': [
                    {
                        'name': 'pool1',
                        'node_count': 1,
                        'machine_type': 'g1-small',
                        'disk_size': 20,
                    }
                ]
            }
        ],
        'nfs-server': {
            'zone': 'us-central1-b',
            'machine_type': 'n1-standard-1'
        }
    },
    "prod": {
        "cidr": "10.136.0.0/14",
        "subnetworks": [
            {
                "region": "us-central1",
                "cidr": "10.136.0.0/20"
            },
            {
                "region": "us-west1",
                "cidr": "10.136.32.0/20"
            },
            {
                "region": "us-east1",
                "cidr": "10.136.64.0/20"
            },
            {
                "region": "europe-west1",
                "cidr": "10.136.96.0/20"
            },
            {
                "region": "asia-east1",
                "cidr": "10.136.128.0/20"
            },
            {
                "region": "asia-northeast1",
                "cidr": "10.136.160.0/20"
            },
            {
                "region": "asia-southeast1",
                "cidr": "10.136.192.0/20"
            },
            {
                "region": "us-east4",
                "cidr": "10.136.224.0/20"
            }
        ],
        'gke_clusters': [
            {
                'name': 'cluster1',
                'zone': 'us-central1-b',  #  Primary zone
                'subnetwork': 'us-central1',
                'locations': ['us-central1-a', 'us-central1-b', 'us-central1-c'],  #  Additional zones. Not required.
                'nodepools': [
                    {
                        'name': 'pool1',
                        'node_count': 1,
                        'machine_type': 'g1-small',
                        'disk_size': 20,
                    }
                ]
            }
        ],
        'nfs-server': {
            'zone': 'us-central1-b',
            'machine_type': 'n1-standard-1'
        }
    }
}
