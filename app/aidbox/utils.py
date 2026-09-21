from dataclasses import dataclass

from fhirpy import AsyncFHIRClient

from .sdk import sdk


def build_user_client(request, fhir_client=None, external_fhir_base_url=None):
    """Same base, authenticated by the caller's headers instead of the app's credentials."""
    headers = request["headers"].copy()
    fhir_client = fhir_client or request["app"]["client"]

    # We removed content-length because populate extract are post operations
    # and post queries contains content-length that must not be set as default header
    if "content-length" in headers:
        headers.pop("content-length")

    url = external_fhir_base_url or fhir_client.url

    return type(fhir_client)(url, extra_headers=headers)


def get_aidbox_fhir_client(aidbox_client):
    return AsyncFHIRClient(
        f"{aidbox_client.url}/fhir",
        authorization=aidbox_client.authorization,
        extra_headers=aidbox_client.extra_headers,
    )


def get_organization_client(aidbox_client, organization):
    if isinstance(organization, str):
        org_id = organization
    else:
        org_id = organization.id
    return AsyncFHIRClient(
        f"{aidbox_client.url}/Organization/{org_id}/fhir/",
        authorization=aidbox_client.authorization,
        extra_headers=aidbox_client.extra_headers,
    )


def resolve_fhir_client(operation, request):
    aidbox_client = request["app"]["client"]
    if operation["request"][1] == "Organization":
        return get_organization_client(aidbox_client, request["route-params"]["org_id"])

    return get_aidbox_fhir_client(aidbox_client)


@dataclass
class AidboxSdcRequest:
    """
    Representation of SDC specific data
    extracted from original aidbox request
    """

    fhir_client: AsyncFHIRClient
    route_params: dict
    resource: dict
    request: dict


def prepare_args(fn):
    def wrap(operation, request):
        request = AidboxSdcRequest(
            resolve_fhir_client(operation, request),
            request["route-params"],
            request.get("resource", None),
            request,
        )
        return fn(request)

    return wrap


def aidbox_operation(method, path, **kwrgs):
    def register(fn):
        sdk.operation(method, ["Organization", {"name": "org_id"}, "fhir"] + path, **kwrgs)(fn)
        sdk.operation(method, ["fhir"] + path, **kwrgs)(fn)
        return fn

    return register
