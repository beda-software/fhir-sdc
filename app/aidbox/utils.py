from dataclasses import dataclass

from fhirpy import AsyncFHIRClient

from app.sdc.utils import get_external_fhir_base_url_from_resource
from app.utils import build_user_client

from .sdk import sdk


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

    # The caller, at our Aidbox; rebuild_at_external_fhir_base_url moves it to the caller's data server.
    user_client: AsyncFHIRClient
    route_params: dict
    resource: dict
    request: dict


def prepare_args(fn):
    def wrap(operation, request):
        route_client = resolve_fhir_client(operation, request)
        request = AidboxSdcRequest(
            build_user_client(request["headers"], route_client.url),
            request["route-params"],
            request.get("resource", None),
            request,
        )
        return fn(request)

    return wrap


def rebuild_at_external_fhir_base_url(user_client, resource):
    """The same caller's client at the request's externalFhirBaseUrl, when it names one."""
    external_fhir_base_url = get_external_fhir_base_url_from_resource(resource)
    if not external_fhir_base_url:
        return user_client

    return AsyncFHIRClient(external_fhir_base_url, extra_headers=user_client.extra_headers)


def aidbox_operation(method, path, **kwrgs):
    def register(fn):
        sdk.operation(method, ["Organization", {"name": "org_id"}, "fhir"] + path, **kwrgs)(fn)
        sdk.operation(method, ["fhir"] + path, **kwrgs)(fn)
        return fn

    return register
