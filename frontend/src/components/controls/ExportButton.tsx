/**
 * Button to export validation report as PDF.
 */

import { useState } from 'react';
import { FileDown, Loader2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { exportPDF } from '../../services/api';
import { useAppStore } from '../../store/appStore';

export function ExportButton() {
  const { t, i18n } = useTranslation();
  const [isExporting, setIsExporting] = useState(false);
  const { validationReport } = useAppStore();

  const handleExport = async () => {
    if (!validationReport) return;

    setIsExporting(true);
    try {
      const backendLang = i18n.language === 'fi' ? 'fi' : 'en';
      const result = await exportPDF(validationReport, backendLang);

      if (result instanceof Blob) {
        const url = window.URL.createObjectURL(result);
        try {
          const a = document.createElement('a');
          a.href = url;
          a.download = `ifc_report_${validationReport.filename.replace('.ifc', '')}.pdf`;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
        } finally {
          window.URL.revokeObjectURL(url);
        }
      }
    } catch (error) {
      console.error('PDF export failed:', error);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <button
      onClick={handleExport}
      disabled={isExporting || !validationReport}
      className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700
                 disabled:bg-slate-300 text-white rounded-lg font-medium text-sm
                 transition-colors shadow-sm"
    >
      {isExporting ? (
        <Loader2 className="w-4 h-4 animate-spin" />
      ) : (
        <FileDown className="w-4 h-4" />
      )}
      {t('common.export_pdf')}
    </button>
  );
}
