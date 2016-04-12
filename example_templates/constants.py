ENV = {
    "dev": {
        "cidr": "10.100.0.0/16",
        "subnetworks": [
            {
                "zone": "us-central1-b",
                "cidr": "10.100.0.0/20"
            },
            {
                "zone": "us-central1-c",
                "cidr": "10.100.16.0/20"
            },
            {
                "zone": "us-central1-f",
                "cidr": "10.100.32.0/20"
            }
        ]
    },
    "prod": {
        "cidr": "10.200.0.0/16",
        "subnetworks": [
            {
                "zone": "us-central1-b",
                "cidr": "10.200.0.0/20"
            },
            {
                "zone": "us-central1-c",
                "cidr": "10.200.16.0/20"
            },
            {
                "zone": "us-central1-f",
                "cidr": "10.200.32.0/20"
            }
        ]
    }
}