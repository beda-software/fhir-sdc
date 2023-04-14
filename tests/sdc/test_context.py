import uuid

import pytest

from app.test.utils import create_parameters


@pytest.mark.asyncio
async def test_get_questionnaire_context(aidbox_client, safe_db):
    p = aidbox_client.resource("Patient", **{"id": "patient-id"})
    await p.save()

    # Create related resources (Appointment, Organization and Location)
    a = aidbox_client.resource(
        "Appointment",
        **{
            "status": "booked",
            "start": "2020-01-01T00:00",
            "participant": [{"status": "accepted", "actor": p}],
        },
    )
    await a.save()

    organization_name = uuid.uuid4().hex
    organization = aidbox_client.resource("Organization", **{"name": organization_name})
    await organization.save()

    location_name = uuid.uuid4().hex
    location = aidbox_client.resource("Location", **{"name": location_name})
    await location.save()

    # Create a new questionnaire with source queries that request created resources above
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "launchContext": [{"name": {"code": "LaunchPatient"}, "type": "patient"}],
            "contained": [
                {
                    "id": "Data1",
                    "type": "batch",
                    "entry": [
                        {
                            "request": {
                                "url": "Appointment?patient={{%LaunchPatient.id}}",
                                "method": "GET",
                            }
                        },
                        {"request": {"url": f"/Location/{location.id}", "method": "GET"}},
                    ],
                    "resourceType": "Bundle",
                },
                {
                    "id": "Data2",
                    "type": "batch",
                    "entry": [
                        {"request": {"url": f"/Organization/{organization.id}", "method": "GET"}}
                    ],
                    "resourceType": "Bundle",
                },
            ],
            "sourceQueries": [{"localRef": "Bundle#Data1"}, {"localRef": "Bundle#Data2"}],
        },
    )
    await q.save()

    assert q.id is not None

    # Execute get context request and assert that output bundle has the related resources
    context = await aidbox_client.execute(
        f"Questionnaire/$context",
        method="POST",
        data=create_parameters(Questionnaire=q, LaunchPatient=p),
        params=None,
    )

    assert len(context["Data1"]["entry"]) == 2

    expected_appointment = next(
        (
            item
            for item in context["Data1"]["entry"][0]["resource"]["entry"]
            if item["resource"]["resourceType"] == "Appointment"
        ),
        None,
    )

    assert expected_appointment["resource"]["start"] == "2020-01-01T00:00"

    expected_location = next(
        (
            item
            for item in context["Data1"]["entry"]
            if item["resource"]["resourceType"] == "Location"
        ),
        None,
    )

    assert expected_location["resource"]["name"] == location_name

    expected_organization = next(
        (
            item
            for item in context["Data2"]["entry"]
            if item["resource"]["resourceType"] == "Organization"
        ),
        None,
    )

    assert expected_organization["resource"]["name"] == organization_name

    assert len(context["Data2"]["entry"]) == 1
