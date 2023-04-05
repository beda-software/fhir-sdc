import pytest
from fhirpy.base.lib import OperationOutcome

from app.test.utils import create_parameters


@pytest.mark.asyncio
async def test_email_uniq(aidbox_client, safe_db):
    q = aidbox_client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "sourceQueries": [
                {"localRef": "Bundle#AllEmails"},
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
                                "url": "/Patient?_elements=telecom&email={{%QuestionnaireResponse.repeat(item).where(linkId='email-uniq').answer.value.string}}",
                            },
                        },
                    ],
                }
            ],
            "item": [
                {
                    "type": "string",
                    "linkId": "email",
                    "constraint": [
                        {
                            "key": "email-uniq",
                            "requirements": "Any email should present only once in the system",
                            "severity": "error",
                            "human": "Email already exists",
                            "expression": {
                                "language": "text/fhirpath",
                                "expression": "%AllEmails.entry.resource.entry.resource.telecom.where(system = 'email').value contains %QuestionnaireResponse.repeat(item).where(linkId='email-uniq').answer.value.string",
                            },
                        }
                    ],
                },
            ],
        },
    )
    await q.save()

    p = aidbox_client.resource(
        "Patient", telecom=[{"system": "email", "value": "p1@beda.software"}]
    )
    await p.save()

    valid = aidbox_client.resource(
        "QuestionnaireResponse",
        status="final",
        item=[
            {
                "linkId": "email-uniq",
                "answer": [{"value": {"string": "p2@beda.software"}}],
            }
        ],
    )
    await valid.save()

    invalid = aidbox_client.resource(
        "QuestionnaireResponse",
        status="final",
        item=[
            {
                "linkId": "email-uniq",
                "answer": [{"value": {"string": "p1@beda.software"}}],
            }
        ],
    )
    await invalid.save()

    with pytest.raises(OperationOutcome):
        assert await aidbox_client.execute(
            "QuestionnaireResponse/$constraint-check",
            data=create_parameters(Questionnaire=q, QuestionnaireResponse=invalid),
        )

    result = await aidbox_client.execute(
        "QuestionnaireResponse/$constraint-check",
        data=create_parameters(Questionnaire=q, QuestionnaireResponse=valid),
    )

    assert result["resourceType"] == "QuestionnaireResponse"
