import apiClient from './api';
import { ResumeData } from '../types';
import { handleApiError, logError, shouldUseMockData } from '../utils/errorHandler';
import { sampleResumeData } from '../data/sampleData';

// Constants for API endpoints (without the /api/v1 prefix as it's already in the baseURL)
const RESUME_API = {
  UPLOAD: '/resume/upload',
  SAVE: '/resume/save',
  GET_ALL: '/resumes',  // Endpoint for getting all resumes
  GET_ONE: (id: string) => `/resumes/${id}`,
  DELETE: (id: string) => `/resumes/${id}`,
};

export interface ResumeListResponse {
  resumes: ResumeData[];
  total: number;
}

/**
 * Upload and process a resume PDF file
 * @param file PDF file to upload
 * @returns Processed resume data
 */
export const uploadResume = async (file: File): Promise<ResumeData> => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await apiClient.post<ResumeData>(RESUME_API.UPLOAD, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  } catch (error) {
    // Log the error for debugging
    logError(error, 'uploadResume');
    
    // Format the error
    const formattedError = handleApiError(error);
    
    // If we're in development and mock data is enabled, return sample data
    if (shouldUseMockData()) {
      console.warn('Using sample resume data due to API error:', formattedError.message);
      return sampleResumeData as ResumeData;
    }
    
    // Otherwise, throw the formatted error
    throw formattedError;
  }
};

/**
 * Save resume data to the database
 * @param resumeData Resume data to save
 * @returns Response with resume ID and status
 */
export const saveResume = async (resumeData: ResumeData): Promise<{ resume_id: string, message: string }> => {
  try {
    const response = await apiClient.post<{ resume_id: string, message: string }>(
      RESUME_API.SAVE, 
      resumeData
    );
    return response.data;
  } catch (error) {
    // Log the error for debugging
    logError(error, 'saveResume');
    
    // Format the error
    const formattedError = handleApiError(error);
    
    // If we're in development and mock data is enabled, return sample response
    if (shouldUseMockData()) {
      console.warn('Using mock save response due to API error:', formattedError.message);
      return { 
        resume_id: "60f9b0b3e6b3a2001c8e4567", 
        message: 'Resume saved successfully (mock)' 
      };
    }
    
    // Otherwise, throw the formatted error
    throw formattedError;
  }
};

/**
 * Get all resumes
 * @returns List of all resumes
 */
export const getAllResumes = async (): Promise<ResumeData[]> => {
  try {
    const response = await apiClient.get<ResumeData[]>(RESUME_API.GET_ALL);
    return response.data;
  } catch (error) {
    // Log the error for debugging
    console.error('Error in getAllResumes:', error);
    logError(error, 'getAllResumes');
    
    if (shouldUseMockData()) {
      console.warn('Using sample resume data due to API error');
      return [sampleResumeData as ResumeData];
    }
    
    // Return empty array in case of error
    return [];
  }
};

/**
 * Get a specific resume by ID
 * @param resumeId Resume ID
 * @returns Resume data
 */
export const getResumeById = async (resumeId: string): Promise<ResumeData> => {
  const response = await apiClient.get<ResumeData>(RESUME_API.GET_ONE(resumeId));
  return response.data;
};

/**
 * Update a resume
 * @param resumeId Resume ID
 * @param resumeData Updated resume data
 * @returns Updated resume data
 */
export const updateResume = async (resumeId: string, resumeData: Partial<ResumeData>): Promise<ResumeData> => {
  const response = await apiClient.put<ResumeData>(RESUME_API.GET_ONE(resumeId), resumeData);
  return response.data;
};

/**
 * Delete a resume
 * @param resumeId Resume ID
 */
export const deleteResume = async (resumeId: string): Promise<void> => {
  await apiClient.delete(RESUME_API.DELETE(resumeId));
};
