async def from_first_class_extension(fce_resource, aidbox_client):
    fhir_resource = await aidbox_client.execute(
        "/$to-format/fhir", method="post", data=fce_resource, params=None
    )
    return fhir_resource.get("resource")


async def to_first_class_extension(fhir_resource, aidbox_client):
    fce_resource = await aidbox_client.execute(
        "/$to-format/aidbox", method="post", data=fhir_resource, params=None
    )
    return fce_resource.get("resource")
