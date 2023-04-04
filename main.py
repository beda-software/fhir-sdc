import logging

import coloredlogs
import sentry_sdk
from aidbox_python_sdk.main import create_app as _create_app
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

# Don't remove these imports
import app.operations
from app.sdk import sdk

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
    return _create_app(sdk)
