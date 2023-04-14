practitioner_fhir_QuestionnaireResponse = {
    "authored": "2023-04-05T06:09:09Z",
    "id": "cedd0c3e-be1a-4c1b-92af-351ed76fe41e",
    "item": [
        {"answer": [{"valueString": "Patel"}], "linkId": "last-name"},
        {"answer": [{"valueString": "Sanjay"}], "linkId": "first-name"},
        {"answer": [{"valueString": "Kumar"}], "linkId": "middle-name"},
        {
            "answer": [
                {
                    "valueCoding": {
                        "code": "394579002",
                        "display": "Cardiology",
                        "system": "http://snomed.info/sct",
                    }
                }
            ],
            "linkId": "specialty",
        },
    ],
    "meta": {
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T06:09:10.640955Z"}],
        "lastUpdated": "2023-04-05T06:09:10.640955Z",
        "versionId": "20415",
    },
    "resourceType": "QuestionnaireResponse",
    "status": "completed",
}


practitioner_aidbox_QuestionnaireResponse = {
    "authored": "2023-04-05T06:09:09Z",
    "id": "cedd0c3e-be1a-4c1b-92af-351ed76fe41e",
    "item": [
        {"answer": [{"value": {"string": "Patel"}}], "linkId": "last-name"},
        {"answer": [{"value": {"string": "Sanjay"}}], "linkId": "first-name"},
        {"answer": [{"value": {"string": "Kumar"}}], "linkId": "middle-name"},
        {
            "answer": [
                {
                    "value": {
                        "Coding": {
                            "code": "394579002",
                            "display": "Cardiology",
                            "system": "http://snomed.info/sct",
                        }
                    }
                }
            ],
            "linkId": "specialty",
        },
    ],
    "meta": {
        "createdAt": "2023-04-05T06:09:10.640955Z",
        "lastUpdated": "2023-04-05T06:09:10.640955Z",
        "versionId": "20415",
    },
    "resourceType": "QuestionnaireResponse",
    "status": "completed",
}

patient_fhir_QuestionnaireResponse = {
    "authored": "2023-04-05T06:03:19Z",
    "id": "24306b57-b463-4e39-807f-e715a80bbe5f",
    "item": [
        {"answer": [{"value": {}}], "linkId": "patient-id"},
        {"answer": [{"valueString": "Nguyen"}], "linkId": "last-name"},
        {"answer": [{"valueString": "Emily"}], "linkId": "first-name"},
        {"answer": [{"valueString": "Marie"}], "linkId": "middle-name"},
        {"answer": [{"valueDate": "1991-12-29"}], "linkId": "birth-date"},
        {"answer": [{"valueString": "female"}], "linkId": "gender"},
        {"answer": [{"valueString": "123-45-6789"}], "linkId": "ssn"},
        {"answer": [{"valueString": "15551234567"}], "linkId": "mobile"},
    ],
    "meta": {
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T06:03:21.353895Z"}],
        "lastUpdated": "2023-04-05T06:03:21.353895Z",
        "versionId": "20412",
    },
    "resourceType": "QuestionnaireResponse",
    "status": "completed",
}

patient_aidbox_QuestionnaireResponse = {
    "authored": "2023-04-05T06:03:19Z",
    "id": "24306b57-b463-4e39-807f-e715a80bbe5f",
    "item": [
        {"answer": [{"value": {}}], "linkId": "patient-id"},
        {"answer": [{"value": {"string": "Nguyen"}}], "linkId": "last-name"},
        {"answer": [{"value": {"string": "Emily"}}], "linkId": "first-name"},
        {"answer": [{"value": {"string": "Marie"}}], "linkId": "middle-name"},
        {"answer": [{"value": {"date": "1991-12-29"}}], "linkId": "birth-date"},
        {"answer": [{"value": {"string": "female"}}], "linkId": "gender"},
        {"answer": [{"value": {"string": "123-45-6789"}}], "linkId": "ssn"},
        {"answer": [{"value": {"string": "15551234567"}}], "linkId": "mobile"},
    ],
    "meta": {
        "createdAt": "2023-04-05T06:03:21.353895Z",
        "lastUpdated": "2023-04-05T06:03:21.353895Z",
        "versionId": "20412",
    },
    "resourceType": "QuestionnaireResponse",
    "status": "completed",
}

allergies_fhir_QuestionnaireResponse = {
    "authored": "2023-04-05T06:27:57Z",
    "id": "cf6d9d4b-bfcd-463f-9d26-b6769c2a3fc3",
    "item": [
        {
            "answer": [{"valueString": "683e382b-fed4-433e-9b6d-a847a7953bc0"}],
            "linkId": "patientId",
        },
        {"answer": [{"valueString": "Emily Nguyen"}], "linkId": "patientName"},
        {
            "answer": [
                {
                    "valueReference": {
                        "display": "Sanjay Patel - Cardiology",
                        "reference": "PractitionerRole/429e6a55-8a64-4ede-ad12-1206522253eb",
                        "resource": {
                            "healthcareService": [
                                {
                                    "display": "The first appointment",
                                    "id": "consultation",
                                    "resourceType": "HealthcareService",
                                },
                                {
                                    "display": "A follow up visit",
                                    "id": "follow-up",
                                    "resourceType": "HealthcareService",
                                },
                            ],
                            "id": "429e6a55-8a64-4ede-ad12-1206522253eb",
                            "meta": {
                                "createdAt": "2023-04-05T06:09:11.092359Z",
                                "lastUpdated": "2023-04-05T06:09:11.092359Z",
                                "versionId": "20418",
                            },
                            "practitioner": {
                                "id": "42e9bdc0-4fe6-4b8d-a6a5-fcb68f1fe836",
                                "resource": {
                                    "id": "42e9bdc0-4fe6-4b8d-a6a5-fcb68f1fe836",
                                    "meta": {
                                        "createdAt": "2023-04-05T06:09:11.092359Z",
                                        "lastUpdated": "2023-04-05T06:09:11.092359Z",
                                        "versionId": "20416",
                                    },
                                    "name": [{"family": "Patel", "given": ["Sanjay", "Kumar"]}],
                                    "resourceType": "Practitioner",
                                },
                                "resourceType": "Practitioner",
                            },
                            "resourceType": "PractitionerRole",
                            "specialty": [
                                {
                                    "coding": [
                                        {
                                            "code": "394579002",
                                            "display": "Cardiology",
                                            "system": "http://snomed.info/sct",
                                        }
                                    ]
                                }
                            ],
                        },
                    }
                }
            ],
            "linkId": "practitioner-role",
        },
        {
            "answer": [
                {
                    "valueCoding": {
                        "code": "consultation",
                        "display": "The first appointment",
                        "system": "http://fhir.org/guides/argonaut-scheduling/CodeSystem/visit-type",
                    }
                }
            ],
            "linkId": "service",
        },
        {"answer": [{"valueDate": "2023-04-26"}], "linkId": "date"},
        {
            "item": [
                {"answer": [{"valueTime": "15:00:00"}], "linkId": "start-time"},
                {"answer": [{"valueTime": "16:00:00"}], "linkId": "end-time"},
            ],
            "linkId": "Time period",
        },
    ],
    "meta": {
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T06:27:58.499391Z"}],
        "lastUpdated": "2023-04-05T06:27:58.499391Z",
        "versionId": "20420",
    },
    "resourceType": "QuestionnaireResponse",
    "status": "completed",
}

allergies_aidbox_QuestionnaireResponse = {
    "authored": "2023-04-05T06:27:57Z",
    "id": "cf6d9d4b-bfcd-463f-9d26-b6769c2a3fc3",
    "item": [
        {
            "answer": [{"value": {"string": "683e382b-fed4-433e-9b6d-a847a7953bc0"}}],
            "linkId": "patientId",
        },
        {"answer": [{"value": {"string": "Emily Nguyen"}}], "linkId": "patientName"},
        {
            "answer": [
                {
                    "value": {
                        "Reference": {
                            "display": "Sanjay Patel - Cardiology",
                            "id": "429e6a55-8a64-4ede-ad12-1206522253eb",
                            "resource": {
                                "healthcareService": [
                                    {
                                        "display": "The first appointment",
                                        "id": "consultation",
                                        "resourceType": "HealthcareService",
                                    },
                                    {
                                        "display": "A follow up visit",
                                        "id": "follow-up",
                                        "resourceType": "HealthcareService",
                                    },
                                ],
                                "id": "429e6a55-8a64-4ede-ad12-1206522253eb",
                                "meta": {
                                    "createdAt": "2023-04-05T06:09:11.092359Z",
                                    "lastUpdated": "2023-04-05T06:09:11.092359Z",
                                    "versionId": "20418",
                                },
                                "practitioner": {
                                    "id": "42e9bdc0-4fe6-4b8d-a6a5-fcb68f1fe836",
                                    "resource": {
                                        "id": "42e9bdc0-4fe6-4b8d-a6a5-fcb68f1fe836",
                                        "meta": {
                                            "createdAt": "2023-04-05T06:09:11.092359Z",
                                            "lastUpdated": "2023-04-05T06:09:11.092359Z",
                                            "versionId": "20416",
                                        },
                                        "name": [{"family": "Patel", "given": ["Sanjay", "Kumar"]}],
                                        "resourceType": "Practitioner",
                                    },
                                    "resourceType": "Practitioner",
                                },
                                "resourceType": "PractitionerRole",
                                "specialty": [
                                    {
                                        "coding": [
                                            {
                                                "code": "394579002",
                                                "display": "Cardiology",
                                                "system": "http://snomed.info/sct",
                                            }
                                        ]
                                    }
                                ],
                            },
                            "resourceType": "PractitionerRole",
                        }
                    }
                }
            ],
            "linkId": "practitioner-role",
        },
        {
            "answer": [
                {
                    "value": {
                        "Coding": {
                            "code": "consultation",
                            "display": "The first appointment",
                            "system": "http://fhir.org/guides/argonaut-scheduling/CodeSystem/visit-type",
                        }
                    }
                }
            ],
            "linkId": "service",
        },
        {"answer": [{"value": {"date": "2023-04-26"}}], "linkId": "date"},
        {
            "item": [
                {"answer": [{"value": {"time": "15:00:00"}}], "linkId": "start-time"},
                {"answer": [{"value": {"time": "16:00:00"}}], "linkId": "end-time"},
            ],
            "linkId": "Time period",
        },
    ],
    "meta": {
        "createdAt": "2023-04-05T06:27:58.499391Z",
        "lastUpdated": "2023-04-05T06:27:58.499391Z",
        "versionId": "20420",
    },
    "resourceType": "QuestionnaireResponse",
    "status": "completed",
}

gad7_fhir_QuestionnaireResponse = {
    "questionnaire": "gad-7",
    "meta": {
        "lastUpdated": "2023-04-06T01:29:05.681893Z",
        "versionId": "20442",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-06T01:28:53.793848Z"}],
    },
    "encounter": {"reference": "Encounter/e133b999-9e91-4ebd-967e-450bad770682"},
    "item": [
        {"answer": [{"valueDateTime": "2023-04-06T01:28:52+00:00"}], "linkId": "dateTime"},
        {
            "answer": [{"valueString": "683e382b-fed4-433e-9b6d-a847a7953bc0"}],
            "linkId": "patientId",
        },
        {"answer": [{"valueString": "Emily Nguyen"}], "linkId": "patientName"},
        {
            "item": [
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        }
                    ],
                    "linkId": "69725-0",
                },
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        }
                    ],
                    "linkId": "68509-9",
                },
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        }
                    ],
                    "linkId": "69733-4",
                },
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        }
                    ],
                    "linkId": "69734-2",
                },
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        }
                    ],
                    "linkId": "69735-9",
                },
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        }
                    ],
                    "linkId": "69689-8",
                },
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        }
                    ],
                    "linkId": "69736-7",
                },
                {"answer": [{"valueInteger": 9}], "linkId": "anxiety-score"},
            ],
            "linkId": "gad-7",
        },
    ],
    "resourceType": "QuestionnaireResponse",
    "source": {"reference": "Patient/683e382b-fed4-433e-9b6d-a847a7953bc0"},
    "status": "completed",
    "id": "a00b8309-f74f-462c-a7e4-64852d5bf707",
    "authored": "2023-04-06T01:29:05Z",
}

gad7_aidbox_QuestionnaireResponse = {
    "questionnaire": "gad-7",
    "meta": {
        "lastUpdated": "2023-04-06T01:29:05.681893Z",
        "createdAt": "2023-04-06T01:28:53.793848Z",
        "versionId": "20442",
    },
    "encounter": {"id": "e133b999-9e91-4ebd-967e-450bad770682", "resourceType": "Encounter"},
    "item": [
        {"answer": [{"value": {"dateTime": "2023-04-06T01:28:52+00:00"}}], "linkId": "dateTime"},
        {
            "answer": [{"value": {"string": "683e382b-fed4-433e-9b6d-a847a7953bc0"}}],
            "linkId": "patientId",
        },
        {"answer": [{"value": {"string": "Emily Nguyen"}}], "linkId": "patientName"},
        {
            "item": [
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        }
                    ],
                    "linkId": "69725-0",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        }
                    ],
                    "linkId": "68509-9",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        }
                    ],
                    "linkId": "69733-4",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        }
                    ],
                    "linkId": "69734-2",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        }
                    ],
                    "linkId": "69735-9",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        }
                    ],
                    "linkId": "69689-8",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        }
                    ],
                    "linkId": "69736-7",
                },
                {"answer": [{"value": {"integer": 9}}], "linkId": "anxiety-score"},
            ],
            "linkId": "gad-7",
        },
    ],
    "resourceType": "QuestionnaireResponse",
    "source": {"id": "683e382b-fed4-433e-9b6d-a847a7953bc0", "resourceType": "Patient"},
    "status": "completed",
    "id": "a00b8309-f74f-462c-a7e4-64852d5bf707",
    "authored": "2023-04-06T01:29:05Z",
}

medication_fhir_QuestionnaireResponse = {
    "questionnaire": "medication",
    "meta": {
        "lastUpdated": "2023-04-06T01:59:42.145206Z",
        "versionId": "20458",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-06T01:59:02.311377Z"}],
    },
    "encounter": {"reference": "Encounter/e133b999-9e91-4ebd-967e-450bad770682"},
    "item": [
        {"answer": [{"valueDateTime": "2023-04-06T01:59:00+00:00"}], "linkId": "dateTime"},
        {
            "answer": [{"valueString": "e133b999-9e91-4ebd-967e-450bad770682"}],
            "linkId": "encounterId",
        },
        {
            "answer": [{"valueString": "683e382b-fed4-433e-9b6d-a847a7953bc0"}],
            "linkId": "patientId",
        },
        {"answer": [{"valueString": "Emily Nguyen"}], "linkId": "patientName"},
        {
            "answer": [
                {
                    "valueCoding": {
                        "code": "261000",
                        "system": "http://snomed.info/sct",
                        "display": "Codeine phosphate",
                    }
                }
            ],
            "linkId": "medication",
        },
        {"answer": [{"valueString": "25 or 20"}], "linkId": "dosage"},
        {"answer": [{"valueDate": "2023-04-10"}], "linkId": "start-date"},
        {"answer": [{"valueDate": "2023-04-17"}], "linkId": "stop-date"},
        {"answer": [{"valueString": "nothing"}], "linkId": "notes"},
    ],
    "resourceType": "QuestionnaireResponse",
    "source": {"reference": "Patient/683e382b-fed4-433e-9b6d-a847a7953bc0"},
    "status": "completed",
    "id": "3d077aed-ccd4-43d4-843e-0e2224e7571e",
    "authored": "2023-04-06T01:59:41Z",
}

medication_aidbox_QuestionnaireResponse = {
    "questionnaire": "medication",
    "meta": {
        "lastUpdated": "2023-04-06T01:59:42.145206Z",
        "createdAt": "2023-04-06T01:59:02.311377Z",
        "versionId": "20458",
    },
    "encounter": {"id": "e133b999-9e91-4ebd-967e-450bad770682", "resourceType": "Encounter"},
    "item": [
        {"answer": [{"value": {"dateTime": "2023-04-06T01:59:00+00:00"}}], "linkId": "dateTime"},
        {
            "answer": [{"value": {"string": "e133b999-9e91-4ebd-967e-450bad770682"}}],
            "linkId": "encounterId",
        },
        {
            "answer": [{"value": {"string": "683e382b-fed4-433e-9b6d-a847a7953bc0"}}],
            "linkId": "patientId",
        },
        {"answer": [{"value": {"string": "Emily Nguyen"}}], "linkId": "patientName"},
        {
            "answer": [
                {
                    "value": {
                        "Coding": {
                            "code": "261000",
                            "system": "http://snomed.info/sct",
                            "display": "Codeine phosphate",
                        }
                    }
                }
            ],
            "linkId": "medication",
        },
        {"answer": [{"value": {"string": "25 or 20"}}], "linkId": "dosage"},
        {"answer": [{"value": {"date": "2023-04-10"}}], "linkId": "start-date"},
        {"answer": [{"value": {"date": "2023-04-17"}}], "linkId": "stop-date"},
        {"answer": [{"value": {"string": "nothing"}}], "linkId": "notes"},
    ],
    "resourceType": "QuestionnaireResponse",
    "source": {"id": "683e382b-fed4-433e-9b6d-a847a7953bc0", "resourceType": "Patient"},
    "status": "completed",
    "id": "3d077aed-ccd4-43d4-843e-0e2224e7571e",
    "authored": "2023-04-06T01:59:41Z",
}

