import logging
import os


class FHIRAppSettings:
    def __init__(self, **custom_settings):
        self._custom_settings = custom_settings
        for name, value in custom_settings.items():
            # if not hasattr(self, name):
            #     raise TypeError('{} is not a valid setting name'.format(name))
            setattr(self, name, value)


constraint_legacy_behavior = os.getenv("CONSTRAINT_LEGACY_BEHAVIOR", "False").lower() == "true"
extract_source_queries_legacy_behavior = (
    os.getenv("EXTRACT_SOURCE_QUERIES_LEGACY_BEHAVIOR", "True").lower() == "true"
)

if constraint_legacy_behavior:
    logging.warning(
        "CONSTRAINT_LEGACY_BEHAVIOR is deprecated and will be enforced to be set to false in fhir-sdc@3.x.x"
    )

if extract_source_queries_legacy_behavior:
    logging.warning(
        "EXTRACT_SOURCE_QUERIES_LEGACY_BEHAVIOR is deprecated and will be enforced to be set to false in fhir-sdc@3.x.x"
    )

settings = FHIRAppSettings(
    JUTE_SERVICE=os.getenv("JUTE_SERVICE", "http://jute:8090/parse-template"),
    BASE_URL=os.getenv("BASE_URL", "http://devbox:8080/fhir"),
    AUTH_TOKEN=os.getenv("AUTH_TOKEN"),
    FHIRPATH_MAPPING_SERVICE=os.getenv("FHIRPATH_MAPPING_SERVICE"),
    CONSTRAINT_LEGACY_BEHAVIOR=constraint_legacy_behavior,
    EXTRACT_SOURCE_QUERIES_LEGACY_BEHAVIOR=extract_source_queries_legacy_behavior,
)
