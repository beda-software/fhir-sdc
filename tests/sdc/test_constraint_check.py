import pytest
from fhirpy.base.lib import OperationOutcome

from app.test.utils import create_parameters


@pytest.mark.asyncio
async def test_fce_email_uniq(fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-sourceQueries",
                    "valueReference": {
                        "reference": "#AllEmails"
                    }
                }
            ],
            "contained": [
                {
                    "resourceType": "Bundle",
                    "id": "AllEmails",
                    "type": "batch",
                    "entry": [
                        {
                            "request": {
                                "url": "/Patient?_elements=telecom&email={{%QuestionnaireResponse.repeat(item).where(linkId='email-uniq').answer.valueString}}",
                                "method": "GET",
                            }
                        }
                    ],
                }
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "email",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-constraint",
                            "extension": [
                                {
                                    "url": "key",
                                    "valueString": "email-uniq"
                                },
                                {
                                    "url": "requirements",
                                    "valueString": "Any email should present only once in the system"
                                },
                                {
                                    "url": "severity",
                                    "valueCode": "error"
                                },
                                {
                                    "url": "human",
                                    "valueString": "Email already exists"
                                },
                                {
                                    "url": "expression",
                                    "valueString": "(%AllEmails.entry.resource.entry.resource.telecom.where(system = 'email').value contains %QuestionnaireResponse.repeat(item).where(linkId='email-uniq').answer.valueString).not().not()"
                                }
                            ]
                        }
                    ]
                }
            ],
        },
    )
    await q.save()

    p = fhir_client.resource(
        "Patient",
        **{
            "telecom": [
                {
                    "system": "email",
                    "value": "p1@beda.software",
                }
            ]
        },
    )
    await p.save()

    valid = fhir_client.resource(
        "QuestionnaireResponse",
        **{
            "status": "completed",
            "questionnaire": q.id,
            "subject": p,
            "item": [
                {
                    "linkId": "email-uniq",
                    "answer": [{"valueString": "p2@beda.software"}],
                }
            ],
        },
    )
    await valid.save()

    invalid = fhir_client.resource(
        "QuestionnaireResponse",
        **{
            "status": "completed",
            "questionnaire": q.id,
            "subject": p,
            "item": [
                {
                    "linkId": "email-uniq",
                    "answer": [{"valueString": "p1@beda.software"}],
                }
            ],
        },
    )
    await invalid.save()

    with pytest.raises(OperationOutcome):
        assert await fhir_client.execute(
            "QuestionnaireResponse/$constraint-check",
            data=create_parameters(Questionnaire=q, QuestionnaireResponse=invalid),
        )

    result = await fhir_client.execute(
        "QuestionnaireResponse/$constraint-check",
        data=create_parameters(Questionnaire=q, QuestionnaireResponse=valid),
    )

    assert result["resourceType"] == "QuestionnaireResponse"


@pytest.mark.asyncio
async def test_fhir_email_uniq(fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-sourceQueries",
                    "valueReference": {
                        "reference": "#AllEmails"
                    }
                }
            ],
            "contained": [
                {
                    "resourceType": "Bundle",
                    "id": "AllEmails",
                    "type": "batch",
                    "entry": [
                        {
                            "request": {
                                "method": "GET",
                                "url": "/Patient?_elements=telecom&email={{%QuestionnaireResponse.repeat(item).where(linkId='email-uniq').answer.valueString}}",
                            },
                        },
                    ],
                }
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "email",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-constraint",
                            "extension": [
                                {
                                    "url": "key",
                                    "valueString": "email-uniq"
                                },
                                {
                                    "url": "requirements",
                                    "valueString": "Any email should present only once in the system"
                                },
                                {
                                    "url": "severity",
                                    "valueCode": "error"
                                },
                                {
                                    "url": "human",
                                    "valueString": "Email already exists"
                                },
                                {
                                    "url": "expression",
                                    "valueString": "(%AllEmails.entry.resource.entry.resource.telecom.where(system = 'email').value contains %QuestionnaireResponse.repeat(item).where(linkId='email-uniq').answer.valueString).not().not()"
                                }
                            ]
                        }
                    ]
                },
            ],
        },
    )
    await q.save()

    p = fhir_client.resource(
        "Patient", telecom=[{"system": "email", "value": "p1@beda.software"}]
    )
    await p.save()

    valid = fhir_client.resource(
        "QuestionnaireResponse",
        status="completed",
        item=[
            {
                "linkId": "email-uniq",
                "answer": [{"valueString": "p2@beda.software"}],
            }
        ],
    )
    await valid.save()

    invalid = fhir_client.resource(
        "QuestionnaireResponse",
        status="completed",
        item=[
            {
                "linkId": "email-uniq",
                "answer": [{"valueString": "p1@beda.software"}],
            }
        ],
    )
    await invalid.save()

    with pytest.raises(OperationOutcome):
        assert await fhir_client.execute(
            "QuestionnaireResponse/$constraint-check",
            data=create_parameters(Questionnaire=q, QuestionnaireResponse=invalid),
        )

    result = await fhir_client.execute(
        "QuestionnaireResponse/$constraint-check",
        data=create_parameters(Questionnaire=q, QuestionnaireResponse=valid),
    )

    assert result["resourceType"] == "QuestionnaireResponse"
