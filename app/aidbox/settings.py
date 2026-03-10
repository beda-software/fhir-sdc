import logging
import os

from aidbox_python_sdk.settings import Required
from aidbox_python_sdk.settings import Settings as AidboxSettings


class Settings(AidboxSettings):
    JUTE_SERVICE = Required(v_type=str)
    FHIRPATH_MAPPING_SERVICE = str


create_manifest_attrs = os.getenv("CREATE_MANIFEST_ATTRS", "True").lower() == "true"
constraint_legacy_behavior = (
    os.getenv("CONSTRAINT_LEGACY_BEHAVIOR", "True").lower() == "true"
)

if create_manifest_attrs:
    raise Exception(
        "CREATE_MANIFEST_ATTRS must be set to false, fhir-sdc@2.x.x does not support it"
    )

if constraint_legacy_behavior:
    logging.warning(
        "CONSTRAINT_LEGACY_BEHAVIOR is deprecated and will be enforced to be set to false in fhir-sdc@3.x.x"
    )


settings = Settings(
    JUTE_SERVICE=os.getenv("JUTE_SERVICE", "aidbox"),
    FHIRPATH_MAPPING_SERVICE=os.getenv("FHIRPATH_MAPPING_SERVICE"),
    # For legacy usage:
    # CONSTRAINT_LEGACY_BEHAVIOR - pre-save legacy behavior of constraint when then condition was reversed
    CONSTRAINT_LEGACY_BEHAVIOR=constraint_legacy_behavior,
)
