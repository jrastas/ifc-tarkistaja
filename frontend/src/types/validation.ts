/**
 * Types for IFC validation results.
 */

export type ValidationStatus = 'valid' | 'missing' | 'invalid' | 'warning';

export interface FieldValidation {
  field_name: string;
  field_name_en: string;
  is_required: boolean;
  is_present: boolean;
  value: unknown;
  ifc_entity: string;
  ifc_property: string;
  status: ValidationStatus;
}

export interface CategoryValidation {
  id: string;
  name: string;
  name_en: string;
  icon: string;
  fields: FieldValidation[];
  compliance_percentage: number;
  required_compliance: number;
}

export interface CoordinateInfo {
  system: string | null;
  easting: number | null;
  northing: number | null;
  elevation_system: string | null;
  valid: boolean;
}

export interface ValidationReport {
  filename: string;
  timestamp: string;
  ifc_schema: string;
  overall_compliance: number;
  required_compliance: number;
  categories: CategoryValidation[];
  coordinate_system: CoordinateInfo;
  warnings: string[];
  errors: string[];
}

export interface ValidationResponse {
  success: boolean;
  report: ValidationReport | null;
  error: string | null;
}
