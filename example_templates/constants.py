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
            }
        ],
        'gke_clusters': [
            {
                'name': 'my-cluster',
                'zone': 'us-central1-b',  #  Primary zone
                'subnetwork': 'us-central1',
                'locations': ['us-central1-a', 'us-central1-b', 'us-central1-c'],  #  Additional zones. Not required.
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
            }
        ]
    }
}