physicalexam_fhir_QuestionnaireResponse = {
    "questionnaire": "physical-exam",
    "meta": {
        "lastUpdated": "2023-04-06T02:05:52.434771Z",
        "versionId": "20470",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-06T02:05:32.668369Z"}],
    },
    "encounter": {"reference": "Encounter/e133b999-9e91-4ebd-967e-450bad770682"},
    "item": [
        {
            "item": [
                {
                    "answer": [
                        {
                            "valueString": "Well nourished, well developed, awake and alert, resting comfortably in no acute distress, cooperative on exam"
                        }
                    ],
                    "linkId": "general",
                },
                {
                    "answer": [
                        {
                            "valueString": "NCAT, PERRL, normal conjunctivae, nonicteric sclerae, bilateral EAC/TM clear, no nasal discharge, OP clear, moist mucous membranes"
                        }
                    ],
                    "linkId": "heent",
                },
                {
                    "answer": [
                        {"valueString": "Supple, normal ROM, no lymphadenopathy/masses, nontender"}
                    ],
                    "linkId": "neck",
                },
                {
                    "answer": [{"valueString": "RRR, normal S1/S2, no murmurs/gallops/rub"}],
                    "linkId": "cardiovascular",
                },
                {
                    "answer": [
                        {
                            "valueString": "No respiratory distress, lungs CTAB: no rales, rhonchi, or wheeze"
                        }
                    ],
                    "linkId": "pulmonary",
                },
                {
                    "answer": [
                        {
                            "valueString": "Soft and non-tender with no guarding or rebound; +BS normoactive, no tympany on auscultation"
                        }
                    ],
                    "linkId": "abdominal",
                },
                {
                    "answer": [{"valueString": "Normal ROM of UE and LE, normal bulk and tone,"}],
                    "linkId": "musculoskeletal",
                },
                {
                    "answer": [
                        {
                            "valueString": "Pulses intact with normal cap refill, no LE pitting edema or calf tenderness"
                        }
                    ],
                    "linkId": "extremities",
                },
                {
                    "answer": [
                        {
                            "valueString": "AAOx3, converses normally. CN II - XII grossly intact. Gait and coordination intact. 5+ BL UE/LE strength, no gross motor or sensory defects"
                        }
                    ],
                    "linkId": "neurologic",
                },
                {
                    "answer": [
                        {
                            "valueString": "Normal mood and affect. Judgement/competence is appropriate"
                        }
                    ],
                    "linkId": "psychiatric",
                },
                {
                    "answer": [
                        {
                            "valueString": "Warm, dry, and intact. No rashes, dermatoses, petechiae, or lesions"
                        }
                    ],
                    "linkId": "skin",
                },
                {
                    "answer": [
                        {
                            "valueString": "Normal sensation bilaterally on soles of feet with 10g monofilament"
                        }
                    ],
                    "linkId": "monofilament",
                },
                {
                    "answer": [
                        {
                            "valueString": "The chest wall is symmetric, without deformity, and is atraumatic in appearance"
                        }
                    ],
                    "linkId": "chest",
                },
                {
                    "answer": [
                        {"valueString": "External genitalia without erythema, exudate or discharge"}
                    ],
                    "linkId": "genitourinary-female",
                },
                {
                    "answer": [
                        {
                            "valueString": "Normal external anus and normal tone. No palpable masses, normal mucosa, brown stool. Hemoccult negative"
                        }
                    ],
                    "linkId": "rectal",
                },
                {
                    "answer": [
                        {
                            "valueString": "No enlarged lymph nodes of occipital, pre- and postauricular, submandibular, anterior or posterior cervical, or supraclavicular identified"
                        }
                    ],
                    "linkId": "lymphatic",
                },
            ],
            "linkId": "physical-exam-group",
        }
    ],
    "resourceType": "QuestionnaireResponse",
    "source": {"reference": "Patient/683e382b-fed4-433e-9b6d-a847a7953bc0"},
    "status": "completed",
    "id": "288fd914-b836-47dd-863a-e7d86a923f28",
    "authored": "2023-04-06T02:05:51Z",
}

physicalexam_aidbox_QuestionnaireResponse = {
    "questionnaire": "physical-exam",
    "meta": {
        "lastUpdated": "2023-04-06T02:05:52.434771Z",
        "createdAt": "2023-04-06T02:05:32.668369Z",
        "versionId": "20470",
    },
    "encounter": {"id": "e133b999-9e91-4ebd-967e-450bad770682", "resourceType": "Encounter"},
    "item": [
        {
            "item": [
                {
                    "answer": [
                        {
                            "value": {
                                "string": "Well nourished, well developed, awake and alert, resting comfortably in no acute distress, cooperative on exam"
                            }
                        }
                    ],
                    "linkId": "general",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "string": "NCAT, PERRL, normal conjunctivae, nonicteric sclerae, bilateral EAC/TM clear, no nasal discharge, OP clear, moist mucous membranes"
                            }
                        }
                    ],
                    "linkId": "heent",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "string": "Supple, normal ROM, no lymphadenopathy/masses, nontender"
                            }
                        }
                    ],
                    "linkId": "neck",
                },
                {
                    "answer": [{"value": {"string": "RRR, normal S1/S2, no murmurs/gallops/rub"}}],
                    "linkId": "cardiovascular",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "string": "No respiratory distress, lungs CTAB: no rales, rhonchi, or wheeze"
                            }
                        }
                    ],
                    "linkId": "pulmonary",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "string": "Soft and non-tender with no guarding or rebound; +BS normoactive, no tympany on auscultation"
                            }
                        }
                    ],
                    "linkId": "abdominal",
                },
                {
                    "answer": [
                        {"value": {"string": "Normal ROM of UE and LE, normal bulk and tone,"}}
                    ],
                    "linkId": "musculoskeletal",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "string": "Pulses intact with normal cap refill, no LE pitting edema or calf tenderness"
                            }
                        }
                    ],
                    "linkId": "extremities",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "string": "AAOx3, converses normally. CN II - XII grossly intact. Gait and coordination intact. 5+ BL UE/LE strength, no gross motor or sensory defects"
                            }
                        }
                    ],
                    "linkId": "neurologic",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "string": "Normal mood and affect. Judgement/competence is appropriate"
                            }
                        }
                    ],
                    "linkId": "psychiatric",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "string": "Warm, dry, and intact. No rashes, dermatoses, petechiae, or lesions"
                            }
                        }
                    ],
                    "linkId": "skin",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "string": "Normal sensation bilaterally on soles of feet with 10g monofilament"
                            }
                        }
                    ],
                    "linkId": "monofilament",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "string": "The chest wall is symmetric, without deformity, and is atraumatic in appearance"
                            }
                        }
                    ],
                    "linkId": "chest",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "string": "External genitalia without erythema, exudate or discharge"
                            }
                        }
                    ],
                    "linkId": "genitourinary-female",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "string": "Normal external anus and normal tone. No palpable masses, normal mucosa, brown stool. Hemoccult negative"
                            }
                        }
                    ],
                    "linkId": "rectal",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "string": "No enlarged lymph nodes of occipital, pre- and postauricular, submandibular, anterior or posterior cervical, or supraclavicular identified"
                            }
                        }
                    ],
                    "linkId": "lymphatic",
                },
            ],
            "linkId": "physical-exam-group",
        }
    ],
    "resourceType": "QuestionnaireResponse",
    "source": {"id": "683e382b-fed4-433e-9b6d-a847a7953bc0", "resourceType": "Patient"},
    "status": "completed",
    "id": "288fd914-b836-47dd-863a-e7d86a923f28",
    "authored": "2023-04-06T02:05:51Z",
}

reviewofsystems_fhir_QuestionnaireResponse = {
    "authored": "2023-04-06T02:11:08Z",
    "encounter": {"reference": "Encounter/e133b999-9e91-4ebd-967e-450bad770682"},
    "id": "d575fe05-9db2-4df8-b131-48bb5d27509d",
    "item": [
        {"answer": [{"valueBoolean": True}], "linkId": "provider-viewed-confirmation"},
        {
            "item": [
                {"answer": [{"value": {}}], "linkId": "general"},
                {"answer": [{"valueBoolean": True}], "linkId": "heent"},
                {"answer": [{"valueString": "heent"}], "linkId": "heent-comment"},
                {"answer": [{"value": {}}], "linkId": "cardiovascular"},
                {"answer": [{"value": {}}], "linkId": "respiratory"},
                {"answer": [{"valueBoolean": True}], "linkId": "gastrointestinal"},
                {
                    "answer": [{"valueString": "gastrointestinal"}],
                    "linkId": "gastrointestinal-comment",
                },
                {"answer": [{"value": {}}], "linkId": "genitourinary"},
                {"answer": [{"value": {}}], "linkId": "musculoskeletal"},
                {"answer": [{"value": {}}], "linkId": "neurologic"},
                {"answer": [{"valueBoolean": True}], "linkId": "psychiatric"},
                {"answer": [{"valueString": "psychiatric"}], "linkId": "psychiatric-comment"},
                {"answer": [{"value": {}}], "linkId": "skin"},
                {"answer": [{"value": {}}], "linkId": "other"},
            ],
            "linkId": "abnormal-systems-group",
        },
    ],
    "meta": {
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-06T02:10:37.718483Z"}],
        "lastUpdated": "2023-04-06T02:11:09.776717Z",
        "versionId": "20480",
    },
    "questionnaire": "review-of-systems",
    "resourceType": "QuestionnaireResponse",
    "source": {"reference": "Patient/683e382b-fed4-433e-9b6d-a847a7953bc0"},
    "status": "completed",
}

reviewofsystems_aidbox_QuestionnaireResponse = {
    "authored": "2023-04-06T02:11:08Z",
    "encounter": {"id": "e133b999-9e91-4ebd-967e-450bad770682", "resourceType": "Encounter"},
    "id": "d575fe05-9db2-4df8-b131-48bb5d27509d",
    "item": [
        {"answer": [{"value": {"boolean": True}}], "linkId": "provider-viewed-confirmation"},
        {
            "item": [
                {"answer": [{"value": {}}], "linkId": "general"},
                {"answer": [{"value": {"boolean": True}}], "linkId": "heent"},
                {"answer": [{"value": {"string": "heent"}}], "linkId": "heent-comment"},
                {"answer": [{"value": {}}], "linkId": "cardiovascular"},
                {"answer": [{"value": {}}], "linkId": "respiratory"},
                {"answer": [{"value": {"boolean": True}}], "linkId": "gastrointestinal"},
                {
                    "answer": [{"value": {"string": "gastrointestinal"}}],
                    "linkId": "gastrointestinal-comment",
                },
                {"answer": [{"value": {}}], "linkId": "genitourinary"},
                {"answer": [{"value": {}}], "linkId": "musculoskeletal"},
                {"answer": [{"value": {}}], "linkId": "neurologic"},
                {"answer": [{"value": {"boolean": True}}], "linkId": "psychiatric"},
                {"answer": [{"value": {"string": "psychiatric"}}], "linkId": "psychiatric-comment"},
                {"answer": [{"value": {}}], "linkId": "skin"},
                {"answer": [{"value": {}}], "linkId": "other"},
            ],
            "linkId": "abnormal-systems-group",
        },
    ],
    "meta": {
        "createdAt": "2023-04-06T02:10:37.718483Z",
        "lastUpdated": "2023-04-06T02:11:09.776717Z",
        "versionId": "20480",
    },
    "questionnaire": "review-of-systems",
    "resourceType": "QuestionnaireResponse",
    "source": {"id": "683e382b-fed4-433e-9b6d-a847a7953bc0", "resourceType": "Patient"},
    "status": "completed",
}

vitals_fhir_QuestionnaireResponse = {
    "questionnaire": "vitals",
    "meta": {
        "lastUpdated": "2023-04-06T02:20:25.903562Z",
        "versionId": "20492",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-06T02:19:51.712237Z"}],
    },
    "encounter": {"reference": "Encounter/e133b999-9e91-4ebd-967e-450bad770682"},
    "item": [
        {
            "answer": [{"valueString": "683e382b-fed4-433e-9b6d-a847a7953bc0"}],
            "linkId": "patientId",
        },
        {"answer": [{"valueString": "Emily Nguyen"}], "linkId": "patientName"},
        {"answer": [{"valueInteger": 180}], "linkId": "height"},
        {"answer": [{"valueInteger": 80}], "linkId": "weight"},
        {"answer": [{"valueInteger": 36}], "linkId": "temperature"},
        {"answer": [{"valueInteger": 56}], "linkId": "oxygen-saturation"},
        {"answer": [{"valueInteger": 100}], "linkId": "pulse-rate"},
        {"answer": [{"valueInteger": 50}], "linkId": "respiratory-rate"},
        {
            "item": [
                {
                    "item": [
                        {"answer": [{"valueInteger": 45}], "linkId": "blood-pressure-systolic"},
                        {"answer": [{"valueInteger": 67}], "linkId": "blood-pressure-diastolic"},
                    ],
                    "linkId": "blood-pressure-systolic-diastolic",
                },
                {
                    "answer": [{"valueCoding": {"code": "sitting", "display": "Sitting"}}],
                    "linkId": "blood-pressure-positions",
                },
                {
                    "answer": [{"valueCoding": {"code": "biceps-left", "display": "Biceps left"}}],
                    "linkId": "blood-pressure-arm",
                },
            ],
            "linkId": "blood-pressure",
        },
        {"answer": [{"valueInteger": 24.69}], "linkId": "bmi"},
    ],
    "resourceType": "QuestionnaireResponse",
    "source": {"reference": "Patient/683e382b-fed4-433e-9b6d-a847a7953bc0"},
    "status": "completed",
    "id": "a583cc11-99c6-4719-acab-cb3fb72f5078",
    "authored": "2023-04-06T02:20:25Z",
}

vitals_aidbox_QuestionnaireResponse = {
    "questionnaire": "vitals",
    "meta": {
        "lastUpdated": "2023-04-06T02:20:25.903562Z",
        "createdAt": "2023-04-06T02:19:51.712237Z",
        "versionId": "20492",
    },
    "encounter": {"id": "e133b999-9e91-4ebd-967e-450bad770682", "resourceType": "Encounter"},
    "item": [
        {
            "answer": [{"value": {"string": "683e382b-fed4-433e-9b6d-a847a7953bc0"}}],
            "linkId": "patientId",
        },
        {"answer": [{"value": {"string": "Emily Nguyen"}}], "linkId": "patientName"},
        {"answer": [{"value": {"integer": 180}}], "linkId": "height"},
        {"answer": [{"value": {"integer": 80}}], "linkId": "weight"},
        {"answer": [{"value": {"integer": 36}}], "linkId": "temperature"},
        {"answer": [{"value": {"integer": 56}}], "linkId": "oxygen-saturation"},
        {"answer": [{"value": {"integer": 100}}], "linkId": "pulse-rate"},
        {"answer": [{"value": {"integer": 50}}], "linkId": "respiratory-rate"},
        {
            "item": [
                {
                    "item": [
                        {
                            "answer": [{"value": {"integer": 45}}],
                            "linkId": "blood-pressure-systolic",
                        },
                        {
                            "answer": [{"value": {"integer": 67}}],
                            "linkId": "blood-pressure-diastolic",
                        },
                    ],
                    "linkId": "blood-pressure-systolic-diastolic",
                },
                {
                    "answer": [{"value": {"Coding": {"code": "sitting", "display": "Sitting"}}}],
                    "linkId": "blood-pressure-positions",
                },
                {
                    "answer": [
                        {"value": {"Coding": {"code": "biceps-left", "display": "Biceps left"}}}
                    ],
                    "linkId": "blood-pressure-arm",
                },
            ],
            "linkId": "blood-pressure",
        },
        {"answer": [{"value": {"integer": 24.69}}], "linkId": "bmi"},
    ],
    "resourceType": "QuestionnaireResponse",
    "source": {"id": "683e382b-fed4-433e-9b6d-a847a7953bc0", "resourceType": "Patient"},
    "status": "completed",
    "id": "a583cc11-99c6-4719-acab-cb3fb72f5078",
    "authored": "2023-04-06T02:20:25Z",
}

phq2phq9_fhir_QuestionnaireResponse = {
    "authored": "2023-04-06T02:33:05Z",
    "encounter": {"reference": "Encounter/e133b999-9e91-4ebd-967e-450bad770682"},
    "id": "846558b9-4c03-4af6-a258-62b0390633e2",
    "item": [
        {"answer": [{"valueDateTime": "2023-04-06T02:32:40+00:00"}], "linkId": "dateTime"},
        {
            "answer": [{"valueString": "683e382b-fed4-433e-9b6d-a847a7953bc0"}],
            "linkId": "patientId",
        },
        {"answer": [{"valueString": "Emily Nguyen"}], "linkId": "patientName"},
        {
            "item": [
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "display": "Not at all",
                                "system": "http://loinc.org",
                            }
                        }
                    ],
                    "linkId": "44250-9",
                },
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "display": "Several days",
                                "system": "http://loinc.org",
                            }
                        }
                    ],
                    "linkId": "44255-8",
                },
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "display": "More than half the days",
                                "system": "http://loinc.org",
                            }
                        }
                    ],
                    "linkId": "44259-0",
                },
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "display": "Nearly every day",
                                "system": "http://loinc.org",
                            }
                        }
                    ],
                    "linkId": "44254-1",
                },
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "display": "More than half the days",
                                "system": "http://loinc.org",
                            }
                        }
                    ],
                    "linkId": "44251-7",
                },
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "display": "Several days",
                                "system": "http://loinc.org",
                            }
                        }
                    ],
                    "linkId": "44258-2",
                },
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "display": "Not at all",
                                "system": "http://loinc.org",
                            }
                        }
                    ],
                    "linkId": "44252-5",
                },
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "display": "Several days",
                                "system": "http://loinc.org",
                            }
                        }
                    ],
                    "linkId": "44253-3",
                },
                {
                    "answer": [
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "display": "More than half the days",
                                "system": "http://loinc.org",
                            }
                        }
                    ],
                    "linkId": "44260-8",
                },
                {"answer": [{"valueInteger": 12}], "linkId": "phq9-total-score"},
            ],
            "linkId": "phq2phq9",
        },
    ],
    "meta": {
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-06T02:32:41.569773Z"}],
        "lastUpdated": "2023-04-06T02:33:06.758734Z",
        "versionId": "20508",
    },
    "questionnaire": "phq2phq9",
    "resourceType": "QuestionnaireResponse",
    "source": {"reference": "Patient/683e382b-fed4-433e-9b6d-a847a7953bc0"},
    "status": "completed",
}

