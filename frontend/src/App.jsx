import React, { useState, useEffect } from 'react'
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Grid,
  AppBar,
  Toolbar,
  Paper,
} from '@mui/material'
import { Nature, Science, LocalFlorist } from '@mui/icons-material'
import ModelSelector from './components/ModelSelector'
import ImageUploader from './components/ImageUploader'
import SampleImages from './components/SampleImages' 
import PredictionResults from './components/PredictionResults'
import LoadingProgress from './components/LoadingProgress'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function App() {
  const [selectedModel, setSelectedModel] = useState('')
  const [selectedImage, setSelectedImage] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [models, setModels] = useState([])
  const [sampleImages, setSampleImages] = useState([])

  useEffect(() => {
    fetchModels()
    fetchSampleImages()
  }, [])

  const fetchModels = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/models`)
      setModels(response.data)
      if (response.data.length > 0) {
        setSelectedModel(response.data[0].name)
      }
    } catch (error) {
      console.error('Error fetching models:', error)
    }
  }

  const fetchSampleImages = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/sample-images`)
      setSampleImages(response.data)
    } catch (error) {
      console.error('Error fetching sample images:', error)
    }
  }

  const handleImageSelect = (imagePath, imageFile = null) => {
    setSelectedImage({ path: imagePath, file: imageFile })
    setPrediction(null) // Clear previous prediction
  }

  const handlePredict = async () => {
    if (!selectedImage || !selectedModel) return

    setLoading(true)
    setPrediction(null)

    try {
      let imagePath = selectedImage.path

      // If it's an uploaded file, upload it first
      if (selectedImage.file) {
        const formData = new FormData()
        formData.append('file', selectedImage.file)
        
        const uploadResponse = await axios.post(`${API_BASE_URL}/upload`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        
        imagePath = uploadResponse.data.message
      }

      // Make prediction
      const predictionData = new FormData()
      predictionData.append('model_type', selectedModel)
      predictionData.append('image_path', imagePath)

      const response = await axios.post(`${API_BASE_URL}/predict`, predictionData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      setPrediction({
        ...response.data,
        imagePath: `${API_BASE_URL}${imagePath}`
      })
    } catch (error) {
      console.error('Error making prediction:', error)
      setPrediction({
        success: false,
        message: error.response?.data?.detail || 'Prediction failed'
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh', backgroundColor: '#F1F8E9' }}>
      {/* Header */}
      <AppBar position="static" sx={{ background: 'linear-gradient(45deg, #4CAF50 30%, #66BB6A 90%)' }}>
        <Toolbar>
          <LocalFlorist sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Basil Disease Detection Tool
          </Typography>
          <Science sx={{ ml: 2 }} />
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* Introduction */}
        <Paper sx={{ p: 3, mb: 4, backgroundColor: '#E8F5E8' }}>
          <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
            <Nature sx={{ mr: 2, color: '#4CAF50' }} />
            AIML-Powered Basil Health Analysis
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Upload an image of a basil leaf or select from our samples to detect diseases and learn about 
            their impact on medicinal properties. Our advanced machine learning models can identify various 
            diseases including Downy Mildew, Fusarium Wilt, Gray Mold, and Septoria Leaf Spot.
          </Typography>
        </Paper>

        <Grid container spacing={4}>
          {/* Left Column - Controls */}
          <Grid item xs={12} md={6}>
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  1. Select ML Model
                </Typography>
                <ModelSelector
                  models={models}
                  selectedModel={selectedModel}
                  onModelChange={setSelectedModel}
                />
              </CardContent>
            </Card>

            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  2. Choose Image
                </Typography>
                <ImageUploader onImageSelect={handleImageSelect} />
              </CardContent>
            </Card>

            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Or Select Sample Image
                </Typography>
                <SampleImages
                  images={sampleImages}
                  onImageSelect={handleImageSelect}
                  selectedImage={selectedImage}
                />
              </CardContent>
            </Card>
          </Grid>

          {/* Right Column - Results */}
          <Grid item xs={12} md={6}>
            {loading && <LoadingProgress />}
            
            {selectedImage && !loading && (
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Selected Image
                  </Typography>
                  <Box sx={{ textAlign: 'center', mb: 2 }}>
                    <img
                      src={selectedImage.file ? URL.createObjectURL(selectedImage.file) : `${API_BASE_URL}${selectedImage.path}`}
                      alt="Selected leaf"
                      style={{
                        maxWidth: '100%',
                        maxHeight: '300px',
                        borderRadius: '8px',
                        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                      }}
                    />
                  </Box>
                  <Box sx={{ textAlign: 'center' }}>
                    <button
                      onClick={handlePredict}
                      disabled={!selectedModel || loading}
                      style={{
                        backgroundColor: '#4CAF50',
                        color: 'white',
                        border: 'none',
                        padding: '12px 24px',
                        borderRadius: '8px',
                        fontSize: '16px',
                        fontWeight: '500',
                        cursor: selectedModel && !loading ? 'pointer' : 'not-allowed',
                        opacity: selectedModel && !loading ? 1 : 0.6,
                      }}
                    >
                      🔬 Analyze Leaf Health
                    </button>
                  </Box>
                </CardContent>
              </Card>
            )}

            {prediction && (
              <PredictionResults prediction={prediction} />
            )}
          </Grid>
        </Grid>
      </Container>
    </Box>
  )
}

export default App