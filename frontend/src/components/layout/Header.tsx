import React from 'react';
import { AppBar, Toolbar, Typography, Box, Tab, Tabs, useTheme } from '@mui/material';
import { Link, useLocation } from 'react-router-dom';
import DescriptionIcon from '@mui/icons-material/Description';

interface HeaderProps {
  title?: string;
}

const Header: React.FC<HeaderProps> = ({ title = 'Resume Skill Extractor' }) => {
  const theme = useTheme();
  const location = useLocation();
  const [value, setValue] = React.useState(0);

  React.useEffect(() => {
    if (location.pathname === '/') setValue(0);
    else if (location.pathname === '/jd-matching') setValue(1);
    else if (location.pathname === '/profile') setValue(2);
    else if (location.pathname.startsWith('/resumes')) setValue(3);
  }, [location.pathname]);

  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <AppBar position="sticky" sx={{ backgroundColor: theme.palette.primary.main }}>
      <Toolbar variant="dense" sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Box display="flex" alignItems="center">
          <DescriptionIcon sx={{ mr: 1 }} />
          <Typography variant="h6" component="div" sx={{ fontWeight: 'bold' }}>
            {title}
          </Typography>
        </Box>
        <Tabs 
          value={value} 
          onChange={handleChange} 
          textColor="inherit"
          TabIndicatorProps={{ style: { display: 'none' } }}
          sx={{ 
            '& .MuiTab-root': {
              borderRadius: '8px 8px 0 0',
              minHeight: '40px',
              backgroundColor: 'rgba(255, 255, 255, 0.1)',
              marginRight: '5px',
              '&.Mui-selected': {
                backgroundColor: 'white',
                color: theme.palette.primary.main,
              },
              '&:hover:not(.Mui-selected)': {
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
              }
            }
          }}
        >
          <Tab label="Summary View" component={Link} to="/" />
          <Tab label="JD Matching" component={Link} to="/jd-matching" />
          <Tab label="Resume Search" component={Link} to="/resumes" />
          <Tab label="Profile" component={Link} to="/profile" />
        </Tabs>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
