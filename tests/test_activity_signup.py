def test_signup_adds_participant_to_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    updated_activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in updated_activities[activity_name]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": duplicate_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_rejects_unknown_activity(client):
    # Arrange
    missing_activity = "Sky Diving Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{missing_activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
