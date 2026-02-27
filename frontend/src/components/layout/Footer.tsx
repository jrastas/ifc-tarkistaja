/**
 * Footer component with version info.
 */

import { useTranslation } from 'react-i18next';

export function Footer() {
  const { t } = useTranslation();

  return (
    <footer className="bg-white border-t border-slate-200 px-6 py-4 mt-auto">
      <div className="max-w-4xl mx-auto text-center text-sm text-slate-500">
        <p>
          {t('header.title')} {t('footer.version')} 0.4.2
        </p>
        <p className="text-xs mt-1">{t('footer.description')}</p>
        <p className="text-xs mt-2">
          Copyright © 2025-2026 Jaakko Rastas and IFC Tarkistaja Contributors
        </p>
      </div>
    </footer>
  );
}
