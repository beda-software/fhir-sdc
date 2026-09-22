import os

from app.utils import resolve_fhirpath_service, resolve_jute_service


class FHIRAppSettings:
    def __init__(self, **custom_settings):
        self._custom_settings = custom_settings
        for name, value in custom_settings.items():
            # if not hasattr(self, name):
            #     raise TypeError('{} is not a valid setting name'.format(name))
            setattr(self, name, value)


# Both behaviours are gone in 3.x.x; leaving the variable on would silently invert every constraint.
for removed_setting in ("CONSTRAINT_LEGACY_BEHAVIOR", "EXTRACT_SOURCE_QUERIES_LEGACY_BEHAVIOR"):
    if os.getenv(removed_setting, "").lower() == "true":
        raise Exception(f"{removed_setting} is not supported in fhir-sdc@3.x.x, see the README")

settings = FHIRAppSettings(
    JUTE_SERVICE=resolve_jute_service(),
    BASE_URL=os.getenv("BASE_URL", "http://devbox:8080/fhir"),
    AUTH_TOKEN=os.getenv("AUTH_TOKEN"),
    FHIRPATH_MAPPING_SERVICE=resolve_fhirpath_service(),
)