phq2phq9_aidbox_QuestionnaireResponse = {
    "authored": "2023-04-06T02:33:05Z",
    "encounter": {"id": "e133b999-9e91-4ebd-967e-450bad770682", "resourceType": "Encounter"},
    "id": "846558b9-4c03-4af6-a258-62b0390633e2",
    "item": [
        {"answer": [{"value": {"dateTime": "2023-04-06T02:32:40+00:00"}}], "linkId": "dateTime"},
        {
            "answer": [{"value": {"string": "683e382b-fed4-433e-9b6d-a847a7953bc0"}}],
            "linkId": "patientId",
        },
        {"answer": [{"value": {"string": "Emily Nguyen"}}], "linkId": "patientName"},
        {
            "item": [
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "display": "Not at all",
                                    "system": "http://loinc.org",
                                }
                            }
                        }
                    ],
                    "linkId": "44250-9",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "display": "Several days",
                                    "system": "http://loinc.org",
                                }
                            }
                        }
                    ],
                    "linkId": "44255-8",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "display": "More than half the days",
                                    "system": "http://loinc.org",
                                }
                            }
                        }
                    ],
                    "linkId": "44259-0",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "display": "Nearly every day",
                                    "system": "http://loinc.org",
                                }
                            }
                        }
                    ],
                    "linkId": "44254-1",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "display": "More than half the days",
                                    "system": "http://loinc.org",
                                }
                            }
                        }
                    ],
                    "linkId": "44251-7",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "display": "Several days",
                                    "system": "http://loinc.org",
                                }
                            }
                        }
                    ],
                    "linkId": "44258-2",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "display": "Not at all",
                                    "system": "http://loinc.org",
                                }
                            }
                        }
                    ],
                    "linkId": "44252-5",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "display": "Several days",
                                    "system": "http://loinc.org",
                                }
                            }
                        }
                    ],
                    "linkId": "44253-3",
                },
                {
                    "answer": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "display": "More than half the days",
                                    "system": "http://loinc.org",
                                }
                            }
                        }
                    ],
                    "linkId": "44260-8",
                },
                {"answer": [{"value": {"integer": 12}}], "linkId": "phq9-total-score"},
            ],
            "linkId": "phq2phq9",
        },
    ],
    "meta": {
        "createdAt": "2023-04-06T02:32:41.569773Z",
        "lastUpdated": "2023-04-06T02:33:06.758734Z",
        "versionId": "20508",
    },
    "questionnaire": "phq2phq9",
    "resourceType": "QuestionnaireResponse",
    "source": {"id": "683e382b-fed4-433e-9b6d-a847a7953bc0", "resourceType": "Patient"},
    "status": "completed",
}

immunization_fhir_QuestionnaireResponse = {
    "questionnaire": "immunization",
    "meta": {
        "lastUpdated": "2023-04-06T02:39:03.018390Z",
        "versionId": "20519",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-06T02:38:51.964987Z"}],
    },
    "encounter": {"reference": "Encounter/e133b999-9e91-4ebd-967e-450bad770682"},
    "item": [
        {"answer": [{"valueDateTime": "2023-04-06T02:38:50+00:00"}], "linkId": "dateTime"},
        {
            "answer": [{"valueString": "e133b999-9e91-4ebd-967e-450bad770682"}],
            "linkId": "encounterId",
        },
        {
            "answer": [{"valueString": "683e382b-fed4-433e-9b6d-a847a7953bc0"}],
            "linkId": "patientId",
        },
        {"answer": [{"valueString": "Emily Nguyen"}], "linkId": "patientName"},
        {
            "answer": [
                {
                    "valueCoding": {
                        "code": "173",
                        "system": "http://hl7.org/fhir/sid/cvx",
                        "display": "cholera, BivWC",
                    }
                }
            ],
            "linkId": "vaccine-code",
        },
        {"answer": [{"valueDate": "2023-04-13"}], "linkId": "date-of-injection"},
    ],
    "resourceType": "QuestionnaireResponse",
    "source": {"reference": "Patient/683e382b-fed4-433e-9b6d-a847a7953bc0"},
    "status": "completed",
    "id": "5d59e534-a7ce-4254-8a41-31b3895ea525",
    "authored": "2023-04-06T02:39:02Z",
}

immunization_aidbox_QuestionnaireResponse = {
    "questionnaire": "immunization",
    "meta": {
        "lastUpdated": "2023-04-06T02:39:03.018390Z",
        "createdAt": "2023-04-06T02:38:51.964987Z",
        "versionId": "20519",
    },
    "encounter": {"id": "e133b999-9e91-4ebd-967e-450bad770682", "resourceType": "Encounter"},
    "item": [
        {"answer": [{"value": {"dateTime": "2023-04-06T02:38:50+00:00"}}], "linkId": "dateTime"},
        {
            "answer": [{"value": {"string": "e133b999-9e91-4ebd-967e-450bad770682"}}],
            "linkId": "encounterId",
        },
        {
            "answer": [{"value": {"string": "683e382b-fed4-433e-9b6d-a847a7953bc0"}}],
            "linkId": "patientId",
        },
        {"answer": [{"value": {"string": "Emily Nguyen"}}], "linkId": "patientName"},
        {
            "answer": [
                {
                    "value": {
                        "Coding": {
                            "code": "173",
                            "system": "http://hl7.org/fhir/sid/cvx",
                            "display": "cholera, BivWC",
                        }
                    }
                }
            ],
            "linkId": "vaccine-code",
        },
        {"answer": [{"value": {"date": "2023-04-13"}}], "linkId": "date-of-injection"},
    ],
    "resourceType": "QuestionnaireResponse",
    "source": {"id": "683e382b-fed4-433e-9b6d-a847a7953bc0", "resourceType": "Patient"},
    "status": "completed",
    "id": "5d59e534-a7ce-4254-8a41-31b3895ea525",
    "authored": "2023-04-06T02:39:02Z",
}

cardiology_fhir_QuestionnaireResponse = {
    "questionnaire": "cardiology-example",
    "meta": {
        "lastUpdated": "2023-04-06T02:43:40.015349Z",
        "versionId": "20529",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-06T02:43:16.150751Z"}],
    },
    "encounter": {"reference": "Encounter/e133b999-9e91-4ebd-967e-450bad770682"},
    "item": [
        {"answer": [{"valueString": "123"}], "linkId": "complaints"},
        {"answer": [{"valueString": "123"}], "linkId": "examination-objective"},
        {"answer": [{"valueString": "321"}], "linkId": "observations-data"},
        {"answer": [{"valueString": "321"}], "linkId": "lab-data"},
        {
            "item": [
                {
                    "item": [
                        {
                            "answer": [
                                {
                                    "valueCoding": {
                                        "code": "BA40",
                                        "system": "http://id.who.int/icd/release/11/mms",
                                        "display": "BA40 Angina pectoris",
                                    }
                                }
                            ],
                            "linkId": "ds-icd-11",
                        },
                        {"answer": [{"valueString": "desc 123"}], "linkId": "ds-text"},
                    ],
                    "linkId": "ds-main",
                }
            ],
            "linkId": "group-ds",
        },
    ],
    "resourceType": "QuestionnaireResponse",
    "source": {"reference": "Patient/683e382b-fed4-433e-9b6d-a847a7953bc0"},
    "status": "completed",
    "id": "16917bdf-309f-4cd7-9a8a-56a928dbedea",
    "authored": "2023-04-06T02:43:39Z",
}

cardiology_aidbox_QuestionnaireResponse = {
    "questionnaire": "cardiology-example",
    "meta": {
        "lastUpdated": "2023-04-06T02:43:40.015349Z",
        "createdAt": "2023-04-06T02:43:16.150751Z",
        "versionId": "20529",
    },
    "encounter": {"id": "e133b999-9e91-4ebd-967e-450bad770682", "resourceType": "Encounter"},
    "item": [
        {"answer": [{"value": {"string": "123"}}], "linkId": "complaints"},
        {"answer": [{"value": {"string": "123"}}], "linkId": "examination-objective"},
        {"answer": [{"value": {"string": "321"}}], "linkId": "observations-data"},
        {"answer": [{"value": {"string": "321"}}], "linkId": "lab-data"},
        {
            "item": [
                {
                    "item": [
                        {
                            "answer": [
                                {
                                    "value": {
                                        "Coding": {
                                            "code": "BA40",
                                            "system": "http://id.who.int/icd/release/11/mms",
                                            "display": "BA40 Angina pectoris",
                                        }
                                    }
                                }
                            ],
                            "linkId": "ds-icd-11",
                        },
                        {"answer": [{"value": {"string": "desc 123"}}], "linkId": "ds-text"},
                    ],
                    "linkId": "ds-main",
                }
            ],
            "linkId": "group-ds",
        },
    ],
    "resourceType": "QuestionnaireResponse",
    "source": {"id": "683e382b-fed4-433e-9b6d-a847a7953bc0", "resourceType": "Patient"},
    "status": "completed",
    "id": "16917bdf-309f-4cd7-9a8a-56a928dbedea",
    "authored": "2023-04-06T02:43:39Z",
}

allergies_inprogress_fhir_QuestionnaireResponse = {
    "questionnaire": "allergies",
    "meta": {
        "lastUpdated": "2023-04-06T02:48:18.132716Z",
        "versionId": "20530",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-06T02:48:18.132716Z"}],
    },
    "encounter": {"reference": "Encounter/e133b999-9e91-4ebd-967e-450bad770682"},
    "item": [
        {"answer": [{"valueDateTime": "2023-04-06T02:48:16+00:00"}], "linkId": "dateTime"},
        {
            "answer": [{"valueString": "683e382b-fed4-433e-9b6d-a847a7953bc0"}],
            "linkId": "patientId",
        },
        {"answer": [{"valueString": "Emily Nguyen"}], "linkId": "patientName"},
        {
            "answer": [
                {
                    "valueCoding": {
                        "code": "active",
                        "system": "http://terminology.hl7.org/ValueSet/allergyintolerance-clinical",
                        "display": "Active",
                    }
                }
            ],
            "linkId": "status",
        },
        {"answer": [], "linkId": "type"},
        {"answer": [], "linkId": "reaction"},
        {"answer": [{"value": {}}], "linkId": "notes"},
    ],
    "resourceType": "QuestionnaireResponse",
    "source": {"reference": "Patient/683e382b-fed4-433e-9b6d-a847a7953bc0"},
    "status": "in-progress",
    "id": "f0a0b4cf-ff0e-47e2-814d-3327a138653e",
    "authored": "2023-04-06T02:48:17.734Z",
}

allergies_inprogress_aidbox_QuestionnaireResponse = {
    "questionnaire": "allergies",
    "meta": {
        "lastUpdated": "2023-04-06T02:48:18.132716Z",
        "createdAt": "2023-04-06T02:48:18.132716Z",
        "versionId": "20530",
    },
    "encounter": {"id": "e133b999-9e91-4ebd-967e-450bad770682", "resourceType": "Encounter"},
    "item": [
        {"answer": [{"value": {"dateTime": "2023-04-06T02:48:16+00:00"}}], "linkId": "dateTime"},
        {
            "answer": [{"value": {"string": "683e382b-fed4-433e-9b6d-a847a7953bc0"}}],
            "linkId": "patientId",
        },
        {"answer": [{"value": {"string": "Emily Nguyen"}}], "linkId": "patientName"},
        {
            "answer": [
                {
                    "value": {
                        "Coding": {
                            "code": "active",
                            "system": "http://terminology.hl7.org/ValueSet/allergyintolerance-clinical",
                            "display": "Active",
                        }
                    }
                }
            ],
            "linkId": "status",
        },
        {"answer": [], "linkId": "type"},
        {"answer": [], "linkId": "reaction"},
        {"answer": [{"value": {}}], "linkId": "notes"},
    ],
    "resourceType": "QuestionnaireResponse",
    "source": {"id": "683e382b-fed4-433e-9b6d-a847a7953bc0", "resourceType": "Patient"},
    "status": "in-progress",
    "id": "f0a0b4cf-ff0e-47e2-814d-3327a138653e",
    "authored": "2023-04-06T02:48:17.734Z",
}

newappointment_fhir_QuestionnaireResponse = {
    "authored": "2023-04-05T06:27:57Z",
    "id": "cf6d9d4b-bfcd-463f-9d26-b6769c2a3fc3",
    "item": [
        {
            "answer": [{"valueString": "683e382b-fed4-433e-9b6d-a847a7953bc0"}],
            "linkId": "patientId",
        },
        {"answer": [{"valueString": "Emily Nguyen"}], "linkId": "patientName"},
        {
            "answer": [
                {
                    "valueReference": {
                        "display": "Sanjay Patel - Cardiology",
                        "reference": "PractitionerRole/429e6a55-8a64-4ede-ad12-1206522253eb",
                        "resource": {
                            "healthcareService": [
                                {
                                    "display": "The first appointment",
                                    "id": "consultation",
                                    "resourceType": "HealthcareService",
                                },
                                {
                                    "display": "A follow up visit",
                                    "id": "follow-up",
                                    "resourceType": "HealthcareService",
                                },
                            ],
                            "id": "429e6a55-8a64-4ede-ad12-1206522253eb",
                            "meta": {
                                "createdAt": "2023-04-05T06:09:11.092359Z",
                                "lastUpdated": "2023-04-05T06:09:11.092359Z",
                                "versionId": "20418",
                            },
                            "practitioner": {
                                "id": "42e9bdc0-4fe6-4b8d-a6a5-fcb68f1fe836",
                                "resource": {
                                    "id": "42e9bdc0-4fe6-4b8d-a6a5-fcb68f1fe836",
                                    "meta": {
                                        "createdAt": "2023-04-05T06:09:11.092359Z",
                                        "lastUpdated": "2023-04-05T06:09:11.092359Z",
                                        "versionId": "20416",
                                    },
                                    "name": [{"family": "Patel", "given": ["Sanjay", "Kumar"]}],
                                    "resourceType": "Practitioner",
                                },
                                "resourceType": "Practitioner",
                            },
                            "resourceType": "PractitionerRole",
                            "specialty": [
                                {
                                    "coding": [
                                        {
                                            "code": "394579002",
                                            "display": "Cardiology",
                                            "system": "http://snomed.info/sct",
                                        }
                                    ]
                                }
                            ],
                        },
                    }
                }
            ],
            "linkId": "practitioner-role",
        },
        {
            "answer": [
                {
                    "valueCoding": {
                        "code": "consultation",
                        "display": "The first appointment",
                        "system": "http://fhir.org/guides/argonaut-scheduling/CodeSystem/visit-type",
                    }
                }
            ],
            "linkId": "service",
        },
        {"answer": [{"valueDate": "2023-04-26"}], "linkId": "date"},
        {
            "item": [
                {"answer": [{"valueTime": "15:00:00"}], "linkId": "start-time"},
                {"answer": [{"valueTime": "16:00:00"}], "linkId": "end-time"},
            ],
            "linkId": "Time period",
        },
    ],
    "meta": {
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T06:27:58.499391Z"}],
        "lastUpdated": "2023-04-05T06:27:58.499391Z",
        "versionId": "20420",
    },
    "resourceType": "QuestionnaireResponse",
    "status": "completed",
}

newappointment_aidbox_QuestionnaireResponse = {
    "authored": "2023-04-05T06:27:57Z",
    "id": "cf6d9d4b-bfcd-463f-9d26-b6769c2a3fc3",
    "item": [
        {
            "answer": [{"value": {"string": "683e382b-fed4-433e-9b6d-a847a7953bc0"}}],
            "linkId": "patientId",
        },
        {"answer": [{"value": {"string": "Emily Nguyen"}}], "linkId": "patientName"},
        {
            "answer": [
                {
                    "value": {
                        "Reference": {
                            "display": "Sanjay Patel - Cardiology",
                            "id": "429e6a55-8a64-4ede-ad12-1206522253eb",
                            "resource": {
                                "healthcareService": [
                                    {
                                        "display": "The first appointment",
                                        "id": "consultation",
                                        "resourceType": "HealthcareService",
                                    },
                                    {
                                        "display": "A follow up visit",
                                        "id": "follow-up",
                                        "resourceType": "HealthcareService",
                                    },
                                ],
                                "id": "429e6a55-8a64-4ede-ad12-1206522253eb",
                                "meta": {
                                    "createdAt": "2023-04-05T06:09:11.092359Z",
                                    "lastUpdated": "2023-04-05T06:09:11.092359Z",
                                    "versionId": "20418",
                                },
                                "practitioner": {
                                    "id": "42e9bdc0-4fe6-4b8d-a6a5-fcb68f1fe836",
                                    "resource": {
                                        "id": "42e9bdc0-4fe6-4b8d-a6a5-fcb68f1fe836",
                                        "meta": {
                                            "createdAt": "2023-04-05T06:09:11.092359Z",
                                            "lastUpdated": "2023-04-05T06:09:11.092359Z",
                                            "versionId": "20416",
                                        },
                                        "name": [{"family": "Patel", "given": ["Sanjay", "Kumar"]}],
                                        "resourceType": "Practitioner",
                                    },
                                    "resourceType": "Practitioner",
                                },
                                "resourceType": "PractitionerRole",
                                "specialty": [
                                    {
                                        "coding": [
                                            {
                                                "code": "394579002",
                                                "display": "Cardiology",
                                                "system": "http://snomed.info/sct",
                                            }
                                        ]
                                    }
                                ],
                            },
                            "resourceType": "PractitionerRole",
                        }
                    }
                }
            ],
            "linkId": "practitioner-role",
        },
        {
            "answer": [
                {
                    "value": {
                        "Coding": {
                            "code": "consultation",
                            "display": "The first appointment",
                            "system": "http://fhir.org/guides/argonaut-scheduling/CodeSystem/visit-type",
                        }
                    }
                }
            ],
            "linkId": "service",
        },
        {"answer": [{"value": {"date": "2023-04-26"}}], "linkId": "date"},
        {
            "item": [
                {"answer": [{"value": {"time": "15:00:00"}}], "linkId": "start-time"},
                {"answer": [{"value": {"time": "16:00:00"}}], "linkId": "end-time"},
            ],
            "linkId": "Time period",
        },
    ],
    "meta": {
        "createdAt": "2023-04-05T06:27:58.499391Z",
        "lastUpdated": "2023-04-05T06:27:58.499391Z",
        "versionId": "20420",
    },
    "resourceType": "QuestionnaireResponse",
    "status": "completed",
}

beverages_aidbox_Questionnaire = {
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/baverages",
    "item": [
        {
            "linkId": "slider",
            "itemControl": {"coding": [{"code": "slider"}]},
            "start": 1,
            "type": "decimal",
            "stop": 20,
            "helpText": "How many beverages you are consuming per day?",
            "stopLabel": "20+",
            "sliderStepValue": 2,
            "text": "Frequency per week",
        },
        {
            "text": "Beverage",
            "type": "choice",
            "linkId": "beverage-type",
            "itemControl": {"coding": [{"code": "solid-radio-button"}]},
            "answerOption": [
                {"value": {"Coding": {"code": "beer", "display": "Beer"}}},
                {"value": {"Coding": {"code": "wine", "display": "Wine"}}},
                {"value": {"Coding": {"code": "none", "display": "None"}}},
            ],
            "adjustLastToRight": True,
        },
    ],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
    "name": "Beverages",
    "status": "draft",
    "subjectType": ["Patient"],
    "id": "beverages",
    "resourceType": "Questionnaire",
}

