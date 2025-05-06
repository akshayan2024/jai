"""
Pytest configuration file.
"""

import os
import sys
import pytest

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import constants loader
from jai_api.constants import load_all_constants

@pytest.fixture(scope="session", autouse=True)
def load_constants():
    """Load all constants before running tests."""
    load_all_constants()
    return True

# Create a dummy logger fixture
@pytest.fixture
def mock_logger(monkeypatch):
    """Mock logger to avoid file IO during tests."""
    class MockLogger:
        def debug(self, message):
            pass
            
        def info(self, message):
            pass
            
        def warning(self, message):
            pass
            
        def error(self, message):
            pass
    
    # Mock the get_logger function
    def mock_get_logger(*args, **kwargs):
        return MockLogger()
    
    # Apply the patch
    monkeypatch.setattr("jai_api.utils.logger.get_logger", mock_get_logger)
    
    return MockLogger() 