import pytest
from aiohttp import web

from app.fhir_server.operations import routes
from app.fhir_server.settings import FHIRAppSettings


@pytest.fixture
async def fhir_server_client(fhir_client, aiohttp_client):
    app = web.Application()
    app.add_routes(routes)
    app["client"] = fhir_client
    app["settings"] = FHIRAppSettings(
        JUTE_SERVICE="http://jute:8090/parse-template",
        FHIRPATH_MAPPING_SERVICE=None,
    )
    return await aiohttp_client(app)
