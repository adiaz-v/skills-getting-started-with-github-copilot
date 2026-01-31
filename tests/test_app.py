from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities_returns_200_and_json():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # Ensure there is at least one known activity
    assert "Chess Club" in data


def test_signup_and_duplicate_handling():
    activity = "Chess Club"
    test_email = "testuser@example.com"

    # Ensure not present first (if present, remove)
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)

    res = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert res.status_code == 200
    assert test_email in activities[activity]["participants"]

    # Duplicate signup should return 400
    res2 = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert res2.status_code == 400

    # Cleanup
    activities[activity]["participants"].remove(test_email)


def test_unregister_participant_success_and_not_found():
    activity = "Chess Club"
    test_email = "removeme@example.com"

    # Ensure participant is present
    if test_email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(test_email)

    res = client.post(f"/activities/{activity}/unregister", json={"email": test_email})
    assert res.status_code == 200
    assert test_email not in activities[activity]["participants"]

    # Trying to remove again should produce 404
    res2 = client.post(f"/activities/{activity}/unregister", json={"email": test_email})
    assert res2.status_code == 404
