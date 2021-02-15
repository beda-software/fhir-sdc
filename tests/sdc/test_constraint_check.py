import pytest
from fhirpy.base.lib import OperationOutcome
from tests.utils import create_parameters


async def test_email_uniquest(sdk, safe_db):
    q = sdk.client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "launchContext": [{"name": "LaunchPatient", "type": "Patient",},],
            "sourceQueries": [{"localRef": "Bundle#AllEmails"},],
            "contained": [
                {
                    "resourceType": "Bundle",
                    "id": "AllEmails",
                    "type": "batch",
                    "entry": [
                        {
                            "request": {
                                "method": "GET",
                                "url": "Patient?_elements=telecom",
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
                                "expression": "%AllEmails.entry.resource.entry.resource.telecom.where(system = 'email).value contains QuestionnaireResponse.repeat(item).where(linkId='email-uniq').answer.value.string",
                            },
                        }
                    ],
                },
            ],
        }
    )
    await q.save()

    p = sdk.client.resource(
        "Patient", telecom=[{"system": "email", "value": "p1@beda.software"}]
    )
    await p.save()

    valid = sdk.client.resource(
        "QuestionnaireResponse",
        status="final",
        item=[
            {"linkId": "email", "answer": [{"value": {"string": "p2@beda.software"}}]}
        ],
    )
    await valid.save()

    invalid = sdk.client.resource(
        "QuestionnaireResponse",
        status="final",
        item=[
            {"linkId": "email", "answer": [{"value": {"string": "p1@beda.software"}}]}
        ],
    )
    await invalid.save()

    with pytest.raises(OperationOutcome):
        assert await sdk.client.execute(
            "QuestionnaireResponse/$constraint-check",
            data=create_parameters(Questionnaire=q, QuestionnaireResponse=invalid),
        )

    result = await sdk.client.execute(
        "QuestionnaireResponse/$constraint-check",
        data=create_parameters(Questionnaire=q, QuestionnaireResponse=valid),
    )

    assert result["resourceType"] == "QuestionnaireResponse"


async def test_email_uniquest_optimized(sdk, safe_db):
    q = sdk.client.resource(
        "Questionnaire",
        **{
            "status": "active",
            "launchContext": [{"name": "LaunchPatient", "type": "Patient",},],
            "sourceQueries": [{"localRef": "Bundle#AllEmails"},],
            "contained": [
                {
                    "resourceType": "Bundle",
                    "id": "AllEmails",
                    "type": "batch",
                    "entry": [
                        {
                            "request": {
                                "method": "GET",
                                "url": "Patient?_elements=telecom&email={{%QuestionnaireResponse.repeat(item).where(linkId='email-uniq').answer.value.string}}",
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
                                "expression": "%AllEmails.entry.resource.entry.resource.telecom.where(system = 'email).value contains QuestionnaireResponse.repeat(item).where(linkId='email-uniq').answer.value.string",
                            },
                        }
                    ],
                },
            ],
        }
    )
    await q.save()

    p = sdk.client.resource(
        "Patient", telecom=[{"system": "email", "value": "p1@beda.software"}]
    )
    await p.save()

    valid = sdk.client.resource(
        "QuestionnaireResponse",
        status="final",
        item=[
            {"linkId": "email", "answer": [{"value": {"string": "p2@beda.software"}}]}
        ],
    )
    await valid.save()

    invalid = sdk.client.resource(
        "QuestionnaireResponse",
        status="final",
        item=[
            {"linkId": "email", "answer": [{"value": {"string": "p1@beda.software"}}]}
        ],
    )
    await invalid.save()

    with pytest.raises(OperationOutcome):
        assert await sdk.client.execute(
            "QuestionnaireResponse/$constraint-check",
            data=create_parameters(Questionnaire=q, QuestionnaireResponse=invalid),
        )

    result = await sdk.client.execute(
        "QuestionnaireResponse/$constraint-check",
        data=create_parameters(Questionnaire=q, QuestionnaireResponse=valid),
    )

    assert result["resourceType"] == "QuestionnaireResponse"
