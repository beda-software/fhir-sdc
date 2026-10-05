import os

import simplejson as json
from aiohttp import web
from fhirpy import AsyncFHIRClient

# The incoming request's own framing and addressing; forwarding them would describe the wrong request.
NOT_FORWARDED_HEADERS = {"content-length", "host", "transfer-encoding"}


def resolve_jute_service():
    jute_service = os.getenv("JUTE_SERVICE", "")
    if jute_service.lower() == "aidbox":
        raise Exception(
            "Aidbox no longer renders JUTE mappers; JUTE_SERVICE must point at a service"
        )

    return jute_service


def resolve_fhirpath_service():
    fhirpath_service = os.getenv("FHIRPATH_MAPPING_SERVICE", "")
    # `fpml` names the in-process renderer, every other value is a service url.
    return "fpml" if fhirpath_service.lower() == "fpml" else fhirpath_service


def get_extract_services(app):
    jute_service = app["settings"].JUTE_SERVICE
    fhir_mapping_service = app["settings"].FHIRPATH_MAPPING_SERVICE
    return {"JUTE": jute_service, "FHIRPath": fhir_mapping_service}


def build_user_client(headers, base_url) -> AsyncFHIRClient:
    """A client at base_url authenticated by the caller's own headers, never the app's credentials."""
    forwarded = {
        name: value for name, value in headers.items() if name.lower() not in NOT_FORWARDED_HEADERS
    }
    return AsyncFHIRClient(base_url, extra_headers=forwarded)


def render_json(result) -> web.Response:
    """simplejson keeps the Decimals that FHIRPath and the mappers produce."""
    return web.json_response(result, dumps=json.dumps)
