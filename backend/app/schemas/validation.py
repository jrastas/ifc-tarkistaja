"""Pydantic models for validation requests and responses."""

from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, field_serializer, Field, field_validator


class ValidationStatus(str, Enum):
    """Status of a field validation."""
    VALID = "valid"
    MISSING = "missing"
    INVALID = "invalid"
    WARNING = "warning"


class FieldValidation(BaseModel):
    """Validation result for a single field."""
    field_name: str
    field_name_en: str
    is_required: bool
    is_present: bool
    value: Optional[Any] = None
    ifc_entity: str
    ifc_property: str
    status: ValidationStatus


class CategoryValidation(BaseModel):
    """Validation results for a category of fields."""
    id: str
    name: str
    name_en: str
    icon: str
    fields: List[FieldValidation]
    compliance_percentage: float
    required_compliance: float


class CoordinateInfo(BaseModel):
    """Coordinate system information from the IFC file."""
    system: Optional[str] = None
    easting: Optional[float] = None
    northing: Optional[float] = None
    elevation_system: Optional[str] = None
    valid: bool = False


class ValidationReport(BaseModel):
    """Complete validation report for an IFC file."""
    filename: str
    timestamp: datetime
    ifc_schema: str
    overall_compliance: float
    required_compliance: float
    categories: List[CategoryValidation]
    coordinate_system: CoordinateInfo
    warnings: List[str] = Field(max_length=2000)
    errors: List[str] = Field(max_length=2000)

    @field_validator('warnings', 'errors')
    def validate_issue_length(cls, v):
        truncated = []
        for item in v:
            if len(item) > 1000:
                # Truncate instead of raising to prevent 500 errors
                truncated.append(item[:997] + "...")
            else:
                truncated.append(item)
        return truncated

    @field_serializer('timestamp')
    def serialize_timestamp(self, value: datetime) -> str:
        """Serialize timestamp to ISO 8601 string for consistent API contract."""
        return value.isoformat()


class ValidationResponse(BaseModel):
    """API response for validation requests."""
    success: bool
    report: Optional[ValidationReport] = None
    error: Optional[str] = None
