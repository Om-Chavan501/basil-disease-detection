import React, { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Box, Typography, Paper } from '@mui/material'
import { CloudUpload, PhotoCamera } from '@mui/icons-material'

const ImageUploader = ({ onImageSelect }) => {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0]
      onImageSelect(null, file) // Pass null for path, file for uploaded file
    }
  }, [onImageSelect])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.bmp']
    },
    multiple: false,
    maxSize: 10485760 // 10MB
  })

  return (
    <Paper
      {...getRootProps()}
      sx={{
        p: 3,
        textAlign: 'center',
        cursor: 'pointer',
        border: '2px dashed',
        borderColor: isDragActive ? 'primary.main' : 'grey.300',
        backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
        transition: 'all 0.3s ease',
        '&:hover': {
          borderColor: 'primary.main',
          backgroundColor: 'action.hover',
        }
      }}
    >
      <input {...getInputProps()} />
      <CloudUpload sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
      
      {isDragActive ? (
        <Typography variant="h6" color="primary">
          Drop the image here...
        </Typography>
      ) : (
        <Box>
          <Typography variant="h6" gutterBottom>
            Drag & drop an image here
          </Typography>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            or click to select from your device
          </Typography>
          <Typography variant="caption" color="text.secondary">
            Supported formats: JPG, PNG, BMP (max 10MB)
          </Typography>
        </Box>
      )}
    </Paper>
  )
}

export default ImageUploader