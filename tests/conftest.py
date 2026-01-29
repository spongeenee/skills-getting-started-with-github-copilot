"""Pytest configuration and fixtures for FastAPI tests."""
import sys
from pathlib import Path
from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities as original_activities


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to their original state before each test."""
    # Store original state
    global original_activities
    original_state = deepcopy(original_activities)
    
    # Perform the test
    yield
    
    # Reset activities after test
    import app as app_module
    app_module.activities.clear()
    app_module.activities.update(deepcopy(original_state))

