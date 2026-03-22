from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_and_job_flow():
    login = client.post(
        "/auth/login",
        data={"username": "admin", "password": "change-me-now"},
    )
    assert login.status_code == 200, login.text
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    created = client.post(
        "/jobs",
        headers=headers,
        json={
            "job_type": "scrape",
            "target": "https://example.com",
            "options": {"max_pages": 3, "depth": 1},
        },
    )
    assert created.status_code == 201, created.text
    job_id = created.json()["id"]

    status_resp = client.get(f"/jobs/{job_id}", headers=headers)
    assert status_resp.status_code == 200, status_resp.text

    result_resp = client.get(f"/results/{job_id}", headers=headers)
    assert result_resp.status_code in (200, 409), result_resp.text
