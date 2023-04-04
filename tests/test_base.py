import pytest

# The next 4 tests check that the system works correctly
# Both client and aidbox available via HTTP on runtime
# Each save_db transaction separated from other
# Please keep all this test and don't remove them
# If any of this test fails that mean
# that system is in the inconsistent state and all tests become flaky


@pytest.mark.asyncio
async def test_health_check(client):
    resp = await client.get("/health")
    assert resp.status == 200
    json = await resp.json()
    assert json == {"status": "OK"}


@pytest.mark.asyncio
async def test_live_health_check(client):
    resp = await client.get("/live")
    assert resp.status == 200
    json = await resp.json()
    assert json == {"status": "OK"}


@pytest.mark.asyncio
async def test_database_isolation__1(aidbox_client, safe_db):
    patients = await aidbox_client.resources("Patient").fetch_all()
    assert len(patients) == 0

    patient = aidbox_client.resource("Patient")
    await patient.save()

    patients = await aidbox_client.resources("Patient").fetch_all()
    assert len(patients) == 1


@pytest.mark.asyncio
async def test_database_isolation__2(aidbox_client, safe_db):
    patients = await aidbox_client.resources("Patient").fetch_all()
    assert len(patients) == 0

    patient = aidbox_client.resource("Patient")
    await patient.save()

    patient = aidbox_client.resource("Patient")
    await patient.save()

    patients = await aidbox_client.resources("Patient").fetch_all()
    assert len(patients) == 2