beverages_fhir_Questionnaire = {
    "subjectType": ["Patient"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
    "name": "Beverages",
    "item": [
        {
            "linkId": "slider",
            "type": "decimal",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                    "valueCodeableConcept": {"coding": [{"code": "slider"}]},
                },
                {
                    "url": "https://beda.software/fhir-emr-questionnaire/slider-start",
                    "valueInteger": 1,
                },
                {
                    "url": "https://beda.software/fhir-emr-questionnaire/slider-stop",
                    "valueInteger": 20,
                },
                {
                    "url": "https://beda.software/fhir-emr-questionnaire/help-text",
                    "valueString": "How many beverages you are consuming per day?",
                },
                {
                    "url": "https://beda.software/fhir-emr-questionnaire/slider-stop-label",
                    "valueString": "20+",
                },
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-sliderStepValue",
                    "valueInteger": 2,
                },
            ],
            "text": "Frequency per week",
        },
        {
            "text": "Beverage",
            "type": "choice",
            "linkId": "beverage-type",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                    "valueCodeableConcept": {"coding": [{"code": "solid-radio-button"}]},
                },
                {
                    "url": "https://beda.software/fhir-emr-questionnaire/adjust-last-to-right",
                    "valueBoolean": True,
                },
            ],
            "answerOption": [
                {"valueCoding": {"code": "beer", "display": "Beer"}},
                {"valueCoding": {"code": "wine", "display": "Wine"}},
                {"valueCoding": {"code": "none", "display": "None"}},
            ],
        },
    ],
    "resourceType": "Questionnaire",
    "status": "draft",
    "id": "beverages",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/baverages",
}

allergies_aidbox_Questionnaire = {
    "subjectType": ["Encounter", "Patient"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
    "launchContext": [
        {"name": {"code": "LaunchPatient"}, "type": "patient"},
        {"name": {"code": "Author"}, "type": "resource"},
    ],
    "name": "Allergies",
    "item": [
        {
            "text": "DateTime",
            "type": "dateTime",
            "hidden": True,
            "linkId": "dateTime",
            "initialExpression": {"language": "text/fhirpath", "expression": "now()"},
        },
        {
            "text": "PatientId",
            "type": "string",
            "hidden": True,
            "linkId": "patientId",
            "initialExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
        },
        {
            "text": "PatientName",
            "type": "string",
            "hidden": True,
            "linkId": "patientName",
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Patient.name.given[0] + ' ' + %Patient.name.family",
            },
        },
        {
            "text": "Type",
            "type": "choice",
            "linkId": "type",
            "required": True,
            "itemControl": {"coding": [{"code": "inline-choice"}]},
            "answerOption": [
                {
                    "value": {
                        "Coding": {
                            "code": "418634005",
                            "system": "http://hl7.org/fhir/allergy-intolerance-category",
                            "display": "Drug",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "414285001",
                            "system": "http://hl7.org/fhir/allergy-intolerance-category",
                            "display": "Food",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "426232007",
                            "system": "http://hl7.org/fhir/allergy-intolerance-category",
                            "display": "Environmental",
                        }
                    }
                },
            ],
        },
        {
            "text": "Reaction",
            "type": "choice",
            "linkId": "reaction",
            "repeats": True,
            "itemControl": {"coding": [{"code": "inline-choice"}]},
            "answerOption": [
                {
                    "value": {
                        "Coding": {
                            "code": "39579001",
                            "system": "http://snomed.ct",
                            "display": "Anaphylaxis",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "25064002",
                            "system": "http://snomed.ct",
                            "display": "Headache",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "247472004",
                            "system": "http://snomed.ct",
                            "display": "Hives (Wheal)",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "422587007",
                            "system": "http://snomed.ct",
                            "display": "Nausea",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "422400008",
                            "system": "http://snomed.ct",
                            "display": "Vomiting",
                        }
                    }
                },
            ],
        },
        {
            "text": "Substance",
            "type": "choice",
            "linkId": "substance-drug",
            "enableWhen": [
                {
                    "answer": {"Coding": {"code": "418634005", "system": "http://snomed.ct"}},
                    "operator": "=",
                    "question": "type",
                }
            ],
            "itemControl": {"coding": [{"code": "inline-choice"}]},
            "answerOption": [
                {
                    "value": {
                        "Coding": {
                            "code": "LA26702-3",
                            "system": "http://loinc.org",
                            "display": "Aspirin",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "LA30119-4",
                            "system": "http://loinc.org",
                            "display": "Iodine",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "LA14348-9",
                            "system": "http://loinc.org",
                            "display": "Naproxen, ketoprofen or other non-steroidal",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "LA28487-9",
                            "system": "http://loinc.org",
                            "display": "Penicillin",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "LA30118-6",
                            "system": "http://loinc.org",
                            "display": "Sulfa drugs",
                        }
                    }
                },
            ],
        },
        {
            "text": "Substance",
            "type": "choice",
            "linkId": "substance-food",
            "enableWhen": [
                {
                    "answer": {"Coding": {"code": "414285001", "system": "http://snomed.ct"}},
                    "operator": "=",
                    "question": "type",
                }
            ],
            "itemControl": {"coding": [{"code": "inline-choice"}]},
            "answerOption": [
                {
                    "value": {
                        "Coding": {
                            "code": "102259006",
                            "system": "http://snomed.ct",
                            "display": "Citrus fruit",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "102260001",
                            "system": "http://snomed.ct",
                            "display": "Peanut butter",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "102261002",
                            "system": "http://snomed.ct",
                            "display": "Strawberry",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "102262009",
                            "system": "http://snomed.ct",
                            "display": "Chocolate",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "102263004",
                            "system": "http://snomed.ct",
                            "display": "Eggs",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "102264005",
                            "system": "http://snomed.ct",
                            "display": "Cheese",
                        }
                    }
                },
            ],
        },
        {
            "text": "Substance",
            "type": "choice",
            "linkId": "substance-environmental",
            "enableWhen": [
                {
                    "answer": {"Coding": {"code": "426232007", "system": "http://snomed.ct"}},
                    "operator": "=",
                    "question": "type",
                }
            ],
            "itemControl": {"coding": [{"code": "inline-choice"}]},
            "answerOption": [
                {
                    "value": {
                        "Coding": {
                            "code": "111088007",
                            "system": "http://snomed.ct",
                            "display": "Latex",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "256259004",
                            "system": "http://snomed.ct",
                            "display": "Pollen",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "256277009",
                            "system": "http://snomed.ct",
                            "display": "Grass pollen",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "256417003",
                            "system": "http://snomed.ct",
                            "display": "Horse dander",
                        }
                    }
                },
            ],
        },
        {"text": "Notes", "type": "string", "linkId": "notes"},
        {
            "text": "Active",
            "type": "string",
            "hidden": True,
            "linkId": "status",
            "initial": [
                {
                    "value": {
                        "Coding": {
                            "code": "active",
                            "system": "http://terminology.hl7.org/ValueSet/allergyintolerance-clinical",
                            "display": "Active",
                        }
                    }
                }
            ],
        },
    ],
    "mapping": [{"id": "allergy-extract", "resourceType": "Mapping"}],
    "resourceType": "Questionnaire",
    "status": "active",
    "id": "allergies",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/allergies",
}

allergies_fhir_Questionnaire = {
    "subjectType": ["Encounter", "Patient"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
    "name": "Allergies",
    "item": [
        {
            "text": "DateTime",
            "type": "dateTime",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {"language": "text/fhirpath", "expression": "now()"},
                },
            ],
            "linkId": "dateTime",
        },
        {
            "text": "PatientId",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
                },
            ],
            "linkId": "patientId",
        },
        {
            "text": "PatientName",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.name.given[0] + ' ' + %Patient.name.family",
                    },
                },
            ],
            "linkId": "patientName",
        },
        {
            "text": "Type",
            "type": "choice",
            "linkId": "type",
            "required": True,
            "answerOption": [
                {
                    "valueCoding": {
                        "code": "418634005",
                        "system": "http://hl7.org/fhir/allergy-intolerance-category",
                        "display": "Drug",
                    }
                },
                {
                    "valueCoding": {
                        "code": "414285001",
                        "system": "http://hl7.org/fhir/allergy-intolerance-category",
                        "display": "Food",
                    }
                },
                {
                    "valueCoding": {
                        "code": "426232007",
                        "system": "http://hl7.org/fhir/allergy-intolerance-category",
                        "display": "Environmental",
                    }
                },
            ],
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                    "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                }
            ],
        },
        {
            "text": "Reaction",
            "type": "choice",
            "linkId": "reaction",
            "repeats": True,
            "answerOption": [
                {
                    "valueCoding": {
                        "code": "39579001",
                        "system": "http://snomed.ct",
                        "display": "Anaphylaxis",
                    }
                },
                {
                    "valueCoding": {
                        "code": "25064002",
                        "system": "http://snomed.ct",
                        "display": "Headache",
                    }
                },
                {
                    "valueCoding": {
                        "code": "247472004",
                        "system": "http://snomed.ct",
                        "display": "Hives (Wheal)",
                    }
                },
                {
                    "valueCoding": {
                        "code": "422587007",
                        "system": "http://snomed.ct",
                        "display": "Nausea",
                    }
                },
                {
                    "valueCoding": {
                        "code": "422400008",
                        "system": "http://snomed.ct",
                        "display": "Vomiting",
                    }
                },
            ],
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                    "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                }
            ],
        },
        {
            "text": "Substance",
            "type": "choice",
            "linkId": "substance-drug",
            "enableWhen": [
                {
                    "question": "type",
                    "operator": "=",
                    "answerCoding": {"code": "418634005", "system": "http://snomed.ct"},
                }
            ],
            "answerOption": [
                {
                    "valueCoding": {
                        "code": "LA26702-3",
                        "system": "http://loinc.org",
                        "display": "Aspirin",
                    }
                },
                {
                    "valueCoding": {
                        "code": "LA30119-4",
                        "system": "http://loinc.org",
                        "display": "Iodine",
                    }
                },
                {
                    "valueCoding": {
                        "code": "LA14348-9",
                        "system": "http://loinc.org",
                        "display": "Naproxen, ketoprofen or other non-steroidal",
                    }
                },
                {
                    "valueCoding": {
                        "code": "LA28487-9",
                        "system": "http://loinc.org",
                        "display": "Penicillin",
                    }
                },
                {
                    "valueCoding": {
                        "code": "LA30118-6",
                        "system": "http://loinc.org",
                        "display": "Sulfa drugs",
                    }
                },
            ],
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                    "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                }
            ],
        },
        {
            "text": "Substance",
            "type": "choice",
            "linkId": "substance-food",
            "enableWhen": [
                {
                    "question": "type",
                    "operator": "=",
                    "answerCoding": {"code": "414285001", "system": "http://snomed.ct"},
                }
            ],
            "answerOption": [
                {
                    "valueCoding": {
                        "code": "102259006",
                        "system": "http://snomed.ct",
                        "display": "Citrus fruit",
                    }
                },
                {
                    "valueCoding": {
                        "code": "102260001",
                        "system": "http://snomed.ct",
                        "display": "Peanut butter",
                    }
                },
                {
                    "valueCoding": {
                        "code": "102261002",
                        "system": "http://snomed.ct",
                        "display": "Strawberry",
                    }
                },
                {
                    "valueCoding": {
                        "code": "102262009",
                        "system": "http://snomed.ct",
                        "display": "Chocolate",
                    }
                },
                {
                    "valueCoding": {
                        "code": "102263004",
                        "system": "http://snomed.ct",
                        "display": "Eggs",
                    }
                },
                {
                    "valueCoding": {
                        "code": "102264005",
                        "system": "http://snomed.ct",
                        "display": "Cheese",
                    }
                },
            ],
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                    "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                }
            ],
        },
        {
            "text": "Substance",
            "type": "choice",
            "linkId": "substance-environmental",
            "enableWhen": [
                {
                    "question": "type",
                    "operator": "=",
                    "answerCoding": {"code": "426232007", "system": "http://snomed.ct"},
                }
            ],
            "answerOption": [
                {
                    "valueCoding": {
                        "code": "111088007",
                        "system": "http://snomed.ct",
                        "display": "Latex",
                    }
                },
                {
                    "valueCoding": {
                        "code": "256259004",
                        "system": "http://snomed.ct",
                        "display": "Pollen",
                    }
                },
                {
                    "valueCoding": {
                        "code": "256277009",
                        "system": "http://snomed.ct",
                        "display": "Grass pollen",
                    }
                },
                {
                    "valueCoding": {
                        "code": "256417003",
                        "system": "http://snomed.ct",
                        "display": "Horse dander",
                    }
                },
            ],
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                    "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                }
            ],
        },
        {"text": "Notes", "type": "string", "linkId": "notes"},
        {
            "text": "Active",
            "type": "string",
            "initial": [
                {
                    "valueCoding": {
                        "code": "active",
                        "system": "http://terminology.hl7.org/ValueSet/allergyintolerance-clinical",
                        "display": "Active",
                    }
                }
            ],
            "linkId": "status",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                }
            ],
        },
    ],
    "resourceType": "Questionnaire",
    "extension": [
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "LaunchPatient",
                    },
                },
                {"url": "type", "valueCode": "patient"},
            ],
        },
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "Author",
                    },
                },
                {"url": "type", "valueCode": "resource"},
            ],
        },
        {
            "url": "http://beda.software/fhir-extensions/questionnaire-mapper",
            "valueReference": {"reference": "Mapping/allergy-extract"},
        },
    ],
    "status": "active",
    "id": "allergies",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/allergies",
}

encounter_create_aidbox_Questionnaire = {
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
    "launchContext": [{"name": {"code": "Patient"}, "type": "patient"}],
    "name": "encounter-create",
    "item": [
        {
            "text": "PatientId",
            "type": "string",
            "hidden": True,
            "linkId": "patientId",
            "initialExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
        },
        {
            "text": "PatientName",
            "type": "string",
            "linkId": "patientName",
            "readOnly": True,
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Patient.name.given[0] + ' ' + %Patient.name.family",
            },
        },
        {
            "text": "Practitioner",
            "type": "reference",
            "linkId": "practitioner-role",
            "required": True,
            "choiceColumn": [
                {
                    "path": "practitioner.resource.name.given.first() + ' ' + practitioner.resource.name.family + ' - ' + specialty.first().coding.display",
                    "forDisplay": True,
                }
            ],
            "answerExpression": {
                "language": "application/x-fhir-query",
                "expression": "PractitionerRole?_assoc=practitioner",
            },
            "referenceResource": ["PractitionerRole"],
        },
        {
            "text": "Service",
            "type": "choice",
            "linkId": "service",
            "repeats": False,
            "required": True,
            "answerOption": [
                {
                    "value": {
                        "Coding": {
                            "code": "consultation",
                            "system": "http://fhir.org/guides/argonaut-scheduling/CodeSystem/visit-type",
                            "display": "The first appointment",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "follow-up",
                            "system": "http://fhir.org/guides/argonaut-scheduling/CodeSystem/visit-type",
                            "display": "A follow up visit",
                        }
                    }
                },
            ],
        },
        {"text": "Date", "type": "date", "linkId": "date"},
        {
            "item": [
                {"type": "time", "linkId": "start-time"},
                {"type": "time", "linkId": "end-time"},
            ],
            "text": "Time",
            "type": "group",
            "linkId": "Time period",
            "itemControl": {"coding": [{"code": "time-range-picker"}]},
        },
    ],
    "mapping": [{"id": "encounter-create-extract", "resourceType": "Mapping"}],
    "resourceType": "Questionnaire",
    "title": "Encounter create",
    "status": "active",
    "id": "encounter-create",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/encounter-create",
}

encounter_create_fhir_Questionnaire = {
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
    "name": "encounter-create",
    "item": [
        {
            "text": "PatientId",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
                },
            ],
            "linkId": "patientId",
        },
        {
            "text": "PatientName",
            "type": "string",
            "linkId": "patientName",
            "readOnly": True,
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.name.given[0] + ' ' + %Patient.name.family",
                    },
                }
            ],
        },
        {
            "text": "Practitioner",
            "type": "reference",
            "linkId": "practitioner-role",
            "required": True,
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-choiceColumn",
                    "extension": [
                        {
                            "url": "path",
                            "valueString": "practitioner.resource.name.given.first() + ' ' + practitioner.resource.name.family + ' - ' + specialty.first().coding.display",
                        },
                        {"url": "forDisplay", "valueBoolean": True},
                    ],
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-answerExpression",
                    "valueExpression": {
                        "language": "application/x-fhir-query",
                        "expression": "PractitionerRole?_assoc=practitioner",
                    },
                },
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-referenceResource",
                    "valueCode": "PractitionerRole",
                },
            ],
        },
        {
            "text": "Service",
            "type": "choice",
            "linkId": "service",
            "repeats": False,
            "required": True,
            "answerOption": [
                {
                    "valueCoding": {
                        "code": "consultation",
                        "system": "http://fhir.org/guides/argonaut-scheduling/CodeSystem/visit-type",
                        "display": "The first appointment",
                    }
                },
                {
                    "valueCoding": {
                        "code": "follow-up",
                        "system": "http://fhir.org/guides/argonaut-scheduling/CodeSystem/visit-type",
                        "display": "A follow up visit",
                    }
                },
            ],
        },
        {"text": "Date", "type": "date", "linkId": "date"},
        {
            "item": [
                {"type": "time", "linkId": "start-time"},
                {"type": "time", "linkId": "end-time"},
            ],
            "text": "Time",
            "type": "group",
            "linkId": "Time period",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                    "valueCodeableConcept": {"coding": [{"code": "time-range-picker"}]},
                }
            ],
        },
    ],
    "resourceType": "Questionnaire",
    "title": "Encounter create",
    "extension": [
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "Patient",
                    },
                },
                {"url": "type", "valueCode": "patient"},
            ],
        },
        {
            "url": "http://beda.software/fhir-extensions/questionnaire-mapper",
            "valueReference": {"reference": "Mapping/encounter-create-extract"},
        },
    ],
    "status": "active",
    "id": "encounter-create",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/encounter-create",
}

