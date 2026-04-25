def test_signup_fails_with_invalid_activity(client):
    # Arrange
    email = "invalid@mergington.edu"
    invalid_activity = "Nonexistent Club"

    # Act
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Activity not found" in result["detail"]


def test_signup_fails_with_duplicate_email(client):
    # Arrange
    email = "duplicate@mergington.edu"
    activity_name = "Gym Class"
    client.post(f"/activities/{activity_name}/signup?email={email}")  # First signup

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")  # Duplicate

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "already signed up" in result["detail"]


def test_unregister_fails_not_signed_up(client):
    # Arrange
    email = "notsigned@mergington.edu"
    activity_name = "Gym Class"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "not signed up" in result["detail"]


def test_unregister_fails_invalid_activity(client):
    # Arrange
    email = "invalidunreg@mergington.edu"
    invalid_activity = "Fake Activity"

    # Act
    response = client.delete(f"/activities/{invalid_activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Activity not found" in result["detail"]


def test_signup_with_missing_email_param(client):
    # Arrange
    activity_name = "Gym Class"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")  # No email param

    # Assert
    assert response.status_code == 422  # Unprocessable Entity for missing required param


def test_unregister_with_missing_email_param(client):
    # Arrange
    activity_name = "Gym Class"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup")  # No email param

    # Assert
    assert response.status_code == 422  # Unprocessable Entity for missing required param


def test_activity_names_are_case_sensitive(client):
    # Arrange
    email = "case@mergington.edu"
    wrong_case_activity = "chess club"  # lowercase, but actual is "Chess Club"

    # Act
    response = client.post(f"/activities/{wrong_case_activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404  # Should not find due to case sensitivity


def test_participant_list_consistency_after_operations(client):
    # Arrange
    email1 = "consistent1@mergington.edu"
    email2 = "consistent2@mergington.edu"
    activity_name = "Gym Class"

    # Act: Sign up two students
    client.post(f"/activities/{activity_name}/signup?email={email1}")
    client.post(f"/activities/{activity_name}/signup?email={email2}")

    # Assert: Both are in the list
    response = client.get("/activities")
    data = response.json()
    participants = data[activity_name]["participants"]
    assert email1 in participants
    assert email2 in participants
    assert len(participants) == 2

    # Act: Remove one
    client.delete(f"/activities/{activity_name}/signup?email={email1}")

    # Assert: Only one remains
    response = client.get("/activities")
    data = response.json()
    participants = data[activity_name]["participants"]
    assert email1 not in participants
    assert email2 in participants
    assert len(participants) == 1