/**
 * Utility functions for translating backend validation data.
 */

/**
 * Get the translated category name based on current language.
 */
export function getCategoryName(
  _categoryId: string,
  name: string,
  name_en: string,
  _t: unknown,
  language: string
): string {
  return language === 'en' ? name_en : name;
}

/**
 * Get the translated field name based on current language.
 */
export function getFieldName(
  _categoryId: string,
  _fieldId: string | undefined,
  field_name: string,
  field_name_en: string,
  _t: unknown,
  language: string
): string {
  return language === 'en' ? field_name_en : field_name;
}
