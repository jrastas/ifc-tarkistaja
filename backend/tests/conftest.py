"""Pytest configuration and fixtures."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_ifc_path() -> Path:
    """Return path to the sample IFC file."""
    return Path(__file__).parent / "fixtures" / "sample.ifc"


@pytest.fixture
def sample_ifc_bytes(sample_ifc_path: Path) -> bytes:
    """Return contents of the sample IFC file."""
    return sample_ifc_path.read_bytes()
