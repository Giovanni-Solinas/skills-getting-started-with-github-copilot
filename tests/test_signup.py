def test_signup_success_adds_participant(client):
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_fails_when_activity_not_found(client):
    response = client.post("/activities/Unknown%20Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_fails_when_already_registered(client):
    existing_email = "michael@mergington.edu"

    response = client.post(f"/activities/Chess%20Club/signup?email={existing_email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_success_removes_participant(client):
    existing_email = "michael@mergington.edu"

    response = client.delete(f"/activities/Chess%20Club/signup?email={existing_email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {existing_email} from Chess Club"

    activities = client.get("/activities").json()
    assert existing_email not in activities["Chess Club"]["participants"]


def test_unregister_fails_when_activity_not_found(client):
    response = client.delete("/activities/Unknown%20Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_fails_when_participant_not_registered(client):
    missing_email = "notregistered@mergington.edu"

    response = client.delete(f"/activities/Chess%20Club/signup?email={missing_email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_isolation_starts_each_test_from_clean_state(client):
    baseline_email = "michael@mergington.edu"

    activities = client.get("/activities").json()
    assert baseline_email in activities["Chess Club"]["participants"]
