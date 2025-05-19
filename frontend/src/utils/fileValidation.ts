import { UI_CONFIG } from '../config';

/**
 * Validation result interface
 */
export interface ValidationResult {
  isValid: boolean;
  error?: string;
}

/**
 * Validates that the file is a PDF and within the allowed size limit
 */
export const validatePdfFile = (file: File): ValidationResult => {
  // Check file type
  if (!UI_CONFIG.ALLOWED_FILE_TYPES.includes(file.type)) {
    return {
      isValid: false,
      error: `Invalid file type. Only PDF files are allowed.`
    };
  }

  // Check file size
  if (file.size > UI_CONFIG.MAX_FILE_SIZE) {
    const maxSizeMB = UI_CONFIG.MAX_FILE_SIZE / (1024 * 1024);
    return {
      isValid: false,
      error: `File is too large. Maximum size is ${maxSizeMB}MB.`
    };
  }

  return { isValid: true };
};

/**
 * Formats file size to a human-readable string
 */
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};
