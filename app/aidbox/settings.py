import os

from aidbox_python_sdk.settings import Required
from aidbox_python_sdk.settings import Settings as AidboxSettings


class Settings(AidboxSettings):
    JUTE_SERVICE = Required(v_type=str)
    FHIRPATH_MAPPING_SERVICE = str


settings = Settings(
    JUTE_SERVICE=os.getenv("JUTE_SERVICE", "aidbox"),
    FHIRPATH_MAPPING_SERVICE=os.getenv("FHIRPATH_MAPPING_SERVICE"),

    # For legacy usage:
    # CREATE_MANIFEST_ATTRS - if beda-emr-core profile is not used
    CREATE_MANIFEST_ATTRS=os.getenv("CREATE_MANIFEST_ATTRS", "True").lower() == "true",
    # CONSTRAINT_LEGACY_BEHAVIOR - pre-save legacy behavior of constraint when then condition was reversed
    CONSTRAINT_LEGACY_BEHAVIOR=os.getenv("CONSTRAINT_LEGACY_BEHAVIOR", "True").lower()
    == "true",

    EXTRACT_TIMEOUT=int(os.getenv("EXTRACT_TIMEOUT", "60000")),
)
