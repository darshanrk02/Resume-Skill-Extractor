import api from './api';
import { Tag } from '../types';

/**
 * Get all available tags
 */
export const getTags = async (): Promise<Tag[]> => {
  try {
    const response = await api.get('/tags');
    return response.data;
  } catch (error) {
    console.error('Error fetching tags:', error);
    throw error;
  }
};

/**
 * Add tags to a resume
 * @param resumeId - ID of the resume
 * @param tags - List of tag names to add
 */
export const addTagsToResume = async (resumeId: string, tags: string[]): Promise<any> => {
  try {
    const response = await api.post(`/resumes/${resumeId}/tags`, tags);
    return response.data;
  } catch (error) {
    console.error('Error adding tags to resume:', error);
    throw error;
  }
};

/**
 * Remove a tag from a resume
 * @param resumeId - ID of the resume
 * @param tagName - Name of the tag to remove
 */
export const removeTagFromResume = async (resumeId: string, tagName: string): Promise<any> => {
  try {
    const response = await api.delete(`/resumes/${resumeId}/tags/${tagName}`);
    return response.data;
  } catch (error) {
    console.error('Error removing tag from resume:', error);
    throw error;
  }
};

/**
 * Get resumes filtered by tags
 * @param tags - List of tag names to filter by
 */
export const getResumesByTags = async (tags: string[]): Promise<any> => {
  try {
    // Build query string with multiple tags parameters
    const queryParams = tags.map(tag => `tags=${encodeURIComponent(tag)}`).join('&');
    const url = `/resumes?${queryParams}`;
    console.log(`Fetching resumes with URL: ${url}`);
    
    const response = await api.get(url);
    console.log('API response:', response);
    
    if (Array.isArray(response.data)) {
      console.log(`Found ${response.data.length} matching resumes`);
    } else {
      console.log('Response data is not an array:', response.data);
    }
    
    return response.data;
  } catch (error: any) {
    console.error('Error fetching resumes by tags:', error);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
    throw error;
  }
};