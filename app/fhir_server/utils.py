from aiohttp import web
from fhirpy import AsyncFHIRClient

# The incoming request's own framing and addressing; forwarding them would describe the wrong request.
NOT_FORWARDED_HEADERS = {"content-length", "host", "transfer-encoding"}


def build_user_client(request: web.Request) -> AsyncFHIRClient:
    headers = {
        name: value
        for name, value in request.headers.items()
        if name.lower() not in NOT_FORWARDED_HEADERS
    }
    return AsyncFHIRClient(request.app["settings"].BASE_URL, extra_headers=headers)
