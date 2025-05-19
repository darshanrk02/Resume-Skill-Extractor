import apiClient from './api';
import { ResumeMatch, MatchResult } from '../types';
import { handleApiError, logError, shouldUseMockData } from '../utils/errorHandler';
import { sampleMatchData } from '../data/sampleData';

const MATCH_API = '/matches';

export interface MatchListResponse {
  matches: ResumeMatch[];
  total: number;
}

/**
 * Create a new match between a resume and job description
 * @param resumeId Resume ID
 * @param jobDescriptionId Job description ID
 * @returns Match result with score and details
 */
export const createMatch = async (resumeId: number, jobDescriptionId: number): Promise<MatchResult> => {
  try {
    const response = await apiClient.post<MatchResult>(MATCH_API, {
      resume_id: resumeId,
      job_description_id: jobDescriptionId
    });
    
    return response.data;
  } catch (error) {
    // Log the error for debugging
    logError(error, 'createMatch');
    
    // Format the error
    const formattedError = handleApiError(error);
    
    // If we're in development and mock data is enabled, return sample data
    if (shouldUseMockData()) {
      console.warn('Using sample match data due to API error:', formattedError.message);
      
      // Create a mock match result based on the sample match data
      const mockMatchResult: MatchResult = {
        id: 1,
        resumeId: resumeId,
        jobDescriptionId: jobDescriptionId,
        score: sampleMatchData.matchPercentage,
        matchedSkills: sampleMatchData.matchedSkills,
        missingSkills: sampleMatchData.missingSkills,
        recommendation: sampleMatchData.recommendation,
        analysis: sampleMatchData.analysis,
        createdDate: new Date().toISOString()
      };
      
      return mockMatchResult;
    }
    
    // Otherwise, throw the formatted error
    throw formattedError;
  }
};

/**
 * Get all matches with pagination
 * @param skip Number of items to skip
 * @param limit Maximum number of items to return
 * @returns List of matches and total count
 */
export const getMatches = async (skip = 0, limit = 10): Promise<MatchListResponse> => {
  try {
    const response = await apiClient.get<MatchListResponse>(MATCH_API, {
      params: { skip, limit },
    });
    
    return response.data;
  } catch (error) {
    // Log the error for debugging
    logError(error, 'getMatches');
    
    // Format the error
    const formattedError = handleApiError(error);
    
    // If we're in development and mock data is enabled, return sample data
    if (shouldUseMockData()) {
      console.warn('Using sample match list data due to API error:', formattedError.message);
      return {
        matches: [sampleMatchData],
        total: 1
      };
    }
    
    // Otherwise, throw the formatted error
    throw formattedError;
  }
};

/**
 * Get matches for a specific resume
 * @param resumeId Resume ID
 * @returns List of matches for the resume
 */
export const getMatchesByResumeId = async (resumeId: number): Promise<ResumeMatch[]> => {
  const response = await apiClient.get<ResumeMatch[]>(`${MATCH_API}/resume/${resumeId}`);
  return response.data;
};

/**
 * Get matches for a specific job description
 * @param jobDescriptionId Job description ID
 * @returns List of matches for the job description
 */
export const getMatchesByJobDescriptionId = async (jobDescriptionId: number): Promise<ResumeMatch[]> => {
  const response = await apiClient.get<ResumeMatch[]>(`${MATCH_API}/job-description/${jobDescriptionId}`);
  return response.data;
};

/**
 * Get a specific match by ID
 * @param matchId Match ID
 * @returns Match data
 */
export const getMatchById = async (matchId: number): Promise<ResumeMatch> => {
  const response = await apiClient.get<ResumeMatch>(`${MATCH_API}/${matchId}`);
  return response.data;
};

/**
 * Delete a match
 * @param matchId Match ID
 */
export const deleteMatch = async (matchId: number): Promise<void> => {
  await apiClient.delete(`${MATCH_API}/${matchId}`);
};
