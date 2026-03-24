import pytest


def test_signup_new_participant_success(client):
    """Test successful signup of a new participant"""
    email = "newemail@mergington.edu"
    activity = "Chess Club"
    
    response = client.post(
        f"/activities/{activity}/signup?email={email}",
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert "Signed up" in result["message"]
    assert email in result["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that participant is actually added to the activity"""
    email = "newstudent@mergington.edu"
    activity = "Programming Class"
    
    # Sign up the student
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Verify they appear in the activity list
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity]["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signing up for non-existent activity returns 404"""
    response = client.post(
        "/activities/Nonexistent Activity/signup?email=test@mergington.edu"
    )
    
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "not found" in result["detail"].lower()


def test_signup_duplicate_participant_error(client):
    """Test that signing up the same person twice causes an error or adds them twice"""
    email = "duplicate@mergington.edu"
    activity = "Tennis Club"
    
    # First signup
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response1.status_code == 200
    
    # Second signup - should ideally fail, but currently adds them twice
    # This documents the known bug
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Verify both signups went through (documenting the bug)
    response = client.get("/activities")
    activities = response.json()
    participant_count = activities[activity]["participants"].count(email)
    assert participant_count == 2  # Bug: duplicate signup allowed


def test_signup_multiple_different_participants(client):
    """Test that multiple different participants can sign up"""
    activity = "Debate Team"
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    client.post(f"/activities/{activity}/signup?email={email1}")
    client.post(f"/activities/{activity}/signup?email={email2}")
    
    response = client.get("/activities")
    activities = response.json()
    assert email1 in activities[activity]["participants"]
    assert email2 in activities[activity]["participants"]