gad7_aidbox_Questionnaire = {
    "subjectType": ["Encounter", "Patient"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
    "launchContext": [
        {"name": {"code": "Patient"}, "type": "patient"},
        {"name": {"code": "Author"}, "type": "resource"},
    ],
    "name": "GAD-7",
    "item": [
        {
            "text": "DateTime",
            "type": "dateTime",
            "hidden": True,
            "linkId": "dateTime",
            "initialExpression": {"language": "text/fhirpath", "expression": "now()"},
        },
        {
            "text": "PatientId",
            "type": "string",
            "hidden": True,
            "linkId": "patientId",
            "initialExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
        },
        {
            "text": "PatientName",
            "type": "string",
            "hidden": True,
            "linkId": "patientName",
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Patient.name.given[0] + ' ' + %Patient.name.family",
            },
        },
        {
            "item": [
                {
                    "text": "Feeling nervous, anxious, or on edge",
                    "type": "choice",
                    "linkId": "69725-0",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "Not being able to stop or control worrying",
                    "type": "choice",
                    "linkId": "68509-9",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "Worrying too much about different things",
                    "type": "choice",
                    "linkId": "69733-4",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "Trouble relaxing",
                    "type": "choice",
                    "linkId": "69734-2",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "Being so restless that it is hard to sit still",
                    "type": "choice",
                    "linkId": "69735-9",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "Becoming easily annoyed or irritable",
                    "type": "choice",
                    "linkId": "69689-8",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "Feeling afraid, as if something awful might happen",
                    "type": "choice",
                    "linkId": "69736-7",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "GAD-7 Anxiety Severity Score",
                    "type": "integer",
                    "linkId": "anxiety-score",
                    "readOnly": True,
                    "required": True,
                    "itemControl": {"coding": [{"code": "anxiety-score"}]},
                    "calculatedExpression": {
                        "language": "text/fhirpath",
                        "expression": "%QuestionnaireResponse.item.item.answer.children().children().where(code='LA6569-3').count() + %QuestionnaireResponse.item.item.answer.children().children().where(code='LA6570-1').count() * 2 + %QuestionnaireResponse.item.item.answer.children().children().where(code='LA6571-9').count() * 3",
                    },
                },
            ],
            "text": "Over the last two weeks, how often have you been bothered by the following problems?",
            "type": "group",
            "linkId": "gad-7",
        },
    ],
    "mapping": [{"id": "gad-7-extract", "resourceType": "Mapping"}],
    "resourceType": "Questionnaire",
    "status": "active",
    "id": "gad-7",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/gad7",
}

gad7_fhir_Questionnaire = {
    "subjectType": ["Encounter", "Patient"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
    "name": "GAD-7",
    "item": [
        {
            "text": "DateTime",
            "type": "dateTime",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {"language": "text/fhirpath", "expression": "now()"},
                },
            ],
            "linkId": "dateTime",
        },
        {
            "text": "PatientId",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
                },
            ],
            "linkId": "patientId",
        },
        {
            "text": "PatientName",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.name.given[0] + ' ' + %Patient.name.family",
                    },
                },
            ],
            "linkId": "patientName",
        },
        {
            "item": [
                {
                    "text": "Feeling nervous, anxious, or on edge",
                    "type": "choice",
                    "linkId": "69725-0",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "Not being able to stop or control worrying",
                    "type": "choice",
                    "linkId": "68509-9",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "Worrying too much about different things",
                    "type": "choice",
                    "linkId": "69733-4",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "Trouble relaxing",
                    "type": "choice",
                    "linkId": "69734-2",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "Being so restless that it is hard to sit still",
                    "type": "choice",
                    "linkId": "69735-9",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "Becoming easily annoyed or irritable",
                    "type": "choice",
                    "linkId": "69689-8",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "Feeling afraid, as if something awful might happen",
                    "type": "choice",
                    "linkId": "69736-7",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "GAD-7 Anxiety Severity Score",
                    "type": "integer",
                    "linkId": "anxiety-score",
                    "readOnly": True,
                    "required": True,
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "anxiety-score"}]},
                        },
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-calculatedExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "%QuestionnaireResponse.item.item.answer.children().children().where(code='LA6569-3').count() + %QuestionnaireResponse.item.item.answer.children().children().where(code='LA6570-1').count() * 2 + %QuestionnaireResponse.item.item.answer.children().children().where(code='LA6571-9').count() * 3",
                            },
                        },
                    ],
                },
            ],
            "text": "Over the last two weeks, how often have you been bothered by the following problems?",
            "type": "group",
            "linkId": "gad-7",
        },
    ],
    "resourceType": "Questionnaire",
    "extension": [
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "Patient",
                    },
                },
                {"url": "type", "valueCode": "patient"},
            ],
        },
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "Author",
                    },
                },
                {"url": "type", "valueCode": "resource"},
            ],
        },
        {
            "url": "http://beda.software/fhir-extensions/questionnaire-mapper",
            "valueReference": {"reference": "Mapping/gad-7-extract"},
        },
    ],
    "status": "active",
    "id": "gad-7",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/gad7",
}

immunization_aidbox_Questionnaire = {
    "subjectType": ["Encounter", "Patient"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
    "launchContext": [
        {"name": {"code": "Patient"}, "type": "patient"},
        {"name": {"code": "Author"}, "type": "resource"},
    ],
    "name": "Immunization",
    "item": [
        {
            "text": "DateTime",
            "type": "dateTime",
            "hidden": True,
            "linkId": "dateTime",
            "initialExpression": {"language": "text/fhirpath", "expression": "now()"},
        },
        {
            "text": "EncounterId",
            "type": "string",
            "hidden": True,
            "linkId": "encounterId",
            "initialExpression": {"language": "text/fhirpath", "expression": "%Encounter.id"},
        },
        {
            "text": "PatientId",
            "type": "string",
            "hidden": True,
            "linkId": "patientId",
            "required": True,
            "initialExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
        },
        {
            "text": "PatientName",
            "type": "string",
            "hidden": True,
            "linkId": "patientName",
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Patient.name.given[0] + ' ' + %Patient.name.family",
            },
        },
        {
            "text": "Vaccine",
            "type": "choice",
            "linkId": "vaccine-code",
            "required": True,
            "answerOption": [
                {
                    "value": {
                        "Coding": {
                            "code": "143",
                            "system": "http://hl7.org/fhir/sid/cvx",
                            "display": "Adenovirus types 4 and 7",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "24",
                            "system": "http://hl7.org/fhir/sid/cvx",
                            "display": "anthrax",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "173",
                            "system": "http://hl7.org/fhir/sid/cvx",
                            "display": "cholera, BivWC",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "56",
                            "system": "http://hl7.org/fhir/sid/cvx",
                            "display": "dengue fever",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "12",
                            "system": "http://hl7.org/fhir/sid/cvx",
                            "display": "diphtheria antitoxin",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "52",
                            "system": "http://hl7.org/fhir/sid/cvx",
                            "display": "Hep A, adult",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "58",
                            "system": "http://hl7.org/fhir/sid/cvx",
                            "display": "Hep C",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "60",
                            "system": "http://hl7.org/fhir/sid/cvx",
                            "display": "herpes simplex 2",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "61",
                            "system": "http://hl7.org/fhir/sid/cvx",
                            "display": "HIV",
                        }
                    }
                },
            ],
        },
        {"text": "Date of injection", "type": "date", "linkId": "date-of-injection"},
    ],
    "mapping": [{"id": "immunization-extract", "resourceType": "Mapping"}],
    "resourceType": "Questionnaire",
    "status": "active",
    "id": "immunization",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/immunization",
}

immunization_fhir_Questionnaire = {
    "subjectType": ["Encounter", "Patient"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
    "name": "Immunization",
    "item": [
        {
            "text": "DateTime",
            "type": "dateTime",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {"language": "text/fhirpath", "expression": "now()"},
                },
            ],
            "linkId": "dateTime",
        },
        {
            "text": "EncounterId",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {"language": "text/fhirpath", "expression": "%Encounter.id"},
                },
            ],
            "linkId": "encounterId",
        },
        {
            "text": "PatientId",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
                },
            ],
            "linkId": "patientId",
            "required": True,
        },
        {
            "text": "PatientName",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.name.given[0] + ' ' + %Patient.name.family",
                    },
                },
            ],
            "linkId": "patientName",
        },
        {
            "text": "Vaccine",
            "type": "choice",
            "linkId": "vaccine-code",
            "required": True,
            "answerOption": [
                {
                    "valueCoding": {
                        "code": "143",
                        "system": "http://hl7.org/fhir/sid/cvx",
                        "display": "Adenovirus types 4 and 7",
                    }
                },
                {
                    "valueCoding": {
                        "code": "24",
                        "system": "http://hl7.org/fhir/sid/cvx",
                        "display": "anthrax",
                    }
                },
                {
                    "valueCoding": {
                        "code": "173",
                        "system": "http://hl7.org/fhir/sid/cvx",
                        "display": "cholera, BivWC",
                    }
                },
                {
                    "valueCoding": {
                        "code": "56",
                        "system": "http://hl7.org/fhir/sid/cvx",
                        "display": "dengue fever",
                    }
                },
                {
                    "valueCoding": {
                        "code": "12",
                        "system": "http://hl7.org/fhir/sid/cvx",
                        "display": "diphtheria antitoxin",
                    }
                },
                {
                    "valueCoding": {
                        "code": "52",
                        "system": "http://hl7.org/fhir/sid/cvx",
                        "display": "Hep A, adult",
                    }
                },
                {
                    "valueCoding": {
                        "code": "58",
                        "system": "http://hl7.org/fhir/sid/cvx",
                        "display": "Hep C",
                    }
                },
                {
                    "valueCoding": {
                        "code": "60",
                        "system": "http://hl7.org/fhir/sid/cvx",
                        "display": "herpes simplex 2",
                    }
                },
                {
                    "valueCoding": {
                        "code": "61",
                        "system": "http://hl7.org/fhir/sid/cvx",
                        "display": "HIV",
                    }
                },
            ],
        },
        {"text": "Date of injection", "type": "date", "linkId": "date-of-injection"},
    ],
    "resourceType": "Questionnaire",
    "extension": [
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "Patient",
                    },
                },
                {"url": "type", "valueCode": "patient"},
            ],
        },
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "Author",
                    },
                },
                {"url": "type", "valueCode": "resource"},
            ],
        },
        {
            "url": "http://beda.software/fhir-extensions/questionnaire-mapper",
            "valueReference": {"reference": "Mapping/immunization-extract"},
        },
    ],
    "status": "active",
    "id": "immunization",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/immunization",
}

medication_aidbox_Questionnaire = {
    "subjectType": ["Encounter", "Patient"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
    "launchContext": [
        {"name": {"code": "Patient"}, "type": "patient"},
        {"name": {"code": "Author"}, "type": "resource"},
    ],
    "name": "Medication",
    "item": [
        {
            "text": "DateTime",
            "type": "dateTime",
            "hidden": True,
            "linkId": "dateTime",
            "initialExpression": {"language": "text/fhirpath", "expression": "now()"},
        },
        {
            "text": "EncounterId",
            "type": "string",
            "hidden": True,
            "linkId": "encounterId",
            "initialExpression": {"language": "text/fhirpath", "expression": "%Encounter.id"},
        },
        {
            "text": "PatientId",
            "type": "string",
            "hidden": True,
            "linkId": "patientId",
            "required": True,
            "initialExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
        },
        {
            "text": "PatientName",
            "type": "string",
            "hidden": True,
            "linkId": "patientName",
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Patient.name.given[0] + ' ' + %Patient.name.family",
            },
        },
        {
            "text": "Medication name",
            "type": "choice",
            "linkId": "medication",
            "required": True,
            "answerOption": [
                {
                    "value": {
                        "Coding": {
                            "code": "261000",
                            "system": "http://snomed.info/sct",
                            "display": "Codeine phosphate",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "2336001",
                            "system": "http://snomed.info/sct",
                            "display": "Fibrinogen Tokyo II",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "363000",
                            "system": "http://snomed.info/sct",
                            "display": "Fibrinogen San Juan",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "519005",
                            "system": "http://snomed.info/sct",
                            "display": "Free protein S",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "585007",
                            "system": "http://snomed.info/sct",
                            "display": "SP - Substance P",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "693002",
                            "system": "http://snomed.info/sct",
                            "display": "Trichothecene",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "698006",
                            "system": "http://snomed.info/sct",
                            "display": "Erythromycin lactobionate",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "699003",
                            "system": "http://snomed.info/sct",
                            "display": "Coal tar extract",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "747006",
                            "system": "http://snomed.info/sct",
                            "display": "Oxamniquine",
                        }
                    }
                },
            ],
        },
        {"text": "Dosage", "type": "string", "linkId": "dosage", "required": True},
        {"text": "Start Date", "type": "date", "linkId": "start-date"},
        {"text": "Stop Date", "type": "date", "linkId": "stop-date"},
        {"text": "Notes", "type": "string", "linkId": "notes"},
    ],
    "mapping": [{"id": "medication-statement-extract", "resourceType": "Mapping"}],
    "resourceType": "Questionnaire",
    "status": "active",
    "id": "medication",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/medication",
}

medication_fhir_Questionnaire = {
    "subjectType": ["Encounter", "Patient"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
    "name": "Medication",
    "item": [
        {
            "text": "DateTime",
            "type": "dateTime",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {"language": "text/fhirpath", "expression": "now()"},
                },
            ],
            "linkId": "dateTime",
        },
        {
            "text": "EncounterId",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {"language": "text/fhirpath", "expression": "%Encounter.id"},
                },
            ],
            "linkId": "encounterId",
        },
        {
            "text": "PatientId",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
                },
            ],
            "linkId": "patientId",
            "required": True,
        },
        {
            "text": "PatientName",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.name.given[0] + ' ' + %Patient.name.family",
                    },
                },
            ],
            "linkId": "patientName",
        },
        {
            "text": "Medication name",
            "type": "choice",
            "linkId": "medication",
            "required": True,
            "answerOption": [
                {
                    "valueCoding": {
                        "code": "261000",
                        "system": "http://snomed.info/sct",
                        "display": "Codeine phosphate",
                    }
                },
                {
                    "valueCoding": {
                        "code": "2336001",
                        "system": "http://snomed.info/sct",
                        "display": "Fibrinogen Tokyo II",
                    }
                },
                {
                    "valueCoding": {
                        "code": "363000",
                        "system": "http://snomed.info/sct",
                        "display": "Fibrinogen San Juan",
                    }
                },
                {
                    "valueCoding": {
                        "code": "519005",
                        "system": "http://snomed.info/sct",
                        "display": "Free protein S",
                    }
                },
                {
                    "valueCoding": {
                        "code": "585007",
                        "system": "http://snomed.info/sct",
                        "display": "SP - Substance P",
                    }
                },
                {
                    "valueCoding": {
                        "code": "693002",
                        "system": "http://snomed.info/sct",
                        "display": "Trichothecene",
                    }
                },
                {
                    "valueCoding": {
                        "code": "698006",
                        "system": "http://snomed.info/sct",
                        "display": "Erythromycin lactobionate",
                    }
                },
                {
                    "valueCoding": {
                        "code": "699003",
                        "system": "http://snomed.info/sct",
                        "display": "Coal tar extract",
                    }
                },
                {
                    "valueCoding": {
                        "code": "747006",
                        "system": "http://snomed.info/sct",
                        "display": "Oxamniquine",
                    }
                },
            ],
        },
        {"text": "Dosage", "type": "string", "linkId": "dosage", "required": True},
        {"text": "Start Date", "type": "date", "linkId": "start-date"},
        {"text": "Stop Date", "type": "date", "linkId": "stop-date"},
        {"text": "Notes", "type": "string", "linkId": "notes"},
    ],
    "resourceType": "Questionnaire",
    "extension": [
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "Patient",
                    },
                },
                {"url": "type", "valueCode": "patient"},
            ],
        },
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "Author",
                    },
                },
                {"url": "type", "valueCode": "resource"},
            ],
        },
        {
            "url": "http://beda.software/fhir-extensions/questionnaire-mapper",
            "valueReference": {"reference": "Mapping/medication-statement-extract"},
        },
    ],
    "status": "active",
    "id": "medication",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/medication",
}

patient_create_aidbox_Questionnaire = {
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
    "name": "patient-create",
    "item": [
        {"text": "patientId", "type": "string", "hidden": True, "linkId": "patient-id"},
        {"text": "Last name", "type": "string", "linkId": "last-name", "required": True},
        {"text": "First name", "type": "string", "linkId": "first-name", "required": True},
        {"text": "Middle name", "type": "string", "linkId": "middle-name"},
        {"text": "Birth date", "type": "date", "linkId": "birth-date"},
        {
            "text": "Gender",
            "type": "choice",
            "linkId": "gender",
            "answerOption": [{"value": {"string": "male"}}, {"value": {"string": "female"}}],
        },
        {"text": "SSN", "type": "string", "linkId": "ssn"},
        {
            "text": "Phone number",
            "type": "string",
            "linkId": "mobile",
            "itemControl": {"coding": [{"code": "phoneWidget"}]},
        },
    ],
    "mapping": [{"id": "patient-create", "resourceType": "Mapping"}],
    "resourceType": "Questionnaire",
    "title": "Patient create",
    "status": "active",
    "id": "patient-create",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/patient-create",
}

patient_create_fhir_Questionnaire = {
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
    "name": "patient-create",
    "item": [
        {
            "text": "patientId",
            "type": "string",
            "linkId": "patient-id",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                }
            ],
        },
        {"text": "Last name", "type": "string", "linkId": "last-name", "required": True},
        {"text": "First name", "type": "string", "linkId": "first-name", "required": True},
        {"text": "Middle name", "type": "string", "linkId": "middle-name"},
        {"text": "Birth date", "type": "date", "linkId": "birth-date"},
        {
            "text": "Gender",
            "type": "choice",
            "linkId": "gender",
            "answerOption": [{"valueString": "male"}, {"valueString": "female"}],
        },
        {"text": "SSN", "type": "string", "linkId": "ssn"},
        {
            "text": "Phone number",
            "type": "string",
            "linkId": "mobile",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                    "valueCodeableConcept": {"coding": [{"code": "phoneWidget"}]},
                }
            ],
        },
    ],
    "resourceType": "Questionnaire",
    "title": "Patient create",
    "extension": [
        {
            "url": "http://beda.software/fhir-extensions/questionnaire-mapper",
            "valueReference": {"reference": "Mapping/patient-create"},
        }
    ],
    "status": "active",
    "id": "patient-create",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/patient-create",
}

