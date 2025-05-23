"""Tests for lineage action."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest

# cisagov Libraries
import lineage
import lineage.entrypoint

TEMPLATE_PATH_BASE = "tests/templates/"

# define sources of version strings
PROJECT_VERSION = lineage.__version__
RELEASE_TAG = os.getenv("RELEASE_TAG")


@pytest.mark.parametrize("template_file", ["clean_template.md", "conflict_template.md"])
def test_load_template(template_file):
    """Test that a template can be successfully loaded."""
    template = lineage.entrypoint.load_template(".", template_file)
    with open(TEMPLATE_PATH_BASE + template_file) as test_file:
        test_template = test_file.read().rstrip()
    assert template == test_template, "template data does not match"


def test_unset_ca_variables():
    """Test that CA variables are unset."""
    os.environ["REQUESTS_CA_BUNDLE"] = "test"
    lineage.entrypoint.clear_ca_variables_in_gha()
    assert "REQUESTS_CA_BUNDLE" not in os.environ


@pytest.mark.skipif(
    RELEASE_TAG in [None, ""], reason="this is not a release (RELEASE_TAG not set)"
)
def test_release_version():
    """Verify that release tag version agrees with the module version."""
    assert (
        RELEASE_TAG == f"v{PROJECT_VERSION}"
    ), "RELEASE_TAG does not match the project version"
