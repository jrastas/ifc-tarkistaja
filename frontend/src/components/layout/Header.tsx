/**
 * Header component with title and language toggle.
 */

import { useTranslation } from 'react-i18next';
import { LanguageToggle } from '../controls/LanguageToggle';

export function Header() {
  const { t } = useTranslation();

  return (
    <header className="bg-white border-b border-slate-200 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div>
            <h1 className="text-xl font-semibold text-slate-800">
              {t('header.title')}
            </h1>
            <div className="flex items-center gap-2">
              <p className="text-sm text-slate-500">{t('header.subtitle')}</p>
              <span className="text-xs bg-amber-100 text-amber-800 px-2 py-0.5 rounded-full font-mono">v0.4.2</span>
            </div>
          </div>
        </div>
        <LanguageToggle />
      </div>
    </header>
  );
}
