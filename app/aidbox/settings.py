import os

from aidbox_python_sdk.settings import Required
from aidbox_python_sdk.settings import Settings as AidboxSettings


class Settings(AidboxSettings):
    JUTE_SERVICE = Required(v_type=str)


settings = Settings(
    JUTE_SERVICE=os.getenv("JUTE_SERVICE", "aidbox"),
    CREATE_MANIFEST_ATTRS=os.getenv("CREATE_MANIFEST_ATTRS", "True"),
)
