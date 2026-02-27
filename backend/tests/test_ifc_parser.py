"""Tests for IFC parser service."""

from pathlib import Path

import pytest

from app.services.ifc_parser import IFCParserService


class TestIFCParserService:
    """Tests for IFCParserService."""

    def test_open_valid_file(self, sample_ifc_path: Path) -> None:
        """Test opening a valid IFC file."""
        parser = IFCParserService()
        result = parser.open_file(str(sample_ifc_path))
        assert result is True
        assert parser.model is not None

    def test_open_invalid_file(self, tmp_path: Path) -> None:
        """Test opening an invalid file raises ValueError."""
        invalid_file = tmp_path / "invalid.ifc"
        invalid_file.write_text("not an ifc file")

        parser = IFCParserService()
        with pytest.raises(ValueError, match="Failed to open IFC file"):
            parser.open_file(str(invalid_file))

    def test_get_schema_version(self, sample_ifc_path: Path) -> None:
        """Test extracting schema version."""
        parser = IFCParserService()
        parser.open_file(str(sample_ifc_path))
        schema = parser.get_schema_version()
        assert schema.startswith("IFC4X3")

    def test_get_schema_version_no_file(self) -> None:
        """Test getting schema version without loading file raises ValueError."""
        parser = IFCParserService()
        with pytest.raises(ValueError, match="No IFC file loaded"):
            parser.get_schema_version()

    def test_get_project(self, sample_ifc_path: Path) -> None:
        """Test extracting IfcProject entity."""
        parser = IFCParserService()
        parser.open_file(str(sample_ifc_path))
        project = parser.get_project()
        assert project is not None
        assert project.Name == "Test Project"

    def test_get_site(self, sample_ifc_path: Path) -> None:
        """Test extracting IfcSite entity."""
        parser = IFCParserService()
        parser.open_file(str(sample_ifc_path))
        site = parser.get_site()
        assert site is not None
        assert site.Name == "Test Site"

    def test_get_building(self, sample_ifc_path: Path) -> None:
        """Test extracting IfcBuilding entity."""
        parser = IFCParserService()
        parser.open_file(str(sample_ifc_path))
        building = parser.get_building()
        assert building is not None
        assert building.Name == "Test Building"

    def test_get_building_storeys(self, sample_ifc_path: Path) -> None:
        """Test extracting IfcBuildingStorey entities."""
        parser = IFCParserService()
        parser.open_file(str(sample_ifc_path))
        storeys = parser.get_building_storeys()
        assert len(storeys) == 1
        assert storeys[0].Name == "First Floor"

    def test_get_pset_value(self, sample_ifc_path: Path) -> None:
        """Test extracting property set value."""
        parser = IFCParserService()
        parser.open_file(str(sample_ifc_path))
        building = parser.get_building()

        num_storeys = parser.get_pset_value(
            building, "Pset_BuildingCommon", "NumberOfStoreys"
        )
        assert num_storeys == 5

        occupancy = parser.get_pset_value(
            building, "Pset_BuildingCommon", "OccupancyType"
        )
        assert occupancy == "Office"

    def test_get_quantity_value(self, sample_ifc_path: Path) -> None:
        """Test extracting quantity value."""
        parser = IFCParserService()
        parser.open_file(str(sample_ifc_path))
        building = parser.get_building()

        area = parser.get_quantity_value(
            building, "Qto_BuildingBaseQuantities", "GrossFloorArea"
        )
        assert area == 4500.0

        volume = parser.get_quantity_value(
            building, "Qto_BuildingBaseQuantities", "GrossVolume"
        )
        assert volume == 18000.0
