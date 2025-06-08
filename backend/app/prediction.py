import os
import cv2
import numpy as np
import joblib
import pandas as pd
from typing import Tuple, Optional, Dict, Any
import time
from skimage.feature import graycomatrix, graycoprops, local_binary_pattern
from skimage.measure import shannon_entropy
from skimage.filters import threshold_otsu
from .disease_info import get_disease_info

class BasilDiseasePredictor:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.models = {}
        self.label_encoders = {}
        self.load_models()
    
    def load_models(self):
        """Load all trained models"""
        try:
            # Random Forest models
            rf_health_path = os.path.join(self.model_path, "healthy_vs_diseased_model.pkl")
            rf_disease_path = os.path.join(self.model_path, "disease_classifier_model.pkl")
            rf_encoder_path = os.path.join(self.model_path, "disease_label_encoder.pkl")
            
            if os.path.exists(rf_health_path):
                self.models['random_forest_health'] = joblib.load(rf_health_path)
                print(f"Loaded Random Forest health model from {rf_health_path}")
            
            if os.path.exists(rf_disease_path):
                self.models['random_forest_disease'] = joblib.load(rf_disease_path)
                print(f"Loaded Random Forest disease model from {rf_disease_path}")
                
            if os.path.exists(rf_encoder_path):
                self.label_encoders['random_forest'] = joblib.load(rf_encoder_path)
                print(f"Loaded Random Forest encoder from {rf_encoder_path}")
            
            # SVM models
            svm_health_path = os.path.join(self.model_path, "healthy_vs_diseased_svm_model.pkl")
            svm_disease_path = os.path.join(self.model_path, "svm_disease_classifier_model.pkl")
            
            if os.path.exists(svm_health_path):
                self.models['svm_health'] = joblib.load(svm_health_path)
                print(f"Loaded SVM health model from {svm_health_path}")
                
            if os.path.exists(svm_disease_path):
                self.models['svm_disease'] = joblib.load(svm_disease_path)
                self.label_encoders['svm'] = self.label_encoders.get('random_forest')  # Use RF encoder
                print(f"Loaded SVM disease model from {svm_disease_path}")
            
            # KNN models
            knn_health_path = os.path.join(self.model_path, "healthy_vs_diseased_knn_model.pkl")
            knn_disease_path = os.path.join(self.model_path, "knn_disease_classifier_model.pkl")
            knn_encoder_path = os.path.join(self.model_path, "knn_disease_label_encoder.pkl")
            
            if os.path.exists(knn_health_path):
                self.models['knn_health'] = joblib.load(knn_health_path)
                print(f"Loaded KNN health model from {knn_health_path}")
            
            if os.path.exists(knn_disease_path):
                self.models['knn_disease'] = joblib.load(knn_disease_path)
                print(f"Loaded KNN disease model from {knn_disease_path}")
            elif os.path.exists(knn_health_path):
                # If no separate KNN disease model, use RF as fallback
                self.models['knn_disease'] = self.models.get('random_forest_disease')
                print("Using Random Forest disease model as fallback for KNN")
            
            if os.path.exists(knn_encoder_path):
                self.label_encoders['knn'] = joblib.load(knn_encoder_path)
                print(f"Loaded KNN encoder from {knn_encoder_path}")
            elif 'knn_health' in self.models:
                # Use RF encoder as fallback
                self.label_encoders['knn'] = self.label_encoders.get('random_forest')
                print("Using Random Forest encoder as fallback for KNN")
            
            print(f"Available models: {list(self.models.keys())}")
            print(f"Available encoders: {list(self.label_encoders.keys())}")
            
        except Exception as e:
            print(f"Error loading models: {e}")
    
    def extract_health_features(self, image: np.ndarray) -> list:
        """Extract features for healthy vs diseased classification"""
        try:
            features = []
            
            # Resize for consistency
            image = cv2.resize(image, (256, 256))
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Texture features using GLCM
            glcm = graycomatrix(gray, distances=[1], angles=[0], symmetric=True, normed=True)
            contrast = graycoprops(glcm, 'contrast')[0, 0]
            dissimilarity = graycoprops(glcm, 'dissimilarity')[0, 0]
            homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
            energy = graycoprops(glcm, 'energy')[0, 0]
            correlation = graycoprops(glcm, 'correlation')[0, 0]
            
            # Color features (mean RGB values)
            r_mean = np.mean(image[:, :, 0])
            g_mean = np.mean(image[:, :, 1])
            b_mean = np.mean(image[:, :, 2])
            
            # Shape feature: leaf contour area
            _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            area = max([cv2.contourArea(c) for c in contours]) if contours else 0
            
            features = [contrast, dissimilarity, homogeneity, energy, correlation,
                       r_mean, g_mean, b_mean, area]
            
            return features
        except Exception as e:
            print(f"Error extracting health features: {e}")
            raise
    
    def extract_disease_features(self, image: np.ndarray) -> dict:
        """Extract features for disease classification"""
        try:
            features = {}
            
            # Parameters
            LBP_RADIUS = 3
            LBP_POINTS = 8 * LBP_RADIUS
            
            # Resize for consistency
            img_resized = cv2.resize(image, (640, 640))
            hsv = cv2.cvtColor(img_resized, cv2.COLOR_BGR2HSV)
            gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
            
            # Mean RGB and HSV
            features['mean_r'] = np.mean(img_resized[:,:,2])
            features['mean_g'] = np.mean(img_resized[:,:,1])
            features['mean_b'] = np.mean(img_resized[:,:,0])
            features['mean_h'] = np.mean(hsv[:,:,0])
            features['mean_s'] = np.mean(hsv[:,:,1])
            features['mean_v'] = np.mean(hsv[:,:,2])
            
            # Yellow Area %
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([35, 255, 255])
            yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
            yellow_area = np.sum(yellow_mask > 0)
            features['yellow_area_percent'] = yellow_area / (640 * 640)
            
            # Texture Entropy
            features['entropy'] = shannon_entropy(gray)
            
            # LBP Texture
            lbp = local_binary_pattern(gray, LBP_POINTS, LBP_RADIUS, method='uniform')
            (hist, _) = np.histogram(lbp.ravel(), bins=np.arange(0, LBP_POINTS + 3), 
                                    range=(0, LBP_POINTS + 2))
            hist = hist.astype("float")
            hist /= (hist.sum() + 1e-6)
            for i in range(len(hist)):
                features[f'lbp_{i}'] = hist[i]
            
            # Spot Count using thresholding
            _, binary = cv2.threshold(gray, threshold_otsu(gray), 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            spot_count = len([cnt for cnt in contours if cv2.contourArea(cnt) > 50])
            features['spot_count'] = spot_count
            
            # Edge Density
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (640 * 640)
            features['edge_density'] = edge_density
            
            # Symmetry Score
            left = gray[:, :gray.shape[1]//2]
            right = cv2.flip(gray[:, gray.shape[1]//2:], 1)
            symmetry_score = 1 - (np.mean(np.abs(left - right)) / 255)
            features['symmetry_score'] = symmetry_score
            
            return features
        except Exception as e:
            print(f"Error extracting disease features: {e}")
            raise
    
    def predict(self, image_path: str, model_type: str) -> Dict[str, Any]:
        """Make prediction using specified model"""
        start_time = time.time()
        
        try:
            # Load image
            print(f"Loading image from: {image_path}")
            image = cv2.imread(image_path)
            if image is None:
                return {
                    "success": False,
                    "prediction": "Error",
                    "message": "Could not load image",
                    "processing_time": time.time() - start_time
                }
            
            print(f"Image loaded successfully, shape: {image.shape}")
            
            # First classification: Healthy vs Diseased
            health_features = self.extract_health_features(image)
            print(f"Health features extracted: {len(health_features)} features")
            
            # Select appropriate health model
            health_model_key = f"{model_type}_health"
            print(f"Looking for model: {health_model_key}")
            
            if health_model_key not in self.models:
                return {
                    "success": False,
                    "prediction": "Error",
                    "message": f"Model {model_type} not available. Available models: {list(self.models.keys())}",
                    "processing_time": time.time() - start_time
                }
            
            health_model = self.models[health_model_key]
            health_prediction = health_model.predict([health_features])[0]
            print(f"Health prediction: {health_prediction}")
            
            # Get confidence for health prediction
            health_confidence = 0.95  # Default confidence
            if hasattr(health_model, 'predict_proba'):
                try:
                    health_probs = health_model.predict_proba([health_features])[0]
                    health_confidence = health_probs[health_prediction]
                    print(f"Health confidence: {health_confidence}")
                except:
                    print("Could not get health prediction probability")
            
            if health_prediction == 0:
                # Healthy plant
                disease_info = get_disease_info("healthy_basil")
                return {
                    "success": True,
                    "prediction": "Healthy Plant",
                    "confidence": float(health_confidence),
                    "disease_info": disease_info,
                    "processing_time": time.time() - start_time
                }
            else:
                # Diseased plant - identify disease
                disease_features = self.extract_disease_features(image)
                print(f"Disease features extracted: {len(disease_features)} features")
                
                # Select disease model
                disease_model_key = f"{model_type}_disease"
                if disease_model_key not in self.models:
                    # Fallback to random forest
                    disease_model_key = "random_forest_disease"
                    if disease_model_key not in self.models:
                        return {
                            "success": False,
                            "prediction": "Error",
                            "message": "No disease classification model available",
                            "processing_time": time.time() - start_time
                        }
                    print(f"Using fallback disease model: {disease_model_key}")
                
                disease_model = self.models[disease_model_key]
                print(f"Using disease model: {disease_model_key}")
                
                # Handle different model types for disease prediction
                if model_type == 'knn' and 'knn_disease' in self.models:
                    # KNN disease model exists, use it
                    try:
                        # Prepare features for KNN disease model
                        if hasattr(disease_model, 'feature_names_in_'):
                            df_columns = disease_model.feature_names_in_
                            features_dict = {col: disease_features.get(col, 0) for col in df_columns}
                            features_df = pd.DataFrame([features_dict])
                            features_array = features_df.values
                            
                            # Predict disease
                            disease_prediction = disease_model.predict(features_array)[0]
                        else:
                            # If no feature names, convert dict to array matching training order
                            # This assumes the same feature order as training
                            features_list = []
                            expected_features = ['mean_r', 'mean_g', 'mean_b', 'mean_h', 'mean_s', 'mean_v', 
                                               'yellow_area_percent', 'entropy'] + \
                                              [f'lbp_{i}' for i in range(26)] + \
                                              ['spot_count', 'edge_density', 'symmetry_score']
                            
                            for feat_name in expected_features:
                                features_list.append(disease_features.get(feat_name, 0))
                            
                            disease_prediction = disease_model.predict([features_list])[0]
                        
                        print(f"Disease prediction: {disease_prediction}")
                        
                        # Get confidence
                        confidence = 0.75  # Default for KNN
                        if hasattr(disease_model, 'predict_proba'):
                            try:
                                if 'features_array' in locals():
                                    disease_probs = disease_model.predict_proba(features_array)[0]
                                else:
                                    disease_probs = disease_model.predict_proba([features_list])[0]
                                confidence = disease_probs[disease_prediction]
                            except:
                                print("Could not get disease prediction probability for KNN")
                        
                    except Exception as e:
                        print(f"Error with KNN disease prediction: {e}")
                        return {
                            "success": False,
                            "prediction": "Error",
                            "message": f"KNN disease prediction error: {str(e)}",
                            "processing_time": time.time() - start_time
                        }
                else:
                    # Use standard feature preparation for RF/SVM
                    if hasattr(disease_model, 'feature_names_in_'):
                        df_columns = disease_model.feature_names_in_
                        features_dict = {col: disease_features.get(col, 0) for col in df_columns}
                        features_df = pd.DataFrame([features_dict])
                        
                        # Predict disease
                        disease_prediction = disease_model.predict(features_df)[0]
                        print(f"Disease prediction: {disease_prediction}")
                        
                        # Get confidence
                        if hasattr(disease_model, 'predict_proba'):
                            disease_probs = disease_model.predict_proba(features_df)[0]
                            confidence = disease_probs[disease_prediction]
                        else:
                            confidence = 0.75  # Default confidence for SVM
                    else:
                        return {
                            "success": False,
                            "prediction": "Error",
                            "message": "Model feature names not available",
                            "processing_time": time.time() - start_time
                        }
                
                # Get disease name
                encoder_key = model_type if model_type in self.label_encoders else 'random_forest'
                if encoder_key not in self.label_encoders:
                    return {
                        "success": False,
                        "prediction": "Error",
                        "message": "Label encoder not available",
                        "processing_time": time.time() - start_time
                    }
                
                encoder = self.label_encoders[encoder_key]
                disease_name = encoder.inverse_transform([disease_prediction])[0]
                print(f"Disease name: {disease_name}")
                
                # Get disease info
                disease_info = get_disease_info(disease_name)
                
                return {
                    "success": True,
                    "prediction": f"Diseased Plant - {disease_info['name']}",
                    "confidence": float(confidence),
                    "disease_info": disease_info,
                    "processing_time": time.time() - start_time
                }
        
        except Exception as e:
            print(f"Prediction error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "prediction": "Error",
                "message": f"Prediction error: {str(e)}",
                "processing_time": time.time() - start_time
            }