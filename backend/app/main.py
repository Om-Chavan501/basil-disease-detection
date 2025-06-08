import os
import shutil
import uuid
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import asyncio

from .prediction import BasilDiseasePredictor
from .models import PredictionResponse, SampleImage, ModelInfo
from .disease_info import get_all_diseases

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Basil Disease Detection API",
    description="API for detecting diseases in basil leaves using machine learning",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
MODEL_PATH = os.getenv("MODEL_PATH", "./models")
SAMPLE_IMAGES_PATH = os.getenv("SAMPLE_IMAGES_PATH", "./sample_images")
UPLOAD_PATH = os.getenv("UPLOAD_PATH", "./uploads")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,bmp").split(",")

# Create directories
os.makedirs(UPLOAD_PATH, exist_ok=True)
os.makedirs(SAMPLE_IMAGES_PATH, exist_ok=True)

# Initialize predictor
print(f"Initializing predictor with model path: {MODEL_PATH}")
predictor = BasilDiseasePredictor(MODEL_PATH)

# Mount static files
app.mount("/uploads", StaticFiles(directory=UPLOAD_PATH), name="uploads")
app.mount("/samples", StaticFiles(directory=SAMPLE_IMAGES_PATH), name="samples")

# Sample images data
SAMPLE_IMAGES = [
    {
        "name": "Healthy Basil 1",
        "path": "/samples/healthy/healthy_1.jpg",
        "category": "healthy",
        "description": "Fresh, green basil leaf with no visible symptoms"
    },
    {
        "name": "Healthy Basil 2", 
        "path": "/samples/healthy/healthy_2.jpg",
        "category": "healthy",
        "description": "Vibrant basil leaf showing optimal health"
    },
    {
        "name": "Downy Mildew",
        "path": "/samples/diseased/downy_mildew.jpg", 
        "category": "diseased",
        "description": "Yellowing between leaf veins characteristic of downy mildew"
    },
    {
        "name": "Fusarium Wilt",
        "path": "/samples/diseased/fusarium_wilt.jpg",
        "category": "diseased", 
        "description": "Wilted basil showing signs of fusarium infection"
    },
    {
        "name": "Gray Mold",
        "path": "/samples/diseased/gray_mold.jpg",
        "category": "diseased",
        "description": "Basil leaf with gray fuzzy mold growth"
    }
]

@app.get("/")
async def root():
    return {"message": "Basil Disease Detection API", "version": "1.0.0"}

@app.get("/models", response_model=List[ModelInfo])
async def get_available_models():
    """Get list of available models"""
    models = []
    
    if 'random_forest_health' in predictor.models:
        models.append(ModelInfo(
            name="random_forest",
            description="Random Forest Classifier - Good balance of accuracy and speed",
            accuracy=0.92
        ))
    
    if 'svm_health' in predictor.models:
        models.append(ModelInfo(
            name="svm", 
            description="Support Vector Machine - High accuracy for complex patterns",
            accuracy=0.89
        ))
    
    if 'knn_health' in predictor.models:
        models.append(ModelInfo(
            name="knn",
            description="K-Nearest Neighbors - Simple and interpretable",
            accuracy=0.87
        ))
    
    return models

@app.get("/sample-images", response_model=List[SampleImage])
async def get_sample_images():
    """Get list of sample images"""
    return [SampleImage(**img) for img in SAMPLE_IMAGES]

@app.get("/diseases")
async def get_disease_information():
    """Get information about all diseases"""
    return get_all_diseases()

@app.post("/upload", response_model=PredictionResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload and save an image file"""
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Supported: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    # Save file
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.{file_extension}"
    file_path = os.path.join(UPLOAD_PATH, filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    return PredictionResponse(
        success=True,
        prediction="File uploaded successfully",
        processing_time=0.0,
        message=f"/uploads/{filename}"
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict_disease(
    model_type: str = Form(...),
    image_path: str = Form(...)
):
    """Predict disease from uploaded image"""
    
    # Validate model type
    available_models = ["random_forest", "svm", "knn"]
    if model_type not in available_models:
        return PredictionResponse(
            success=False,
            prediction="Error",
            message="Invalid model type",
            processing_time=0.0
        )
    
    # Handle sample images vs uploaded images
    if image_path.startswith("/samples/"):
        full_path = image_path.replace("/samples/", SAMPLE_IMAGES_PATH + "/")
    elif image_path.startswith("/uploads/"):
        full_path = image_path.replace("/uploads/", UPLOAD_PATH + "/")
    else:
        return PredictionResponse(
            success=False,
            prediction="Error",
            message="Invalid image path",
            processing_time=0.0
        )
    
    if not os.path.exists(full_path):
        return PredictionResponse(
            success=False,
            prediction="Error",
            message="Image not found",
            processing_time=0.0
        )
    
    # Make prediction
    result = predictor.predict(full_path, model_type)
    
    return PredictionResponse(**result)

@app.delete("/cleanup")
async def cleanup_uploads():
    """Clean up uploaded files (for development)"""
    try:
        for filename in os.listdir(UPLOAD_PATH):
            file_path = os.path.join(UPLOAD_PATH, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        return {"message": "Upload directory cleaned"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)