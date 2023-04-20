import logging
import os

import aiohttp_cors
import coloredlogs
import sentry_sdk
from aiohttp import web
from fhirpy.lib import AsyncFHIRClient
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

coloredlogs.install(level="DEBUG", fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logging.getLogger("aidbox_sdk").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)
logging.getLogger("faker").setLevel(logging.WARNING)

sentry_logging = LoggingIntegration(
    level=logging.DEBUG,  # Capture info and above as breadcrumbs
    event_level=logging.WARNING,  # Send warnings as events
)
sentry_sdk.init(integrations=[AioHttpIntegration(), sentry_logging])


async def create_gunicorn_app():
    if os.getenv("APP_ID") is None:
        return create_fhir_app()
    else:
        return create_app()


# TODO: Add config param for aidbox-python-sdk pytest plugin
# to select create_app
def create_app():
    from aidbox_python_sdk.main import init as init_aidbox_app
    from aidbox_python_sdk.main import setup_routes as setup_aidbox_app_routes

    from app.aidbox import sdk

    app = web.Application()
    app.cleanup_ctx.append(init_aidbox_app)
    app.update(
        settings=sdk.settings,
        sdk=sdk,
    )
    setup_aidbox_app_routes(app)
    return app


async def fhir_app_on_startup(app: web.Application):
    from app.fhir_server.settings import settings

    app["settings"] = settings
    app["client"] = AsyncFHIRClient(settings.BASE_URL, authorization=f"Basic {settings.AUTH_TOKEN}")


def create_fhir_app():
    from app.fhir_server.operations import routes as fhir_routes

    app = web.Application()
    app.add_routes(fhir_routes)
    app.on_startup.append(fhir_app_on_startup)

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        },
    )

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)

    return app