patient_edit_aidbox_Questionnaire = {
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
    "launchContext": [{"name": {"code": "Patient"}, "type": "patient"}],
    "name": "edit-patient",
    "item": [
        {
            "text": "patientId",
            "type": "string",
            "hidden": True,
            "linkId": "patient-id",
            "readOnly": True,
            "initialExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
        },
        {
            "text": "Last name",
            "type": "string",
            "linkId": "last-name",
            "required": True,
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Patient.name.family",
            },
        },
        {
            "text": "First name",
            "type": "string",
            "linkId": "first-name",
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Patient.name.given[0]",
            },
        },
        {
            "text": "Middle name",
            "type": "string",
            "linkId": "middle-name",
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Patient.name.given[1]",
            },
        },
        {
            "text": "Birth date",
            "type": "date",
            "linkId": "birth-date",
            "initialExpression": {"language": "text/fhirpath", "expression": "%Patient.birthDate"},
        },
        {
            "text": "Gender",
            "type": "choice",
            "linkId": "gender",
            "answerOption": [{"value": {"string": "male"}}, {"value": {"string": "female"}}],
            "initialExpression": {"language": "text/fhirpath", "expression": "%Patient.gender"},
        },
        {
            "text": "SSN",
            "type": "string",
            "linkId": "ssn",
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Patient.identifier.where(system='1.2.643.100.3').value",
            },
        },
        {
            "text": "Phone number",
            "type": "string",
            "linkId": "mobile",
            "itemControl": {"coding": [{"code": "phoneWidget"}]},
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Patient.telecom.where(system='phone').value",
            },
        },
    ],
    "mapping": [{"id": "patient-create", "resourceType": "Mapping"}],
    "resourceType": "Questionnaire",
    "title": "Edit patient",
    "status": "active",
    "id": "patient-edit",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/patient-edit",
}

patient_edit_fhir_Questionnaire = {
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
    "name": "edit-patient",
    "item": [
        {
            "text": "patientId",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
                },
            ],
            "linkId": "patient-id",
            "readOnly": True,
        },
        {
            "text": "Last name",
            "type": "string",
            "linkId": "last-name",
            "required": True,
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.name.family",
                    },
                }
            ],
        },
        {
            "text": "First name",
            "type": "string",
            "linkId": "first-name",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.name.given[0]",
                    },
                }
            ],
        },
        {
            "text": "Middle name",
            "type": "string",
            "linkId": "middle-name",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.name.given[1]",
                    },
                }
            ],
        },
        {
            "text": "Birth date",
            "type": "date",
            "linkId": "birth-date",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.birthDate",
                    },
                }
            ],
        },
        {
            "text": "Gender",
            "type": "choice",
            "linkId": "gender",
            "answerOption": [{"valueString": "male"}, {"valueString": "female"}],
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.gender",
                    },
                }
            ],
        },
        {
            "text": "SSN",
            "type": "string",
            "linkId": "ssn",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.identifier.where(system='1.2.643.100.3').value",
                    },
                }
            ],
        },
        {
            "text": "Phone number",
            "type": "string",
            "linkId": "mobile",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                    "valueCodeableConcept": {"coding": [{"code": "phoneWidget"}]},
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.telecom.where(system='phone').value",
                    },
                },
            ],
        },
    ],
    "resourceType": "Questionnaire",
    "title": "Edit patient",
    "extension": [
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "Patient",
                    },
                },
                {"url": "type", "valueCode": "patient"},
            ],
        },
        {
            "url": "http://beda.software/fhir-extensions/questionnaire-mapper",
            "valueReference": {"reference": "Mapping/patient-create"},
        },
    ],
    "status": "active",
    "id": "patient-edit",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/patient-edit",
}

phq2phq9_aidbox_Questionnaire = {
    "subjectType": ["Encounter", "Patient"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
    "launchContext": [
        {"name": {"code": "Patient"}, "type": "patient"},
        {"name": {"code": "Author"}, "type": "resource"},
    ],
    "name": "PHQ-2/PHQ-9 Depression Screening",
    "item": [
        {
            "text": "DateTime",
            "type": "dateTime",
            "hidden": True,
            "linkId": "dateTime",
            "initialExpression": {"language": "text/fhirpath", "expression": "now()"},
        },
        {
            "text": "PatientId",
            "type": "string",
            "hidden": True,
            "linkId": "patientId",
            "initialExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
        },
        {
            "text": "PatientName",
            "type": "string",
            "hidden": True,
            "linkId": "patientName",
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Patient.name.given[0] + ' ' + %Patient.name.family",
            },
        },
        {
            "item": [
                {
                    "text": "Little interest or pleasure in doing things",
                    "type": "choice",
                    "linkId": "44250-9",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "Feeling down, depressed, or hopeless",
                    "type": "choice",
                    "linkId": "44255-8",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "Trouble falling or staying asleep, or sleeping too much",
                    "type": "choice",
                    "linkId": "44259-0",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "Feeling tired or having little energy",
                    "type": "choice",
                    "linkId": "44254-1",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "Poor appetite or overeating",
                    "type": "choice",
                    "linkId": "44251-7",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "Feeling bad about yourself-or that you are a failure or have let yourself or your family down",
                    "type": "choice",
                    "linkId": "44258-2",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "Trouble concentrating on things, such as reading the newspaper or watching television",
                    "type": "choice",
                    "linkId": "44252-5",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "Moving or speaking so slowly that other people could have noticed. Or the opposite-being so fidgety or restless that you have been moving around a lot more than usual",
                    "type": "choice",
                    "linkId": "44253-3",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "Thoughts that you would be better off dead, or of hurting yourself in some way",
                    "type": "choice",
                    "linkId": "44260-8",
                    "required": True,
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6568-5",
                                    "system": "http://loinc.org",
                                    "display": "Not at all",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6569-3",
                                    "system": "http://loinc.org",
                                    "display": "Several days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6570-1",
                                    "system": "http://loinc.org",
                                    "display": "More than half the days",
                                }
                            }
                        },
                        {
                            "value": {
                                "Coding": {
                                    "code": "LA6571-9",
                                    "system": "http://loinc.org",
                                    "display": "Nearly every day",
                                }
                            }
                        },
                    ],
                },
                {
                    "text": "PHQ2/PHQ-9 Depression Severity Score",
                    "type": "integer",
                    "linkId": "phq9-total-score",
                    "readOnly": True,
                    "required": True,
                    "itemControl": {"coding": [{"code": "depression-score"}]},
                    "calculatedExpression": {
                        "language": "text/fhirpath",
                        "expression": "%QuestionnaireResponse.item.item.answer.children().children().where(code='LA6569-3').count() + %QuestionnaireResponse.item.item.answer.children().children().where(code='LA6570-1').count() * 2 + %QuestionnaireResponse.item.item.answer.children().children().where(code='LA6571-9').count() * 3",
                    },
                },
            ],
            "text": "Over the past 2 weeks, how often have you been bothered by:",
            "type": "group",
            "linkId": "phq2phq9",
        },
    ],
    "mapping": [{"id": "phq2phq9-extract", "resourceType": "Mapping"}],
    "resourceType": "Questionnaire",
    "status": "active",
    "id": "phq2phq9",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/phq2phq9",
}

phq2phq9_fhir_Questionnaire = {
    "subjectType": ["Encounter", "Patient"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
    "name": "PHQ-2/PHQ-9 Depression Screening",
    "item": [
        {
            "text": "DateTime",
            "type": "dateTime",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {"language": "text/fhirpath", "expression": "now()"},
                },
            ],
            "linkId": "dateTime",
        },
        {
            "text": "PatientId",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
                },
            ],
            "linkId": "patientId",
        },
        {
            "text": "PatientName",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.name.given[0] + ' ' + %Patient.name.family",
                    },
                },
            ],
            "linkId": "patientName",
        },
        {
            "item": [
                {
                    "text": "Little interest or pleasure in doing things",
                    "type": "choice",
                    "linkId": "44250-9",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "Feeling down, depressed, or hopeless",
                    "type": "choice",
                    "linkId": "44255-8",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "Trouble falling or staying asleep, or sleeping too much",
                    "type": "choice",
                    "linkId": "44259-0",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "Feeling tired or having little energy",
                    "type": "choice",
                    "linkId": "44254-1",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "Poor appetite or overeating",
                    "type": "choice",
                    "linkId": "44251-7",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "Feeling bad about yourself-or that you are a failure or have let yourself or your family down",
                    "type": "choice",
                    "linkId": "44258-2",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "Trouble concentrating on things, such as reading the newspaper or watching television",
                    "type": "choice",
                    "linkId": "44252-5",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "Moving or speaking so slowly that other people could have noticed. Or the opposite-being so fidgety or restless that you have been moving around a lot more than usual",
                    "type": "choice",
                    "linkId": "44253-3",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "Thoughts that you would be better off dead, or of hurting yourself in some way",
                    "type": "choice",
                    "linkId": "44260-8",
                    "required": True,
                    "answerOption": [
                        {
                            "valueCoding": {
                                "code": "LA6568-5",
                                "system": "http://loinc.org",
                                "display": "Not at all",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6569-3",
                                "system": "http://loinc.org",
                                "display": "Several days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6570-1",
                                "system": "http://loinc.org",
                                "display": "More than half the days",
                            }
                        },
                        {
                            "valueCoding": {
                                "code": "LA6571-9",
                                "system": "http://loinc.org",
                                "display": "Nearly every day",
                            }
                        },
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "PHQ2/PHQ-9 Depression Severity Score",
                    "type": "integer",
                    "linkId": "phq9-total-score",
                    "readOnly": True,
                    "required": True,
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "depression-score"}]},
                        },
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-calculatedExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "%QuestionnaireResponse.item.item.answer.children().children().where(code='LA6569-3').count() + %QuestionnaireResponse.item.item.answer.children().children().where(code='LA6570-1').count() * 2 + %QuestionnaireResponse.item.item.answer.children().children().where(code='LA6571-9').count() * 3",
                            },
                        },
                    ],
                },
            ],
            "text": "Over the past 2 weeks, how often have you been bothered by:",
            "type": "group",
            "linkId": "phq2phq9",
        },
    ],
    "resourceType": "Questionnaire",
    "extension": [
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "Patient",
                    },
                },
                {"url": "type", "valueCode": "patient"},
            ],
        },
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "Author",
                    },
                },
                {"url": "type", "valueCode": "resource"},
            ],
        },
        {
            "url": "http://beda.software/fhir-extensions/questionnaire-mapper",
            "valueReference": {"reference": "Mapping/phq2phq9-extract"},
        },
    ],
    "status": "active",
    "id": "phq2phq9",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/phq2phq9",
}

physicalexam_aidbox_Questionnaire = {
    "subjectType": ["Encounter"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
    "launchContext": [
        {
            "name": {"code": "Patient"},
            "type": "patient",
            "description": "Patient is answering the questionnaire",
        }
    ],
    "name": "Physical exam",
    "item": [
        {
            "item": [
                {
                    "code": [
                        {
                            "code": "71389-1",
                            "system": "http://loinc.org",
                            "display": "CMS - constitutional exam panel",
                        }
                    ],
                    "text": "General",
                    "type": "text",
                    "macro": "Well nourished, well developed, awake and alert, resting comfortably in no acute distress, cooperative on exam",
                    "linkId": "general",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                },
                {
                    "code": [
                        {
                            "code": "71392-5",
                            "system": "http://loinc.org",
                            "display": "CMS - ear-nose-mouth-throat exam panel",
                        }
                    ],
                    "text": "HEENT",
                    "type": "text",
                    "macro": "NCAT, PERRL, normal conjunctivae, nonicteric sclerae, bilateral EAC/TM clear, no nasal discharge, OP clear, moist mucous membranes",
                    "linkId": "heent",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                },
                {
                    "code": [
                        {
                            "code": "71393-3",
                            "system": "http://loinc.org",
                            "display": "CMS - neck exam panel",
                        }
                    ],
                    "text": "Neck",
                    "type": "text",
                    "macro": "Supple, normal ROM, no lymphadenopathy/masses, nontender",
                    "linkId": "neck",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                },
                {
                    "code": [
                        {
                            "code": "71395-8",
                            "system": "http://loinc.org",
                            "display": "CMS - cardiovascular exam panel",
                        }
                    ],
                    "text": "Cardiovascular",
                    "type": "text",
                    "macro": "RRR, normal S1/S2, no murmurs/gallops/rub",
                    "linkId": "cardiovascular",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                },
                {
                    "code": [
                        {
                            "code": "71394-1",
                            "system": "http://loinc.org",
                            "display": "CMS - respiratory exam panel",
                        }
                    ],
                    "text": "Pulmonary",
                    "type": "text",
                    "macro": "No respiratory distress, lungs CTAB: no rales, rhonchi, or wheeze",
                    "linkId": "pulmonary",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                },
                {
                    "code": [
                        {
                            "code": "71397-4",
                            "system": "http://loinc.org",
                            "display": "CMS - gastrointestinal - abdomen exam panel",
                        }
                    ],
                    "text": "Abdominal",
                    "type": "text",
                    "macro": "Soft and non-tender with no guarding or rebound; +BS normoactive, no tympany on auscultation",
                    "linkId": "abdominal",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                },
                {
                    "code": [
                        {
                            "code": "71402-2",
                            "system": "http://loinc.org",
                            "display": "CMS - musculoskeletal exam panel",
                        }
                    ],
                    "text": "Musculoskeletal",
                    "type": "text",
                    "macro": "Normal ROM of UE and LE, normal bulk and tone,",
                    "linkId": "musculoskeletal",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                },
                {
                    "code": [
                        {
                            "code": "71401-4",
                            "system": "http://loinc.org",
                            "display": "CMS - extremities exam panel",
                        }
                    ],
                    "text": "Extremities",
                    "type": "text",
                    "macro": "Pulses intact with normal cap refill, no LE pitting edema or calf tenderness",
                    "linkId": "extremities",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                },
                {
                    "code": [
                        {
                            "code": "71404-8",
                            "system": "http://loinc.org",
                            "display": "CMS - neurologic exam panel",
                        }
                    ],
                    "text": "Neurologic",
                    "type": "text",
                    "macro": "AAOx3, converses normally. CN II - XII grossly intact. Gait and coordination intact. 5+ BL UE/LE strength, no gross motor or sensory defects",
                    "linkId": "neurologic",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                },
                {
                    "code": [
                        {
                            "code": "71405-5",
                            "system": "http://loinc.org",
                            "display": "CMS - psychiatric exam panel",
                        }
                    ],
                    "text": "Psychiatric",
                    "type": "text",
                    "macro": "Normal mood and affect. Judgement/competence is appropriate",
                    "linkId": "psychiatric",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                },
                {
                    "code": [
                        {
                            "code": "71403-0",
                            "system": "http://loinc.org",
                            "display": "CMS - skin exam panel",
                        }
                    ],
                    "text": "Skin",
                    "type": "text",
                    "macro": "Warm, dry, and intact. No rashes, dermatoses, petechiae, or lesions",
                    "linkId": "skin",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                },
                {
                    "code": [
                        {
                            "code": "32473-1",
                            "system": "http://loinc.org",
                            "display": "Physical findings.sensation",
                        }
                    ],
                    "text": "Monofilament",
                    "type": "text",
                    "macro": "Normal sensation bilaterally on soles of feet with 10g monofilament",
                    "linkId": "monofilament",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                },
                {
                    "text": "Other Systems (optional)",
                    "type": "display",
                    "linkId": "other-systems-optional",
                },
                {
                    "code": [
                        {
                            "code": "71396-6",
                            "system": "http://loinc.org",
                            "display": "CMS - breast exam panel",
                        }
                    ],
                    "text": "Chest",
                    "type": "text",
                    "macro": "The chest wall is symmetric, without deformity, and is atraumatic in appearance",
                    "linkId": "chest",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                },
                {
                    "code": [
                        {
                            "code": "71399-0",
                            "system": "http://loinc.org",
                            "display": "CMS - genitourinary exam - female panel",
                        }
                    ],
                    "text": "Genitourinary",
                    "type": "text",
                    "macro": "External genitalia without erythema, exudate or discharge",
                    "linkId": "genitourinary-female",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                    "enableWhenExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.gender = 'female'",
                    },
                },
                {
                    "code": [
                        {
                            "code": "71398-2",
                            "system": "http://loinc.org",
                            "display": "CMS - genitourinary exam - male panel",
                        }
                    ],
                    "text": "Genitourinary",
                    "type": "text",
                    "macro": "Penis without lesions. No urethral discharge. Testes normal size without masses or tenderness. No scrotal masses. No hernia",
                    "linkId": "genitourinary-male",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                    "enableWhenExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.gender = 'male'",
                    },
                },
                {
                    "code": [
                        {
                            "code": "8708-0",
                            "system": "http://loinc.org",
                            "display": "Phys find Rectum",
                        }
                    ],
                    "text": "Rectal",
                    "type": "text",
                    "macro": "Normal external anus and normal tone. No palpable masses, normal mucosa, brown stool. Hemoccult negative",
                    "linkId": "rectal",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                },
                {
                    "code": [
                        {
                            "code": "71400-6",
                            "system": "http://loinc.org",
                            "display": "CMS - lymphatic exam panel",
                        }
                    ],
                    "text": "Lymphatic",
                    "type": "text",
                    "macro": "No enlarged lymph nodes of occipital, pre- and postauricular, submandibular, anterior or posterior cervical, or supraclavicular identified",
                    "linkId": "lymphatic",
                    "itemControl": {"coding": [{"code": "text-with-macro"}]},
                },
            ],
            "type": "group",
            "linkId": "physical-exam-group",
        }
    ],
    "resourceType": "Questionnaire",
    "status": "active",
    "id": "physical-exam",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/physical-exam",
}

