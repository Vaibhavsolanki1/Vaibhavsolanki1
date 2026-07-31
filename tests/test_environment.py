import sys


def test_python_version() -> None:
    """Ensure Python version is 3.11 or newer."""
    assert sys.version_info >= (3, 11), "Python 3.11+ is required"


def test_imports() -> None:
    """Ensure core required standard and third-party libraries import correctly."""
    import jinja2
    import pydantic
    import yaml

    import scripts

    assert yaml.__name__ == "yaml"
    assert pydantic.__name__ == "pydantic"
    assert jinja2.__name__ == "jinja2"
    assert scripts.__version__ == "2.0.0"
