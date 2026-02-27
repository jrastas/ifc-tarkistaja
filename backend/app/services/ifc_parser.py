"""IFC file parsing service using ifcopenshell."""

from typing import Any, Optional

import ifcopenshell


class IFCParserService:
    """Service for parsing IFC files and extracting entities."""

    def __init__(self) -> None:
        """Initialize the parser service."""
        self.model: Optional[ifcopenshell.file] = None

    def open_file(self, file_path: str) -> bool:
        """Open IFC file and store model reference.

        Args:
            file_path: Path to the IFC file.

        Returns:
            True if file was opened successfully.

        Raises:
            ValueError: If file cannot be opened.
        """
        try:
            self.model = ifcopenshell.open(file_path)
            return True
        except Exception as e:
            raise ValueError(f"Failed to open IFC file: {str(e)}")

    def get_schema_version(self) -> str:
        """Get IFC schema version.

        Returns:
            Schema version string (e.g., 'IFC4X3_ADD2').

        Raises:
            ValueError: If no IFC file is loaded.
        """
        if not self.model:
            raise ValueError("No IFC file loaded")
        return self.model.schema

    def get_project(self) -> Optional[Any]:
        """Get IfcProject entity.

        Returns:
            The first IfcProject entity or None if not found.
        """
        if not self.model:
            return None
        projects = self.model.by_type("IfcProject")
        return projects[0] if projects else None

    def get_site(self) -> Optional[Any]:
        """Get IfcSite entity.

        Returns:
            The first IfcSite entity or None if not found.
        """
        if not self.model:
            return None
        sites = self.model.by_type("IfcSite")
        return sites[0] if sites else None

    def get_building(self) -> Optional[Any]:
        """Get IfcBuilding entity.

        Returns:
            The first IfcBuilding entity or None if not found.
        """
        if not self.model:
            return None
        buildings = self.model.by_type("IfcBuilding")
        return buildings[0] if buildings else None

    def get_building_storeys(self) -> list:
        """Get all IfcBuildingStorey entities.

        Returns:
            List of IfcBuildingStorey entities.
        """
        if not self.model:
            return []
        return self.model.by_type("IfcBuildingStorey")

    def get_pset_value(
        self, entity: Any, pset_name: str, prop_name: str
    ) -> Optional[Any]:
        """Get property value from a property set.

        Checks both the entity's direct property sets and its type definition's
        property sets (for elements with types like IfcWallType, IfcTransportElementType, etc.).

        Args:
            entity: The IFC entity to get the property from.
            pset_name: Name of the property set (e.g., 'Pset_BuildingCommon').
            prop_name: Name of the property within the set.

        Returns:
            The property value or None if not found.
        """
        if not entity:
            return None

        # First, check the entity's direct property sets
        for rel in getattr(entity, "IsDefinedBy", []):
            if rel.is_a("IfcRelDefinesByProperties"):
                pset = rel.RelatingPropertyDefinition
                if pset.is_a("IfcPropertySet"):
                    if pset.Name == pset_name:
                        for prop in pset.HasProperties:
                            if prop.Name == prop_name:
                                if hasattr(prop, "NominalValue") and prop.NominalValue:
                                    return prop.NominalValue.wrappedValue

        # If not found, check the entity's type definition (e.g., IfcTransportElementType)
        # Properties on the type apply to all instances of that type
        # IFC4 uses IsTypedBy relationship for type definitions
        for rel in getattr(entity, "IsTypedBy", []):
            if rel.is_a("IfcRelDefinesByType"):
                type_def = rel.RelatingType
                if type_def and hasattr(type_def, "HasPropertySets"):
                    for pset in type_def.HasPropertySets or []:
                        if pset.is_a("IfcPropertySet") and pset.Name == pset_name:
                            for prop in pset.HasProperties:
                                if prop.Name == prop_name:
                                    if hasattr(prop, "NominalValue") and prop.NominalValue:
                                        return prop.NominalValue.wrappedValue

        return None

    def get_quantity_value(
        self, entity: Any, qto_name: str, quantity_name: str
    ) -> Optional[Any]:
        """Get quantity value from a quantity set.

        Args:
            entity: The IFC entity to get the quantity from.
            qto_name: Name of the quantity set (e.g., 'Qto_BuildingBaseQuantities').
            quantity_name: Name of the quantity within the set.

        Returns:
            The quantity value or None if not found.
        """
        if not entity:
            return None

        for rel in getattr(entity, "IsDefinedBy", []):
            if rel.is_a("IfcRelDefinesByProperties"):
                qto = rel.RelatingPropertyDefinition
                if qto.is_a("IfcElementQuantity") and qto.Name == qto_name:
                    for quantity in qto.Quantities:
                        if quantity.Name == quantity_name:
                            # Handle different quantity types
                            if quantity.is_a("IfcQuantityArea"):
                                return quantity.AreaValue
                            elif quantity.is_a("IfcQuantityLength"):
                                return quantity.LengthValue
                            elif quantity.is_a("IfcQuantityVolume"):
                                return quantity.VolumeValue
                            elif quantity.is_a("IfcQuantityCount"):
                                return quantity.CountValue
        return None
