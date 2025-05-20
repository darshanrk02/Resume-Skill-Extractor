/**
 * Application configuration settings
 */

// API configuration
export const API_CONFIG = {
  BASE_URL: window.location.hostname === 'localhost' ? 'http://localhost:8000/api/v1' : '/api/v1',
  TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3,
};

// Feature flags
export const FEATURES = {
  ENABLE_MOCK_DATA: false, // Disable mock data to use real data from the backend
  ENABLE_ANALYTICS: false, // Analytics tracking
  ENABLE_ADVANCED_MATCHING: true, // Advanced matching algorithms
};

// UI configuration
export const UI_CONFIG = {
  ANIMATION_DURATION: 300, // ms
  SNACKBAR_DURATION: 5000, // 5 seconds
  MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_FILE_TYPES: ['application/pdf'],
};

// Theme colors (matching our design system)
export const THEME_COLORS = {
  PRIMARY: '#1f2d3d',
  SECONDARY: '#4a90e2',
  ACCENT: '#50e3c2',
  SUCCESS: '#28a745',
  WARNING: '#ffc107',
  ERROR: '#dc3545',
  LIGHT_BG: '#f4f6f9',
};
