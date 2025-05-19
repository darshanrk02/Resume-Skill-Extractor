import React, { useState, useRef } from 'react';
import { Box, Alert, CircularProgress, Typography, useTheme } from '@mui/material';
import JobDescriptionInput from '../components/jdmatching/JobDescriptionInput';
import ResumeMatchAnalysis from '../components/jdmatching/ResumeMatchAnalysis';
import { apiClient } from '../services/apiClient';
import { useNotification } from '../context/NotificationContext';
import { 
  JobDescription, 
  BackendMatch, 
  UIResumeMatch, 
  SkillMatch, 
  MissingSkill 
} from '../types/jdMatching';

const JDMatchingPage = () => {
  const theme = useTheme();
  const { showNotification } = useNotification();
  const [matchData, setMatchData] = useState<UIResumeMatch | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadedResume, setUploadedResume] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleResumeUpload = async (file: File) => {
    setIsUploading(true);
    setError(null);
    
    try {
      // In a real app, you would upload the file to your backend here
      // For now, we'll just set the file in state
      setUploadedResume(file);
      showNotification('success', 'Resume uploaded successfully', 'Success');
    } catch (error) {
      console.error('Error uploading resume:', error);
      setError('Failed to upload resume. Please try again.');
      showNotification('error', 'Failed to upload resume', 'Error');
    } finally {
      setIsUploading(false);
    }
  };

  const handleRemoveResume = () => {
    setUploadedResume(null);
    setMatchData(null);
  };

  const handleAnalyzeJD = async (jobDescription: JobDescription, resumeFile: File | null) => {
    if (!resumeFile) {
      setError('Please upload a resume first');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Create FormData to send the file and job description
      const formData = new FormData();
      formData.append('resume', resumeFile);
      formData.append('job_description', jobDescription.text);
      
      if (jobDescription.title) {
        formData.append('job_title', jobDescription.title);
      }
      if (jobDescription.company) {
        formData.append('company', jobDescription.company);
      }

      console.log('Sending request to /api/v1/analyze with:', {
        jobTitle: jobDescription.title,
        company: jobDescription.company,
        resumeName: resumeFile.name
      });

      const response = await apiClient.post<BackendMatch>('/api/v1/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Received response:', response.data);
      const match = response.data;

      // Format the response for the UI
      const formattedMatch: UIResumeMatch = {
        resumeId: 'current-resume',
        name: resumeFile.name.split('.')[0] || 'Resume',
        title: 'Candidate',
        matchPercentage: (typeof match.match_percentage === 'number' ? match.match_percentage : 0) * 100, // Convert to percentage
        matchedSkills: (match.skill_matches || []).map((s: any) => ({
          skill: s.skill || s.name || 'Unknown Skill',
          matched: true,
          weight: s.similarity_score || s.weight || 1,
          similarityScore: s.similarity_score
        })),
        missingSkills: (match.missing_skills || []).map((s: any) => ({
          skill: s.name || s.skill || 'Unknown Skill',
          matched: false,
          weight: s.weight || 1
        })),
        recommendation: match.recommendation || 'No recommendation available',
        confidenceLevel: (() => {
          const score = match.confidence_score || 0;
          return score >= 0.8 ? 'high' : score >= 0.6 ? 'medium' : 'low';
 })(),
        analysis: Array.isArray(match.explanation) 
          ? match.explanation.join('\n') 
          : match.explanation || 'No analysis available.'
      };

      console.log('Formatted match data:', formattedMatch);
      setMatchData(formattedMatch);
    } catch (error) {
      console.error('Error analyzing job description:', error);
      const errorMessage = error instanceof Error 
        ? error.message 
        : typeof error === 'string' 
          ? error 
          : 'Failed to analyze job description';
      
      console.error('Error details:', {
        error,
        response: (error as any)?.response?.data
      });
      
      setError(errorMessage);
      showNotification('error', errorMessage, 'Analysis Failed');
      showNotification('error', errorMessage, 'Analysis Failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setMatchData(null);
    setError(null);
    setUploadedResume(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <Box sx={{ height: '100%', p: 2 }}>
      <Box sx={{ 
        display: 'flex', 
        flexDirection: { xs: 'column', lg: 'row' }, 
        gap: 3, 
        height: '100%',
        '& > *': {
          minWidth: 0
        },
        '& > :first-of-type': {
          flex: '0 0 40%',
          maxWidth: '500px',
          [theme.breakpoints.down('lg')]: {
            flex: '1 1 auto',
            maxWidth: '100%',
            width: '100%'
          }
        },
        '& > :last-child': {
          flex: '1 1 0%',
          minWidth: 0
        }
      } as any}>
        {/* Left Panel - Job Description Input */}
        <Box sx={{ 
          display: 'flex',
          flexDirection: 'column',
          height: '100%',
          border: '1px solid',
          borderColor: 'divider',
          borderRadius: 1,
          overflow: 'hidden',
          bgcolor: 'background.paper'
        }}>
          <JobDescriptionInput
            onAnalyze={handleAnalyzeJD}
            onClear={handleClear}
            isLoading={isLoading || isUploading}
            onResumeUpload={handleResumeUpload}
            uploadedResume={uploadedResume}
            onRemoveResume={handleRemoveResume}
          />
          {error && (
            <Alert severity="error" sx={{ m: 2, mt: 0 }}>
              {error}
            </Alert>
          )}
        </Box>

        {/* Right Panel - Analysis Result */}
        <Box sx={{ 
          display: 'flex',
          flexDirection: 'column',
          height: '100%',
          border: '1px solid',
          borderColor: 'divider',
          borderRadius: 1,
          overflow: 'hidden',
          bgcolor: 'background.paper'
        }}>
          {isLoading ? (
            <Box sx={{ 
              display: 'flex', 
              justifyContent: 'center', 
              alignItems: 'center', 
              height: '100%',
              flexDirection: 'column',
              gap: 2
            }}>
              <CircularProgress />
              <Typography>Analyzing job description...</Typography>
            </Box>
          ) : matchData ? (
            <ResumeMatchAnalysis match={matchData} />
          ) : (
            <Box sx={{ 
              display: 'flex', 
              justifyContent: 'center', 
              alignItems: 'center', 
              height: '100%',
              color: 'text.secondary'
            }}>
              <Typography variant="h6">
                {!uploadedResume 
                  ? 'Please upload a resume and enter a job description' 
                  : 'Enter a job description and click Analyze'}
              </Typography>
            </Box>
          )}
        </Box>
      </Box>
    </Box>
  );
};

export default JDMatchingPage;
