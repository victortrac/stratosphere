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
