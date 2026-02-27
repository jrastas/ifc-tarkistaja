/**
 * Summary of errors and warnings.
 */

import { useTranslation } from 'react-i18next';
import { AlertCircle, AlertTriangle, CheckCircle } from 'lucide-react';

interface IssuesSummaryProps {
  errors: string[];
  warnings: string[];
}

export function IssuesSummary({ errors, warnings }: IssuesSummaryProps) {
  const { t } = useTranslation();

  if (errors.length === 0 && warnings.length === 0) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-center gap-2 text-green-700">
          <CheckCircle className="w-5 h-5" />
          <span className="font-medium">{t('results.no_issues')}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Errors */}
      {errors.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center gap-2 text-red-700 mb-3">
            <AlertCircle className="w-5 h-5" />
            <span className="font-medium">{t('results.errors')} ({errors.length})</span>
          </div>
          <ul className="space-y-1">
            {errors.slice(0, 10).map((error, index) => (
              <li key={index} className="text-sm text-red-600 pl-7">
                {error}
              </li>
            ))}
            {errors.length > 10 && (
              <li className="text-sm text-red-500 pl-7 italic">
                ...{t('results.and_more', { count: errors.length - 10 })}
              </li>
            )}
          </ul>
        </div>
      )}

      {/* Warnings */}
      {warnings.length > 0 && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <div className="flex items-center gap-2 text-amber-700 mb-3">
            <AlertTriangle className="w-5 h-5" />
            <span className="font-medium">{t('results.warnings')} ({warnings.length})</span>
          </div>
          <ul className="space-y-1">
            {warnings.slice(0, 10).map((warning, index) => (
              <li key={index} className="text-sm text-amber-600 pl-7">
                {warning}
              </li>
            ))}
            {warnings.length > 10 && (
              <li className="text-sm text-amber-500 pl-7 italic">
                ...{t('results.and_more', { count: warnings.length - 10 })}
              </li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}
