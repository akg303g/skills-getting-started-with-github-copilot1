def test_get_activities_returns_activity_list(client):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_new_participant(client):
    # Arrange
    url = "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up newstudent@mergington.edu for Chess Club"

    get_response = client.get("/activities")
    assert "newstudent@mergington.edu" in get_response.json()["Chess Club"]["participants"]


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    url = "/activities/Chess%20Club/signup?email=michael@mergington.edu"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant_removes_student(client):
    # Arrange
    url = "/activities/Chess%20Club/participants?email=michael@mergington.edu"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

    get_response = client.get("/activities")
    assert "michael@mergington.edu" not in get_response.json()["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    url = "/activities/Chess%20Club/participants?email=missing@mergington.edu"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