physicalexam_fhir_Questionnaire = {
    "subjectType": ["Encounter"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
    "name": "Physical exam",
    "item": [
        {
            "item": [
                {
                    "code": [
                        {
                            "code": "71389-1",
                            "system": "http://loinc.org",
                            "display": "CMS - constitutional exam panel",
                        }
                    ],
                    "text": "General",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "Well nourished, well developed, awake and alert, resting comfortably in no acute distress, cooperative on exam",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                    ],
                    "linkId": "general",
                },
                {
                    "code": [
                        {
                            "code": "71392-5",
                            "system": "http://loinc.org",
                            "display": "CMS - ear-nose-mouth-throat exam panel",
                        }
                    ],
                    "text": "HEENT",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "NCAT, PERRL, normal conjunctivae, nonicteric sclerae, bilateral EAC/TM clear, no nasal discharge, OP clear, moist mucous membranes",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                    ],
                    "linkId": "heent",
                },
                {
                    "code": [
                        {
                            "code": "71393-3",
                            "system": "http://loinc.org",
                            "display": "CMS - neck exam panel",
                        }
                    ],
                    "text": "Neck",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "Supple, normal ROM, no lymphadenopathy/masses, nontender",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                    ],
                    "linkId": "neck",
                },
                {
                    "code": [
                        {
                            "code": "71395-8",
                            "system": "http://loinc.org",
                            "display": "CMS - cardiovascular exam panel",
                        }
                    ],
                    "text": "Cardiovascular",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "RRR, normal S1/S2, no murmurs/gallops/rub",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                    ],
                    "linkId": "cardiovascular",
                },
                {
                    "code": [
                        {
                            "code": "71394-1",
                            "system": "http://loinc.org",
                            "display": "CMS - respiratory exam panel",
                        }
                    ],
                    "text": "Pulmonary",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "No respiratory distress, lungs CTAB: no rales, rhonchi, or wheeze",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                    ],
                    "linkId": "pulmonary",
                },
                {
                    "code": [
                        {
                            "code": "71397-4",
                            "system": "http://loinc.org",
                            "display": "CMS - gastrointestinal - abdomen exam panel",
                        }
                    ],
                    "text": "Abdominal",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "Soft and non-tender with no guarding or rebound; +BS normoactive, no tympany on auscultation",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                    ],
                    "linkId": "abdominal",
                },
                {
                    "code": [
                        {
                            "code": "71402-2",
                            "system": "http://loinc.org",
                            "display": "CMS - musculoskeletal exam panel",
                        }
                    ],
                    "text": "Musculoskeletal",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "Normal ROM of UE and LE, normal bulk and tone,",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                    ],
                    "linkId": "musculoskeletal",
                },
                {
                    "code": [
                        {
                            "code": "71401-4",
                            "system": "http://loinc.org",
                            "display": "CMS - extremities exam panel",
                        }
                    ],
                    "text": "Extremities",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "Pulses intact with normal cap refill, no LE pitting edema or calf tenderness",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                    ],
                    "linkId": "extremities",
                },
                {
                    "code": [
                        {
                            "code": "71404-8",
                            "system": "http://loinc.org",
                            "display": "CMS - neurologic exam panel",
                        }
                    ],
                    "text": "Neurologic",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "AAOx3, converses normally. CN II - XII grossly intact. Gait and coordination intact. 5+ BL UE/LE strength, no gross motor or sensory defects",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                    ],
                    "linkId": "neurologic",
                },
                {
                    "code": [
                        {
                            "code": "71405-5",
                            "system": "http://loinc.org",
                            "display": "CMS - psychiatric exam panel",
                        }
                    ],
                    "text": "Psychiatric",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "Normal mood and affect. Judgement/competence is appropriate",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                    ],
                    "linkId": "psychiatric",
                },
                {
                    "code": [
                        {
                            "code": "71403-0",
                            "system": "http://loinc.org",
                            "display": "CMS - skin exam panel",
                        }
                    ],
                    "text": "Skin",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "Warm, dry, and intact. No rashes, dermatoses, petechiae, or lesions",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                    ],
                    "linkId": "skin",
                },
                {
                    "code": [
                        {
                            "code": "32473-1",
                            "system": "http://loinc.org",
                            "display": "Physical findings.sensation",
                        }
                    ],
                    "text": "Monofilament",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "Normal sensation bilaterally on soles of feet with 10g monofilament",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                    ],
                    "linkId": "monofilament",
                },
                {
                    "text": "Other Systems (optional)",
                    "type": "display",
                    "linkId": "other-systems-optional",
                },
                {
                    "code": [
                        {
                            "code": "71396-6",
                            "system": "http://loinc.org",
                            "display": "CMS - breast exam panel",
                        }
                    ],
                    "text": "Chest",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "The chest wall is symmetric, without deformity, and is atraumatic in appearance",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                    ],
                    "linkId": "chest",
                },
                {
                    "code": [
                        {
                            "code": "71399-0",
                            "system": "http://loinc.org",
                            "display": "CMS - genitourinary exam - female panel",
                        }
                    ],
                    "text": "Genitourinary",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "External genitalia without erythema, exudate or discharge",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-enableWhenExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "%Patient.gender = 'female'",
                            },
                        },
                    ],
                    "linkId": "genitourinary-female",
                },
                {
                    "code": [
                        {
                            "code": "71398-2",
                            "system": "http://loinc.org",
                            "display": "CMS - genitourinary exam - male panel",
                        }
                    ],
                    "text": "Genitourinary",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "Penis without lesions. No urethral discharge. Testes normal size without masses or tenderness. No scrotal masses. No hernia",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                        {
                            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-enableWhenExpression",
                            "valueExpression": {
                                "language": "text/fhirpath",
                                "expression": "%Patient.gender = 'male'",
                            },
                        },
                    ],
                    "linkId": "genitourinary-male",
                },
                {
                    "code": [
                        {
                            "code": "8708-0",
                            "system": "http://loinc.org",
                            "display": "Phys find Rectum",
                        }
                    ],
                    "text": "Rectal",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "Normal external anus and normal tone. No palpable masses, normal mucosa, brown stool. Hemoccult negative",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                    ],
                    "linkId": "rectal",
                },
                {
                    "code": [
                        {
                            "code": "71400-6",
                            "system": "http://loinc.org",
                            "display": "CMS - lymphatic exam panel",
                        }
                    ],
                    "text": "Lymphatic",
                    "type": "text",
                    "extension": [
                        {
                            "url": "https://beda.software/fhir-emr-questionnaire/macro",
                            "valueString": "No enlarged lymph nodes of occipital, pre- and postauricular, submandibular, anterior or posterior cervical, or supraclavicular identified",
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "text-with-macro"}]},
                        },
                    ],
                    "linkId": "lymphatic",
                },
            ],
            "type": "group",
            "linkId": "physical-exam-group",
        }
    ],
    "resourceType": "Questionnaire",
    "extension": [
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "Patient",
                    },
                },
                {"url": "type", "valueCode": "patient"},
                {"url": "description", "valueString": "Patient is answering the questionnaire"},
            ],
        }
    ],
    "status": "active",
    "id": "physical-exam",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/physical-exam",
}

practitioner_create_aidbox_Questionnaire = {
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
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
                    "value": {
                        "Coding": {
                            "code": "394577000",
                            "system": "http://snomed.info/sct",
                            "display": "Anesthetics",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "394579002",
                            "system": "http://snomed.info/sct",
                            "display": "Cardiology",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "394582007",
                            "system": "http://snomed.info/sct",
                            "display": "Dermatology",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "394583002",
                            "system": "http://snomed.info/sct",
                            "display": "Endocrinology",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "419772000",
                            "system": "http://snomed.info/sct",
                            "display": "Family practice",
                        }
                    }
                },
            ],
        },
    ],
    "mapping": [{"id": "practitioner-create", "resourceType": "Mapping"}],
    "resourceType": "Questionnaire",
    "title": "Practitioner create",
    "status": "active",
    "id": "practitioner-create",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/practitioner-create",
}

practitioner_create_fhir_Questionnaire = {
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
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
    "id": "practitioner-create",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/practitioner-create",
}

practitioner_edit_aidbox_Questionnaire = {
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
    "launchContext": [
        {"name": {"code": "Practitioner"}, "type": "practitioner"},
        {"name": {"code": "PractitionerRole"}, "type": "practitionerRole"},
    ],
    "name": "practitioner edit",
    "item": [
        {
            "text": "practitionerId",
            "type": "string",
            "hidden": True,
            "linkId": "practitioner-id",
            "readOnly": True,
            "initialExpression": {"language": "text/fhirpath", "expression": "%Practitioner.id"},
        },
        {
            "text": "practitionerRoleId",
            "type": "string",
            "hidden": True,
            "linkId": "practitioner-role-id",
            "readOnly": True,
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%PractitionerRole.id",
            },
        },
        {
            "text": "First name",
            "type": "string",
            "linkId": "first-name",
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Practitioner.name.given[0]",
            },
        },
        {
            "text": "Middle name",
            "type": "string",
            "linkId": "middle-name",
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Practitioner.name.given[1]",
            },
        },
        {
            "text": "Last name",
            "type": "string",
            "linkId": "last-name",
            "required": True,
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Practitioner.name.family",
            },
        },
        {
            "text": "Specialty",
            "type": "choice",
            "linkId": "specialty",
            "answerOption": [
                {
                    "value": {
                        "Coding": {
                            "code": "394577000",
                            "system": "http://snomed.info/sct",
                            "display": "Anesthetics",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "394579002",
                            "system": "http://snomed.info/sct",
                            "display": "Cardiology",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "394582007",
                            "system": "http://snomed.info/sct",
                            "display": "Dermatology",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "394583002",
                            "system": "http://snomed.info/sct",
                            "display": "Endocrinology",
                        }
                    }
                },
                {
                    "value": {
                        "Coding": {
                            "code": "419772000",
                            "system": "http://snomed.info/sct",
                            "display": "Family practice",
                        }
                    }
                },
            ],
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%PractitionerRole.specialty[0].coding",
            },
        },
    ],
    "mapping": [{"id": "practitioner-edit", "resourceType": "Mapping"}],
    "resourceType": "Questionnaire",
    "title": "Practitioner edit",
    "status": "active",
    "id": "practitioner-edit",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/practitioner-edit",
}

practitioner_edit_fhir_Questionnaire = {
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
    "name": "practitioner edit",
    "item": [
        {
            "text": "practitionerId",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Practitioner.id",
                    },
                },
            ],
            "linkId": "practitioner-id",
            "readOnly": True,
        },
        {
            "text": "practitionerRoleId",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%PractitionerRole.id",
                    },
                },
            ],
            "linkId": "practitioner-role-id",
            "readOnly": True,
        },
        {
            "text": "First name",
            "type": "string",
            "linkId": "first-name",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Practitioner.name.given[0]",
                    },
                }
            ],
        },
        {
            "text": "Middle name",
            "type": "string",
            "linkId": "middle-name",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Practitioner.name.given[1]",
                    },
                }
            ],
        },
        {
            "text": "Last name",
            "type": "string",
            "linkId": "last-name",
            "required": True,
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Practitioner.name.family",
                    },
                }
            ],
        },
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
            "extension": [
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%PractitionerRole.specialty[0].coding",
                    },
                }
            ],
        },
    ],
    "resourceType": "Questionnaire",
    "title": "Practitioner edit",
    "extension": [
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "Practitioner",
                    },
                },
                {"url": "type", "valueCode": "practitioner"},
            ],
        },
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "PractitionerRole",
                    },
                },
                {"url": "type", "valueCode": "practitionerRole"},
            ],
        },
        {
            "url": "http://beda.software/fhir-extensions/questionnaire-mapper",
            "valueReference": {"reference": "Mapping/practitioner-edit"},
        },
    ],
    "status": "active",
    "id": "practitioner-edit",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/practitioner-edit",
}

practitioner_role_create_aidbox_Questionnaire = {
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
    "name": "practitioner-role-create",
    "item": [
        {"text": "Organization", "type": "string", "linkId": "organization"},
        {"text": "Practitioner", "type": "string", "linkId": "practitioner"},
        {"text": "Speciality", "type": "string", "linkId": "specialty"},
    ],
    "mapping": [{"id": "practitioner-role-create", "resourceType": "Mapping"}],
    "resourceType": "Questionnaire",
    "title": "Create practitioner role",
    "status": "active",
    "id": "practitioner-role-create",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/practitioner-role-create",
}

practitioner_role_create_fhir_Questionnaire = {
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
    "name": "practitioner-role-create",
    "item": [
        {"text": "Organization", "type": "string", "linkId": "organization"},
        {"text": "Practitioner", "type": "string", "linkId": "practitioner"},
        {"text": "Speciality", "type": "string", "linkId": "specialty"},
    ],
    "resourceType": "Questionnaire",
    "title": "Create practitioner role",
    "extension": [
        {
            "url": "http://beda.software/fhir-extensions/questionnaire-mapper",
            "valueReference": {"reference": "Mapping/practitioner-role-create"},
        }
    ],
    "status": "active",
    "id": "practitioner-role-create",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/practitioner-role-create",
}

public_appointment_aidbox_Questionnaire = {
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/",
    "item": [
        {"text": "First name", "type": "string", "linkId": "first-name", "required": True},
        {"text": "Last name", "type": "string", "linkId": "last-name", "required": True},
        {
            "text": "Phone number",
            "type": "string",
            "linkId": "mobile",
            "itemControl": {"coding": [{"code": "phoneWidget"}]},
        },
        {
            "text": "Practitioner",
            "type": "choice",
            "linkId": "practitioner-role",
            "required": True,
            "itemControl": {"coding": [{"code": "practitioner-role"}]},
        },
        {
            "text": "Type",
            "type": "choice",
            "hidden": True,
            "linkId": "service-type",
            "initial": [
                {
                    "value": {
                        "Coding": {
                            "code": "consultation",
                            "system": "http://fhir.org/guides/argonaut-scheduling/CodeSystem/visit-type",
                            "display": "The first appointment",
                        }
                    }
                }
            ],
            "required": True,
        },
        {
            "text": "Date and Time",
            "type": "dateTime",
            "linkId": "date-time-slot",
            "required": True,
            "itemControl": {"coding": [{"code": "date-time-slot"}]},
        },
    ],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
    "name": "Appointment",
    "status": "active",
    "mapping": [{"id": "public-appointment-extract", "resourceType": "Mapping"}],
    "id": "public-appointment",
    "resourceType": "Questionnaire",
}

public_appointment_fhir_Questionnaire = {
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
    "name": "Appointment",
    "item": [
        {"text": "First name", "type": "string", "linkId": "first-name", "required": True},
        {"text": "Last name", "type": "string", "linkId": "last-name", "required": True},
        {
            "text": "Phone number",
            "type": "string",
            "linkId": "mobile",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                    "valueCodeableConcept": {"coding": [{"code": "phoneWidget"}]},
                }
            ],
        },
        {
            "text": "Practitioner",
            "type": "choice",
            "linkId": "practitioner-role",
            "required": True,
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                    "valueCodeableConcept": {"coding": [{"code": "practitioner-role"}]},
                }
            ],
        },
        {
            "text": "Type",
            "type": "choice",
            "required": True,
            "linkId": "service-type",
            "initial": [
                {
                    "valueCoding": {
                        "code": "consultation",
                        "system": "http://fhir.org/guides/argonaut-scheduling/CodeSystem/visit-type",
                        "display": "The first appointment",
                    }
                }
            ],
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                }
            ],
        },
        {
            "text": "Date and Time",
            "type": "dateTime",
            "linkId": "date-time-slot",
            "required": True,
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                    "valueCodeableConcept": {"coding": [{"code": "date-time-slot"}]},
                }
            ],
        },
    ],
    "resourceType": "Questionnaire",
    "extension": [
        {
            "url": "http://beda.software/fhir-extensions/questionnaire-mapper",
            "valueReference": {"reference": "Mapping/public-appointment-extract"},
        }
    ],
    "status": "active",
    "id": "public-appointment",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/",
}

