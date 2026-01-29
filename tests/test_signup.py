"""Tests for the signup endpoint."""
import pytest
from urllib.parse import urlencode


class TestSignup:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client):
        """Test successful signup for an activity."""
        response = client.post(
            "/activities/Tennis Club/signup?email=newemail@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "newemail@mergington.edu" in data["message"]

    def test_signup_nonexistent_activity(self, client):
        """Test signup for a non-existent activity."""
        response = client.post(
            "/activities/Nonexistent Activity/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_email(self, client):
        """Test signup with an email that's already registered."""
        # alex@mergington.edu is already in Tennis Club
        response = client.post(
            "/activities/Tennis Club/signup?email=alex@mergington.edu"
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_adds_participant(self, client):
        """Test that signup actually adds the participant."""
        email = "testuser@mergington.edu"
        activity = "Art Club"
        
        # Get initial participant count
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[activity]["participants"].copy()
        
        # Sign up
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
        
        # Check that participant was added
        final_response = client.get("/activities")
        final_participants = final_response.json()[activity]["participants"]
        assert email in final_participants
        assert len(final_participants) == len(initial_participants) + 1

    def test_signup_multiple_activities(self, client):
        """Test that a student can sign up for multiple activities."""
        email = "multiactivity@mergington.edu"
        activities = ["Tennis Club", "Art Club", "Drama Club"]
        
        for activity in activities:
            response = client.post(
                f"/activities/{activity}/signup?email={email}"
            )
            assert response.status_code == 200
        
        # Verify student is in all activities
        final_response = client.get("/activities")
        data = final_response.json()
        for activity in activities:
            assert email in data[activity]["participants"]

    def test_signup_with_email_containing_plus(self, client):
        """Test signup with email containing plus sign."""
        email = "user+test@mergington.edu"
        # URL encode the + sign as %2B
        response = client.post(
            f"/activities/Tennis Club/signup?email=user%2Btest@mergington.edu"
        )
        assert response.status_code == 200
        
        # Verify student was added
        final_response = client.get("/activities")
        assert email in final_response.json()["Tennis Club"]["participants"]

