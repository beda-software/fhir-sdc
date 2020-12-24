from tests.utils import create_parameters


async def test_extract_without_context(sdk, safe_db):
    m = sdk.client.resource(
        "Mapping",
        **{
            "body": {
                "resourceType": "Bundle",
                "type": "transaction",
                "entry": [
                    {
                        "request": {"url": "/Patient", "method": "POST"},
                        "resource": {
                            "resourceType": "Patient",
                            "id": """$ fhirpath("QuestionnaireResponse.item.where(linkId='patientId').answer.children().string").0""",
                        },
                    }
                ],
            }
        }
    )

    await m.save()
    q = sdk.client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "mapping": [
                {
                    "resourceType": "Mapping",
                    "id": m.id,
                }
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientId",
                },
            ],
        }
    )
    await q.save()

    qr = sdk.client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {
                    "linkId": "patientId",
                    "answer": [{"value": {"string": "newPatient"}}],
                }
            ],
        }
    )

    extraction = await q.execute("$extract", data=qr)

    assert len(extraction) == 1

    p = await sdk.client.resources("Patient").search().fetch_all()

    assert len(p) == 1

    assert p[0].id == "newPatient"


async def test_extract_with_context(sdk, safe_db):
    m = sdk.client.resource(
        "Mapping",
        **{
            "body": {
                "resourceType": "Bundle",
                "type": "transaction",
                "entry": [
                    {
                        "request": {"url": "/Patient", "method": "POST"},
                        "resource": {
                            "resourceType": "Patient",
                            "id": """$ fhirpath("QuestionnaireResponse.item.where(linkId='patientId').answer.children().string").0""",
                            "name": [
                                {
                                    "text": """$ fhirpath("ContextResource.name")""",
                                }
                            ],
                        },
                    }
                ],
            }
        }
    )

    await m.save()
    q = sdk.client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "mapping": [
                {
                    "resourceType": "Mapping",
                    "id": m.id,
                }
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "patientId",
                },
            ],
        }
    )
    await q.save()

    qr = sdk.client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": q.id,
            "item": [
                {
                    "linkId": "patientId",
                    "answer": [{"value": {"string": "newPatient"}}],
                }
            ],
        }
    )

    context = {"resourceType": "ContextResource", "name": "Name"}
    extraction = await q.execute(
        "$extract",
        data=create_parameters(QuestionnaireResponse=qr, ContextResource=context),
    )

    assert len(extraction) == 1

    p = await sdk.client.resources("Patient").search().fetch_all()

    assert len(p) == 1

    assert p[0].id == "newPatient"
    assert p[0].name[0].text == "Name"


async def test_extract_using_list_endpoint_with_context(sdk, safe_db):
    m = sdk.client.resource(
        "Mapping",
        **{
            "body": {
                "resourceType": "Bundle",
                "type": "transaction",
                "entry": [
                    {
                        "request": {"url": "/Patient", "method": "POST"},
                        "resource": {
                            "resourceType": "Patient",
                            "id": """$ fhirpath("QuestionnaireResponse.item.where(linkId='patientId').answer.children().string").0""",
                            "name": [
                                {
                                    "text": """$ fhirpath("ContextResource.name")""",
                                }
                            ],
                        },
                    }
                ],
            }
        }
    )

    await m.save()
    q = {
        "resourceType": "Questionnaire",
        "status": "active",
        "mapping": [
            {
                "resourceType": "Mapping",
                "id": m.id,
            }
        ],
        "item": [
            {
                "type": "string",
                "linkId": "patientId",
            },
        ],
    }

    qr = sdk.client.resource(
        "QuestionnaireResponse",
        **{
            "questionnaire": "virtual_id",
            "item": [
                {
                    "linkId": "patientId",
                    "answer": [{"value": {"string": "newPatient"}}],
                }
            ],
        }
    )
    context = {"resourceType": "ContextResource", "name": "Name"}

    extraction = await sdk.client.execute(
        "Questionnaire/$extract",
        data=create_parameters(
            Questionnaire=q, QuestionnaireResponse=qr, ContextResource=context
        ),
    )

    assert len(extraction) == 1

    p = await sdk.client.resources("Patient").search().fetch_all()

    assert len(p) == 1

    assert p[0].id == "newPatient"
    assert p[0].name[0].text == "Name"
