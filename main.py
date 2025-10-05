"""
Ornakala Backend Application Entry Point

This module serves as the main entry point for the Ornakala Backend API.
It provides customer-facing services for jewelry discovery and personalization.
"""

__version__ = "1.0.0"
__author__ = "Ornakala Team"


def get_app_info() -> dict[str, str]:
    """
    Get basic application information.

    Returns:
        dict[str, str]: Application information including name and version.
    """
    return {
        "name": "Ornakala Backend",
        "version": __version__,
        "description": "Backend service for Ornakala's customer platform",
        "status": "development"
    }


def main() -> None:
    """Main application entry point."""
    app_info = get_app_info()
    print(f"Starting {app_info['name']} v{app_info['version']}")
    print(f"Status: {app_info['status']}")


if __name__ == "__main__":
    main()
