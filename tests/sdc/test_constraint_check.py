import pytest
from fhirpy.base.lib import OperationOutcome

from app.test.utils import create_parameters
from tests.test_utils import (
    make_source_queries_ext,
    make_item_constraint_ext
)


@pytest.mark.asyncio
async def test_email_uniq(fhir_client, safe_db):
    q = fhir_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "extension": [
                make_source_queries_ext("#AllEmails")
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
                        make_item_constraint_ext(
                            key="email-uniq",
                            requirements="Any email should present only once in the system",
                            severity="error",
                            human="Email already exists",
                            expression="(%AllEmails.entry.resource.entry.resource.telecom.where(system = 'email').value contains %QuestionnaireResponse.repeat(item).where(linkId='email-uniq').answer.valueString).not()"
                        )
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
