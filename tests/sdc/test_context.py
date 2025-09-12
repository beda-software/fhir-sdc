import uuid

import pytest

from tests.factories import (
    create_questionnaire,
    make_parameters,
    make_launch_context_ext,
    make_source_queries_ext
)


@pytest.mark.asyncio
async def test_get_questionnaire_context(fhir_client, safe_db):
    p = fhir_client.resource("Patient", **{"id": "patient-id"})
    await p.save()

    # Create related resources (Appointment, Organization and Location)
    a = fhir_client.resource(
        "Appointment",
        **{
            "status": "booked",
            "start": "2020-01-01T00:00:00Z",
            "end": "2020-01-01T00:30:00Z",
            "participant": [{"status": "accepted", "actor": p}],
        },
    )
    await a.save()

    organization_name = uuid.uuid4().hex
    organization = fhir_client.resource("Organization", **{"name": organization_name})
    await organization.save()

    location_name = uuid.uuid4().hex
    location = fhir_client.resource("Location", **{"name": location_name})
    await location.save()

    # Create a new questionnaire with source queries that request created resources above
    q = await create_questionnaire(
        fhir_client,
        {
            "status": "active",
            "extension": [
                make_launch_context_ext("LaunchPatient", "Patient"),
                make_source_queries_ext("#Data1"),
                make_source_queries_ext("#Data2")
            ],
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
        },
    )

    # Execute get context request and assert that output bundle has the related resources
    context = await fhir_client.execute(
        "Questionnaire/$context",
        method="POST",
        data=make_parameters(Questionnaire=q, LaunchPatient=p),
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

    assert expected_appointment["resource"]["start"] == "2020-01-01T00:00:00Z"

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
