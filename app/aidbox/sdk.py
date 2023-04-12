from aidbox_python_sdk.sdk import SDK

from app.settings import settings

from .manifest import manifest

sdk = SDK(settings, resources=manifest)
