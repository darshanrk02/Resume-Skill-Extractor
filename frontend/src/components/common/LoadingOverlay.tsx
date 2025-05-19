import React from 'react';
import { Box, CircularProgress, Typography, useTheme } from '@mui/material';
import { THEME_COLORS } from '../../config';

interface LoadingOverlayProps {
  message?: string;
  fullScreen?: boolean;
  transparent?: boolean;
}

/**
 * A reusable loading overlay component
 * Can be used as a full-screen overlay or within a container
 */
const LoadingOverlay: React.FC<LoadingOverlayProps> = ({
  message = 'Loading...',
  fullScreen = false,
  transparent = false,
}) => {
  const theme = useTheme();

  return (
    <Box
      sx={{
        position: fullScreen ? 'fixed' : 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: transparent 
          ? 'rgba(255, 255, 255, 0.7)' 
          : theme.palette.background.paper,
        zIndex: theme.zIndex.modal,
      }}
    >
      <CircularProgress 
        size={48} 
        sx={{ 
          color: THEME_COLORS.SECONDARY,
          mb: 2 
        }} 
      />
      {message && (
        <Typography variant="body1" color="textSecondary">
          {message}
        </Typography>
      )}
    </Box>
  );
};

export default LoadingOverlay;
