from aiohttp import web
from aiohttp.test_utils import make_mocked_request

from app.fhir_server.settings import FHIRAppSettings
from app.fhir_server.utils import build_user_client


def test_user_client_forwards_the_callers_headers():
    app = web.Application()
    app["settings"] = FHIRAppSettings(BASE_URL="http://fhir.example/fhir")
    request = make_mocked_request(
        "POST",
        "/Questionnaire/$populate",
        headers={
            "Authorization": "Bearer caller-token",
            "X-Correlation-Id": "abc",
            "Host": "fhir-sdc.example",
            "Content-Length": "42",
            "Transfer-Encoding": "chunked",
        },
        app=app,
    )

    client = build_user_client(request)
    assert client.url == "http://fhir.example/fhir"
    assert client.extra_headers == {
        "Authorization": "Bearer caller-token",
        "X-Correlation-Id": "abc",
    }
