async def test_resolve_expression(sdk, safe_db):
    raw_expression = "/Patient/{{%LaunchPatient.id}}"
    expected_expression = "/Patient/test-id"
    env = {
        "LaunchPatient": {
            "resourceType": "Patient",
            "id": "test-id"
        }
    }
    data = {
        "expression": raw_expression,
        "env": env
    }
    resolved_expression = await sdk.client.execute(f"Questionnaire/$resolve-expression", method='POST',
                                                   data=data, params=None)
    assert resolved_expression == expected_expression
