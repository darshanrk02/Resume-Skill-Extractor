import React, { useState, useRef, ChangeEvent } from 'react';
import { 
  Box, 
  Typography, 
  TextField, 
  Button, 
  CircularProgress,
  Paper,
  IconButton,
  Stack,
  Avatar,
  Tooltip
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import ClearIcon from '@mui/icons-material/Clear';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DescriptionIcon from '@mui/icons-material/Description';
import DeleteIcon from '@mui/icons-material/Delete';
import { JobDescription } from '../../types/jdMatching';

interface JobDescriptionInputProps {
  onAnalyze: (jobDescription: JobDescription, resumeFile: File | null) => Promise<void>;
  onClear: () => void;
  isLoading: boolean;
  onResumeUpload: (file: File) => Promise<void>;
  uploadedResume: File | null;
  onRemoveResume: () => void;
}

const JobDescriptionInput: React.FC<JobDescriptionInputProps> = ({ 
  onAnalyze, 
  onClear, 
  isLoading, 
  onResumeUpload,
  uploadedResume,
  onRemoveResume
}) => {
  const [jobDescriptionText, setJobDescriptionText] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleTextChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setJobDescriptionText(event.target.value);
  };

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    
    // Check file type
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!validTypes.includes(file.type)) {
      alert('Please upload a PDF or Word document');
      return;
    }
    
    // Check file size (max 5MB)
    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
      alert('File size should be less than 5MB');
      return;
    }
    
    try {
      await onResumeUpload(file);
      // Reset file input to allow re-uploading the same file
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Failed to upload resume. Please try again.');
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const parseJobDescription = (text: string): { title: string; company: string; text: string } => {
    // Simple parsing to extract job title and company from the text
    const lines = text.split('\n').filter(line => line.trim() !== '');
    let title = 'Job Position';
    let company = 'Company';
    
    // Try to extract title and company from the first few lines
    if (lines.length > 0) {
      const firstLine = lines[0].trim();
      // Check if first line looks like a title (e.g., "Senior Software Engineer at Tech Corp")
      const titleMatch = firstLine.match(/(.+?)\s+(?:at|@|\|\s*)(.+)/i);
      if (titleMatch) {
        title = titleMatch[1].trim();
        company = titleMatch[2].trim();
      } else if (firstLine.length < 50) {  // If it's a short line, assume it's a title
        title = firstLine;
        if (lines.length > 1 && lines[1].trim().length < 50) {
          company = lines[1].trim();
        }
      }
    }
    
    return {
      title,
      company,
      text: jobDescriptionText
    };
  };

  const handleAnalyze = async () => {
    if (jobDescriptionText.trim() === '') {
      alert('Please enter job requirements or paste a job description');
      return;
    }

    if (!uploadedResume) {
      alert('Please upload a resume');
      return;
    }

    try {
      const parsedJD = parseJobDescription(jobDescriptionText);
      console.log('Analyzing with job description:', parsedJD);
      await onAnalyze(parsedJD, uploadedResume);
    } catch (error) {
      console.error('Error analyzing job description:', error);
      alert('Failed to analyze job description. Please check the console for details.');
    }
  };

  const handleClear = () => {
    setJobDescriptionText('');
    onClear();
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    const files = e.dataTransfer.files;
    if (!files || files.length === 0) return;
    
    // Only process the first file
    const file = files[0];
    
    // Check file type
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!validTypes.includes(file.type)) {
      alert('Please upload a PDF or Word document');
      return;
    }
    
    // Check file size (max 5MB)
    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
      alert('File size should be less than 5MB');
      return;
    }
    
    try {
      await onResumeUpload(file);
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Failed to upload resume. Please try again.');
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Resume Upload Section */}
      <Paper 
        variant="outlined" 
        sx={{ 
          m: 2, 
          p: 2, 
          borderRadius: 1,
          border: '2px dashed',
          borderColor: 'divider',
          backgroundColor: 'background.paper',
          '&:hover': {
            borderColor: 'primary.main',
            cursor: 'pointer',
            '& .upload-icon': {
              color: 'primary.main'
            }
          }
        }}
        onClick={handleUploadClick}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".pdf,.doc,.docx"
          style={{ display: 'none' }}
        />
        
        {!uploadedResume ? (
          <Box sx={{ textAlign: 'center', py: 3 }}>
            <CloudUploadIcon 
              className="upload-icon" 
              sx={{ fontSize: 48, color: 'text.secondary', mb: 1 }} 
            />
            <Typography variant="subtitle1" gutterBottom>
              Upload Resume
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Drag & drop a file here or click to browse
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
              Supported formats: PDF, DOC, DOCX
            </Typography>
          </Box>
        ) : (
          <Stack direction="row" spacing={2} alignItems="center">
            <Avatar sx={{ bgcolor: 'primary.light' }}>
              <DescriptionIcon />
            </Avatar>
            <Box sx={{ flex: 1, minWidth: 0 }}>
              <Typography noWrap>{uploadedResume.name}</Typography>
              <Typography variant="caption" color="text.secondary">
                {formatFileSize(uploadedResume.size)}
              </Typography>
            </Box>
            <IconButton 
              size="small" 
              onClick={(e) => {
                e.stopPropagation();
                onRemoveResume();
              }}
              disabled={isLoading}
            >
              <DeleteIcon fontSize="small" />
            </IconButton>
          </Stack>
        )}
      </Paper>

      {/* Job Description Section */}
      <Box sx={{ 
        p: 2, 
        borderBottom: '1px solid', 
        borderColor: 'divider',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        bgcolor: 'background.default'
      }}>
        <Typography variant="h6" component="div">
          Job Description
        </Typography>
        <Tooltip title="Clear all">
          <IconButton 
            size="small" 
            onClick={handleClear}
            disabled={isLoading || (!jobDescriptionText && !uploadedResume)}
          >
            <ClearIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      </Box>
      
      <Box sx={{ 
        flex: 1, 
        p: 2,
        overflow: 'auto',
        display: 'flex',
        flexDirection: 'column',
        bgcolor: 'background.paper',
        gap: 2
      }}>
        <TextField
          multiline
          fullWidth
          placeholder="Paste job description here..."
          value={jobDescriptionText}
          onChange={handleTextChange}
          variant="outlined"
          disabled={isLoading}
          minRows={15}
          maxRows={20}
          sx={{ 
            flex: 1,
            '& .MuiOutlinedInput-root': {
              height: '100%',
              '& textarea': {
                minHeight: '200px',
                boxSizing: 'border-box',
                resize: 'vertical',
                lineHeight: 1.5,
                fontSize: '0.875rem'
              }
            }
          }}
        />
      </Box>
      
      <Box sx={{ 
        p: 2, 
        borderTop: '1px solid', 
        borderColor: 'divider',
        display: 'flex',
        justifyContent: 'flex-end',
        gap: 2,
        bgcolor: 'background.default'
      }}>
        <Button
          variant="outlined"
          onClick={handleClear}
          disabled={isLoading || (!jobDescriptionText && !uploadedResume)}
          startIcon={<ClearIcon />}
        >
          Clear
        </Button>
        <Button
          variant="contained"
          onClick={handleAnalyze}
          disabled={isLoading || !jobDescriptionText || !uploadedResume}
          startIcon={isLoading ? <CircularProgress size={20} /> : <PlayArrowIcon />}
          sx={{ minWidth: 120 }}
        >
          {isLoading ? 'Analyzing...' : 'Analyze'}
        </Button>
      </Box>
    </Box>
  );
};

export default JobDescriptionInput;
