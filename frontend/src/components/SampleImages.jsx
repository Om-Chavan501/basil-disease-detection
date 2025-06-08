import React from 'react'
import { Grid, Card, CardMedia, CardContent, Typography, Chip, Box } from '@mui/material'
import { CheckCircle, Warning } from '@mui/icons-material'

const SampleImages = ({ images, onImageSelect, selectedImage }) => {
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

  return (
    <Grid container spacing={2}>
      {images.map((image, index) => (
        <Grid item xs={6} sm={4} key={index}>
          <Card
            sx={{
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              border: selectedImage?.path === image.path ? '2px solid' : '1px solid',
              borderColor: selectedImage?.path === image.path ? 'primary.main' : 'divider',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: 4,
              }
            }}
            onClick={() => onImageSelect(image.path)}
          >
            <CardMedia
              component="img"
              height="120"
              image={`${API_BASE_URL}${image.path}`}
              alt={image.name}
              sx={{ objectFit: 'cover' }}
            />
            <CardContent sx={{ p: 1.5 }}>
              <Typography variant="caption" component="div" gutterBottom>
                {image.name}
              </Typography>
              <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                <Chip
                  icon={image.category === 'healthy' ? <CheckCircle /> : <Warning />}
                  label={image.category}
                  color={image.category === 'healthy' ? 'success' : 'warning'}
                  size="small"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  )
}

export default SampleImages