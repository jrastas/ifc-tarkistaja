/**
 * Tests for app store.
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { useAppStore } from './appStore';

describe('appStore', () => {
  beforeEach(() => {
    // Reset store state before each test
    useAppStore.setState({
      file: null,
      isValidating: false,
      validationReport: null,
      error: null,
      viewMode: 'required',
    });
  });

  it('sets file correctly', () => {
    const file = new File(['content'], 'test.ifc', { type: 'application/x-step' });
    useAppStore.getState().setFile(file);
    expect(useAppStore.getState().file).toBe(file);
  });

  it('clears error when setting file', () => {
    useAppStore.setState({ error: 'Previous error' });
    const file = new File(['content'], 'test.ifc', { type: 'application/x-step' });
    useAppStore.getState().setFile(file);
    expect(useAppStore.getState().error).toBeNull();
  });

  it('sets validating state', () => {
    useAppStore.getState().setValidating(true);
    expect(useAppStore.getState().isValidating).toBe(true);

    useAppStore.getState().setValidating(false);
    expect(useAppStore.getState().isValidating).toBe(false);
  });

  it('sets validation report', () => {
    const mockReport = {
      filename: 'test.ifc',
      timestamp: '2024-01-15T10:30:00',
      ifc_schema: 'IFC4X3_ADD2',
      overall_compliance: 0.75,
      required_compliance: 0.85,
      categories: [],
      coordinate_system: {
        system: 'EPSG:3879',
        easting: null,
        northing: null,
        elevation_system: null,
        valid: true,
      },
      warnings: [],
      errors: [],
    };

    useAppStore.getState().setValidationReport(mockReport);
    expect(useAppStore.getState().validationReport).toEqual(mockReport);
  });

  it('sets error', () => {
    useAppStore.getState().setError('Test error message');
    expect(useAppStore.getState().error).toBe('Test error message');
  });

  it('toggles view mode', () => {
    expect(useAppStore.getState().viewMode).toBe('required');

    useAppStore.getState().setViewMode('all');
    expect(useAppStore.getState().viewMode).toBe('all');

    useAppStore.getState().setViewMode('required');
    expect(useAppStore.getState().viewMode).toBe('required');
  });

  it('resets state correctly', () => {
    // Set some state
    const file = new File(['content'], 'test.ifc', { type: 'application/x-step' });
    useAppStore.setState({
      file,
      validationReport: {
        filename: 'test.ifc',
        timestamp: '2024-01-15T10:30:00',
        ifc_schema: 'IFC4X3_ADD2',
        overall_compliance: 0.75,
        required_compliance: 0.85,
        categories: [],
        coordinate_system: {
          system: 'EPSG:3879',
          easting: null,
          northing: null,
          elevation_system: null,
          valid: true,
        },
        warnings: [],
        errors: [],
      },
      error: 'Some error',
      viewMode: 'all',
    });

    // Reset
    useAppStore.getState().reset();

    // Verify reset
    expect(useAppStore.getState().file).toBeNull();
    expect(useAppStore.getState().validationReport).toBeNull();
    expect(useAppStore.getState().error).toBeNull();
    expect(useAppStore.getState().isValidating).toBe(false);
    // viewMode is preserved (user preference)
    expect(useAppStore.getState().viewMode).toBe('all');
  });
});
