async def test_extract(sdk, extract, safe_db):
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
                            "id": """$ fhirpath("item.where(linkId='patientId').answer.children().string").0""",
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
            "mapping": [{"resourceType": "Mapping", "id": m.id,}],
            "item": [{"type": "string", "linkId": "patientId",},],
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

    extraction = await extract(q.id, qr)

    assert len(extraction) == 1

    p = await sdk.client.resources("Patient").search().fetch_all()

    assert len(p) == 1

    assert p[0].id == "newPatient"
