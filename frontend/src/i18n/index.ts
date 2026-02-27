/**
 * i18n configuration for multi-language support.
 */

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import fi from './fi.json';
import en from './en.json';

// Get saved language from localStorage or use default
const savedLanguage = ['fi', 'en'].includes(localStorage.getItem('i18nextLng') || '') ? localStorage.getItem('i18nextLng')! : 'fi';

i18n.use(initReactI18next).init({
  resources: {
    fi: { translation: fi },
    en: { translation: en },
  },
  lng: savedLanguage,
  fallbackLng: 'fi',
  interpolation: {
    escapeValue: false, // React already escapes
  },
});

// Save language to localStorage whenever it changes
i18n.on('languageChanged', (lng) => {
  localStorage.setItem('i18nextLng', lng);
});

export default i18n;
