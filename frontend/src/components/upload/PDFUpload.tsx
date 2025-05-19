import React, { useState, useCallback } from 'react';
import { Box, Typography, Button, Paper, Alert } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import { useTheme } from '@mui/material/styles';
import { validatePdfFile, formatFileSize } from '../../utils/fileValidation';
import { useNotification } from '../../context/NotificationContext';

interface PDFUploadProps {
  onFileUpload: (file: File) => void;
}

const PDFUpload: React.FC<PDFUploadProps> = ({ onFileUpload }) => {
  const theme = useTheme();
  const { showNotification } = useNotification();
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);
  
  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);
  
  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    setValidationError(null);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      const validation = validatePdfFile(file);
      
      if (validation.isValid) {
        setSelectedFile(file);
        showNotification('info', `File "${file.name}" ready for upload`, 'File Selected');
      } else {
        setValidationError(validation.error || 'Invalid file');
        showNotification('error', validation.error || 'Invalid file', 'File Error');
      }
    }
  }, [showNotification]);
  
  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setValidationError(null);
    
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const validation = validatePdfFile(file);
      
      if (validation.isValid) {
        setSelectedFile(file);
        showNotification('info', `File "${file.name}" ready for upload`, 'File Selected');
      } else {
        setValidationError(validation.error || 'Invalid file');
        showNotification('error', validation.error || 'Invalid file', 'File Error');
      }
    }
  }, [showNotification]);
  
  const handleBrowseClick = useCallback(() => {
    document.getElementById('file-upload')?.click();
  }, []);
  
  const handleUpload = useCallback(() => {
    if (selectedFile) {
      setValidationError(null);
      onFileUpload(selectedFile);
    } else {
      alert('Please select a file first');
    }
  }, [selectedFile, onFileUpload]);
  
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <Typography 
        variant="h2" 
        sx={{ 
          textAlign: 'center', 
          mb: 2, 
          color: theme.palette.primary.main 
        }}
      >
        PDF Resume Upload
      </Typography>
      
      <Paper
        elevation={0}
        sx={{
          border: '2px dashed',
          borderColor: dragActive ? theme.palette.secondary.main : theme.palette.divider,
          borderRadius: 2,
          backgroundColor: dragActive ? 'rgba(74, 144, 226, 0.05)' : 'white',
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          mb: 2,
          cursor: 'pointer',
          transition: 'all 0.3s',
          '&:hover': {
            borderColor: theme.palette.secondary.main,
            backgroundColor: 'rgba(74, 144, 226, 0.05)',
          },
          p: 2
        }}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleBrowseClick}
      >
        <input
          type="file"
          id="file-upload"
          accept="application/pdf"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        <CloudUploadIcon 
          sx={{ 
            fontSize: 60, 
            color: dragActive ? theme.palette.secondary.main : '#aaa',
            mb: 2
          }} 
        />
        <Typography align="center" sx={{ color: '#666' }}>
          Drag and drop a PDF file here,<br />
          or <span style={{ color: theme.palette.secondary.main, fontWeight: 600 }}>browse</span>
        </Typography>
        {validationError && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {validationError}
          </Alert>
        )}
        
        {selectedFile && (
          <Box sx={{ 
            textAlign: 'center', 
            mt: 2,
            p: 2,
            border: '1px solid',
            borderColor: 'divider',
            borderRadius: 1,
            bgcolor: 'background.paper'
          }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 1 }}>
              <InsertDriveFileIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="body1" fontWeight="medium">
                {selectedFile.name}
              </Typography>
            </Box>
            
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Size: {formatFileSize(selectedFile.size)}
            </Typography>
            
            <Button
              variant="contained"
              color="primary"
              onClick={handleUpload}
              startIcon={<CloudUploadIcon />}
              fullWidth
            >
              Upload and Process
            </Button>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default PDFUpload;
