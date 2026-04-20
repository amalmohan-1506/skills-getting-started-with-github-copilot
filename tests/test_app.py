"""
Tests for the Mergington High School API
Using AAA (Arrange-Act-Assert) testing pattern
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestActivities:
    """Tests for the /activities endpoint"""
    
    def test_get_activities(self):
        """Test retrieving all activities"""
        # Arrange - No special setup needed
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert len(activities) == 9
    
    def test_activity_structure(self):
        """Test that activities have the correct structure"""
        # Arrange - No special setup needed
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        activity = activities["Chess Club"]
        
        # Assert
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)


class TestSignup:
    """Tests for signup/registration endpoints"""
    
    def test_signup_for_activity(self):
        """Test signing up for an activity"""
        # Arrange
        activity_name = "Basketball Team"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert "Signed up" in response_data["message"]
        assert email in response_data["message"]
    
    def test_signup_duplicate(self):
        """Test that duplicate signups are rejected"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already enrolled
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert "already signed up" in response_data["detail"]
    
    def test_signup_nonexistent_activity(self):
        """Test signing up for a non-existent activity"""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert "not found" in response_data["detail"]
    
    def test_signup_adds_to_participants(self):
        """Test that signup adds student to participants list"""
        # Arrange
        activity_name = "Soccer Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify student was added to the activity
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]


class TestUnregister:
    """Tests for unregistration endpoint"""
    
    def test_unregister_from_activity(self):
        """Test unregistering from an activity"""
        # Arrange
        activity_name = "Art Club"
        email = "student@mergington.edu"
        
        # First sign up the student
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert "Unregistered" in response_data["message"]
    
    def test_unregister_not_enrolled(self):
        """Test unregistering when not enrolled"""
        # Arrange
        activity_name = "Drama Club"
        email = "notstudent@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert "not signed up" in response_data["detail"]
    
    def test_unregister_nonexistent_activity(self):
        """Test unregistering from non-existent activity"""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert "not found" in response_data["detail"]


class TestRoot:
    """Tests for the root endpoint"""
    
    def test_root_redirect(self):
        """Test that root endpoint redirects to index.html"""
        # Arrange - No special setup needed
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"