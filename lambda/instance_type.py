EC2_INSTANCE_TYPES = {
    "t2.micro": {
        "memory": "1 GiB",
        "storage": "EBS only",
        "pricing": {
            "On-Demand": "$0.0116 per hour",
            "Spot": "$0.0042 per hour"
        }
    },
    "t2.small": {
        "memory": "2 GiB",
        "storage": "EBS only",
        "pricing": {
            "On-Demand": "$0.023 per hour",
            "Spot": "$0.0075 per hour"
        }
    },
    "t2.medium": {
        "memory": "4 GiB",
        "storage": "EBS only",
        "pricing": {
            "On-Demand": "$0.0464 per hour",
            "Spot": "$0.0141 per hour"
        }
    }
}