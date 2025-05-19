import apiClient from './api';
import { JobDescription } from '../types';
import { handleApiError, logError, shouldUseMockData } from '../utils/errorHandler';
import { sampleJobDescription } from '../data/sampleData';

const JD_API = '/job-descriptions';

export interface JobDescriptionListResponse {
  job_descriptions: JobDescription[];
  total: number;
}

/**
 * Create a new job description
 * @param jobDescriptionData Job description data
 * @returns Created job description
 */
export const createJobDescription = async (jobDescriptionData: Omit<JobDescription, 'id' | 'created_date'>): Promise<JobDescription> => {
  try {
    const response = await apiClient.post<JobDescription>(JD_API, jobDescriptionData);
    return response.data;
  } catch (error) {
    // Log the error for debugging
    logError(error, 'createJobDescription');
    
    // Format the error
    const formattedError = handleApiError(error);
    
    // If we're in development and mock data is enabled, return sample data
    if (shouldUseMockData()) {
      console.warn('Using sample job description data due to API error:', formattedError.message);
      return { ...sampleJobDescription, ...jobDescriptionData };
    }
    
    // Otherwise, throw the formatted error
    throw formattedError;
  }
};

/**
 * Get all job descriptions with pagination
 * @param skip Number of items to skip
 * @param limit Maximum number of items to return
 * @returns List of job descriptions and total count
 */
export const getJobDescriptions = async (skip = 0, limit = 10): Promise<JobDescriptionListResponse> => {
  try {
    const response = await apiClient.get<JobDescriptionListResponse>(JD_API, {
      params: { skip, limit },
    });
    
    return response.data;
  } catch (error) {
    // Log the error for debugging
    logError(error, 'getJobDescriptions');
    
    // Format the error
    const formattedError = handleApiError(error);
    
    // If we're in development and mock data is enabled, return sample data
    if (shouldUseMockData()) {
      console.warn('Using sample job description list data due to API error:', formattedError.message);
      return {
        job_descriptions: [sampleJobDescription],
        total: 1
      };
    }
    
    // Otherwise, throw the formatted error
    throw formattedError;
  }
};

/**
 * Get a specific job description by ID
 * @param jobDescriptionId Job description ID
 * @returns Job description data
 */
export const getJobDescriptionById = async (jobDescriptionId: number): Promise<JobDescription> => {
  const response = await apiClient.get<JobDescription>(`${JD_API}/${jobDescriptionId}`);
  return response.data;
};

/**
 * Update a job description
 * @param jobDescriptionId Job description ID
 * @param jobDescriptionData Updated job description data
 * @returns Updated job description data
 */
export const updateJobDescription = async (
  jobDescriptionId: number, 
  jobDescriptionData: Partial<JobDescription>
): Promise<JobDescription> => {
  const response = await apiClient.put<JobDescription>(`${JD_API}/${jobDescriptionId}`, jobDescriptionData);
  return response.data;
};

/**
 * Delete a job description
 * @param jobDescriptionId Job description ID
 */
export const deleteJobDescription = async (jobDescriptionId: number): Promise<void> => {
  await apiClient.delete(`${JD_API}/${jobDescriptionId}`);
};
