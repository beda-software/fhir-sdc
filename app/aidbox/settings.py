import os

from aidbox_python_sdk.settings import Required
from aidbox_python_sdk.settings import Settings as AidboxSettings


class Settings(AidboxSettings):
    JUTE_SERVICE = Required(v_type=str)
    FHIRPATH_MAPPING_SERVICE = str


create_manifest_attrs = os.getenv("CREATE_MANIFEST_ATTRS", "True").lower() == "true"

if create_manifest_attrs:
    raise Exception(
        "CREATE_MANIFEST_ATTRS must be set to false, fhir-sdc@2.x.x does not support it"
    )


settings = Settings(
    JUTE_SERVICE=os.getenv("JUTE_SERVICE", "aidbox"),
    FHIRPATH_MAPPING_SERVICE=os.getenv("FHIRPATH_MAPPING_SERVICE"),
)
