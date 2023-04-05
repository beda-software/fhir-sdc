from aidbox_python_sdk.sdk import SDK

from app.settings import settings

from .manifest import meta_resources_v2_7_0, meta_resources_v3_0_0

resources = meta_resources_v3_0_0 if settings.SDC_VERSION == "3.0.0" else meta_resources_v2_7_0
sdk = SDK(settings, resources=resources)
