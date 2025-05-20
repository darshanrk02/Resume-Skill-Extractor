import React, { useState, useEffect, useCallback } from 'react';
import { 
  Box, 
  CircularProgress, 
  Typography, 
  Paper, 
  Chip, 
  Stack, 
  Card, 
  CardContent, 
  CardActions,
  Button,
  Divider
} from '@mui/material';
import TagSelector from '../components/common/TagSelector';
import { ResumeData, Tag } from '../types';
import { getAllResumes } from '../services/resumeService';
import { getResumesByTags } from '../services/tagService';
import { useNotification } from '../context/NotificationContext';

const ResumeSearchPage: React.FC = () => {
  const [selectedTags, setSelectedTags] = useState<Tag[]>([]);
  const [resumes, setResumes] = useState<ResumeData[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedResume, setSelectedResume] = useState<ResumeData | null>(null);
  
  const { showNotification } = useNotification();

  // Fetch all resumes on page load
  useEffect(() => {
    const fetchResumes = async () => {
      setLoading(true);
      try {
        const data = await getAllResumes();
        setResumes(data);
      } catch (error) {
        console.error('Error fetching resumes:', error);
        showNotification('error', 'Failed to load resumes', 'Error');
      } finally {
        setLoading(false);
      }
    };

    fetchResumes();
  }, [showNotification]);

  // Create a memoized filter function to prevent unnecessary re-renders
  const filterResumesByTags = useCallback(async () => {
    if (selectedTags.length === 0) {
      // If no tags selected, fetch all resumes
      try {
        setLoading(true);
        const resumes = await getAllResumes();
        setResumes(resumes);
      } catch (error) {
        console.error('Error fetching all resumes:', error);
        showNotification('error', 'Failed to fetch all resumes', 'Error');
      } finally {
        setLoading(false);
      }
      return;
    }

    setLoading(true);
    try {
      const tagNames = selectedTags.map(tag => tag.name);
      console.log('Filtering by tags:', tagNames);
      const filteredResumes = await getResumesByTags(tagNames);
      console.log('Filtered resumes:', filteredResumes);
      setResumes(filteredResumes);
      
      // Show feedback about results
      if (filteredResumes.length === 0) {
        showNotification('info', 'No resumes matched the selected tags', 'No Results');
      } else {
        showNotification('success', `Found ${filteredResumes.length} matching resumes`, 'Results');
      }
    } catch (error) {
      console.error('Error filtering resumes by tags:', error);
      showNotification('error', 'Failed to filter resumes by tags', 'Filter Error');
      
      // Try to fall back to all resumes
      try {
        const allResumes = await getAllResumes();
        setResumes(allResumes);
      } catch (fallbackError) {
        console.error('Fallback error:', fallbackError);
      }
    } finally {
      setLoading(false);
    }
  }, [selectedTags, showNotification]);

  // Use the memoized function in the effect
  useEffect(() => {
    filterResumesByTags();
  }, [filterResumesByTags]);

  const handleTagChange = (tags: Tag[]) => {
    setSelectedTags(tags);
  };

  const handleViewDetails = (resume: ResumeData) => {
    setSelectedResume(resume);
  };

  return (
    <Box sx={{ height: '100%', p: 2, overflow: 'auto' }}>
      <Typography variant="h4" sx={{ mb: 3 }}>Resume Search</Typography>
      
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
        {/* Filter Panel */}
        <Box sx={{ 
          width: { xs: '100%', md: '280px' },
          flexShrink: 0
        }}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" sx={{ mb: 2 }}>Filter Options</Typography>
            
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" sx={{ mb: 1 }}>Filter by Tags</Typography>
              <TagSelector 
                selectedTags={selectedTags}
                onChange={handleTagChange}
                label="Tags"
                placeholder="Select or create tags..."
              />
            </Box>
          </Paper>
      </Box>
        
        {/* Results Panel */}
        <Box sx={{ 
          flexGrow: 1,
          width: { 
            xs: '100%', 
            md: selectedResume ? 'calc(100% - 630px)' : 'calc(100% - 320px)' 
          }
        }}>
          <Paper sx={{ p: 2, height: '100%', overflowY: 'auto' }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Results ({resumes.length} resume{resumes.length !== 1 ? 's' : ''})
            </Typography>

      {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
              <Stack spacing={2}>
                {resumes.map((resume, index) => (
                  <Card key={index} variant="outlined">
                  <CardContent>
                      <Typography variant="h6">
                        {resume.contact_info?.name || `Resume ${index + 1}`}
                      </Typography>
                      
                      {resume.contact_info?.email && (
                        <Typography variant="body2" color="text.secondary">
                          {resume.contact_info.email}
                    </Typography>
                      )}
                      
                      {resume.summary && (
                        <Typography variant="body2" sx={{ mt: 1, mb: 1 }}>
                          {resume.summary.length > 120 
                            ? `${resume.summary.substring(0, 120)}...` 
                            : resume.summary}
                    </Typography>
                      )}
                      
                      {resume.skills && resume.skills.length > 0 && (
                    <Box sx={{ mt: 1 }}>
                          <Typography variant="subtitle2">Skills:</Typography>
                          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                            {resume.skills.slice(0, 8).map((skill, i) => (
                        <Chip 
                                key={i} 
                                label={skill.name} 
                          size="small" 
                                variant="outlined" 
                        />
                      ))}
                            {resume.skills.length > 8 && (
                        <Chip 
                                label={`+${resume.skills.length - 8} more`} 
                          size="small"
                          variant="outlined"
                        />
                      )}
                    </Box>
                        </Box>
                      )}
                      
                      {resume.tags && resume.tags.length > 0 && (
                        <Box sx={{ mt: 1 }}>
                          <Typography variant="subtitle2">Tags:</Typography>
                          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                            {resume.tags.map((tag, i) => (
                              <Chip 
                                key={i} 
                                label={tag.name} 
                                size="small" 
                                color="primary"
                                variant="outlined" 
                              />
                            ))}
                          </Box>
                        </Box>
                      )}
                    </CardContent>
                    <CardActions>
                      <Button 
                        size="small" 
                        onClick={() => handleViewDetails(resume)}
                      >
                        View Details
                      </Button>
                    </CardActions>
                  </Card>
                ))}
                
                {resumes.length === 0 && !loading && (
                  <Box sx={{ p: 3, textAlign: 'center' }}>
                    <Typography variant="body1" color="text.secondary">
                      No resumes found matching your filters.
                    </Typography>
                  </Box>
                )}
              </Stack>
            )}
          </Paper>
        </Box>
        
        {/* Details Panel */}
        {selectedResume && (
          <Box sx={{ 
            width: { xs: '100%', md: '300px' },
            flexShrink: 0
          }}>
            <Paper sx={{ p: 2, height: '100%', overflowY: 'auto' }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">Resume Details</Typography>
                <Button size="small" onClick={() => setSelectedResume(null)}>Close</Button>
              </Box>
              
              <Divider sx={{ mb: 2 }} />
              
              <Typography variant="h5" sx={{ mb: 1 }}>
                {selectedResume.contact_info?.name || 'Unnamed Resume'}
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                {selectedResume.contact_info?.email && (
                  <Typography variant="body2">
                    Email: {selectedResume.contact_info.email}
                  </Typography>
                )}
                {selectedResume.contact_info?.phone && (
                  <Typography variant="body2">
                    Phone: {selectedResume.contact_info.phone}
                  </Typography>
                )}
                {selectedResume.contact_info?.location && (
                  <Typography variant="body2">
                    Location: {selectedResume.contact_info.location}
                  </Typography>
                )}
              </Box>
              
              {selectedResume.summary && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle1">Summary</Typography>
                  <Typography variant="body2">{selectedResume.summary}</Typography>
                </Box>
              )}
              
              {selectedResume.skills && selectedResume.skills.length > 0 && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle1">Skills</Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                    {selectedResume.skills.map((skill, i) => (
                      <Chip 
                        key={i} 
                        label={skill.name} 
                        size="small" 
                        variant="outlined" 
                      />
                    ))}
                  </Box>
                </Box>
              )}
              
              {selectedResume.experience && selectedResume.experience.length > 0 && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle1">Experience</Typography>
                  <Stack spacing={1} sx={{ mt: 1 }}>
                    {selectedResume.experience.map((exp, i) => (
                      <Box key={i}>
                        <Typography variant="subtitle2">{exp.position} at {exp.company}</Typography>
                        <Typography variant="body2" color="text.secondary">
                          {exp.start_date} - {exp.end_date || 'Present'}
                        </Typography>
                        {exp.description && (
                          <Typography variant="body2">{exp.description}</Typography>
                        )}
                      </Box>
                    ))}
                  </Stack>
                </Box>
              )}
              
              {selectedResume.education && selectedResume.education.length > 0 && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle1">Education</Typography>
                  <Stack spacing={1} sx={{ mt: 1 }}>
                    {selectedResume.education.map((edu, i) => (
                      <Box key={i}>
                        <Typography variant="subtitle2">{edu.degree} in {edu.field_of_study}</Typography>
                        <Typography variant="body2">{edu.institution}</Typography>
                        <Typography variant="body2" color="text.secondary">
                          {edu.start_date} - {edu.end_date}
                        </Typography>
                      </Box>
                    ))}
                  </Stack>
                </Box>
              )}
            </Paper>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default ResumeSearchPage;