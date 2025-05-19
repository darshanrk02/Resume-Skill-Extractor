import React from 'react';
import { Box, Typography, Paper, List, ListItem, ListItemText, Divider } from '@mui/material';

const ProfilePage: React.FC = () => {
  return (
    <Box sx={{ height: '100%', p: 3, overflow: 'auto' }}>
      <Typography variant="h5" sx={{ mb: 3 }}>User Profile</Typography>
      
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>Account Information</Typography>
        <List>
          <ListItem>
            <ListItemText primary="Name" secondary="User Name" />
          </ListItem>
          <Divider />
          <ListItem>
            <ListItemText primary="Email" secondary="user@example.com" />
          </ListItem>
          <Divider />
          <ListItem>
            <ListItemText primary="Account Type" secondary="Premium" />
          </ListItem>
        </List>
      </Paper>
      
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>Usage Statistics</Typography>
        <List>
          <ListItem>
            <ListItemText primary="Resumes Uploaded" secondary="5" />
          </ListItem>
          <Divider />
          <ListItem>
            <ListItemText primary="Job Descriptions Analyzed" secondary="12" />
          </ListItem>
          <Divider />
          <ListItem>
            <ListItemText primary="Last Activity" secondary="May 17, 2025" />
          </ListItem>
        </List>
      </Paper>
      
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>Preferences</Typography>
        <List>
          <ListItem>
            <ListItemText 
              primary="Default Export Format" 
              secondary="JSON" 
            />
          </ListItem>
          <Divider />
          <ListItem>
            <ListItemText 
              primary="Skills Highlighting" 
              secondary="Enabled" 
            />
          </ListItem>
          <Divider />
          <ListItem>
            <ListItemText 
              primary="AI Recommendations" 
              secondary="Enabled" 
            />
          </ListItem>
        </List>
      </Paper>
    </Box>
  );
};

export default ProfilePage;
