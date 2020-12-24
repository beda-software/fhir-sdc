def create_parameters(**payload):
    return {
        "resourceType": "Parameters",
        "parameter": [
            {"name": name, "resource": resource} for name, resource in payload.items()
        ],
    }