import os

from aidbox_python_sdk.settings import Required
from aidbox_python_sdk.settings import Settings as AidboxSettings

from app.utils import resolve_jute_service


class Settings(AidboxSettings):
    JUTE_SERVICE = Required(v_type=str)
    FHIRPATH_MAPPING_SERVICE = str


create_manifest_attrs = os.getenv("CREATE_MANIFEST_ATTRS", "True").lower() == "true"

if create_manifest_attrs:
    raise Exception(
        "CREATE_MANIFEST_ATTRS must be set to false, fhir-sdc@2.x.x does not support it"
    )


# Both behaviours are gone in 3.x.x; leaving the variable on would silently invert every constraint.
for removed_setting in ("CONSTRAINT_LEGACY_BEHAVIOR", "EXTRACT_SOURCE_QUERIES_LEGACY_BEHAVIOR"):
    if os.getenv(removed_setting, "").lower() == "true":
        raise Exception(f"{removed_setting} is not supported in fhir-sdc@3.x.x, see the README")

settings = Settings(
    JUTE_SERVICE=resolve_jute_service(),
    FHIRPATH_MAPPING_SERVICE=os.getenv("FHIRPATH_MAPPING_SERVICE"),
)
