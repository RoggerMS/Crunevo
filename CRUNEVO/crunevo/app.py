from crunevo import create_app as core_create_app


def create_app():
    """Compatibility wrapper for tests."""
    return core_create_app()
