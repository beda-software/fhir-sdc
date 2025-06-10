import pytest

from app.sdc.populate import populate

questionnaire = {
  "meta": {
    "profile": [
      "https://emr-core.beda.software/StructureDefinition/fhir-emr-questionnaire"
    ],
  },
  "launchContext": [
    {
      "name": {
        "code": "Schedule"
      },
      "type": [
        "Schedule"
      ],
      "description": "Schedule to edit"
    }
  ],
  "name": "edit-schedule",
  "item": [
    {
      "item": [
        {
          "item": [
            {
              "text": "Day of the week",
              "type": "choice",
              "linkId": "day-of-the-week",
              "repeats": True,
              "answerOption": [
                {
                  "value": {
                    "Coding": {
                      "code": "sun",
                      "system": "http://hl7.org/fhir/ValueSet/days-of-week",
                      "display": "Sunday"
                    }
                  }
                },
                {
                  "value": {
                    "Coding": {
                      "code": "mon",
                      "system": "http://hl7.org/fhir/ValueSet/days-of-week",
                      "display": "Monday"
                    }
                  }
                },
                {
                  "value": {
                    "Coding": {
                      "code": "tue",
                      "system": "http://hl7.org/fhir/ValueSet/days-of-week",
                      "display": "Tuesday"
                    }
                  }
                }
              ],
              "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Questionnaire.repeat(item).where(linkId='day-of-the-week').answerOption.valueCoding.where(code in 'sun')"
              }
            },
            {
              "text": "Time start",
              "type": "time",
              "linkId": "time-start",
              "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%context.valueTiming.repeat.timeOfDay"
              }
            }
          ],
          "text": "Time period",
          "type": "group",
          "linkId": "time-period",
          "repeats": True,
          "itemPopulationContext": {
            "language": "text/fhirpath",
            "expression": "%Schedule.extension.where(url='http://example.com')"
          }
        }
      ],
      "type": "group",
      "linkId": "root-group"
    }
  ],
  "mapping": [
    {
      "id": "edit-schedule-extract",
      "resourceType": "Mapping"
    }
  ],
  "resourceType": "Questionnaire",
  "title": "Edit Schedule",
  "status": "active",
  "id": "edit-schedule",
  "url": "edit-schedule"
}

env = {
    "Schedule": {
        "actor": [
            {
                "reference": "Patient/Patient1"
            }
        ],
        "extension": [
            {
                "url": "http://example.com",
                "value":{
                    "Timing": {
                        "repeat": {
                            "dayOfWeek": [
                                "mon",
                                "tue"
                            ],
                        }
                    }
                }
            }
        ],
        "resourceType": "Schedule",
    },
    "Questionnaire": questionnaire
}

expected_qr = {
    "resourceType": "QuestionnaireResponse",
    "questionnaire": questionnaire["id"],
    "item": [
        {
            "linkId": "root-group",
            "item": [
                {
                    "linkId": "time-period",
                    "item": [
                        {
                            "linkId": "day-of-the-week",
                            "answer": [
                                {
                                    "valueCoding": {
                                        "code": "sun",
                                        "system": "http://hl7.org/fhir/ValueSet/days-of-week",
                                        "display": "Sunday"
                                    }
                                }
                            ]
                        },
                    ]
                }
            ]
        }
    ],
    "status": "completed"
}


@pytest.mark.asyncio
async def test_initial_expression_multiple_select(aidbox_client, safe_db):
    schedule_example = aidbox_client.resource("Schedule", **env["Schedule"])

    await schedule_example.save()

    assert schedule_example.id is not None

    questionnaire_response = await populate(aidbox_client, questionnaire, env)

    assert questionnaire_response == expected_qr
