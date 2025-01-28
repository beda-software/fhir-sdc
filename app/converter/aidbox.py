import simplejson as json


async def from_first_class_extension(fce_resource, aidbox_client):
    fhir_resource = await aidbox_client.execute(
        "/$to-format/fhir", method="post", data=json.loads(json.dumps(fce_resource)), params=None
    )
    return fhir_resource.get("resource")


async def to_first_class_extension(fhir_resource, aidbox_client):
    fce_resource = await aidbox_client.execute(
        "/$to-format/aidbox", method="post", data=json.loads(json.dumps(fhir_resource)), params=None
    )
    return fce_resource.get("resource")
