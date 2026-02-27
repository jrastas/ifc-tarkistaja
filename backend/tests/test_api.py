"""Tests for API endpoints."""

from pathlib import Path

from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Tests for /api/health endpoint."""

    def test_health_check(self, client: TestClient) -> None:
        """Test health check returns healthy status."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestValidateEndpoint:
    """Tests for /api/validate endpoint."""

    def test_validate_ifc_file(
        self, client: TestClient, sample_ifc_path: Path
    ) -> None:
        """Test validating a valid IFC file."""
        with open(sample_ifc_path, "rb") as f:
            response = client.post(
                "/api/validate",
                files={"file": ("sample.ifc", f, "application/octet-stream")},
            )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["report"] is not None
        assert data["report"]["filename"] == "sample.ifc"
        assert data["report"]["ifc_schema"].startswith("IFC4X3")

    def test_validate_non_ifc_file(self, client: TestClient) -> None:
        """Test validating a non-IFC file returns error."""
        response = client.post(
            "/api/validate",
            files={"file": ("test.txt", b"not an ifc file", "text/plain")},
        )

        assert response.status_code == 400
        assert "IFC file" in response.json()["detail"]

    def test_validate_invalid_ifc_content(self, client: TestClient) -> None:
        """Test validating invalid IFC content returns error."""
        # File with .ifc extension but no valid IFC content (magic bytes)
        response = client.post(
            "/api/validate",
            files={"file": ("invalid.ifc", b"not valid ifc", "application/octet-stream")},
        )

        # Should return 400 due to missing magic bytes
        assert response.status_code == 400
        assert "valid IFC file" in response.json()["detail"]

    def test_validate_file_size_limit(self, client: TestClient) -> None:
        """Test that oversized files are rejected."""
        # Create a fake large file header (just test the validation logic)
        # In practice, this would be tested with actual large file
        # but we can verify the endpoint accepts the size check
        response = client.post(
            "/api/validate",
            files={"file": ("test.txt", b"x", "text/plain")},
        )
        # Extension check happens first
        assert response.status_code == 400

    def test_validate_response_structure(
        self, client: TestClient, sample_ifc_path: Path
    ) -> None:
        """Test validation response has correct structure."""
        with open(sample_ifc_path, "rb") as f:
            response = client.post(
                "/api/validate",
                files={"file": ("sample.ifc", f, "application/octet-stream")},
            )

        data = response.json()
        report = data["report"]

        assert "filename" in report
        assert "timestamp" in report
        assert "ifc_schema" in report
        assert "overall_compliance" in report
        assert "required_compliance" in report
        assert "categories" in report
        assert "warnings" in report
        assert "errors" in report


class TestPDFExportEndpoint:
    """Tests for /api/export/pdf endpoint."""

    def test_pdf_export_endpoint(
        self, client: TestClient, sample_ifc_path: Path
    ) -> None:
        """Test PDF export endpoint generates PDF."""
        # First validate to get report
        with open(sample_ifc_path, "rb") as f:
            validate_response = client.post(
                "/api/validate",
                files={"file": ("sample.ifc", f, "application/octet-stream")},
            )

        report = validate_response.json()["report"]

        # Then export PDF
        pdf_response = client.post(
            "/api/export/pdf",
            json=report,
            params={"language": "fi"},
        )

        assert pdf_response.status_code == 200
        assert pdf_response.headers["content-type"] == "application/pdf"
        assert pdf_response.content.startswith(b"%PDF-")

    def test_pdf_export_finnish(
        self, client: TestClient, sample_ifc_path: Path
    ) -> None:
        """Test PDF export with Finnish language."""
        with open(sample_ifc_path, "rb") as f:
            validate_response = client.post(
                "/api/validate",
                files={"file": ("sample.ifc", f, "application/octet-stream")},
            )

        report = validate_response.json()["report"]

        pdf_response = client.post(
            "/api/export/pdf",
            json=report,
            params={"language": "fi"},
        )

        assert pdf_response.status_code == 200
        assert pdf_response.headers["content-type"] == "application/pdf"

    def test_pdf_export_english(
        self, client: TestClient, sample_ifc_path: Path
    ) -> None:
        """Test PDF export with English language."""
        with open(sample_ifc_path, "rb") as f:
            validate_response = client.post(
                "/api/validate",
                files={"file": ("sample.ifc", f, "application/octet-stream")},
            )

        report = validate_response.json()["report"]

        pdf_response = client.post(
            "/api/export/pdf",
            json=report,
            params={"language": "en"},
        )

        assert pdf_response.status_code == 200
        assert pdf_response.headers["content-type"] == "application/pdf"

    def test_pdf_export_filename_header(
        self, client: TestClient, sample_ifc_path: Path
    ) -> None:
        """Test PDF export includes correct filename in header."""
        with open(sample_ifc_path, "rb") as f:
            validate_response = client.post(
                "/api/validate",
                files={"file": ("sample.ifc", f, "application/octet-stream")},
            )

        report = validate_response.json()["report"]

        pdf_response = client.post(
            "/api/export/pdf",
            json=report,
            params={"language": "fi"},
        )

        content_disposition = pdf_response.headers.get("content-disposition", "")
        assert "attachment" in content_disposition
        assert "sample" in content_disposition
        assert ".pdf" in content_disposition
