import React, { useState, useEffect } from 'react'
import { Card, CardContent, LinearProgress, Typography, Box } from '@mui/material'
import { Science } from '@mui/icons-material'

const LoadingProgress = () => {
  const [progress, setProgress] = useState(0)
  const [message, setMessage] = useState('Initializing analysis...')

  const messages = [
    'Initializing analysis...',
    'Loading image...',
    'Extracting features...',
    'Analyzing texture patterns...',
    'Computing color properties...',
    'Running ML model...',
    'Finalizing results...'
  ]

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress((oldProgress) => {
        const newProgress = oldProgress + 100 / 70 // Complete in ~7 seconds
        
        // Update message based on progress
        const messageIndex = Math.min(
          Math.floor((newProgress / 100) * messages.length),
          messages.length - 1
        )
        setMessage(messages[messageIndex])
        
        if (newProgress >= 100) {
          clearInterval(timer)
          return 100
        }
        return newProgress
      })
    }, 100)

    return () => clearInterval(timer)
  }, [])

  return (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Science sx={{ mr: 2, color: 'primary.main' }} />
          <Typography variant="h6">
            Analyzing Leaf Health...
          </Typography>
        </Box>
        
        <LinearProgress 
          variant="determinate" 
          value={progress} 
          sx={{ 
            height: 8, 
            borderRadius: 4,
            mb: 2,
            '& .MuiLinearProgress-bar': {
              borderRadius: 4,
            }
          }} 
        />
        
        <Typography variant="body2" color="text.secondary" align="center">
          {message}
        </Typography>
      </CardContent>
    </Card>
  )
}

export default LoadingProgress