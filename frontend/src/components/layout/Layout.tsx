import React from 'react';
import { Box, Container, Paper } from '@mui/material';
import Header from './Header';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      minHeight: '100vh',
      backgroundColor: 'background.default'
    }}>
      <Header />
      <Container maxWidth="xl" sx={{ flex: 1, py: 2 }}>
        <Paper 
          sx={{ 
            borderRadius: '0 0 8px 8px', 
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
            height: 'calc(100vh - 64px - 16px)', // 64px header height, 16px for padding
            overflow: 'hidden',
            display: 'flex',
            flexDirection: 'column'
          }}
        >
          {children}
        </Paper>
      </Container>
    </Box>
  );
};

export default Layout;
