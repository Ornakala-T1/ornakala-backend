"""
Test module for main application functionality.

This module contains unit tests for the main application entry point.
"""

import pytest
from main import get_app_info, main


def test_get_app_info():
    """Test that get_app_info returns expected structure."""
    app_info = get_app_info()
    
    assert isinstance(app_info, dict)
    assert "name" in app_info
    assert "version" in app_info
    assert "description" in app_info
    assert "status" in app_info
    
    assert app_info["name"] == "Ornakala Backend"
    assert app_info["version"] == "1.0.0"
    assert app_info["status"] == "development"


def test_get_app_info_types():
    """Test that get_app_info returns correct types."""
    app_info = get_app_info()
    
    for key, value in app_info.items():
        assert isinstance(key, str)
        assert isinstance(value, str)


def test_main_function():
    """Test that main function executes without errors."""
    # This test just ensures main() doesn't raise an exception
    try:
        main()
    except Exception as e:
        pytest.fail(f"main() raised {e} unexpectedly!")


def test_app_name_not_empty():
    """Test that application name is not empty."""
    app_info = get_app_info()
    assert len(app_info["name"]) > 0


def test_version_format():
    """Test that version follows semantic versioning format."""
    app_info = get_app_info()
    version = app_info["version"]
    
    # Basic check for semantic versioning (x.y.z)
    parts = version.split(".")
    assert len(parts) == 3
    
    for part in parts:
        assert part.isdigit()