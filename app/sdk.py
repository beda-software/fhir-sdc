import os
import app.manifest
from aidbox_python_sdk.sdk import SDK
from aidbox_python_sdk.settings import Settings

sdc_version = os.getenv('SDC_VERSION')
sdk_settings = Settings()

resources = app.manifest.meta_resources_v3_0_0 if sdc_version == '3.0.0' else app.manifest.meta_resources_v2_7_0
sdk = SDK(sdk_settings, resources=resources)
