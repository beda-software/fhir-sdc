from aidbox_python_sdk.aidboxpy import AsyncAidboxClient
from fhirpy import AsyncFHIRClient


def get_user_sdk_client(request):
    headers = request["headers"].copy()
    client = request["app"]["client"]

    # We removed content-length because populate extract are post operations
    # and post queries contains content-length that must not be set as default header
    if "content-length" in headers:
        headers.pop("content-length")

    return AsyncAidboxClient(client.url, extra_headers=headers)


def get_aidbox_fhir_client(aidbox_client):
    return AsyncFHIRClient(
        f"{aidbox_client.url}/fhir",
        authorization=aidbox_client.authorization,
        extra_headers=aidbox_client.extra_headers,
    )
