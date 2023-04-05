import logging

import coloredlogs
import sentry_sdk
from aidbox_python_sdk.main import init as init_aidbox_app
from aidbox_python_sdk.main import setup_routes as setup_aidbox_app_routes
from aiohttp import web
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from app.aidbox import sdk

coloredlogs.install(level="DEBUG", fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logging.getLogger("aidbox_sdk").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)

sentry_logging = LoggingIntegration(
    level=logging.DEBUG,  # Capture info and above as breadcrumbs
    event_level=logging.WARNING,  # Send warnings as events
)
sentry_sdk.init(integrations=[AioHttpIntegration(), sentry_logging])


def create_app():
    app = web.Application()
    app.cleanup_ctx.append(init_aidbox_app)
    app.update(
        settings=sdk.settings,
        sdk=sdk,
    )
    setup_aidbox_app_routes(app)
    return app


async def create_gunicorn_app():
    return create_app()
