"""Validation service for IFC compliance checking."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)

from app.schemas.validation import (
    CategoryValidation,
    CoordinateInfo,
    FieldValidation,
    ValidationReport,
    ValidationStatus,
)
from app.services.ifc_parser import IFCParserService

# --- Mapping File Schemas ---

class MappingField(BaseModel):
    id: Optional[str] = None
    name_fi: Optional[str] = None
    name_en: Optional[str] = None
    ifc_entity: Optional[str] = None
    ifc_property: Optional[str] = None
    required: bool = False
    default_value: Optional[str] = None

class MappingCategory(BaseModel):
    name_fi: str
    name_en: str
    icon: Optional[str] = "folder"
    ifc_entity: Optional[str] = None
    fields: List[MappingField] = []

class MappingFile(BaseModel):
    categories: Dict[str, MappingCategory] = {}

# ----------------------------


class ValidatorService:
    """Service for validating IFC files against Finnish building permit requirements."""

    # Localized messages for error/warning reporting
    MESSAGES = {
        "fi": {
            "missing": "puuttuu",
            "optional_missing": "(valinnainen) puuttuu",
        },
        "en": {
            "missing": "is missing",
            "optional_missing": "(optional) is missing",
        },
    }

    def _get_localized_name(self, name_fi: str, name_en: str) -> str:
        """Get the localized field name based on current language."""
        return name_en if self.language == "en" else name_fi

    def _get_localized_category_name(self, cat_id: str, name_fi: str, name_en: str) -> str:
        """Get the localized category name based on current language."""
        return name_en if self.language == "en" else name_fi

    def __init__(self, language: str = "fi") -> None:
        """Initialize the validator with mapping files.

        Args:
            language: Language code for messages ('fi' or 'en').
        """
        self.language = language if language in self.MESSAGES else "fi"
        self.mappings = self._load_mappings()

    def _load_mappings(self) -> Dict[str, Any]:
        """Load YAML mapping files.

        Returns:
            Dictionary containing liite1 and liite2 mappings.
        """
        mappings_dir = Path(__file__).parent.parent / "mappings"

        liite1_path = mappings_dir / "liite1.yaml"
        liite2_path = mappings_dir / "liite2.yaml"

        mappings: Dict[str, Any] = {"liite1": {}, "liite2": {}}

        if liite1_path.exists():
            with open(liite1_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                try:
                    # Validate against schema
                    validated = MappingFile(**data)
                    mappings["liite1"] = validated.model_dump(mode='json')
                except ValidationError as e:
                    logger.error(f"Validation error in liite1.yaml: {e}")
                    # Fallback to empty or raw data? Security-wise safe to fail or stick to validated data.
                    # We will use raw data for now but log error to unblock, or ideally fail hard in dev.
                    # For this fix, let's log and use empty to prevent runtime crashes if structure is totally wrong
                    mappings["liite1"] = {}

        if liite2_path.exists():
            with open(liite2_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                try:
                     validated = MappingFile(**data)
                     mappings["liite2"] = validated.model_dump(mode='json')
                except ValidationError as e:
                     logger.error(f"Validation error in liite2.yaml: {e}")
                     mappings["liite2"] = {}

        return mappings

    def validate(self, parser: IFCParserService, filename: str) -> ValidationReport:
        """Run full validation and return report.

        Args:
            parser: IFC parser service with loaded model.
            filename: Original filename of the IFC file.

        Returns:
            Complete validation report.
        """
        categories: List[CategoryValidation] = []
        all_errors: List[str] = []
        all_warnings: List[str] = []

        # Get localized messages for the selected language
        msgs = self.MESSAGES[self.language]

        # Validate each category from Liite 1
        for cat_id, cat_def in self.mappings["liite1"].get("categories", {}).items():
            category_result = self._validate_category(parser, cat_id, cat_def)
            categories.append(category_result)

            # Collect errors and warnings using correct language
            cat_name = self._get_localized_category_name(
                cat_id, category_result.name, category_result.name_en
            )
            for field in category_result.fields:
                field_name = self._get_localized_name(
                    field.field_name, field.field_name_en
                )
                if field.status == ValidationStatus.MISSING and field.is_required:
                    all_errors.append(
                        f"{cat_name}: {field_name} {msgs['missing']}"
                    )
                elif field.status == ValidationStatus.WARNING:
                    all_warnings.append(
                        f"{cat_name}: {field_name} {msgs['optional_missing']}"
                    )

        # Validate each category from Liite 2
        for cat_id, cat_def in self.mappings["liite2"].get("categories", {}).items():
            category_result = self._validate_category(parser, cat_id, cat_def)
            categories.append(category_result)

            # Collect errors and warnings using correct language
            cat_name = self._get_localized_category_name(
                cat_id, category_result.name, category_result.name_en
            )
            for field in category_result.fields:
                field_name = self._get_localized_name(
                    field.field_name, field.field_name_en
                )
                if field.status == ValidationStatus.MISSING and field.is_required:
                    all_errors.append(
                        f"{cat_name}: {field_name} {msgs['missing']}"
                    )
                elif field.status == ValidationStatus.WARNING:
                    all_warnings.append(
                        f"{cat_name}: {field_name} {msgs['optional_missing']}"
                    )

        # Calculate overall compliance
        total_fields = sum(len(c.fields) for c in categories)
        valid_fields = sum(
            sum(1 for f in c.fields if f.status == ValidationStatus.VALID)
            for c in categories
        )

        total_required = sum(
            sum(1 for f in c.fields if f.is_required) for c in categories
        )
        valid_required = sum(
            sum(
                1
                for f in c.fields
                if f.is_required and f.status == ValidationStatus.VALID
            )
            for c in categories
        )

        overall_compliance = valid_fields / total_fields if total_fields > 0 else 0
        required_compliance = (
            valid_required / total_required if total_required > 0 else 0
        )

        # Get coordinate info
        coordinate_info = self._extract_coordinates(parser)

        return ValidationReport(
            filename=filename,
            timestamp=datetime.utcnow(),
            ifc_schema=parser.get_schema_version(),
            overall_compliance=round(overall_compliance, 4),
            required_compliance=round(required_compliance, 4),
            categories=categories,
            coordinate_system=coordinate_info,
            warnings=all_warnings,
            errors=all_errors,
        )

    def _validate_category(
        self, parser: IFCParserService, cat_id: str, cat_def: Dict[str, Any]
    ) -> CategoryValidation:
        """Validate a single category.

        Args:
            parser: IFC parser service.
            cat_id: Category identifier.
            cat_def: Category definition from YAML.

        Returns:
            Category validation result.
        """
        fields: List[FieldValidation] = []

        for field_def in cat_def.get("fields", []):
            field_result = self._validate_field(parser, cat_def, field_def)
            fields.append(field_result)

        # Calculate category compliance
        total = len(fields)
        valid = sum(1 for f in fields if f.status == ValidationStatus.VALID)
        required = [f for f in fields if f.is_required]
        valid_required = sum(1 for f in required if f.status == ValidationStatus.VALID)

        return CategoryValidation(
            id=cat_id,
            name=cat_def.get("name_fi", cat_id),
            name_en=cat_def.get("name_en", cat_id),
            icon=cat_def.get("icon", "folder"),
            fields=fields,
            compliance_percentage=round(valid / total * 100, 1) if total > 0 else 0,
            required_compliance=(
                round(valid_required / len(required) * 100, 1) if required else 100
            ),
        )

    def _validate_field(
        self,
        parser: IFCParserService,
        cat_def: Dict[str, Any],
        field_def: Dict[str, Any],
    ) -> FieldValidation:
        """Validate a single field.

        Args:
            parser: IFC parser service.
            cat_def: Category definition.
            field_def: Field definition from YAML.

        Returns:
            Field validation result.
        """
        # Resolve ifc_entity with fallback to category level
        # handle None from Pydantic model_dump
        ifc_entity = field_def.get("ifc_entity") 
        if not ifc_entity:
            ifc_entity = cat_def.get("ifc_entity")
        if not ifc_entity:
            ifc_entity = ""

        ifc_property = field_def.get("ifc_property", "")

        # Extract value from IFC
        value = self._extract_property(parser, ifc_entity, ifc_property)

        # If no value found, check for default value
        if value is None or str(value).strip() == "":
            default_value = field_def.get("default_value")
            if default_value:
                value = default_value

        # Consider empty strings or whitespace-only strings as not present
        is_present = value is not None and str(value).strip() != ""
        is_required = field_def.get("required", False)

        if is_present:
            status = ValidationStatus.VALID
        elif is_required:
            status = ValidationStatus.MISSING
        else:
            status = ValidationStatus.WARNING

        return FieldValidation(
            field_name=field_def.get("name_fi", field_def.get("id", "")),
            field_name_en=field_def.get("name_en", field_def.get("id", "")),
            is_required=is_required,
            is_present=is_present,
            value=value,
            ifc_entity=ifc_entity or "",
            ifc_property=ifc_property,
            status=status,
        )

    def _extract_property(
        self, parser: IFCParserService, entity_type: str, property_path: str
    ) -> Optional[Any]:
        """Extract property value from IFC entity.

        Supports multiple paths separated by '|'. Returns the first non-None value found.
        For entity types that can have multiple instances (e.g., IfcSpace), searches all
        entities if the property is not found on the first one.
        """
        if "|" in property_path:
            paths = property_path.split("|")
            for path in paths:
                val = self._extract_property(parser, entity_type, path.strip())
                if val is not None and str(val).strip() != "":
                    return val
            return None

        if not entity_type or not property_path or not parser.model:
            return None

        try:
            # Check if we should search all entities of this type
            # This is needed for cases like shelter (väestönsuoja) where the properties
            # are on a specific IfcSpace, not the first one
            should_search_all = self._should_search_all_entities(entity_type, property_path)

            if should_search_all:
                # Search all entities of this type for the property
                entities = parser.model.by_type(entity_type)
                for entity in entities:
                    val = self._extract_property_from_entity(parser, entity, property_path)
                    if val is not None and str(val).strip() != "":
                        return val
                return None
            else:
                # Get first entity - handle special cases
                entity = self._get_entity(parser, entity_type)
                if entity is None:
                    return None
                return self._extract_property_from_entity(parser, entity, property_path)

        except (AttributeError, KeyError, TypeError) as e:
            # Expected errors when property doesn't exist
            logger.debug(f"Property not found: {entity_type}.{property_path}: {e}")
            return None
        except Exception as e:
            # Unexpected errors - log for debugging
            logger.warning(f"Unexpected error extracting {entity_type}.{property_path}: {e}")
            return None

    def _should_search_all_entities(self, entity_type: str, property_path: str) -> bool:
        """Determine if we should search all entities of a type for a property.

        This is needed for cases where properties might be on a specific entity
        instance, not the first one (e.g., shelter properties on a specific IfcSpace).
        """
        # Search all IfcSpace entities for Finnish shelter property sets
        if entity_type == "IfcSpace" and "FI_VSS" in property_path:
            return True
        return False

    def _extract_property_from_entity(
        self, parser: IFCParserService, entity: Any, property_path: str
    ) -> Optional[Any]:
        """Extract property value from a specific IFC entity.

        Args:
            parser: IFC parser service.
            entity: The IFC entity to extract from.
            property_path: Property path (e.g., "Pset_Common.Status" or "IfcWall.Name").

        Returns:
            Property value or None if not found.
        """
        if entity is None or not property_path:
            return None

        # Check if it's a direct attribute (e.g., IfcBuilding.Name)
        if "." in property_path:
            parts = property_path.split(".")
            # Validate parts has at least 2 elements for property set access
            if len(parts) < 2:
                return None
            if parts[0].startswith("Ifc"):
                # Direct attribute access
                attr_name = parts[-1]
                if hasattr(entity, attr_name):
                    val = getattr(entity, attr_name)
                    return val if val is not None else None
            elif parts[0].startswith("Qto_"):
                # Quantity set
                return parser.get_quantity_value(entity, parts[0], parts[1])
            else:
                # Generic Property Set (Standard or Custom/Localized like FI_*)
                return parser.get_pset_value(entity, parts[0], parts[1])

        return None

    def _get_entity(
        self, parser: IFCParserService, entity_type: str
    ) -> Optional[Any]:
        """Get an entity from the IFC model.

        Args:
            parser: IFC parser service.
            entity_type: IFC entity type.

        Returns:
            Entity or None if not found.
        """
        if not parser.model:
            return None

        # Map entity types to parser methods or direct lookup
        if entity_type == "IfcProject":
            return parser.get_project()
        elif entity_type == "IfcSite":
            return parser.get_site()
        elif entity_type == "IfcBuilding":
            return parser.get_building()
        elif entity_type == "IfcBuildingStorey":
            storeys = parser.get_building_storeys()
            return storeys[0] if storeys else None
        elif entity_type == "IfcOrganization":
            # Get from owner history
            project = parser.get_project()
            if project and hasattr(project, "OwnerHistory") and project.OwnerHistory:
                owner_history = project.OwnerHistory
                if hasattr(owner_history, "OwningUser") and owner_history.OwningUser:
                    person_org = owner_history.OwningUser
                    if hasattr(person_org, "TheOrganization"):
                        return person_org.TheOrganization
            return None
        elif entity_type == "IfcPerson":
            # Get from owner history
            project = parser.get_project()
            if project and hasattr(project, "OwnerHistory") and project.OwnerHistory:
                owner_history = project.OwnerHistory
                if hasattr(owner_history, "OwningUser") and owner_history.OwningUser:
                    person_org = owner_history.OwningUser
                    if hasattr(person_org, "ThePerson"):
                        return person_org.ThePerson
            return None
        elif entity_type == "IfcPostalAddress":
            # Get from building
            building = parser.get_building()
            if building and hasattr(building, "BuildingAddress"):
                return building.BuildingAddress
            return None
        elif entity_type == "IfcRoof":
            # First try IfcRoof entities
            entities = parser.model.by_type("IfcRoof")
            if entities:
                return entities[0]
            # Fallback: check IfcSlab entities with PredefinedType=ROOF
            # (Some models use IfcSlab with ROOF type instead of IfcRoof)
            slabs = parser.model.by_type("IfcSlab")
            for slab in slabs:
                if getattr(slab, "PredefinedType", None) == "ROOF":
                    return slab
            return None
        else:
            # Generic lookup
            entities = parser.model.by_type(entity_type)
            return entities[0] if entities else None

    def _extract_coordinates(self, parser: IFCParserService) -> CoordinateInfo:
        """Extract coordinate system information.

        Args:
            parser: IFC parser service.

        Returns:
            Coordinate system information.
        """
        try:
            site = parser.get_site()
            if not site:
                return CoordinateInfo(valid=False)

            # Check for coordinate reference in project
            project = parser.get_project()
            system = None

            if project:
                for context in project.RepresentationContexts or []:
                    if context.is_a("IfcGeometricRepresentationContext"):
                        if hasattr(context, "HasCoordinateOperation"):
                            crs_ops = context.HasCoordinateOperation
                            if crs_ops:
                                crs = crs_ops[0] if isinstance(crs_ops, tuple) else crs_ops
                                if hasattr(crs, "TargetCRS") and crs.TargetCRS:
                                    if hasattr(crs.TargetCRS, "Name"):
                                        system = str(crs.TargetCRS.Name)

            return CoordinateInfo(
                system=system,
                easting=None,
                northing=None,
                elevation_system="N2000",  # Common in Finland
                valid=system is not None and "ETRS" in str(system or ""),
            )

        except (AttributeError, TypeError) as e:
            # Expected errors when coordinate info doesn't exist
            logger.debug(f"Coordinate info not found: {e}")
            return CoordinateInfo(valid=False)
        except Exception as e:
            # Unexpected errors - log for debugging
            logger.warning(f"Unexpected error extracting coordinates: {e}")
            return CoordinateInfo(valid=False)
