"""
Test module for main application functionality.

This module contains unit tests for the main adefdef t    with patch(\"main.get_app_info\", side_effect=Exception(\"Test error\")), pytest.raises(Exception, match=\"Test error\"):
        main()_main_function_error_handling():
    \"\"\"Test main function behavior when get_app_info fails.\"\"\"
    with patch(\"main.get_app_info\", side_effect=Exception(\"Test error\")), pytest.raises(Exception, match=\"Test error\"):
        main()_main_function_error_handling():
    \"\"\"Test main function behavior when get_app_info fails.\"\"\"
    with patch(\"main.get_app_info\", side_effect=Exception(\"Test error\")), pytest.raises(Exception, match=\"Test error\"):
        main()ation entry point.
"""

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

# Add parent directory to path for importing main module
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import __author__, __version__, get_app_info, main


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
    with patch("sys.stdout", captured_output):
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
    with patch(
        "main.get_app_info",
        return_value={
            "name": "Test App",
            "version": "1.0.0",
            "description": "Test description",
            "status": "test",
        },
    ) as mock_get_app_info:
        with patch("sys.stdout", StringIO()):
            main()
        # Check that get_app_info was called
        assert mock_get_app_info.called


def test_main_function_error_handling():
    """Test main function behavior when get_app_info fails."""
    with patch("main.get_app_info", side_effect=Exception("Test error")):
        with pytest.raises(Exception, match="Test error"):
            main()


def test_description_content():
    """Test that description contains expected keywords."""
    app_info = get_app_info()
    description = app_info["description"].lower()

    assert "backend" in description
    assert "ornakala" in description
    assert "customer" in description or "platform" in description


def test_module_level_variables():
    """Test that module-level variables are accessible and correct."""
    # Import the module to access module-level variables
    import main

    # Test __version__
    assert hasattr(main, "__version__")
    assert main.__version__ == "1.0.0"
    assert isinstance(main.__version__, str)

    # Test __author__
    assert hasattr(main, "__author__")
    assert main.__author__ == "Ornakala Team"
    assert isinstance(main.__author__, str)


def test_main_script_execution_block():
    """Test the if __name__ == '__main__' block execution."""
    import subprocess
    import sys

    # Run the main.py script as a subprocess to test the __main__ block
    result = subprocess.run(
        [sys.executable, "main.py"],
        capture_output=True,
        text=True,
        cwd=".",
        check=False,
    )

    # Check that the script ran successfully
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    # Check that the output contains expected content
    output = result.stdout
    assert "Starting Ornakala Backend" in output
    assert "v1.0.0" in output
    assert "Status: development" in output


def test_main_execution_directly():
    """Test calling main() directly to ensure the if __name__ == '__main__' line is covered."""
    # This test helps cover the main() call that would happen in the __main__ block
    with patch("builtins.print") as mock_print:
        from main import main

        main()

        # Verify that print was called with expected content
        assert mock_print.call_count == 2
        calls = [call.args[0] for call in mock_print.call_args_list]

        assert any("Starting Ornakala Backend v1.0.0" in call for call in calls)
        assert any("Status: development" in call for call in calls)


def test_main_as_script_execution():
    """Test the __main__ block by simulating script execution."""
    import contextlib
    import io

    import coverage

    # Create a coverage instance
    cov = coverage.Coverage(source=["main"])
    cov.start()

    try:
        # Execute the main.py file as __main__ using exec
        with open("main.py") as f:
            code = compile(f.read(), "main.py", "exec")

        # Create namespace that simulates running as __main__
        namespace = {"__name__": "__main__"}

        # Capture stdout
        stdout_buffer = io.StringIO()
        with contextlib.redirect_stdout(stdout_buffer):
            exec(code, namespace)

        output = stdout_buffer.getvalue()

        # Verify the expected output
        assert "Starting Ornakala Backend v1.0.0" in output
        assert "Status: development" in output

    finally:
        cov.stop()
        cov.save()


def test_version_in_get_app_info():
    """Test that get_app_info uses the module-level __version__."""
    import main

    app_info = get_app_info()

    # Verify that the version in app_info matches the module-level __version__
    assert app_info["version"] == main.__version__
    assert app_info["version"] == "1.0.0"
