import pytest


def test_unregister_existing_participant_success(client):
    """Test successful unregistration of an existing participant"""
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already a participant
    
    response = client.post(
        f"/activities/{activity}/unregister?email={email}"
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert "Unregistered" in result["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes the participant"""
    activity = "Programming Class"
    email = "emma@mergington.edu"  # Already a participant
    
    # Verify they're there before unregister
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]
    
    # Unregister
    client.post(f"/activities/{activity}/unregister?email={email}")
    
    # Verify they're gone
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]


def test_unregister_nonexistent_activity_returns_404(client):
    """Test that unregistering from non-existent activity returns 404"""
    response = client.post(
        "/activities/Fake Activity/unregister?email=test@mergington.edu"
    )
    
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result


def test_unregister_nonexistent_participant_returns_404(client):
    """Test that unregistering a non-participant returns 404"""
    activity = "Chess Club"
    email = "nonexistent@mergington.edu"
    
    response = client.post(
        f"/activities/{activity}/unregister?email={email}"
    )
    
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "not found" in result["detail"].lower()


def test_unregister_then_signup_again(client):
    """Test that a participant can sign up again after unregistering"""
    activity = "Gym Class"
    email = "john@mergington.edu"
    
    # Unregister
    client.post(f"/activities/{activity}/unregister?email={email}")
    
    # Verify they're gone
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]
    
    # Sign up again
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Verify they're back (should only appear once)
    response = client.get("/activities")
    participants = response.json()[activity]["participants"]
    assert email in participants
    assert participants.count(email) == 1
