import pytest

pytest_plugins = ["aidbox_python_sdk.pytest_plugin", "pytester"]


@pytest.fixture(scope="session")
def sdk(client):
    return client.server.app["sdk"]


@pytest.fixture
def populate(sdk):
    async def wrapper(q_id, **payload):
        return await sdk.client._do_request(
            "post",
            "Questionnaire/{0}/$populate".format(q_id),
            data={
                "resourceType": "Parameters",
                "parameter": [
                    {"name": name, "resource": resource}
                    for name, resource in payload.items()
                ],
            },
        )

    return wrapper


@pytest.fixture
def extract(sdk):
    async def wrapper(q_id, questionnaire_response):
        return await sdk.client._do_request(
            "post",
            "Questionnaire/{0}/$extract".format(q_id),
            data=questionnaire_response,
        )

    return wrapper
