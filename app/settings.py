import os

from aidbox_python_sdk.settings import Required
from aidbox_python_sdk.settings import Settings as AidboxSettings


class Settings(AidboxSettings):
    SDC_VERSION = Required(v_type=str)
    JUTE_SERVICE = Required(v_type=str)


settings = Settings(
    SDC_VERSION=os.getenv("SDC_VERSION", "2.7.0"), JUTE_SERVICE=os.getenv("JUTE_SERVICE", "aidbox")
)
