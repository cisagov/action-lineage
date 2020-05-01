#!/usr/bin/env pytest -vs
"""Tests for abp action."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest

# cisagov Libraries
import _version

# define sources of version strings
PROJECT_VERSION = _version.__version__
RELEASE_TAG = os.getenv("RELEASE_TAG")


@pytest.mark.skipif(
    RELEASE_TAG in [None, ""], reason="this is not a release (RELEASE_TAG not set)"
)
def test_release_version():
    """Verify that release tag version agrees with the module version."""
    assert (
        RELEASE_TAG == f"v{PROJECT_VERSION}"
    ), "RELEASE_TAG does not match the project version"
