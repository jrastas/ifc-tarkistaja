"""Tests for validator service."""

from pathlib import Path

import pytest

from app.schemas.validation import ValidationStatus
from app.services.ifc_parser import IFCParserService
from app.services.validator import ValidatorService


class TestValidatorService:
    """Tests for ValidatorService."""

    @pytest.fixture
    def validator(self) -> ValidatorService:
        """Create a validator service instance."""
        return ValidatorService()

    @pytest.fixture
    def parser_with_model(self, sample_ifc_path: Path) -> IFCParserService:
        """Create a parser with loaded model."""
        parser = IFCParserService()
        parser.open_file(str(sample_ifc_path))
        return parser

    def test_load_mappings(self, validator: ValidatorService) -> None:
        """Test that YAML mapping files load correctly."""
        assert "liite1" in validator.mappings
        assert "liite2" in validator.mappings
        assert "categories" in validator.mappings["liite1"]
        assert "categories" in validator.mappings["liite2"]

    def test_liite1_has_categories(self, validator: ValidatorService) -> None:
        """Test that Liite 1 has expected categories."""
        categories = validator.mappings["liite1"]["categories"]
        expected_categories = [
            "rakennuksen_tietomalli",
            "suunnittelija",
            "rakennuspaikka",
            "rakennuskohde",
            "ulkokuoren_tiedot",
        ]
        for cat in expected_categories:
            assert cat in categories, f"Missing category: {cat}"

    def test_liite2_has_categories(self, validator: ValidatorService) -> None:
        """Test that Liite 2 has expected categories."""
        categories = validator.mappings["liite2"]["categories"]
        expected_categories = ["huoneisto", "kerros", "seina", "ovi", "ikkuna"]
        for cat in expected_categories:
            assert cat in categories, f"Missing category: {cat}"

    def test_validate_returns_report(
        self, validator: ValidatorService, parser_with_model: IFCParserService
    ) -> None:
        """Test that validate returns a validation report."""
        report = validator.validate(parser_with_model, "test.ifc")

        assert report.filename == "test.ifc"
        assert report.ifc_schema.startswith("IFC4X3")
        assert 0 <= report.overall_compliance <= 1
        assert 0 <= report.required_compliance <= 1
        assert len(report.categories) > 0

    def test_validate_extracts_site_name(
        self, validator: ValidatorService, parser_with_model: IFCParserService
    ) -> None:
        """Test that site name is correctly extracted."""
        report = validator.validate(parser_with_model, "test.ifc")

        # Find rakennuspaikka category
        site_category = next(
            (c for c in report.categories if c.id == "rakennuspaikka"), None
        )
        assert site_category is not None

        # Find name field
        name_field = next(
            (f for f in site_category.fields if f.field_name == "Nimi"), None
        )
        assert name_field is not None
        assert name_field.status == ValidationStatus.VALID
        assert name_field.value == "Test Site"

    def test_validate_extracts_building_name(
        self, validator: ValidatorService, parser_with_model: IFCParserService
    ) -> None:
        """Test that building name is correctly extracted."""
        report = validator.validate(parser_with_model, "test.ifc")

        # Find rakennuskohde category
        building_category = next(
            (c for c in report.categories if c.id == "rakennuskohde"), None
        )
        assert building_category is not None

        # Find name field
        name_field = next(
            (f for f in building_category.fields if f.field_name == "Nimi"), None
        )
        assert name_field is not None
        assert name_field.status == ValidationStatus.VALID
        assert name_field.value == "Test Building"

    def test_validate_extracts_pset_values(
        self, validator: ValidatorService, parser_with_model: IFCParserService
    ) -> None:
        """Test that property set values are correctly extracted."""
        report = validator.validate(parser_with_model, "test.ifc")

        # Find rakennuspaikka category
        site_category = next(
            (c for c in report.categories if c.id == "rakennuspaikka"), None
        )
        assert site_category is not None

        # Find kiinteistötunnus field (from Pset_SiteCommon.LandTitleNumber)
        property_id_field = next(
            (f for f in site_category.fields if f.field_name == "Kiinteistötunnus"),
            None,
        )
        assert property_id_field is not None
        assert property_id_field.status == ValidationStatus.VALID
        assert property_id_field.value == "091-001-0001-0001"

    def test_validate_extracts_quantity_values(
        self, validator: ValidatorService, parser_with_model: IFCParserService
    ) -> None:
        """Test that quantity set values are correctly extracted."""
        report = validator.validate(parser_with_model, "test.ifc")

        # Find ulkokuori category
        envelope_category = next(
            (c for c in report.categories if c.id == "ulkokuoren_tiedot"), None
        )
        assert envelope_category is not None

        # Find kokonaisala field (from Qto_BuildingBaseQuantities.GrossFloorArea)
        area_field = next(
            (f for f in envelope_category.fields if f.field_name == "Kokonaisala"),
            None,
        )
        assert area_field is not None
        assert area_field.status == ValidationStatus.VALID
        assert area_field.value == 4500.0

    def test_validate_marks_missing_required_fields(
        self, validator: ValidatorService, parser_with_model: IFCParserService
    ) -> None:
        """Test that missing required fields are marked correctly."""
        report = validator.validate(parser_with_model, "test.ifc")

        # There should be some errors for missing required fields
        assert len(report.errors) > 0

        # Check that errors mention "puuttuu" (Finnish for "missing")
        assert any("puuttuu" in error for error in report.errors)

    def test_validate_marks_missing_optional_fields_as_warning(
        self, validator: ValidatorService, parser_with_model: IFCParserService
    ) -> None:
        """Test that missing optional fields get warning status."""
        report = validator.validate(parser_with_model, "test.ifc")

        # Find a category with optional fields
        any_warning = False
        for category in report.categories:
            for field in category.fields:
                if not field.is_required and not field.is_present:
                    assert field.status == ValidationStatus.WARNING
                    any_warning = True

        assert any_warning, "Should have at least one warning for optional fields"

    def test_compliance_calculation(
        self, validator: ValidatorService, parser_with_model: IFCParserService
    ) -> None:
        """Test that compliance percentages are calculated correctly."""
        report = validator.validate(parser_with_model, "test.ifc")

        # Overall compliance should be between 0 and 1
        assert 0 <= report.overall_compliance <= 1

        # Required compliance should be between 0 and 1
        assert 0 <= report.required_compliance <= 1

        # Each category should have compliance percentages
        for category in report.categories:
            assert 0 <= category.compliance_percentage <= 100
            assert 0 <= category.required_compliance <= 100

    def test_category_has_required_fields(
        self, validator: ValidatorService
    ) -> None:
        """Test that categories in mappings have fields marked as required."""
        liite1_categories = validator.mappings["liite1"]["categories"]

        # rakennuspaikka should have required fields
        site_cat = liite1_categories.get("rakennuspaikka", {})
        fields = site_cat.get("fields", [])

        required_fields = [f for f in fields if f.get("required", False)]
        assert len(required_fields) > 0, "rakennuspaikka should have required fields"
