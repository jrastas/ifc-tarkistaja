/**
 * Main application component.
 * Shows validation results when file is loaded.
 */

import { useCallback, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { RefreshCw } from 'lucide-react';
import { Header } from './components/layout/Header';
import { Footer } from './components/layout/Footer';
import { DropZone } from './components/upload/DropZone';
import { SummaryDashboard } from './components/results/SummaryDashboard';
import { CategoryAccordion } from './components/results/CategoryAccordion';
import { IssuesSummary } from './components/results/IssuesSummary';
import { ViewModeToggle } from './components/controls/ViewModeToggle';
import { ExportButton } from './components/controls/ExportButton';
import { useAppStore } from './store/appStore';
import { validateIFCFile } from './services/api';

function App() {
  const {
    file,
    isValidating,
    validationReport,
    error,
    viewMode,
    setFile,
    setValidating,
    setValidationReport,
    setError,
    setViewMode,
    reset,
  } = useAppStore();

  const { t, i18n } = useTranslation();
  const prevLanguageRef = useRef(i18n.language);

  const handleFileSelect = useCallback(
    async (selectedFile: File) => {
      setFile(selectedFile);
      setValidating(true);
      setError(null);
      setValidationReport(null);

      try {
        const backendLang = i18n.language === 'fi' ? 'fi' : 'en';
        const response = await validateIFCFile(selectedFile, backendLang as 'fi' | 'en');

        if (response.success && response.report) {
          setValidationReport(response.report);
        } else {
          setError(response.error || 'Validation failed');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setValidating(false);
      }
    },
    [setFile, setValidating, setError, setValidationReport, i18n.language]
  );

  // Re-validate when language changes (if a file is loaded)
  useEffect(() => {
    if (prevLanguageRef.current !== i18n.language && file && !isValidating) {
      prevLanguageRef.current = i18n.language;
      // Re-validate with new language
      handleFileSelect(file);
    }
  }, [i18n.language, file, isValidating, handleFileSelect]);

  // Upload view - shown when no file is selected
  if (!file) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col">
        <Header />
        <main className="flex-1 px-6 py-8">
          <div className="max-w-2xl mx-auto">
            <DropZone
              onFileSelect={handleFileSelect}
              selectedFile={file}
              isLoading={isValidating}
              error={error}
            />
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  // Results view - shown when file is loaded
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Header />

      <main className="flex-1 px-6 py-8 overflow-auto">
        <div className="max-w-4xl mx-auto space-y-4">
          {/* File info and upload */}
          <DropZone
            onFileSelect={handleFileSelect}
            selectedFile={file}
            isLoading={isValidating}
            error={error}
          />

          {/* Results section */}
          {validationReport && (
            <>
              {/* Summary Dashboard */}
              <SummaryDashboard report={validationReport} />

              {/* Issues Summary */}
              <IssuesSummary
                errors={validationReport.errors}
                warnings={validationReport.warnings}
              />

              {/* Export Button */}
              <div className="flex justify-end">
                <ExportButton />
              </div>

              {/* View Mode Toggle and Categories */}
              <div className="bg-white rounded-xl border border-slate-200 p-4">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-semibold text-slate-800 text-sm">
                    {t('common.categories')} ({validationReport.categories.length})
                  </h3>
                  <ViewModeToggle
                    viewMode={viewMode}
                    onViewModeChange={setViewMode}
                  />
                </div>

                <div className="space-y-2">
                  {validationReport.categories.map((category) => (
                    <CategoryAccordion
                      key={category.id}
                      category={category}
                      showOnlyRequired={viewMode === 'required'}
                    />
                  ))}
                </div>
              </div>

              {/* Reset button */}
              <div className="flex justify-center pt-2">
                <button
                  onClick={reset}
                  className="flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-sm font-medium transition-colors"
                >
                  <RefreshCw className="w-4 h-4" />
                  {t('common.reset')}
                </button>
              </div>
            </>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;
