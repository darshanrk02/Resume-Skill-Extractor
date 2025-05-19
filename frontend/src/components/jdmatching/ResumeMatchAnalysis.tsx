import React from 'react';
import { Box, Typography, Chip, CircularProgress } from '@mui/material';

interface MatchedSkill {
  skill: string;
  matched: boolean;
  weight: number;
}

interface UIResumeMatch {
  resumeId: string;
  name: string;
  title: string;
  matchPercentage: number;
  matchedSkills: MatchedSkill[];
  missingSkills: MatchedSkill[];
  recommendation: string;
  confidenceLevel: 'high' | 'medium' | 'low';
  analysis: string;
}

interface ResumeMatchAnalysisProps {
  match: UIResumeMatch;
}

const ResumeMatchAnalysis: React.FC<ResumeMatchAnalysisProps> = ({ match }) => {
  const getConfidenceColor = (level: string): string => {
    switch (level) {
      case 'high':
        return '#4caf50';
      case 'medium':
        return '#ff9800';
      case 'low':
        return '#f44336';
      default:
        return '#757575';
    }
  };

  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      height: '100%',
      p: 3,
      overflow: 'auto'
    }}>
      {/* Header with name and title */}
      <Box sx={{ 
        mb: 3,
        pb: 2,
        borderBottom: '1px solid',
        borderColor: 'divider'
      }}>
        <Typography variant="h5" component="div" sx={{ mb: 1 }}>
          {match.name}
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          {match.title}
        </Typography>
      </Box>

      {/* Match percentage and recommendation */}
      <Box sx={{ 
        display: 'flex', 
        flexDirection: { xs: 'column', md: 'row' }, 
        gap: 4,
        mb: 4,
        alignItems: 'flex-start'
      }}>
        <Box sx={{ 
          position: 'relative', 
          display: 'inline-flex',
          alignSelf: 'center',
          mb: { xs: 2, md: 0 }
        }}>
          <CircularProgress
            variant="determinate"
            value={match.matchPercentage}
            size={120}
            thickness={4}
            sx={{
              color: getConfidenceColor(match.confidenceLevel),
              backgroundColor: 'background.default',
              borderRadius: '50%',
              p: 0.5
            }}
          />
          <Box sx={{
            top: 0,
            left: 0,
            bottom: 0,
            right: 0,
            position: 'absolute',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            textAlign: 'center'
          }}>
            <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
              {`${Math.round(match.matchPercentage)}%`}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Match Score
            </Typography>
          </Box>
        </Box>


        <Box sx={{ flex: 1 }}>
          <Typography variant="h6" gutterBottom>
            {match.recommendation}
          </Typography>
          <Typography 
            variant="body1" 
            color="text.secondary" 
            sx={{ 
              whiteSpace: 'pre-line',
              lineHeight: 1.6
            }}
          >
            {match.analysis}
          </Typography>
        </Box>
      </Box>

      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 3 }}>
        {/* Matched Skills */}
        <Box>
          <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'medium' }}>
            Matched Skills
          </Typography>
          <Box sx={{ 
            display: 'flex', 
            flexWrap: 'wrap', 
            gap: 1,
            '& .MuiChip-root': {
              borderRadius: 1,
              fontWeight: 'medium'
            }
          }}>
            {match.matchedSkills.map((skill: MatchedSkill, index: number) => (
              <Chip
                key={index}
                label={`${skill.skill} (${Math.round(skill.weight * 100)}%)`}
                color="primary"
                variant="filled"
                size="small"
              />
            ))}
          </Box>
        </Box>

        {/* Missing Skills */}
        {match.missingSkills.length > 0 && (
          <Box>
            <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'medium' }}>
              Missing Skills
            </Typography>
            <Box sx={{ 
              display: 'flex', 
              flexWrap: 'wrap', 
              gap: 1,
              '& .MuiChip-root': {
                borderRadius: 1,
                fontWeight: 'medium'
              }
            }}>
              {match.missingSkills.map((skill: MatchedSkill, index: number) => (
                <Chip
                  key={index}
                  label={skill.skill}
                  color="error"
                  variant="outlined"
                  size="small"
                />
              ))}
            </Box>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default ResumeMatchAnalysis;
