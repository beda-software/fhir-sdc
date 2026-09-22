import os


def resolve_jute_service():
    jute_service = os.getenv("JUTE_SERVICE", "").strip().strip('"')
    if not jute_service or jute_service.lower() == "aidbox":
        raise Exception("JUTE_SERVICE must point at a JUTE service, see the README")

    return jute_service


def get_extract_services(app):
    jute_service = app["settings"].JUTE_SERVICE
    fhir_mapping_service = app["settings"].FHIRPATH_MAPPING_SERVICE
    return {"JUTE": jute_service, "FHIRPath": fhir_mapping_service}
