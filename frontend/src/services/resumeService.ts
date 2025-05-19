import apiClient from './api';
import { ResumeData } from '../types';
import { handleApiError, logError, shouldUseMockData } from '../utils/errorHandler';
import { sampleResumeData } from '../data/sampleData';

const RESUME_API = {
  UPLOAD: '/resume/upload',
  SAVE: '/resume/save',
  GET_ALL: '/resumes',  // Endpoint for getting all resumes
  GET_ONE: (id: number) => `/resume/${id}`,
  DELETE: (id: number) => `/resume/${id}`,
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
export const saveResume = async (resumeData: ResumeData): Promise<{ resume_id: number, message: string }> => {
  try {
    const response = await apiClient.post<{ resume_id: number, message: string }>(
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
        resume_id: 123, 
        message: 'Resume saved successfully (mock)' 
      };
    }
    
    // Otherwise, throw the formatted error
    throw formattedError;
  }
};

/**
 * Get all resumes with pagination
 * @param skip Number of items to skip
 * @param limit Maximum number of items to return
 * @returns List of resumes and total count
 */
export const getResumes = async (skip = 0, limit = 10): Promise<ResumeListResponse> => {
  try {
    console.log(`Fetching resumes from: ${RESUME_API.GET_ALL}?skip=${skip}&limit=${limit}`);
    const response = await apiClient.get<ResumeListResponse>(
      RESUME_API.GET_ALL,
      { params: { skip, limit } }
    );
    
    console.log('API Response:', response);
    
    // Ensure we always return valid resume data
    const data = response.data || { resumes: [], total: 0 };
    console.log('Processed data:', data);
    
    return {
      resumes: Array.isArray(data) ? data : (Array.isArray(data.resumes) ? data.resumes : []),
      total: data.total || (Array.isArray(data) ? data.length : 0)
    };
  } catch (error) {
    // Log the error for debugging
    console.error('Error in getResumes:', error);
    logError(error, 'getResumes');
    
    if (shouldUseMockData()) {
      console.warn('Using sample resume data due to API error');
      return {
        resumes: [sampleResumeData],
        total: 1
      };
    }
    
    // Return empty data structure in case of error
    return {
      resumes: [],
      total: 0
    };
  }
};

/**
 * Get a specific resume by ID
 * @param resumeId Resume ID
 * @returns Resume data
 */
export const getResumeById = async (resumeId: number): Promise<ResumeData> => {
  const response = await apiClient.get<ResumeData>(RESUME_API.GET_ONE(resumeId));
  return response.data;
};

/**
 * Update a resume
 * @param resumeId Resume ID
 * @param resumeData Updated resume data
 * @returns Updated resume data
 */
export const updateResume = async (resumeId: number, resumeData: Partial<ResumeData>): Promise<ResumeData> => {
  const response = await apiClient.put<ResumeData>(RESUME_API.GET_ONE(resumeId), resumeData);
  return response.data;
};

/**
 * Delete a resume
 * @param resumeId Resume ID
 */
export const deleteResume = async (resumeId: number): Promise<void> => {
  await apiClient.delete(RESUME_API.DELETE(resumeId));
};
