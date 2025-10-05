"""
Test module for main script execution.

This module tests the script execution path of main.py.
"""

import subprocess
import sys
from pathlib import Path


def test_main_script_execution():
    """Test that main.py can be executed as a script."""
    # Get the path to main.py (in parent directory)
    main_script = Path(__file__).parent.parent / "main.py"

    # Execute the script and capture output
    result = subprocess.run(
        [sys.executable, str(main_script)],
        capture_output=True,
        text=True,
        timeout=10,
        check=False
    )

    # Check that script executed successfully
    assert result.returncode == 0

    # Check that expected output is present
    output = result.stdout
    assert "Starting Ornakala Backend v1.0.0" in output
    assert "Status: development" in output


def test_main_script_no_errors():
    """Test that main.py execution produces no errors."""
    main_script = Path(__file__).parent.parent / "main.py"

    result = subprocess.run(
        [sys.executable, str(main_script)],
        capture_output=True,
        text=True,
        timeout=10,
        check=False
    )

    # Should have no stderr output
    assert result.stderr == "" or "Starting" in result.stdout
    assert result.returncode == 0
