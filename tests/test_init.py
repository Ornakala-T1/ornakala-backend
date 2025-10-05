"""
Tests for the main package __init__.py module.

This module tests the package-level attributes and ensures they are properly defined.
"""

import pytest


def test_package_version():
    """Test that the package version is properly defined."""
    from __init__ import __version__
    
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert __version__ == "1.0.0"


def test_package_author():
    """Test that the package author is properly defined."""
    from __init__ import __author__
    
    assert __author__ is not None
    assert isinstance(__author__, str)
    assert __author__ == "Ornakala Team"


def test_package_version_format():
    """Test that the version follows semantic versioning format."""
    from __init__ import __version__
    
    # Check that version follows x.y.z format
    version_parts = __version__.split(".")
    assert len(version_parts) == 3
    
    # Check that all parts are numeric
    for part in version_parts:
        assert part.isdigit()


def test_package_author_not_empty():
    """Test that the author field is not empty."""
    from __init__ import __author__
    
    assert len(__author__.strip()) > 0
    assert "Team" in __author__


def test_package_attributes_exist():
    """Test that all expected package attributes exist."""
    import __init__ as package
    
    # Test that attributes exist
    assert hasattr(package, "__version__")
    assert hasattr(package, "__author__")
    
    # Test that they're accessible
    version = getattr(package, "__version__")
    author = getattr(package, "__author__")
    
    assert version is not None
    assert author is not None


def test_package_docstring():
    """Test that the package has a proper docstring."""
    import __init__ as package
    
    assert package.__doc__ is not None
    assert isinstance(package.__doc__, str)
    assert len(package.__doc__.strip()) > 0
    assert "Ornakala" in package.__doc__