/**
 * Drag & drop file upload component for IFC files.
 */

import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileCheck, AlertCircle, Loader2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';

interface DropZoneProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
  isLoading: boolean;
  error: string | null;
}

export function DropZone({
  onFileSelect,
  selectedFile,
  isLoading,
  error,
}: DropZoneProps) {
  const { t } = useTranslation();

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        onFileSelect(acceptedFiles[0]);
      }
    },
    [onFileSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/x-step': ['.ifc'] },
    maxFiles: 1,
    disabled: isLoading,
  });

  return (
    <div
      {...getRootProps()}
      className={`
        border-2 border-dashed rounded-xl p-8 text-center cursor-pointer
        transition-colors
        ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-slate-300 hover:border-blue-400'}
        ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}
      `}
    >
      <input {...getInputProps()} />

      {isLoading ? (
        <div className="flex flex-col items-center">
          <Loader2 className="w-12 h-12 text-blue-600 mb-4 animate-spin" />
          <p className="font-medium text-slate-700">{t('common.validating')}</p>
          <p className="text-sm text-slate-500 mt-1">{t('common.loading')}</p>
        </div>
      ) : selectedFile ? (
        <div className="flex flex-col items-center">
          <FileCheck className="w-12 h-12 text-blue-600 mb-4" />
          <p className="font-medium text-slate-800">{selectedFile.name}</p>
          <p className="text-sm text-slate-500">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
        </div>
      ) : (
        <div className="flex flex-col items-center">
          <Upload className="w-12 h-12 text-slate-400 mb-4" />
          <p className="font-medium text-slate-700">
            {isDragActive ? t('upload.drop_here', 'Drop file here') : t('common.upload')}
          </p>
          <p className="text-sm text-slate-500 mt-1">{t('common.upload_hint')}</p>
        </div>
      )}

      {error && (
        <div className="mt-4 flex items-center justify-center gap-2 text-red-600">
          <AlertCircle className="w-4 h-4" />
          <span className="text-sm">{error}</span>
        </div>
      )}
    </div>
  );
}
