import { AxiosError } from 'axios';
import { FEATURES } from '../config';

/**
 * Standard error response structure
 */
export interface ErrorResponse {
  message: string;
  code?: string;
  details?: string;
  status?: number;
}

/**
 * Process API errors into a standardized format
 */
export const handleApiError = (error: any): ErrorResponse => {
  if (error.isAxiosError) {
    const axiosError = error as AxiosError<any>;
    
    // Handle backend API errors
    if (axiosError.response) {
      const { data, status } = axiosError.response;
      
      return {
        message: data.detail || 'An error occurred while processing your request',
        code: data.code || 'API_ERROR',
        details: JSON.stringify(data),
        status
      };
    }
    
    // Handle network errors
    if (axiosError.request) {
      return {
        message: 'Unable to connect to the server. Please check your internet connection.',
        code: 'NETWORK_ERROR',
        details: 'Request was made but no response was received'
      };
    }
  }
  
  // Handle generic errors
  return {
    message: error.message || 'An unexpected error occurred',
    code: 'UNKNOWN_ERROR',
    details: error.toString()
  };
};

/**
 * Log errors to console or error tracking service
 */
export const logError = (error: any, context?: string): void => {
  if (process.env.NODE_ENV !== 'production') {
    console.error(`Error${context ? ` in ${context}` : ''}:`, error);
  }
  
  // Here you could add integration with error tracking services like Sentry
  // if (FEATURES.ENABLE_ERROR_TRACKING) {
  //   errorTrackingService.captureException(error, { extra: { context } });
  // }
};

/**
 * Determine if we should show mock data when API fails
 */
export const shouldUseMockData = (): boolean => {
  return FEATURES.ENABLE_MOCK_DATA && process.env.NODE_ENV !== 'production';
};
