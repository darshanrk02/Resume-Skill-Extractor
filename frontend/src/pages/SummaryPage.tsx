import React, { useState } from 'react';
import { Box, CircularProgress, Typography, Alert } from '@mui/material';
import Grid from '@mui/material/Grid';
import PDFUpload from '../components/upload/PDFUpload';
import ResumeSummary from '../components/resume/ResumeSummary';
import LoadingOverlay from '../components/common/LoadingOverlay';
import { ResumeData } from '../types';
import { uploadResume, saveResume } from '../services/resumeService';
import { useNotification } from '../context/NotificationContext';
import { ErrorResponse } from '../utils/errorHandler';

// Sample data for demonstration purposes
const sampleResumeData: ResumeData = {
  contact_info: {
    name: 'John Smith',
    email: 'john.smith@example.com',
    phone: '+1 (555) 987-6543',
    location: 'New York, NY'
  },
  summary: 'Passionate software engineer with 5+ years of experience in full-stack development. Proven track record in building scalable web applications using React, Node.js, and cloud infrastructure. Strong collaborator with cross-functional teams to deliver robust and maintainable code.',
  skills: [
    { name: 'React' },
    { name: 'Node.js' },
    { name: 'AWS' },
    { name: 'Docker' },
    { name: 'MongoDB' },
    { name: 'TypeScript' },
    { name: 'Python' },
    { name: 'JavaScript' }
  ],
  projects: [
    {
      title: 'TaskMaster Pro',
      description: 'A productivity web app built with React and Firebase that allows teams to track tasks, set deadlines, and monitor progress in real-time.'
    },
    {
      title: 'SmartCart AI',
      description: 'An AI-powered shopping assistant using Python and OpenCV to detect items and suggest optimized purchases based on user preferences.'
    },
    {
      title: 'Resume Skill Extractor',
      description: 'A parser built using NLP techniques to extract structured data like name, skills, and experience from unstructured resumes in PDF format.'
    }
  ],
  experience: [{
    company: 'Sample Corp',
    position: 'Software Engineer',
    start_date: '2020-01',
    end_date: '2023-05',
    description: 'Developed and maintained web applications using React and Node.js.'
  }],
  education: [
    {
      institution: 'XYZ University',
      degree: 'B.Tech',
      field_of_study: 'Computer Science',
      start_date: '2013',
      end_date: '2017'
    }
  ]
};

const SummaryPage: React.FC = () => {
  const [resumeData, setResumeData] = useState<ResumeData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [currentFile, setCurrentFile] = useState<File | null>(null);
  
  // Use our notification context
  const { showNotification } = useNotification();

  const handleFileUpload = async (file: File) => {
    setIsLoading(true);
    setError(null);
    setCurrentFile(file);
    
    try {
      // Send the file to the backend for processing using our service
      const response = await uploadResume(file);
      setResumeData(response);
      
      // Show success notification
      showNotification(
        'success',
        'Resume successfully processed',
        'Upload Complete'
      );
    } catch (err: any) {
      console.error('Error uploading resume:', err);
      const errorResponse = err as ErrorResponse;
      setError(errorResponse.message || 'Error processing resume. Please try again.');
      
      // Show error notification
      showNotification(
        'error',
        errorResponse.message || 'Error processing resume',
        'Upload Failed'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    if (!resumeData) return;
    
    try {
      setIsLoading(true);
      // Add the file information to the resume data
      const resumeToSave = {
        ...resumeData,
        file_name: currentFile?.name || 'resume.pdf',
        file_type: currentFile?.type || 'application/pdf',
        file_size: currentFile?.size || 0,
        created_at: new Date().toISOString()
      };
      
      const response = await saveResume(resumeToSave);
      
      showNotification(
        'success',
        `Resume saved successfully with ID: ${response.resume_id}`,
        'Save Complete'
      );
    } catch (err: any) {
      console.error('Error saving resume:', err);
      const errorResponse = err as ErrorResponse;
      
      showNotification(
        'error',
        errorResponse.message || 'Error saving resume',
        'Save Failed'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = () => {
    if (!resumeData) return;
    
    // In a real application, this would generate a JSON or CSV file
    // For now, we'll just log the data to the console
    const dataStr = JSON.stringify(resumeData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `${resumeData.contact_info.name.replace(/\s+/g, '_')}_resume.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  return (
    <Box sx={{ height: '100%', p: 2 }}>
      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2, height: '100%' }}>
        <Box 
          sx={{ 
            flex: { xs: '1 1 auto', md: '0 0 33%' },
            height: { xs: 'auto', md: '100%' }, 
            border: '1px solid', 
            borderColor: 'divider',
            borderRadius: 1,
            p: 2
          }}
        >
          <PDFUpload onFileUpload={handleFileUpload} />
          {isLoading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
              <CircularProgress />
              <Typography variant="body2" sx={{ ml: 2 }}>
                Processing resume...
              </Typography>
            </Box>
          )}
          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}
        </Box>
        <Box 
          sx={{ 
            flex: { xs: '1 1 auto', md: '0 0 67%' },
            height: { xs: 'auto', md: '100%' }, 
            border: '1px solid', 
            borderColor: 'divider',
            borderRadius: 1,
            overflow: 'hidden'
          }}
        >
          <ResumeSummary 
            resumeData={resumeData} 
            onExport={handleExport}
            onSave={handleSave}
          />
        </Box>
      </Box>
    </Box>
  );
};

export default SummaryPage;
