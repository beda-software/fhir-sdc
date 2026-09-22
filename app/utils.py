import os


def resolve_jute_service():
    jute_service = os.getenv("JUTE_SERVICE", "")
    if jute_service.lower() == "aidbox":
        raise Exception(
            "Aidbox no longer renders JUTE mappers; JUTE_SERVICE must point at a service"
        )

    return jute_service


def resolve_fhirpath_service():
    fhirpath_service = os.getenv("FHIRPATH_MAPPING_SERVICE", "")
    # `fpml` names the in-process renderer, every other value is a service url.
    return "fpml" if fhirpath_service.lower() == "fpml" else fhirpath_service


def get_extract_services(app):
    jute_service = app["settings"].JUTE_SERVICE
    fhir_mapping_service = app["settings"].FHIRPATH_MAPPING_SERVICE
    return {"JUTE": jute_service, "FHIRPath": fhir_mapping_service}
