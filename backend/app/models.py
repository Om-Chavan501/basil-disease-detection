from pydantic import BaseModel
from typing import Optional, List

class PredictionRequest(BaseModel):
    model_type: str
    image_path: Optional[str] = None

class PredictionResponse(BaseModel):
    success: bool
    prediction: Optional[str] = None  # Make this optional
    confidence: Optional[float] = None
    disease_info: Optional[dict] = None
    processing_time: float
    message: Optional[str] = None

class SampleImage(BaseModel):
    name: str
    path: str
    category: str
    description: str

class ModelInfo(BaseModel):
    name: str
    description: str
    accuracy: Optional[float] = None