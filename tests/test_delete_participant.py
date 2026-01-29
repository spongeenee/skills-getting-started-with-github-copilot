"""Tests for the delete participant endpoint."""
import pytest


class TestDeleteParticipant:
    """Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_delete_participant_success(self, client):
        """Test successful deletion of a participant."""
        # alex@mergington.edu is in Tennis Club initially
        response = client.delete(
            "/activities/Tennis Club/participants/alex@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "removed" in data["message"]

    def test_delete_participant_removes_from_list(self, client):
        """Test that delete actually removes the participant from the list."""
        # james@mergington.edu is in Basketball Team
        email = "james@mergington.edu"
        activity = "Basketball Team"
        
        # Verify participant exists
        initial_response = client.get("/activities")
        assert email in initial_response.json()[activity]["participants"]
        
        # Delete
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        assert response.status_code == 200
        
        # Verify participant is removed
        final_response = client.get("/activities")
        assert email not in final_response.json()[activity]["participants"]

    def test_delete_nonexistent_participant(self, client):
        """Test deletion of a participant that doesn't exist in the activity."""
        response = client.delete(
            "/activities/Tennis Club/participants/nonexistent@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Participant not found" in data["detail"]

    def test_delete_from_nonexistent_activity(self, client):
        """Test deletion from a non-existent activity."""
        response = client.delete(
            "/activities/Nonexistent Activity/participants/test@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_delete_with_email_containing_plus(self, client):
        """Test deletion with email containing plus sign."""
        email = "user+test@mergington.edu"
        activity = "Tennis Club"
        
        # First sign up the participant using URL encoded + sign
        client.post(f"/activities/{activity}/signup?email=user%2Btest@mergington.edu")
        
        # Then delete using URL encoded + sign
        response = client.delete(
            f"/activities/{activity}/participants/user%2Btest@mergington.edu"
        )
        assert response.status_code == 200
        
        # Verify removal
        final_response = client.get("/activities")
        assert email not in final_response.json()[activity]["participants"]
