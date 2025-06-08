import React from 'react'
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Box,
  Chip,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Paper,
} from '@mui/material'
import {
  CheckCircle,
  Warning,
  Error,
  LocalHospital,
  Science,
  Timer,
  Info,
} from '@mui/icons-material'

const PredictionResults = ({ prediction }) => {
  if (!prediction.success) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        <Typography variant="h6">Analysis Failed</Typography>
        <Typography>{prediction.message}</Typography>
      </Alert>
    )
  }

  const diseaseInfo = prediction.disease_info
  const isHealthy = prediction.prediction.includes('Healthy')
  
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'none':
        return 'success'
      case 'moderate':
        return 'warning'
      case 'severe':
        return 'error'
      default:
        return 'info'
    }
  }

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'none':
        return <CheckCircle />
      case 'moderate':
        return <Warning />
      case 'severe':
        return <Error />
      default:
        return <Info />
    }
  }

  return (
    <Box>
      {/* Main Result Card */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Science sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">Analysis Results</Typography>
          </Box>

          <Box sx={{ textAlign: 'center', mb: 2 }}>
            <Typography variant="h4" gutterBottom sx={{ color: diseaseInfo.color }}>
              {diseaseInfo.name}
            </Typography>
            
            <Chip
              icon={getSeverityIcon(diseaseInfo.severity)}
              label={isHealthy ? 'Healthy' : `${diseaseInfo.severity.toUpperCase()} CONDITION`}
              color={getSeverityColor(diseaseInfo.severity)}
              size="large"
              sx={{ mb: 2 }}
            />

            {prediction.confidence && (
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
                <Timer sx={{ fontSize: 16 }} />
                <Typography variant="body2" color="text.secondary">
                  Confidence: {(prediction.confidence * 100).toFixed(1)}% | 
                  Processing time: {prediction.processing_time?.toFixed(2)}s
                </Typography>
              </Box>
            )}
          </Box>

          <Typography variant="body1" sx={{ textAlign: 'center', mb: 2 }}>
            {diseaseInfo.description}
          </Typography>
        </CardContent>
      </Card>

      {/* Detailed Information */}
      <Grid container spacing={3}>
        {/* Medical Impact */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <LocalHospital sx={{ mr: 1, color: 'primary.main' }} />
              Medical Impact
            </Typography>
            
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" color="error">
                <strong>Compounds Affected:</strong>
              </Typography>
              <Typography variant="body2" gutterBottom>
                {diseaseInfo.compounds_affected}
              </Typography>
            </Box>

            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" color="error">
                <strong>Properties Lost:</strong>
              </Typography>
              <Typography variant="body2" gutterBottom>
                {diseaseInfo.properties_lost}
              </Typography>
            </Box>

            <Box>
              <Typography variant="subtitle2" color="success.main">
                <strong>Properties Retained:</strong>
              </Typography>
              <Typography variant="body2">
                {diseaseInfo.properties_retained}
              </Typography>
            </Box>
          </Paper>
        </Grid>

        {/* Usability */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Usability & Applications
            </Typography>
            
            <Alert 
              severity={isHealthy ? 'success' : diseaseInfo.severity === 'severe' ? 'error' : 'warning'}
              sx={{ mb: 2 }}
            >
              <Typography variant="body2">
                <strong>Can it be used?</strong> {diseaseInfo.usability}
              </Typography>
            </Alert>

            <Typography variant="subtitle2" gutterBottom>
              Possible Uses:
            </Typography>
            <List dense>
              {diseaseInfo.medicinal_uses?.map((use, index) => (
                <ListItem key={index} sx={{ py: 0.5 }}>
                  <ListItemIcon sx={{ minWidth: 30 }}>
                    <CheckCircle 
                      sx={{ 
                        fontSize: 16, 
                        color: isHealthy ? 'success.main' : 'warning.main' 
                      }} 
                    />
                  </ListItemIcon>
                  <ListItemText 
                    primary={use}
                    primaryTypographyProps={{ variant: 'body2' }}
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>

      {/* Additional Information for Diseased Plants */}
      {!isHealthy && (
        <Paper sx={{ p: 2, mt: 3, backgroundColor: '#FFF3E0' }}>
          <Alert severity="info" sx={{ mb: 2 }}>
            <Typography variant="body2">
              <strong>Important:</strong> The usability of diseased basil depends on the stage and extent of infection. 
              Early-stage infections may still allow for limited use, while advanced infections typically render 
              the plant unsuitable for consumption.
            </Typography>
          </Alert>
          
          <Typography variant="body2" color="text.secondary">
            <strong>Recommendation:</strong> Consult with a herbalist or medical professional before using diseased 
            plant material for any medicinal purposes. When in doubt, it's safer to dispose of heavily infected leaves properly.
          </Typography>
        </Paper>
      )}
    </Box>
  )
}

export default PredictionResults