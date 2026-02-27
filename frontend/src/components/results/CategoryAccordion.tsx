/**
 * Expandable category section with fields list.
 */

import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { ChevronDown, ChevronRight } from 'lucide-react';
import type { CategoryValidation } from '../../types/validation';
import { FieldValidationRow } from './FieldValidationRow';
import { getCategoryName } from '../../utils/translations';

interface CategoryAccordionProps {
  category: CategoryValidation;
  showOnlyRequired?: boolean;
  defaultExpanded?: boolean;
}

export function CategoryAccordion({
  category,
  showOnlyRequired = false,
  defaultExpanded = false,
}: CategoryAccordionProps) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  const { t, i18n } = useTranslation();

  const filteredFields = showOnlyRequired
    ? category.fields.filter((f) => f.is_required)
    : category.fields;

  if (filteredFields.length === 0) {
    return null;
  }

  // Determine badge color based on compliance
  const getBadgeColor = (compliance: number) => {
    if (compliance >= 90) return 'bg-green-100 text-green-700';
    if (compliance >= 70) return 'bg-amber-100 text-amber-700';
    return 'bg-red-100 text-red-700';
  };

  const validCount = filteredFields.filter((f) => f.status === 'valid').length;
  const totalCount = filteredFields.length;
  const compliance = totalCount > 0 ? (validCount / totalCount) * 100 : 0;

  const categoryName = getCategoryName(
    category.id,
    category.name,
    category.name_en,
    t,
    i18n.language
  );

  return (
    <div className="border border-slate-200 rounded-lg overflow-hidden bg-white">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between px-4 py-3 hover:bg-slate-50 transition-colors"
      >
        <div className="flex items-center gap-3">
          {isExpanded ? (
            <ChevronDown className="w-5 h-5 text-slate-400" />
          ) : (
            <ChevronRight className="w-5 h-5 text-slate-400" />
          )}
          <span className="font-medium text-slate-800">{categoryName}</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-slate-500">
            {validCount}/{totalCount}
          </span>
          <span
            className={`px-2 py-1 text-xs font-medium rounded ${getBadgeColor(compliance)}`}
          >
            {compliance.toFixed(0)}%
          </span>
        </div>
      </button>

      {isExpanded && (
        <div className="border-t border-slate-200">
          {filteredFields.map((field) => (
            <FieldValidationRow
              key={`${field.ifc_entity}-${field.ifc_property}-${field.field_name}`}
              field={field}
              categoryId={category.id}
            />
          ))}
        </div>
      )}
    </div>
  );
}
