/**
 * API service for communicating with the backend.
 */

import axios from 'axios';
import type { ValidationReport, ValidationResponse } from '../types/validation';

// Use empty string for production (nginx proxies /api/*), localhost:8000 for dev
const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

/**
 * Validate an IFC file against Finnish building permit requirements.
 */
export async function validateIFCFile(
  file: File,
  language: 'fi' | 'en' = 'fi'
): Promise<ValidationResponse> {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await api.post<ValidationResponse>('/api/validate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      params: { language },
    });

    return response.data;
  } catch (error) {
    console.error('Validation API error:', error);

    if (axios.isAxiosError(error) && error.response?.data?.error) {
      return {
        success: false,
        report: null,
        error: `Server Error: ${error.response.data.error}`,
      };
    }

    return {
      success: false,
      report: null,
      error: error instanceof Error ? error.message : 'Network error occurred',
    };
  }
}

/**
 * Export validation report as PDF.
 */
export async function exportPDF(
  report: ValidationReport,
  language: 'fi' | 'en'
): Promise<Blob | null> {
  const response = await api.post('/api/export/pdf', report, {
    params: { language },
    responseType: 'blob',
  });
  return response.data;
}

/**
 * Check if the backend is healthy.
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await api.get('/api/health');
    return response.data.status === 'healthy';
  } catch {
    return false;
  }
}
