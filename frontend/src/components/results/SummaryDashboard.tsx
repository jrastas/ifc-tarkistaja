/**
 * Summary dashboard showing overall compliance and quick stats.
 */

import { useTranslation } from 'react-i18next';
import { FileText, AlertTriangle, AlertCircle } from 'lucide-react';
import type { ValidationReport } from '../../types/validation';
import { ComplianceGauge } from './ComplianceGauge';

interface SummaryDashboardProps {
  report: ValidationReport;
}

export function SummaryDashboard({ report }: SummaryDashboardProps) {
  const { t } = useTranslation();
  const totalFields = report.categories.reduce(
    (sum, cat) => sum + cat.fields.length,
    0
  );
  const validFields = report.categories.reduce(
    (sum, cat) => sum + cat.fields.filter((f) => f.status === 'valid').length,
    0
  );
  const requiredFields = report.categories.reduce(
    (sum, cat) => sum + cat.fields.filter((f) => f.is_required).length,
    0
  );
  const validRequiredFields = report.categories.reduce(
    (sum, cat) =>
      sum +
      cat.fields.filter((f) => f.is_required && f.status === 'valid').length,
    0
  );

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6">
      {/* File info */}
      <div className="flex items-center gap-3 mb-6 pb-4 border-b border-slate-100">
        <FileText className="w-6 h-6 text-blue-600" />
        <div>
          <h2 className="font-semibold text-slate-800">{report.filename}</h2>
          <p className="text-sm text-slate-500">
            {report.ifc_schema} | {new Date(report.timestamp).toLocaleString('fi-FI')}
          </p>
        </div>
      </div>

      {/* Compliance gauges */}
      <div className="grid grid-cols-2 gap-8 mb-6">
        <ComplianceGauge
          percentage={report.overall_compliance * 100}
          label={t('results.overall_compliance')}
          size="lg"
        />
        <ComplianceGauge
          percentage={report.required_compliance * 100}
          label={t('results.required_compliance')}
          size="lg"
        />
      </div>

      {/* Quick stats */}
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div className="bg-slate-50 rounded-lg p-3">
          <span className="text-slate-500">{t('results.all_fields')}:</span>
          <span className="ml-2 font-medium text-slate-800">
            {validFields}/{totalFields}
          </span>
        </div>
        <div className="bg-slate-50 rounded-lg p-3">
          <span className="text-slate-500">{t('results.required_fields')}:</span>
          <span className="ml-2 font-medium text-slate-800">
            {validRequiredFields}/{requiredFields}
          </span>
        </div>
      </div>

      {/* Errors and warnings count */}
      {(report.errors.length > 0 || report.warnings.length > 0) && (
        <div className="flex gap-4 mt-4 pt-4 border-t border-slate-100">
          {report.errors.length > 0 && (
            <div className="flex items-center gap-2 text-red-600">
              <AlertCircle className="w-4 h-4" />
              <span className="text-sm font-medium">
                {report.errors.length} {t('results.errors_count')}
              </span>
            </div>
          )}
          {report.warnings.length > 0 && (
            <div className="flex items-center gap-2 text-amber-600">
              <AlertTriangle className="w-4 h-4" />
              <span className="text-sm font-medium">
                {report.warnings.length} {t('results.warnings_count')}
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
