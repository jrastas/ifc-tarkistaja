/**
 * Dropdown language selector with flag icons.
 */

import { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { ChevronDown, Check } from 'lucide-react';

interface Language {
  code: 'fi' | 'en';
  name: string;
  flag: string;
}

const LANGUAGES: Language[] = [
  { code: 'fi', name: 'Suomi', flag: '🇫🇮' },
  { code: 'en', name: 'English', flag: '🇬🇧' },
];

export function LanguageToggle() {
  const { i18n } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const currentLanguage = LANGUAGES.find((lang) => lang.code === i18n.language) || LANGUAGES[0];

  const changeLanguage = (lang: Language) => {
    i18n.changeLanguage(lang.code);
    setIsOpen(false);
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors"
      >
        <span className="text-xl leading-none">{currentLanguage.flag}</span>
        <span className="text-sm font-medium text-slate-700">{currentLanguage.name}</span>
        <ChevronDown className={`w-4 h-4 text-slate-500 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white border border-slate-200 rounded-lg shadow-lg overflow-hidden z-50">
          {LANGUAGES.map((lang) => (
            <button
              key={lang.code}
              onClick={() => changeLanguage(lang)}
              className={`w-full flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 transition-colors ${lang.code === currentLanguage.code ? 'bg-blue-50' : ''
                }`}
            >
              <div className="flex items-center gap-3">
                <span className="text-xl leading-none">{lang.flag}</span>
                <span className="text-sm font-medium text-slate-700">{lang.name}</span>
              </div>
              {lang.code === currentLanguage.code && (
                <Check className="w-4 h-4 text-blue-600" />
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
