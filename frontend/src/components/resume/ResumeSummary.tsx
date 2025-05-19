import React from 'react';
import { Box, Typography, Paper, Chip, Button } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import { useTheme } from '@mui/material/styles';

import { ResumeData, Skill, Project, Education, WorkExperience } from '../../types';

interface ResumeSummaryProps {
  resumeData: ResumeData | null;
  onExport: () => void;
}

const ResumeSummary: React.FC<ResumeSummaryProps> = ({ resumeData, onExport }) => {
  const theme = useTheme();

  if (!resumeData) {
    return (
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100%',
        p: 3
      }}>
        <Typography variant="body1" color="textSecondary">
          Upload a resume to see the extracted information here.
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      height: '100%',
      overflow: 'hidden'
    }}>
      {/* Header with contact info */}
      <Box sx={{ 
        borderBottom: `1px solid ${theme.palette.divider}`,
        p: 2,
        textAlign: 'center'
      }}>
        <Typography variant="h4" sx={{ fontWeight: 'bold', color: theme.palette.primary.main }}>
          {resumeData.contact_info.name}
        </Typography>
        <Typography variant="body1" color="textSecondary">
          {resumeData.contact_info.name}
        </Typography>
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'center', 
          gap: 1, 
          mt: 0.5,
          flexWrap: 'wrap',
          color: theme.palette.text.secondary,
          fontSize: '0.875rem'
        }}>
          <Typography variant="body2">{resumeData.contact_info.location}</Typography>
          <Typography variant="body2">|</Typography>
          <Typography 
            variant="body2" 
            component="a" 
            href={`mailto:${resumeData.contact_info.email}`}
            sx={{ 
              color: theme.palette.secondary.main, 
              textDecoration: 'none',
              '&:hover': { textDecoration: 'underline' }
            }}
          >
            {resumeData.contact_info.email}
          </Typography>
          <Typography variant="body2">|</Typography>
          <Typography 
            variant="body2" 
            component="a" 
            href={`tel:${resumeData.contact_info.phone}`}
            sx={{ 
              color: theme.palette.secondary.main, 
              textDecoration: 'none',
              '&:hover': { textDecoration: 'underline' }
            }}
          >
            {resumeData.contact_info.phone}
          </Typography>
        </Box>
      </Box>

      {/* Scrollable content */}
      <Box sx={{ 
        flex: 1, 
        overflowY: 'auto',
        p: 1
      }}>
        {/* Professional Summary */}
        <Paper sx={{ 
          p: 2, 
          m: 1, 
          border: `1px solid ${theme.palette.divider}`
        }}>
          <Typography 
            variant="h6" 
            sx={{ 
              borderLeft: `4px solid ${theme.palette.secondary.main}`,
              pl: 1.5,
              mb: 1.5,
              color: theme.palette.primary.main
            }}
          >
            Professional Summary
          </Typography>
          <Typography variant="body1" color="textPrimary">
            {resumeData.summary}
          </Typography>
        </Paper>

        {/* Skills */}
        <Paper sx={{ 
          p: 2, 
          m: 1, 
          border: `1px solid ${theme.palette.divider}`
        }}>
          <Typography 
            variant="h6" 
            sx={{ 
              borderLeft: `4px solid ${theme.palette.secondary.main}`,
              pl: 1.5,
              mb: 1.5,
              color: theme.palette.primary.main
            }}
          >
            Skills
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {resumeData.skills.map((skill, index) => (
              <Chip 
                key={index} 
                label={skill.name} 
                sx={{ 
                  backgroundColor: '#e6f0fb',
                  color: '#1e3a8a',
                  fontWeight: 500,
                  fontSize: '0.8rem'
                }} 
              />
            ))}
          </Box>
        </Paper>

        {/* Projects */}
        <Paper sx={{ 
          p: 2, 
          m: 1, 
          border: `1px solid ${theme.palette.divider}`
        }}>
          <Typography 
            variant="h6" 
            sx={{ 
              borderLeft: `4px solid ${theme.palette.secondary.main}`,
              pl: 1.5,
              mb: 1.5,
              color: theme.palette.primary.main
            }}
          >
            Projects
          </Typography>
          {resumeData.projects.map((project, index) => (
            <Box key={index} sx={{ mb: index !== resumeData.projects.length - 1 ? 2 : 0 }}>
              <Typography 
                variant="subtitle1" 
                sx={{ 
                  fontWeight: 'bold',
                  color: theme.palette.text.primary,
                  mb: 0.5
                }}
              >
                {project.title}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {project.description}
              </Typography>
            </Box>
          ))}
        </Paper>

        {/* Experience */}
        <Paper sx={{ 
          p: 2, 
          m: 1, 
          border: `1px solid ${theme.palette.divider}`
        }}>
          <Typography 
            variant="h6" 
            sx={{ 
              borderLeft: `4px solid ${theme.palette.secondary.main}`,
              pl: 1.5,
              mb: 1.5,
              color: theme.palette.primary.main
            }}
          >
            Professional Experience
          </Typography>
          {resumeData?.experience?.map((exp: WorkExperience, index: number) => (
            <Box key={index} sx={{ mb: index !== (resumeData?.experience?.length || 0) - 1 ? 2 : 0 }}>
              <Typography variant="subtitle2" color="textSecondary" sx={{ mb: 0.5 }}>
                {exp.company}
              </Typography>
              <Typography variant="subtitle1" sx={{ fontWeight: 'bold', color: theme.palette.text.primary }}>
                {exp.position}
              </Typography>
              <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
                {exp.start_date} - {exp.end_date || 'Present'}
              </Typography>
              {exp.description.split('\n').map((point: string, i: number) => (
                point.trim() && (
                  <Typography key={i} variant="body2" sx={{ 
                    display: 'flex',
                    alignItems: 'flex-start',
                    mt: 0.5
                  }}>
                    <span style={{ 
                      minWidth: '6px',
                      height: '6px',
                      borderRadius: '50%',
                      backgroundColor: theme.palette.text.secondary,
                      marginRight: '8px',
                      marginTop: '8px'
                    }} />
                    {point.trim()}
                  </Typography>
                )
              ))}
            </Box>
          ))}
          {(!resumeData?.experience || resumeData.experience.length === 0) && (
            <Typography variant="body2" color="textSecondary">
              No work experience listed.
            </Typography>
          )}
        </Paper>

        {/* Education */}
        <Paper sx={{ 
          p: 2, 
          m: 1, 
          border: `1px solid ${theme.palette.divider}`
        }}>
          <Typography 
            variant="h6" 
            sx={{ 
              borderLeft: `4px solid ${theme.palette.secondary.main}`,
              pl: 1.5,
              mb: 1.5,
              color: theme.palette.primary.main
            }}
          >
            Education
          </Typography>
          {resumeData.education.map((edu, index) => (
            <Box key={index} sx={{ mb: index !== resumeData.education.length - 1 ? 2 : 0 }}>
              <Typography variant="subtitle1" sx={{ fontWeight: 'bold', color: theme.palette.text.primary }}>
                {edu.degree} in {edu.field_of_study}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {edu.institution}
              </Typography>

              <Typography variant="body2" color="textSecondary">
                {edu.start_date} - {edu.end_date}
                {edu.gpa && ` • GPA: ${edu.gpa}`}
              </Typography>
            </Box>
          ))}
          {resumeData.education.length === 0 && (
            <Typography variant="body2" color="textSecondary">
              No education listed.
            </Typography>
          )}
        </Paper>
      </Box>

      {/* Export button */}
      <Box sx={{ 
        p: 1.5, 
        borderTop: `1px solid ${theme.palette.divider}`,
        display: 'flex',
        justifyContent: 'flex-end'
      }}>
        <Button 
          variant="contained" 
          color="success" 
          startIcon={<DownloadIcon />}
          onClick={onExport}
        >
          Export
        </Button>
      </Box>
    </Box>
  );
};

export default ResumeSummary;
