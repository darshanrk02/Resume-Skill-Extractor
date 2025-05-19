import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1f2d3d',
    },
    secondary: {
      main: '#4a90e2',
    },
    success: {
      main: '#28a745',
    },
    background: {
      default: '#f4f6f9',
      paper: '#ffffff',
    },
    text: {
      primary: '#4a4a4a',
      secondary: '#666666',
    },
  },
  typography: {
    fontFamily: '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
    h1: {
      fontSize: '1.5rem',
      fontWeight: 600,
    },
    h2: {
      fontSize: '1.25rem',
      fontWeight: 600,
    },
    h3: {
      fontSize: '1.1rem',
      fontWeight: 600,
    },
    body1: {
      fontSize: '0.9rem',
    },
    body2: {
      fontSize: '0.8rem',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
        },
      },
    },
  },
});

export default theme;
