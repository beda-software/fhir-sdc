def get_extract_services(app):
    jute_service = app["settings"].JUTE_SERVICE
    fhir_mapping_service = app["settings"].FHIRPATH_MAPPING_SERVICE
    return {"JUTE": jute_service, "FHIRPath": fhir_mapping_service}
