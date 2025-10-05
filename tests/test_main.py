"""
Test module for main application functionality.

This module contains unit tests for the main application entry point.
"""

import sys
from io import StringIO
from unittest.mock import patch
from pathlib import Path

# Add parent directory to path for importing main module
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import get_app_info, main, __version__, __author__


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


def test_main_function_output():
    """Test that main function produces expected output."""
    # Capture stdout to test print statements
    captured_output = StringIO()
    with patch('sys.stdout', captured_output):
        main()
    
    output = captured_output.getvalue()
    assert "Starting Ornakala Backend v1.0.0" in output
    assert "Status: development" in output


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


def test_module_constants():
    """Test module-level constants."""
    assert __version__ == "1.0.0"
    assert __author__ == "Ornakala Team"
    assert isinstance(__version__, str)
    assert isinstance(__author__, str)


def test_get_app_info_version_consistency():
    """Test that get_app_info returns version consistent with module constant."""
    app_info = get_app_info()
    assert app_info["version"] == __version__


def test_main_function_calls_get_app_info():
    """Test that main function calls get_app_info."""
    with patch('main.get_app_info', return_value={
        "name": "Test App",
        "version": "1.0.0",
        "description": "Test description",
        "status": "test"
    }) as mock_get_app_info:
        with patch('sys.stdout', StringIO()):
            main()
        # Check that get_app_info was called
        assert mock_get_app_info.called


def test_main_function_error_handling():
    """Test main function behavior when get_app_info fails."""
    with patch('main.get_app_info', side_effect=Exception("Test error")):
        try:
            main()
            assert False, "Expected exception was not raised"
        except Exception as e:
            assert str(e) == "Test error"


def test_description_content():
    """Test that description contains expected keywords."""
    app_info = get_app_info()
    description = app_info["description"].lower()
    
    assert "backend" in description
    assert "ornakala" in description
    assert "customer" in description or "platform" in description