from dataclasses import dataclass

from aidbox_python_sdk.aidboxpy import AsyncAidboxClient
from fhirpy import AsyncFHIRClient
from fhirpy.base import AsyncClient

from .sdk import sdk


def get_user_sdk_client(request, client=None, external_fhir_base_url=None):
    headers = request["headers"].copy()
    client = client or request["app"]["client"]

    # We removed content-length because populate extract are post operations
    # and post queries contains content-length that must not be set as default header
    if "content-length" in headers:
        headers.pop("content-length")

    url = external_fhir_base_url or client.url

    return type(client)(url, extra_headers=headers)


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


def get_clients(operation, request):
    aidbox_client = request["app"]["client"]
    if operation["request"][1] == "Organization":
        is_fhir = True
        fhir_client = get_organization_client(aidbox_client, request["route-params"]["org_id"])
    else:
        is_fhir = operation["request"][1] == "fhir"
        fhir_client = get_aidbox_fhir_client(aidbox_client)
    return is_fhir, aidbox_client, fhir_client, fhir_client if is_fhir else aidbox_client


@dataclass
class AidboxSdcRequest:
    """
    Representation of SDC specific data
    extracted from original aidbox request
    """

    is_fhir: bool
    aidbox_client: AsyncAidboxClient
    fhir_client: AsyncFHIRClient
    client: AsyncClient
    route_params: dict
    resource: dict
    request: dict


def prepare_args(fn):
    def wrap(operation, request):
        is_fhir, aidbox_client, fhir_client, client = get_clients(operation, request)
        request = AidboxSdcRequest(
            is_fhir,
            aidbox_client,
            fhir_client,
            client,
            request["route-params"],
            request.get("resource", None),
            request,
        )
        return fn(request)

    return wrap


def aidbox_operation(method, path, **kwrgs):
    def register(fn):
        sdk.operation(method, ["Organization", {"name": "org_id"}, "fhir"] + path, **kwrgs)(fn)
        sdk.operation(method, path, **kwrgs)(fn)
        sdk.operation(method, ["fhir"] + path, **kwrgs)(fn)
        return fn

    return register
