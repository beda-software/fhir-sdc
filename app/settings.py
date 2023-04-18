import os

from aidbox_python_sdk.settings import Required
from aidbox_python_sdk.settings import Settings as AidboxSettings


class Settings(AidboxSettings):
    JUTE_SERVICE = Required(v_type=str)


class FHIRAppSettings:
    def __init__(self, **custom_settings):
        self._custom_settings = custom_settings
        for name, value in custom_settings.items():
            # if not hasattr(self, name):
            #     raise TypeError('{} is not a valid setting name'.format(name))
            setattr(self, name, value)


settings = Settings(
    JUTE_SERVICE=os.getenv("JUTE_SERVICE", "aidbox")
)

fhir_app_settings = FHIRAppSettings(
    JUTE_SERVICE=os.getenv("JUTE_SERVICE", "http://jute:8090/parse-template"),
    BASE_URL=os.getenv("BASE_URL", "http://devbox:8080/fhir"),
)
