import React, { useState, useEffect } from 'react';
import { 
  Autocomplete, 
  Chip, 
  TextField, 
  Paper, 
  Typography, 
  Box,
  CircularProgress
} from '@mui/material';
import { getTags } from '../../services/tagService';
import { Tag } from '../../types';

interface TagSelectorProps {
  selectedTags: Tag[];
  onChange: (tags: Tag[]) => void;
  label?: string;
  placeholder?: string;
}

// Preset tags for testing when no tags are available from API
const PRESET_TAGS: Tag[] = [
  { name: 'python' },
  { name: 'react' },
  { name: 'javascript' },
  { name: 'frontend' },
  { name: 'backend' },
  { name: 'mongodb' },
  { name: 'aws' }
];

const TagSelector: React.FC<TagSelectorProps> = ({ 
  selectedTags = [], 
  onChange, 
  label = "Tags", 
  placeholder = "Select or create tags..." 
}) => {
  const [availableTags, setAvailableTags] = useState<Tag[]>(PRESET_TAGS);
  const [loading, setLoading] = useState<boolean>(false);
  const [inputValue, setInputValue] = useState<string>('');

  // Fetch available tags from the backend
  useEffect(() => {
    const fetchTags = async () => {
      setLoading(true);
      try {
        const tags = await getTags();
        if (tags && tags.length > 0) {
          setAvailableTags(tags);
        } else {
          // Use preset tags if no tags returned from API
          console.log('No tags returned from API, using preset tags');
          setAvailableTags(PRESET_TAGS);
        }
      } catch (error) {
        console.error('Error fetching tags:', error);
        // Use preset tags on error
        setAvailableTags(PRESET_TAGS);
      } finally {
        setLoading(false);
      }
    };

    fetchTags();
  }, []);

  const handleTagChange = (_event: React.SyntheticEvent, value: (string | Tag)[]) => {
    // Convert any string values to Tag objects
    const tagObjects = value.map(item => 
      typeof item === 'string' ? { name: item } : item
    );
    
    onChange(tagObjects);
  };

  // Custom tag rendering to show each tag as a chip
  const renderTags = (value: Tag[], getTagProps: (params: { index: number }) => any) =>
    value.map((option, index) => (
      <Chip
        label={option.name}
        {...getTagProps({ index })}
        key={option.id || option.name}
        size="small"
        color="primary"
        variant="outlined"
      />
    ));

  return (
    <Box>
      <Paper elevation={0} sx={{ p: 1, mb: 2 }}>
        <Typography variant="subtitle2" sx={{ mb: 1 }}>
          {label}
        </Typography>
        <Autocomplete
          multiple
          id="tag-selector"
          options={availableTags}
          value={selectedTags}
          onChange={handleTagChange}
          inputValue={inputValue}
          onInputChange={(_event, newInputValue) => {
            setInputValue(newInputValue);
          }}
          getOptionLabel={(option) => typeof option === 'string' ? option : option.name}
          isOptionEqualToValue={(option, value) => 
            typeof option === 'string' 
              ? option === (typeof value === 'string' ? value : value.name)
              : option.name === (typeof value === 'string' ? value : value.name)
          }
          renderTags={renderTags}
          renderInput={(params) => (
            <TextField
              {...params}
              variant="outlined"
              placeholder={selectedTags.length === 0 ? placeholder : ''}
              InputProps={{
                ...params.InputProps,
                endAdornment: (
                  <React.Fragment>
                    {loading ? <CircularProgress color="inherit" size={20} /> : null}
                    {params.InputProps.endAdornment}
                  </React.Fragment>
                ),
              }}
              size="small"
              fullWidth
            />
          )}
          renderOption={(props, option) => (
            <Box component="li" {...props}>
              {typeof option === 'string' ? option : option.name}
            </Box>
          )}
          freeSolo
          clearOnBlur
          selectOnFocus
        />
      </Paper>
    </Box>
  );
};

export default TagSelector; 