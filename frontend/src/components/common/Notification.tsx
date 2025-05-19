import React from 'react';
import { Snackbar, Alert, AlertProps, AlertTitle } from '@mui/material';
import { THEME_COLORS, UI_CONFIG } from '../../config';

export type NotificationType = 'success' | 'error' | 'info' | 'warning';

export interface NotificationProps {
  open: boolean;
  type: NotificationType;
  message: string;
  title?: string;
  autoHideDuration?: number;
  onClose: () => void;
}

/**
 * Reusable notification component using Material UI's Snackbar and Alert
 */
const Notification: React.FC<NotificationProps> = ({
  open,
  type,
  message,
  title,
  autoHideDuration = UI_CONFIG.SNACKBAR_DURATION,
  onClose,
}) => {
  // Map notification type to color
  const getColor = (): AlertProps['color'] => {
    switch (type) {
      case 'success':
        return 'success';
      case 'error':
        return 'error';
      case 'warning':
        return 'warning';
      case 'info':
        return 'info';
      default:
        return 'info';
    }
  };

  return (
    <Snackbar
      open={open}
      autoHideDuration={autoHideDuration}
      onClose={onClose}
      anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
    >
      <Alert 
        onClose={onClose} 
        severity={type} 
        color={getColor()}
        variant="filled"
        sx={{ 
          width: '100%',
          boxShadow: 3,
          '& .MuiAlert-icon': {
            fontSize: '1.25rem'
          }
        }}
      >
        {title && <AlertTitle>{title}</AlertTitle>}
        {message}
      </Alert>
    </Snackbar>
  );
};

export default Notification;
