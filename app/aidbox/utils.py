from dataclasses import dataclass

from fhirpy import AsyncFHIRClient

from app.sdc.utils import get_external_fhir_base_url_from_resource

from .sdk import sdk


def build_user_client(request, fhir_client, external_fhir_base_url=None):
    """Same base, authenticated by the caller's headers instead of the app's credentials."""
    headers = request["headers"].copy()

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

    user_client: AsyncFHIRClient
    # Points elsewhere only when the request names an external FHIR server for its data.
    data_client: AsyncFHIRClient
    route_params: dict
    resource: dict
    request: dict


def prepare_args(fn):
    def wrap(operation, request):
        route_client = resolve_fhir_client(operation, request)
        user_client = build_user_client(request, route_client)
        external_fhir_base_url = get_external_fhir_base_url_from_resource(request.get("resource"))
        data_client = (
            build_user_client(request, route_client, external_fhir_base_url)
            if external_fhir_base_url
            else user_client
        )
        request = AidboxSdcRequest(
            user_client,
            data_client,
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