review_of_systems_aidbox_Questionnaire = {
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/review-of-systems",
    "item": [
        {
            "code": [
                {
                    "code": "71406-3",
                    "system": "http://loinc.org",
                    "display": "CMS - review of systems panel",
                }
            ],
            "text": "Provider reviewed all systems and state that all are WNL except as noted below\n",
            "type": "boolean",
            "linkId": "provider-viewed-confirmation",
            "initial": [{"value": {"boolean": False}}],
        },
        {
            "item": [
                {
                    "code": [
                        {
                            "code": "71407-1",
                            "system": "http://loinc.org",
                            "display": "CMS - constitutional symptoms panel",
                        }
                    ],
                    "text": "General",
                    "type": "boolean",
                    "linkId": "general",
                },
                {
                    "code": [
                        {
                            "code": "71407-1-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - constitutional symptoms panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "general-comment",
                    "enableWhen": [
                        {"answer": {"boolean": True}, "operator": "=", "question": "general"}
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71409-7",
                            "system": "http://loinc.org",
                            "display": "CMS - ear-nose-mouth-throat panel",
                        }
                    ],
                    "text": "HEENT",
                    "type": "boolean",
                    "linkId": "heent",
                },
                {
                    "code": [
                        {
                            "code": "71409-7-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - ear-nose-mouth-throat panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "heent-comment",
                    "enableWhen": [
                        {"answer": {"boolean": True}, "operator": "=", "question": "heent"}
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71410-5",
                            "system": "http://loinc.org",
                            "display": "CMS - cardiovascular panel",
                        }
                    ],
                    "text": "Cardiovascular",
                    "type": "boolean",
                    "linkId": "cardiovascular",
                },
                {
                    "code": [
                        {
                            "code": "71410-5-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - cardiovascular panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "cardiovascular-comment",
                    "enableWhen": [
                        {"answer": {"boolean": True}, "operator": "=", "question": "cardiovascular"}
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71411-3",
                            "system": "http://loinc.org",
                            "display": "CMS - respiratory panel",
                        }
                    ],
                    "text": "Respiratory",
                    "type": "boolean",
                    "linkId": "respiratory",
                },
                {
                    "code": [
                        {
                            "code": "71411-3-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - respiratory panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "respiratory-comment",
                    "enableWhen": [
                        {"answer": {"boolean": True}, "operator": "=", "question": "respiratory"}
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71412-1",
                            "system": "http://loinc.org",
                            "display": "CMS - gastrointestinal panel",
                        }
                    ],
                    "text": "Gastrointestinal",
                    "type": "boolean",
                    "linkId": "gastrointestinal",
                },
                {
                    "code": [
                        {
                            "code": "71412-1-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - gastrointestinal panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "gastrointestinal-comment",
                    "enableWhen": [
                        {
                            "answer": {"boolean": True},
                            "operator": "=",
                            "question": "gastrointestinal",
                        }
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71413-9",
                            "system": "http://loinc.org",
                            "display": "CMS - genitourinary panel",
                        }
                    ],
                    "text": "Genitourinary",
                    "type": "boolean",
                    "linkId": "genitourinary",
                },
                {
                    "code": [
                        {
                            "code": "71413-9-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - genitourinary panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "genitourinary-comment",
                    "enableWhen": [
                        {"answer": {"boolean": True}, "operator": "=", "question": "genitourinary"}
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71414-7",
                            "system": "http://loinc.org",
                            "display": "CMS - musculoskeletal panel",
                        }
                    ],
                    "text": "Musculoskeletal",
                    "type": "boolean",
                    "linkId": "musculoskeletal",
                },
                {
                    "code": [
                        {
                            "code": "71414-7-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - musculoskeletal panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "musculoskeletal-comment",
                    "enableWhen": [
                        {
                            "answer": {"boolean": True},
                            "operator": "=",
                            "question": "musculoskeletal",
                        }
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71416-2",
                            "system": "http://loinc.org",
                            "display": "CMS - neurological panel",
                        }
                    ],
                    "text": "Neurologic",
                    "type": "boolean",
                    "linkId": "neurologic",
                },
                {
                    "code": [
                        {
                            "code": "71416-2-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - neurological panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "neurologic-comment",
                    "enableWhen": [
                        {"answer": {"boolean": True}, "operator": "=", "question": "neurologic"}
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71417-0",
                            "system": "http://loinc.org",
                            "display": "CMS - psychiatric panel",
                        }
                    ],
                    "text": "Psychiatric",
                    "type": "boolean",
                    "linkId": "psychiatric",
                },
                {
                    "code": [
                        {
                            "code": "71417-0-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - psychiatric panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "psychiatric-comment",
                    "enableWhen": [
                        {"answer": {"boolean": True}, "operator": "=", "question": "psychiatric"}
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71415-4",
                            "system": "http://loinc.org",
                            "display": "CMS - integumentary panel",
                        }
                    ],
                    "text": "Skin",
                    "type": "boolean",
                    "linkId": "skin",
                },
                {
                    "code": [
                        {
                            "code": "71415-4-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - integumentary panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "skin-comment",
                    "enableWhen": [
                        {"answer": {"boolean": True}, "operator": "=", "question": "skin"}
                    ],
                },
                {"text": "Other", "type": "boolean", "linkId": "other"},
                {
                    "type": "text",
                    "linkId": "other-comment",
                    "enableWhen": [
                        {"answer": {"boolean": True}, "operator": "=", "question": "other"}
                    ],
                },
            ],
            "text": "Select abnormal systems",
            "type": "group",
            "linkId": "abnormal-systems-group",
            "enableWhen": [
                {
                    "answer": {"boolean": True},
                    "operator": "=",
                    "question": "provider-viewed-confirmation",
                }
            ],
        },
    ],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
    "name": "Review of Systems",
    "status": "active",
    "subjectType": ["Encounter"],
    "id": "review-of-systems",
    "resourceType": "Questionnaire",
}

review_of_systems_fhir_Questionnaire = {
    "subjectType": ["Encounter"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
    "name": "Review of Systems",
    "item": [
        {
            "code": [
                {
                    "code": "71406-3",
                    "system": "http://loinc.org",
                    "display": "CMS - review of systems panel",
                }
            ],
            "text": "Provider reviewed all systems and state that all are WNL except as noted below\n",
            "type": "boolean",
            "linkId": "provider-viewed-confirmation",
            "initial": [{"valueBoolean": False}],
        },
        {
            "item": [
                {
                    "code": [
                        {
                            "code": "71407-1",
                            "system": "http://loinc.org",
                            "display": "CMS - constitutional symptoms panel",
                        }
                    ],
                    "text": "General",
                    "type": "boolean",
                    "linkId": "general",
                },
                {
                    "code": [
                        {
                            "code": "71407-1-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - constitutional symptoms panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "general-comment",
                    "enableWhen": [{"question": "general", "operator": "=", "answerBoolean": True}],
                },
                {
                    "code": [
                        {
                            "code": "71409-7",
                            "system": "http://loinc.org",
                            "display": "CMS - ear-nose-mouth-throat panel",
                        }
                    ],
                    "text": "HEENT",
                    "type": "boolean",
                    "linkId": "heent",
                },
                {
                    "code": [
                        {
                            "code": "71409-7-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - ear-nose-mouth-throat panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "heent-comment",
                    "enableWhen": [{"question": "heent", "operator": "=", "answerBoolean": True}],
                },
                {
                    "code": [
                        {
                            "code": "71410-5",
                            "system": "http://loinc.org",
                            "display": "CMS - cardiovascular panel",
                        }
                    ],
                    "text": "Cardiovascular",
                    "type": "boolean",
                    "linkId": "cardiovascular",
                },
                {
                    "code": [
                        {
                            "code": "71410-5-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - cardiovascular panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "cardiovascular-comment",
                    "enableWhen": [
                        {"question": "cardiovascular", "operator": "=", "answerBoolean": True}
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71411-3",
                            "system": "http://loinc.org",
                            "display": "CMS - respiratory panel",
                        }
                    ],
                    "text": "Respiratory",
                    "type": "boolean",
                    "linkId": "respiratory",
                },
                {
                    "code": [
                        {
                            "code": "71411-3-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - respiratory panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "respiratory-comment",
                    "enableWhen": [
                        {"question": "respiratory", "operator": "=", "answerBoolean": True}
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71412-1",
                            "system": "http://loinc.org",
                            "display": "CMS - gastrointestinal panel",
                        }
                    ],
                    "text": "Gastrointestinal",
                    "type": "boolean",
                    "linkId": "gastrointestinal",
                },
                {
                    "code": [
                        {
                            "code": "71412-1-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - gastrointestinal panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "gastrointestinal-comment",
                    "enableWhen": [
                        {"question": "gastrointestinal", "operator": "=", "answerBoolean": True}
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71413-9",
                            "system": "http://loinc.org",
                            "display": "CMS - genitourinary panel",
                        }
                    ],
                    "text": "Genitourinary",
                    "type": "boolean",
                    "linkId": "genitourinary",
                },
                {
                    "code": [
                        {
                            "code": "71413-9-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - genitourinary panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "genitourinary-comment",
                    "enableWhen": [
                        {"question": "genitourinary", "operator": "=", "answerBoolean": True}
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71414-7",
                            "system": "http://loinc.org",
                            "display": "CMS - musculoskeletal panel",
                        }
                    ],
                    "text": "Musculoskeletal",
                    "type": "boolean",
                    "linkId": "musculoskeletal",
                },
                {
                    "code": [
                        {
                            "code": "71414-7-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - musculoskeletal panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "musculoskeletal-comment",
                    "enableWhen": [
                        {"question": "musculoskeletal", "operator": "=", "answerBoolean": True}
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71416-2",
                            "system": "http://loinc.org",
                            "display": "CMS - neurological panel",
                        }
                    ],
                    "text": "Neurologic",
                    "type": "boolean",
                    "linkId": "neurologic",
                },
                {
                    "code": [
                        {
                            "code": "71416-2-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - neurological panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "neurologic-comment",
                    "enableWhen": [
                        {"question": "neurologic", "operator": "=", "answerBoolean": True}
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71417-0",
                            "system": "http://loinc.org",
                            "display": "CMS - psychiatric panel",
                        }
                    ],
                    "text": "Psychiatric",
                    "type": "boolean",
                    "linkId": "psychiatric",
                },
                {
                    "code": [
                        {
                            "code": "71417-0-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - psychiatric panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "psychiatric-comment",
                    "enableWhen": [
                        {"question": "psychiatric", "operator": "=", "answerBoolean": True}
                    ],
                },
                {
                    "code": [
                        {
                            "code": "71415-4",
                            "system": "http://loinc.org",
                            "display": "CMS - integumentary panel",
                        }
                    ],
                    "text": "Skin",
                    "type": "boolean",
                    "linkId": "skin",
                },
                {
                    "code": [
                        {
                            "code": "71415-4-comment",
                            "system": "http://loinc.org",
                            "display": "CMS - integumentary panel - comment",
                        }
                    ],
                    "type": "text",
                    "linkId": "skin-comment",
                    "enableWhen": [{"question": "skin", "operator": "=", "answerBoolean": True}],
                },
                {"text": "Other", "type": "boolean", "linkId": "other"},
                {
                    "type": "text",
                    "linkId": "other-comment",
                    "enableWhen": [{"question": "other", "operator": "=", "answerBoolean": True}],
                },
            ],
            "text": "Select abnormal systems",
            "type": "group",
            "linkId": "abnormal-systems-group",
            "enableWhen": [
                {"question": "provider-viewed-confirmation", "operator": "=", "answerBoolean": True}
            ],
        },
    ],
    "resourceType": "Questionnaire",
    "status": "active",
    "id": "review-of-systems",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/review-of-systems",
}

vitals_aidbox_Questionnaire = {
    "subjectType": ["Encounter", "Patient"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "createdAt": "2023-04-05T05:22:35.752466Z",
        "versionId": "694",
    },
    "launchContext": [{"name": {"code": "Patient"}, "type": "patient"}],
    "name": "Vitals",
    "item": [
        {
            "text": "PatientId",
            "type": "string",
            "hidden": True,
            "linkId": "patientId",
            "initialExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
        },
        {
            "text": "PatientName",
            "type": "string",
            "hidden": True,
            "linkId": "patientName",
            "initialExpression": {
                "language": "text/fhirpath",
                "expression": "%Patient.name.given[0] + ' ' + %Patient.name.family",
            },
        },
        {"text": "Height", "type": "integer", "unit": "cm", "linkId": "height"},
        {"text": "Weight", "type": "integer", "unit": "kg", "linkId": "weight"},
        {"text": "Temperature", "type": "integer", "unit": "Celsius", "linkId": "temperature"},
        {
            "text": "Oxygen saturation",
            "type": "integer",
            "unit": "%",
            "linkId": "oxygen-saturation",
        },
        {"text": "Pulse rate", "type": "integer", "unit": "bpm", "linkId": "pulse-rate"},
        {
            "text": "Respiratory Rate",
            "type": "integer",
            "unit": "bpm",
            "linkId": "respiratory-rate",
        },
        {
            "item": [
                {
                    "item": [
                        {
                            "text": "BP systolic",
                            "type": "integer",
                            "unit": "mmHg",
                            "linkId": "blood-pressure-systolic",
                        },
                        {
                            "text": "BP diastolic",
                            "type": "integer",
                            "unit": "mmHg",
                            "linkId": "blood-pressure-diastolic",
                        },
                    ],
                    "type": "group",
                    "linkId": "blood-pressure-systolic-diastolic",
                    "itemControl": {"coding": [{"code": "blood-pressure"}]},
                },
                {
                    "text": "Positions",
                    "type": "choice",
                    "linkId": "blood-pressure-positions",
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {"value": {"Coding": {"code": "sitting", "display": "Sitting"}}},
                        {"value": {"Coding": {"code": "lying", "display": "Lying"}}},
                        {"value": {"Coding": {"code": "standing", "display": "Standing"}}},
                    ],
                },
                {
                    "text": "Arm",
                    "type": "choice",
                    "linkId": "blood-pressure-arm",
                    "itemControl": {"coding": [{"code": "inline-choice"}]},
                    "answerOption": [
                        {"value": {"Coding": {"code": "biceps-left", "display": "Biceps left"}}},
                        {"value": {"Coding": {"code": "biceps-right", "display": "Biceps right"}}},
                    ],
                },
            ],
            "text": "Blood Pressure",
            "type": "group",
            "linkId": "blood-pressure",
        },
        {
            "text": "BMI",
            "type": "integer",
            "unit": "kg/m2",
            "linkId": "bmi",
            "readOnly": True,
            "required": True,
            "calculatedExpression": {
                "language": "text/fhirpath",
                "expression": "(%QuestionnaireResponse.item.where(linkId='weight').answer.value.integer / ((%QuestionnaireResponse.item.where(linkId='height').answer.value.integer / 100) * (%QuestionnaireResponse.item.where(linkId='height').answer.value.integer / 100))).round(2)",
            },
        },
    ],
    "mapping": [{"id": "vitals", "resourceType": "Mapping"}],
    "resourceType": "Questionnaire",
    "status": "active",
    "id": "vitals",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/vitals",
}

vitals_fhir_Questionnaire = {
    "subjectType": ["Encounter", "Patient"],
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
        "lastUpdated": "2023-04-10T03:43:34.792167Z",
        "versionId": "694",
        "extension": [{"url": "ex:createdAt", "valueInstant": "2023-04-05T05:22:35.752466Z"}],
    },
    "name": "Vitals",
    "item": [
        {
            "text": "PatientId",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {"language": "text/fhirpath", "expression": "%Patient.id"},
                },
            ],
            "linkId": "patientId",
        },
        {
            "text": "PatientName",
            "type": "string",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-hidden",
                    "valueBoolean": True,
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "%Patient.name.given[0] + ' ' + %Patient.name.family",
                    },
                },
            ],
            "linkId": "patientName",
        },
        {
            "text": "Height",
            "type": "integer",
            "linkId": "height",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-unit",
                    "valueCoding": "cm",
                }
            ],
        },
        {
            "text": "Weight",
            "type": "integer",
            "linkId": "weight",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-unit",
                    "valueCoding": "kg",
                }
            ],
        },
        {
            "text": "Temperature",
            "type": "integer",
            "linkId": "temperature",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-unit",
                    "valueCoding": "Celsius",
                }
            ],
        },
        {
            "text": "Oxygen saturation",
            "type": "integer",
            "linkId": "oxygen-saturation",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-unit",
                    "valueCoding": "%",
                }
            ],
        },
        {
            "text": "Pulse rate",
            "type": "integer",
            "linkId": "pulse-rate",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-unit",
                    "valueCoding": "bpm",
                }
            ],
        },
        {
            "text": "Respiratory Rate",
            "type": "integer",
            "linkId": "respiratory-rate",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-unit",
                    "valueCoding": "bpm",
                }
            ],
        },
        {
            "item": [
                {
                    "item": [
                        {
                            "text": "BP systolic",
                            "type": "integer",
                            "linkId": "blood-pressure-systolic",
                            "extension": [
                                {
                                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-unit",
                                    "valueCoding": "mmHg",
                                }
                            ],
                        },
                        {
                            "text": "BP diastolic",
                            "type": "integer",
                            "linkId": "blood-pressure-diastolic",
                            "extension": [
                                {
                                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-unit",
                                    "valueCoding": "mmHg",
                                }
                            ],
                        },
                    ],
                    "type": "group",
                    "linkId": "blood-pressure-systolic-diastolic",
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "blood-pressure"}]},
                        }
                    ],
                },
                {
                    "text": "Positions",
                    "type": "choice",
                    "linkId": "blood-pressure-positions",
                    "answerOption": [
                        {"valueCoding": {"code": "sitting", "display": "Sitting"}},
                        {"valueCoding": {"code": "lying", "display": "Lying"}},
                        {"valueCoding": {"code": "standing", "display": "Standing"}},
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
                {
                    "text": "Arm",
                    "type": "choice",
                    "linkId": "blood-pressure-arm",
                    "answerOption": [
                        {"valueCoding": {"code": "biceps-left", "display": "Biceps left"}},
                        {"valueCoding": {"code": "biceps-right", "display": "Biceps right"}},
                    ],
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                            "valueCodeableConcept": {"coding": [{"code": "inline-choice"}]},
                        }
                    ],
                },
            ],
            "text": "Blood Pressure",
            "type": "group",
            "linkId": "blood-pressure",
        },
        {
            "text": "BMI",
            "type": "integer",
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-unit",
                    "valueCoding": "kg/m2",
                },
                {
                    "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-calculatedExpression",
                    "valueExpression": {
                        "language": "text/fhirpath",
                        "expression": "(%QuestionnaireResponse.item.where(linkId='weight').answer.value.integer / ((%QuestionnaireResponse.item.where(linkId='height').answer.value.integer / 100) * (%QuestionnaireResponse.item.where(linkId='height').answer.value.integer / 100))).round(2)",
                    },
                },
            ],
            "linkId": "bmi",
            "readOnly": True,
            "required": True,
        },
    ],
    "resourceType": "Questionnaire",
    "extension": [
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-launchContext",
            "extension": [
                {
                    "url": "name",
                    "valueCoding": {
                        "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/launchContext",
                        "code": "Patient",
                    },
                },
                {"url": "type", "valueCode": "patient"},
            ],
        },
        {
            "url": "http://beda.software/fhir-extensions/questionnaire-mapper",
            "valueReference": {"reference": "Mapping/vitals"},
        },
    ],
    "status": "active",
    "id": "vitals",
    "url": "https://aidbox.emr.beda.software/ui/console#/entities/Questionnaire/vitals",
}

source_queries_fhir_questionnaire = {
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
    },
    "item": [{"linkId": "question-1", "type": "string", "text": "Question"}],
    "status": "active",
    "resourceType": "Questionnaire",
    "contained": [
        {
            "id": "PrePopQuery",
            "type": "batch",
            "entry": [{"request": {"url": "Patient?_id={{%LaunchPatient.id}}", "method": "GET"}}],
            "resourceType": "Bundle",
        }
    ],
    "extension": [
        {
            "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-sourceQueries",
            "valueReference": {"reference": "#Bundle#PrePopQuery"},
        },
    ],
}

source_queries_aidbox_questionnaire = {
    "meta": {
        "profile": ["https://beda.software/beda-emr-questionnaire"],
    },
    "item": [{"linkId": "question-1", "type": "string", "text": "Question"}],
    "status": "active",
    "resourceType": "Questionnaire",
    "contained": [
        {
            "id": "PrePopQuery",
            "type": "batch",
            "entry": [{"request": {"url": "Patient?_id={{%LaunchPatient.id}}", "method": "GET"}}],
            "resourceType": "Bundle",
        }
    ],
    "sourceQueries": [{"localRef": "Bundle#PrePopQuery"}],
}
