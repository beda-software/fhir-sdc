from aiohttp import web
from fhirpy.lib import AsyncFHIRClient
import app.fhir_server.operations  # noqa


async def default_handler(request: web.BaseRequest):
    client: AsyncFHIRClient = request.app["client"]
    client.authorization = request.headers["Authorization"]
    data = await request.json() if request.has_body else None
    result = await client.execute(
        request.path, method=request.method, data=data, params=request.query
    )

    return web.json_response(result)
