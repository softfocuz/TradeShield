import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_exporter(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "exporter@example.com",
            "password": "securepassword123",
            "role": "EXPORTER",
            "exporter_profile": {
                "company_name": "Global Export Ltd",
                "business_registration": "REG123456",
                "country": "Germany",
            },
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "exporter@example.com"
    assert data["role"] == "EXPORTER"
    assert data["exporter_profile"]["company_name"] == "Global Export Ltd"


@pytest.mark.asyncio
async def test_register_importer(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "importer@example.com",
            "password": "securepassword123",
            "role": "IMPORTER",
            "importer_profile": {
                "company_name": "Local Import Inc",
                "import_license": "LIC987654",
                "destination_country": "United States",
            },
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "importer@example.com"
    assert data["role"] == "IMPORTER"
    assert data["importer_profile"]["company_name"] == "Local Import Inc"


@pytest.mark.asyncio
async def test_duplicate_registration(client: AsyncClient):
    payload = {
        "email": "dup@example.com",
        "password": "password123",
        "role": "EXPORTER",
        "exporter_profile": {
            "company_name": "Dup Co",
            "business_registration": "REG999",
            "country": "France",
        },
    }
    res1 = await client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    res2 = await client.post("/api/v1/auth/register", json=payload)
    assert res2.status_code == 400


@pytest.mark.asyncio
async def test_login_and_me(client: AsyncClient):
    reg_payload = {
        "email": "login@example.com",
        "password": "mypassword",
        "role": "EXPORTER",
        "exporter_profile": {
            "company_name": "Login Co",
            "business_registration": "REG888",
            "country": "Canada",
        },
    }
    await client.post("/api/v1/auth/register", json=reg_payload)

    # Login
    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "login@example.com", "password": "mypassword"},
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # Get /users/me
    me_response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == "login@example.com"
    assert me_data["exporter_profile"]["company_name"] == "Login Co"


@pytest.mark.asyncio
async def test_profile_update(client: AsyncClient):
    reg_payload = {
        "email": "update@example.com",
        "password": "mypassword",
        "role": "EXPORTER",
        "exporter_profile": {
            "company_name": "Old Name",
            "business_registration": "REG111",
            "country": "Spain",
        },
    }
    await client.post("/api/v1/auth/register", json=reg_payload)

    login_res = await client.post(
        "/api/v1/auth/login",
        data={"username": "update@example.com", "password": "mypassword"},
    )
    token = login_res.json()["access_token"]

    update_res = await client.patch(
        "/api/v1/users/me/profile",
        json={"exporter_update": {"company_name": "New Name"}},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert update_res.status_code == 200
    assert update_res.json()["exporter_profile"]["company_name"] == "New Name"
    assert update_res.json()["exporter_profile"]["country"] == "Spain"
