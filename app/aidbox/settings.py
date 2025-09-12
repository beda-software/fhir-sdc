import os

from aidbox_python_sdk.settings import Required
from aidbox_python_sdk.settings import Settings as AidboxSettings


class Settings(AidboxSettings):
    JUTE_SERVICE = Required(v_type=str)
    FHIRPATH_MAPPING_SERVICE = str


settings = Settings(
    JUTE_SERVICE=os.getenv("JUTE_SERVICE", "aidbox"),
    FHIRPATH_MAPPING_SERVICE=os.getenv("FHIRPATH_MAPPING_SERVICE"),
)
