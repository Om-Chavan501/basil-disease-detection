import React from 'react'
import { FormControl, InputLabel, Select, MenuItem, Chip, Box, Typography } from '@mui/material'
import { Psychology, Speed, TrendingUp } from '@mui/icons-material'

const ModelSelector = ({ models, selectedModel, onModelChange }) => {
  const getModelIcon = (modelName) => {
    switch (modelName) {
      case 'random_forest':
        return <Psychology />
      case 'svm':
        return <TrendingUp />
      case 'knn':
        return <Speed />
      default:
        return <Psychology />
    }
  }

  const getModelColor = (modelName) => {
    switch (modelName) {
      case 'random_forest':
        return 'primary'
      case 'svm':
        return 'secondary'
      case 'knn':
        return 'info'
      default:
        return 'primary'
    }
  }

  const getModelDescription = (modelName) => {
    switch (modelName) {
      case 'random_forest':
        return 'Ensemble method using multiple decision trees. Best overall performance.'
      case 'svm':
        return 'Support Vector Machine with advanced pattern recognition capabilities.'
      case 'knn':
        return 'Instance-based learning algorithm. Fast and simple classification.'
      default:
        return 'Machine learning model for plant disease detection.'
    }
  }

  return (
    <Box>
      <FormControl fullWidth>
        <InputLabel>Machine Learning Model</InputLabel>
        <Select
          value={selectedModel}
          label="Machine Learning Model"
          onChange={(e) => onModelChange(e.target.value)}
        >
          {models.map((model) => (
            <MenuItem key={model.name} value={model.name}>
              <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                {getModelIcon(model.name)}
                <Box sx={{ ml: 2, flexGrow: 1 }}>
                  <Typography variant="body1">
                    {model.name.replace('_', ' ').toUpperCase()}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {model.description}
                  </Typography>
                </Box>
                {model.accuracy && (
                  <Chip
                    label={`${(model.accuracy * 100).toFixed(1)}%`}
                    color={getModelColor(model.name)}
                    size="small"
                  />
                )}
              </Box>
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      
      {selectedModel && models.find(m => m.name === selectedModel) && (
        <Box sx={{ mt: 2, p: 2, backgroundColor: '#F8F9FA', borderRadius: 1 }}>
          <Typography variant="body2" color="text.secondary">
            <strong>Selected:</strong> {getModelDescription(selectedModel)}
          </Typography>
          {selectedModel === 'knn' && (
            <Typography variant="caption" color="info.main" sx={{ display: 'block', mt: 1 }}>
              💡 KNN works by finding the k most similar training examples and making predictions based on their labels.
            </Typography>
          )}
        </Box>
      )}
    </Box>
  )
}

export default ModelSelector