def test_unregister_removes_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    updated_activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in updated_activities[activity_name]["participants"]


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    missing_activity = "Sky Diving Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{missing_activity}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "not.registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": missing_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in activity"
