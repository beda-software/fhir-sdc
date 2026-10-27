import pytest
from fhirpy import AsyncFHIRClient

from app.aidbox.utils import get_aidbox_fhir_client

pytest_plugins = ["aidbox_python_sdk.pytest_plugin", "pytester"]


@pytest.fixture
def fhir_client(aidbox_client):
    return get_aidbox_fhir_client(aidbox_client)


@pytest.fixture
def typed_fhir_client(aidbox_client):
    """fhirpy cannot serialize pydantic resources without `dump_resource`."""
    return AsyncFHIRClient(
        f"{aidbox_client.url}/fhir",
        authorization=aidbox_client.authorization,
        extra_headers=aidbox_client.extra_headers,
        dump_resource=lambda resource: resource.model_dump(),
    )
