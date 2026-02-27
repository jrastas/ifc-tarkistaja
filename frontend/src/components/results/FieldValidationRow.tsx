/**
 * Row component for displaying a single field's validation status.
 */

import { useTranslation } from 'react-i18next';
import { CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import type { FieldValidation, ValidationStatus } from '../../types/validation';
import { getFieldName } from '../../utils/translations';

interface FieldValidationRowProps {
  field: FieldValidation;
  categoryId?: string;
  showIfcReference?: boolean;
}

const statusConfig: Record<
  ValidationStatus,
  { icon: typeof CheckCircle; color: string; bgColor: string }
> = {
  valid: {
    icon: CheckCircle,
    color: 'text-green-600',
    bgColor: 'bg-green-50',
  },
  missing: {
    icon: XCircle,
    color: 'text-red-600',
    bgColor: 'bg-red-50',
  },
  invalid: {
    icon: XCircle,
    color: 'text-red-600',
    bgColor: 'bg-red-50',
  },
  warning: {
    icon: AlertTriangle,
    color: 'text-amber-600',
    bgColor: 'bg-amber-50',
  },
};

export function FieldValidationRow({
  field,
  categoryId,
  showIfcReference = false,
}: FieldValidationRowProps) {
  const { t, i18n } = useTranslation();
  const config = statusConfig[field.status];
  const Icon = config.icon;

  const fieldName = getFieldName(
    categoryId || '',
    undefined,
    field.field_name,
    field.field_name_en,
    t,
    i18n.language
  );

  const formatValue = (value: unknown): string => {
    if (value === null || value === undefined) return '-';
    if (typeof value === 'boolean') return value ? t('common.yes') : t('common.no');
    if (typeof value === 'number') {
      // Format large numbers with units
      if (value >= 1000) return value.toLocaleString(i18n.language === 'fi' ? 'fi-FI' : 'en-US');
      return value.toString();
    }
    return String(value);
  };

  return (
    <div
      className={`flex items-center justify-between px-4 py-3 border-b border-slate-100 last:border-b-0 ${config.bgColor}`}
    >
      <div className="flex items-center gap-3 flex-1 min-w-0">
        <Icon className={`w-5 h-5 flex-shrink-0 ${config.color}`} />
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-slate-800 truncate">
              {fieldName}
            </span>
            {field.is_required && (
              <span className="px-1.5 py-0.5 text-xs font-medium bg-blue-100 text-blue-700 rounded">
                {t('common.required')}
              </span>
            )}
          </div>
          {showIfcReference && field.ifc_property && (
            <span className="text-xs text-slate-400 font-mono">
              {field.ifc_property}
            </span>
          )}
        </div>
      </div>
      <div className="text-right ml-4">
        <span
          className={`text-sm ${field.is_present ? 'text-slate-700' : 'text-slate-400 italic'}`}
        >
          {formatValue(field.value)}
        </span>
      </div>
    </div>
  );
}
