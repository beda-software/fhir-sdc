import pytest

from app.aidbox.utils import get_aidbox_fhir_client, get_typed_fhir_client

pytest_plugins = ["aidbox_python_sdk.pytest_plugin", "pytester"]


@pytest.fixture
def fhir_client(aidbox_client):
    return get_aidbox_fhir_client(aidbox_client)


@pytest.fixture
def typed_fhir_client(aidbox_client):
    return get_typed_fhir_client(aidbox_client)
