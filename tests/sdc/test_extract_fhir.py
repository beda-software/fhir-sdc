import pytest
from faker import Faker

from app.test.utils import create_parameters

fake = Faker()

questionnaire = {
    "name": "practitioner-create",
    "item": [
        {"text": "Last name", "type": "string", "linkId": "last-name", "required": True},
        {"text": "First name", "type": "string", "linkId": "first-name"},
        {"text": "Middle name", "type": "string", "linkId": "middle-name"},
        {
            "text": "Specialty",
            "type": "choice",
            "linkId": "specialty",
            "answerOption": [
                {
                    "valueCoding": {
                        "code": "394577000",
                        "system": "http://snomed.info/sct",
                        "display": "Anesthetics",
                    }
                },
                {
                    "valueCoding": {
                        "code": "394579002",
                        "system": "http://snomed.info/sct",
                        "display": "Cardiology",
                    }
                },
                {
                    "valueCoding": {
                        "code": "394582007",
                        "system": "http://snomed.info/sct",
                        "display": "Dermatology",
                    }
                },
                {
                    "valueCoding": {
                        "code": "394583002",
                        "system": "http://snomed.info/sct",
                        "display": "Endocrinology",
                    }
                },
                {
                    "valueCoding": {
                        "code": "419772000",
                        "system": "http://snomed.info/sct",
                        "display": "Family practice",
                    }
                },
            ],
        },
    ],
    "resourceType": "Questionnaire",
    "title": "Practitioner create",
    "extension": [
        {
            "url": "http://beda.software/fhir-extensions/questionnaire-mapper",
            "valueReference": {"reference": "Mapping/practitioner-create"},
        }
    ],
    "status": "active",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/practitioner-create",
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
    },
}


mapping = {
    "body": {
        "type": "transaction",
        "entry": {
            "$args": [
                [
                    {
                        "fullUrl": "urn:uuid:practitioner-id",
                        "request": {"url": "/Practitioner", "method": "POST"},
                        "resource": {
                            "name": [
                                {
                                    "given": [
                                        "$ fhirpath(\"QuestionnaireResponse.repeat(item).where(linkId='first-name').answer.valueString\").0",
                                        "$ fhirpath(\"QuestionnaireResponse.repeat(item).where(linkId='middle-name').answer.valueString\").0",
                                    ],
                                    "family": "$ fhirpath(\"QuestionnaireResponse.repeat(item).where(linkId='last-name').answer.valueString\").0",
                                }
                            ],
                            "resourceType": "Practitioner",
                        },
                    }
                ],
                {
                    "$as": "specialtyItem",
                    "$map": "$ fhirpath(\"QuestionnaireResponse.repeat(item).where(linkId='specialty').answer\")",
                    "$body": {
                        "request": {"url": "/PractitionerRole", "method": "POST"},
                        "resource": {
                            "specialty": [{"coding": ["$ specialtyItem.valueCoding"]}],
                            "practitioner": {"uri": "urn:uuid:practitioner-id"},
                            "resourceType": "practitionerRole",
                        },
                    },
                },
            ],
            "$call": "concat",
        },
    },
    "id": "practitioner-create",
    "resourceType": "Mapping",
}


def questionnaire_response(first_name, last_name):
    return {
        "item": [
            {
                "answer": [
                    {
                        "valueString": last_name,
                    }
                ],
                "linkId": "last-name",
            },
            {
                "answer": [
                    {
                        "valueString": first_name,
                    }
                ],
                "linkId": "first-name",
            },
            {
                "answer": [
                    {
                        "valueCoding": {
                            "code": "394583002",
                            "system": "http://snomed.info/sct",
                            "display": "Endocrinology",
                        }
                    }
                ],
                "linkId": "specialty",
            },
        ],
        "status": "completed",
        "authored": "2023-04-10T11:55:02Z",
        "resourceType": "QuestionnaireResponse",
    }


@pytest.mark.asyncio
async def test_context_extraction(aidbox_client, safe_db):
    m = aidbox_client.resource("Mapping", **mapping)
    await m.save()
    assert m.id
    first_name = fake.first_name()
    last_name = fake.last_name()
    await aidbox_client.execute(
        "fhir/Questionnaire/$extract",
        data=create_parameters(
            Questionnaire=questionnaire,
            QuestionnaireResponse=questionnaire_response(first_name, last_name),
        ),
    )

    p = await aidbox_client.resources("Practitioner").search().first()
    assert p["name"] == [{"family": last_name, "given": [first_name]}]
    pr = await aidbox_client.resources("PractitionerRole").search().first()
    assert pr["practitioner"]["id"] == p.id


@pytest.mark.asyncio
async def test_qr_extraction(aidbox_client, safe_db):
    m = aidbox_client.resource("Mapping", **mapping)
    await m.save()
    assert m.id

    q = await aidbox_client.execute("fhir/Questionnaire", data=questionnaire)

    first_name = fake.first_name()
    last_name = fake.last_name()
    await aidbox_client.execute(
        "fhir/Questionnaire/$extract",
        data={**questionnaire_response(first_name, last_name), "questionnaire": q["id"]},
    )

    p = await aidbox_client.resources("Practitioner").search().first()
    assert p["name"] == [{"family": last_name, "given": [first_name]}]
    pr = await aidbox_client.resources("PractitionerRole").search().first()
    assert pr["practitioner"]["id"] == p.id


@pytest.mark.asyncio
async def test_q_extraction(aidbox_client, safe_db):
    m = aidbox_client.resource("Mapping", **mapping)
    await m.save()
    assert m.id

    q = await aidbox_client.execute("fhir/Questionnaire", data=questionnaire)

    first_name = fake.first_name()
    last_name = fake.last_name()
    await aidbox_client.execute(
        f"fhir/Questionnaire/{q['id']}/$extract",
        data={**questionnaire_response(first_name, last_name), "questionnaire": q["id"]},
    )

    p = await aidbox_client.resources("Practitioner").search().first()
    assert p["name"] == [{"family": last_name, "given": [first_name]}]
    pr = await aidbox_client.resources("PractitionerRole").search().first()
    assert pr["practitioner"]["id"] == p.id
