/**
 * Zustand store for application state.
 */

import { create } from 'zustand';
import type { ValidationReport } from '../types/validation';

export type { ValidationReport };

export type ViewMode = 'required' | 'all';

interface AppState {
  file: File | null;
  isValidating: boolean;
  validationReport: ValidationReport | null;
  error: string | null;
  viewMode: ViewMode;

  setFile: (file: File | null) => void;
  setValidating: (isValidating: boolean) => void;
  setValidationReport: (report: ValidationReport | null) => void;
  setError: (error: string | null) => void;
  setViewMode: (mode: ViewMode) => void;
  reset: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  file: null,
  isValidating: false,
  validationReport: null,
  error: null,
  viewMode: 'required',

  setFile: (file) => set({ file, error: null }),
  setValidating: (isValidating) => set({ isValidating }),
  setValidationReport: (report) => set({ validationReport: report }),
  setError: (error) => set({ error }),
  setViewMode: (viewMode) => set({ viewMode }),
  reset: () =>
    set({
      file: null,
      isValidating: false,
      validationReport: null,
      error: null,
    }),
}));
