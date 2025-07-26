import React from 'react';
import { Button, Box, Typography } from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';

const FileUpload = ({ file, setFile }) => {
  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  return (
    <Box>
      <Button
        variant="outlined"
        component="label"
        startIcon={<UploadFileIcon />}
      >
        {file ? 'Change File' : 'Upload File'}
        <input
          type="file"
          accept="image/*,video/*"
          hidden
          onChange={handleChange}
        />
      </Button>
      {file && (
        <Typography variant="body2" mt={1}>
          Selected: {file.name}
        </Typography>
      )}
    </Box>
  );
};

export default FileUpload;
