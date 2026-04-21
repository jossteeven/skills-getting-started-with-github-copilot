def test_get_activities_returns_complete_list(client):
    # Arrange
    # Activities are reset by fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Soccer Club", "Art Club", "Drama Club", "Debate Club", "Science Club"
    ]
    for activity in expected_activities:
        assert activity in data


def test_get_activities_has_all_required_fields(client):
    # Arrange
    # Activities are reset by fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    activity = data["Chess Club"]
    required_fields = ["description", "schedule", "max_participants", "participants"]
    for field in required_fields:
        assert field in activity
    assert isinstance(activity["participants"], list)


def test_get_activities_shows_participant_count(client):
    # Arrange
    # All activities start with empty participants

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    for activity_name, activity_data in data.items():
        assert len(activity_data["participants"]) == 0


def test_signup_succeeds_with_valid_activity_and_email(client):
    # Arrange
    email = "newstudent@mergington.edu"
    activity_name = "Gym Class"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]


def test_signup_adds_participant_to_activity(client):
    # Arrange
    email = "signuptest@mergington.edu"
    activity_name = "Gym Class"

    # Act
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    response = client.get("/activities")
    data = response.json()
    assert email in data[activity_name]["participants"]


def test_signup_response_format_correct(client):
    # Arrange
    email = "format@mergington.edu"
    activity_name = "Gym Class"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert result == {"message": f"Signed up {email} for {activity_name}"}


def test_unregister_succeeds_with_valid_signup(client):
    # Arrange
    email = "unregister@mergington.edu"
    activity_name = "Gym Class"
    client.post(f"/activities/{activity_name}/signup?email={email}")  # Sign up first

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]


def test_unregister_removes_participant(client):
    # Arrange
    email = "removetest@mergington.edu"
    activity_name = "Gym Class"
    client.post(f"/activities/{activity_name}/signup?email={email}")  # Sign up first

    # Act
    client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    response = client.get("/activities")
    data = response.json()
    assert email not in data[activity_name]["participants"]


def test_unregister_response_format_correct(client):
    # Arrange
    email = "unregformat@mergington.edu"
    activity_name = "Gym Class"
    client.post(f"/activities/{activity_name}/signup?email={email}")  # Sign up first

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert result == {"message": f"Unregistered {email} from {activity_name}"}