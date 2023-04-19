import os

class FHIRAppSettings:
    def __init__(self, **custom_settings):
        self._custom_settings = custom_settings
        for name, value in custom_settings.items():
            # if not hasattr(self, name):
            #     raise TypeError('{} is not a valid setting name'.format(name))
            setattr(self, name, value)


settings = FHIRAppSettings(
    JUTE_SERVICE=os.getenv("JUTE_SERVICE", "http://jute:8090/parse-template"),
    BASE_URL=os.getenv("BASE_URL", "http://devbox:8080/fhir"),
    AUTH_TOKEN=os.getenv('AUTH_TOKEN')
)