from aidbox_python_sdk.sdk import SDK
from aidbox_python_sdk.settings import Settings

from app.manifest import entities, meta_resources, seeds, migrations


sdk_settings = Settings(**{})
sdk = SDK(
    sdk_settings,
    entities=entities,
    resources=meta_resources,
    seeds=seeds,
    migrations=migrations)
