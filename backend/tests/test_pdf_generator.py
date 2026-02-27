"""Tests for PDF generator service."""

from pathlib import Path

import pytest

from app.schemas.validation import (
    CategoryValidation,
    CoordinateInfo,
    FieldValidation,
    ValidationReport,
    ValidationStatus,
)
from app.services.pdf_generator import PDFGeneratorService


class TestPDFGeneratorService:
    """Tests for PDFGeneratorService."""

    @pytest.fixture
    def pdf_generator(self) -> PDFGeneratorService:
        """Create a PDF generator service instance."""
        return PDFGeneratorService()

    @pytest.fixture
    def sample_report(self) -> ValidationReport:
        """Create a sample validation report for testing."""
        return ValidationReport(
            filename="test_building.ifc",
            timestamp="2024-01-15T10:30:00",
            ifc_schema="IFC4X3_ADD2",
            overall_compliance=0.75,
            required_compliance=0.85,
            categories=[
                CategoryValidation(
                    id="rakennuspaikka",
                    name="Rakennuspaikka",
                    name_en="Building Site",
                    icon="map-pin",
                    compliance_percentage=80.0,
                    required_compliance=90.0,
                    fields=[
                        FieldValidation(
                            field_name="Nimi",
                            field_name_en="Name",
                            ifc_entity="IfcSite",
                            ifc_property="IfcSite.Name",
                            is_required=True,
                            is_present=True,
                            value="Test Site",
                            status=ValidationStatus.VALID,
                        ),
                        FieldValidation(
                            field_name="Kiinteistötunnus",
                            field_name_en="Property ID",
                            ifc_entity="IfcSite",
                            ifc_property="Pset_SiteCommon.LandTitleNumber",
                            is_required=True,
                            is_present=True,
                            value="091-001-0001-0001",
                            status=ValidationStatus.VALID,
                        ),
                        FieldValidation(
                            field_name="Osoite",
                            field_name_en="Address",
                            ifc_entity="IfcSite",
                            ifc_property="IfcSite.SiteAddress",
                            is_required=False,
                            is_present=False,
                            value=None,
                            status=ValidationStatus.WARNING,
                        ),
                    ],
                ),
                CategoryValidation(
                    id="rakennuskohde",
                    name="Rakennuskohde",
                    name_en="Building",
                    icon="building",
                    compliance_percentage=60.0,
                    required_compliance=70.0,
                    fields=[
                        FieldValidation(
                            field_name="Nimi",
                            field_name_en="Name",
                            ifc_entity="IfcBuilding",
                            ifc_property="IfcBuilding.Name",
                            is_required=True,
                            is_present=True,
                            value="Test Building",
                            status=ValidationStatus.VALID,
                        ),
                        FieldValidation(
                            field_name="Käyttötarkoitus",
                            field_name_en="Usage",
                            ifc_entity="IfcBuilding",
                            ifc_property="Pset_BuildingCommon.OccupancyType",
                            is_required=True,
                            is_present=False,
                            value=None,
                            status=ValidationStatus.MISSING,
                        ),
                    ],
                ),
            ],
            coordinate_system=CoordinateInfo(
                system="EPSG:3879",
                valid=True,
            ),
            warnings=["Optional field 'Osoite' is missing in Rakennuspaikka"],
            errors=["Required field 'Käyttötarkoitus' missing in Rakennuskohde"],
        )

    def test_generate_pdf_returns_bytes(
        self, pdf_generator: PDFGeneratorService, sample_report: ValidationReport
    ) -> None:
        """Test that PDF generation returns bytes."""
        pdf_bytes = pdf_generator.generate(sample_report)
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0

    def test_generate_pdf_is_valid_pdf(
        self, pdf_generator: PDFGeneratorService, sample_report: ValidationReport
    ) -> None:
        """Test that generated PDF has valid PDF header."""
        pdf_bytes = pdf_generator.generate(sample_report)
        # PDF files start with %PDF-
        assert pdf_bytes.startswith(b"%PDF-")

    def test_generate_pdf_finnish(
        self, pdf_generator: PDFGeneratorService, sample_report: ValidationReport
    ) -> None:
        """Test PDF generation with Finnish language."""
        pdf_generator.language = "fi"
        pdf_bytes = pdf_generator.generate(sample_report)
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0

    def test_generate_pdf_english(
        self, pdf_generator: PDFGeneratorService, sample_report: ValidationReport
    ) -> None:
        """Test PDF generation with English language."""
        pdf_generator.language = "en"
        pdf_bytes = pdf_generator.generate(sample_report)
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0

    def test_generate_pdf_with_empty_categories(
        self, pdf_generator: PDFGeneratorService
    ) -> None:
        """Test PDF generation with empty categories."""
        report = ValidationReport(
            filename="empty.ifc",
            timestamp="2024-01-15T10:30:00",
            ifc_schema="IFC4X3_ADD2",
            overall_compliance=0.0,
            required_compliance=0.0,
            categories=[],
            coordinate_system=CoordinateInfo(valid=False),
            warnings=[],
            errors=[],
        )
        pdf_bytes = pdf_generator.generate(report)
        assert isinstance(pdf_bytes, bytes)
        assert pdf_bytes.startswith(b"%PDF-")

    def test_generate_pdf_with_many_errors(
        self, pdf_generator: PDFGeneratorService
    ) -> None:
        """Test PDF generation with many errors and warnings."""
        report = ValidationReport(
            filename="errors.ifc",
            timestamp="2024-01-15T10:30:00",
            ifc_schema="IFC4X3_ADD2",
            overall_compliance=0.2,
            required_compliance=0.3,
            categories=[],
            coordinate_system=CoordinateInfo(valid=False),
            warnings=[f"Warning {i}" for i in range(20)],
            errors=[f"Error {i}" for i in range(20)],
        )
        pdf_bytes = pdf_generator.generate(report)
        assert isinstance(pdf_bytes, bytes)
        assert pdf_bytes.startswith(b"%PDF-")

    def test_generate_pdf_with_special_characters(
        self, pdf_generator: PDFGeneratorService
    ) -> None:
        """Test PDF generation with Finnish special characters."""
        report = ValidationReport(
            filename="äöå_test.ifc",
            timestamp="2024-01-15T10:30:00",
            ifc_schema="IFC4X3_ADD2",
            overall_compliance=0.5,
            required_compliance=0.6,
            categories=[
                CategoryValidation(
                    id="test",
                    name="Täälläkin äöå",
                    name_en="Test Category",
                    icon="test",
                    compliance_percentage=50.0,
                    required_compliance=60.0,
                    fields=[
                        FieldValidation(
                            field_name="Ääkkönen",
                            field_name_en="Finnish chars",
                            ifc_entity="TestEntity",
                            ifc_property="Test.Property",
                            is_required=True,
                            is_present=True,
                            value="Mökkikylä",
                            status=ValidationStatus.VALID,
                        ),
                    ],
                ),
            ],
            coordinate_system=CoordinateInfo(valid=False),
            warnings=["Varoitus äöå merkeillä"],
            errors=["Virhe äöå merkeillä"],
        )
        pdf_bytes = pdf_generator.generate(report)
        assert isinstance(pdf_bytes, bytes)
        assert pdf_bytes.startswith(b"%PDF-")

    def test_load_translations(self, pdf_generator: PDFGeneratorService) -> None:
        """Test that translations are loaded correctly."""
        pdf_generator.language = "fi"
        fi_trans = pdf_generator._load_translations()
        
        pdf_generator.language = "en"
        en_trans = pdf_generator._load_translations()

        assert "report" in fi_trans
        assert "report" in en_trans
        # Assuming different titles
        assert fi_trans.get("report", {}).get("title") != en_trans.get("report", {}).get("title")

    def test_invalid_language_defaults_to_finnish(
        self, pdf_generator: PDFGeneratorService, sample_report: ValidationReport
    ) -> None:
        """Test that invalid language defaults to Finnish."""
        # Should not raise, but use Finnish translations
        pdf_generator.language = "invalid"
        pdf_bytes = pdf_generator.generate(sample_report)
        assert isinstance(pdf_bytes, bytes)
