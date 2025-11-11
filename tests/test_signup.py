from fastapi.testclient import TestClient
from src.app import app, activities


client = TestClient(app)


def test_signup_success():
    activity = "Chess Club"
    email = "test_student@example.com"
    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200, resp.text
    assert email in activities[activity]["participants"]


def test_signup_when_full():
    activity = "Math Club"
    # Make activity full
    activities[activity]["max_participants"] = 1
    activities[activity]["participants"] = ["one@student.edu"]

    resp = client.post(f"/activities/{activity}/signup", params={"email": "another@student.edu"})
    assert resp.status_code == 400


if __name__ == "__main__":
    test_signup_success()
    test_signup_when_full()
    print("tests passed")
