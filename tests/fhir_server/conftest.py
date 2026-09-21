import os

import pytest
from aiohttp import web

from app.fhir_server.middlewares import render_operation_outcome
from app.fhir_server.operations import routes
from app.fhir_server.settings import FHIRAppSettings


@pytest.fixture
async def fhir_server_client(fhir_client, aiohttp_client):
    app = web.Application(middlewares=[render_operation_outcome])
    app.add_routes(routes)
    app["client"] = fhir_client
    app["settings"] = FHIRAppSettings(
        JUTE_SERVICE="http://jute:8090/parse-template",
        FHIRPATH_MAPPING_SERVICE=os.getenv("FHIRPATH_MAPPING_SERVICE"),
    )
    return await aiohttp_client(app)
