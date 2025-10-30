"""
Tumor Detection and Classification Module
Uses pretrained Keras model to classify brain MRI images
"""

import tensorflow as tf
from tensorflow.keras.models import model_from_json
import numpy as np
import cv2
from PIL import Image
import os

# Define the classes that the model can predict (based on actual training data)
CLASSES = ['No Tumor', 'Pituitary Tumor']

# Global variable to store the loaded model
model = None

def load_model():
    """Load the pretrained tumor classification model"""
    global model
    if model is None:
        model_dir = os.path.join(os.path.dirname(__file__), 'model')
        json_path = os.path.join(model_dir, 'model.json')
        weights_path = os.path.join(model_dir, 'model.h5')
        
        try:
            # Load model architecture from JSON
            with open(json_path, 'r') as json_file:
                loaded_model_json = json_file.read()
            
            # Create model from JSON
            model = model_from_json(loaded_model_json)
            
            # Load weights
            model.load_weights(weights_path)
            
            print(f"Model loaded successfully from {json_path} and {weights_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise e
    return model

def preprocess_image(img_path: str) -> np.ndarray:
    """
    Preprocess the input image for model prediction
    
    Args:
        img_path (str): Path to the input image
        
    Returns:
        np.ndarray: Preprocessed image array ready for prediction
    """
    try:
        # Load image using PIL
        image = Image.open(img_path)
        
        # Convert to RGB if it's not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to 224x224 (standard input size for most CNN models)
        image = image.resize((224, 224))
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # Normalize pixel values to [0, 1]
        img_array = img_array.astype(np.float32) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
        
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        raise e

def predict_image(img_path: str) -> dict:
    """
    Predict tumor type from brain MRI image
    
    Args:
        img_path (str): Path to the input MRI image
        
    Returns:
        dict: Dictionary containing prediction results
    """
    try:
        # Load model if not already loaded
        model = load_model()
        
        # Preprocess the image
        processed_image = preprocess_image(img_path)
        
        # Make prediction
        predictions = model.predict(processed_image, verbose=0)
        
        # Get the predicted class index and confidence
        predicted_index = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_index])
        predicted_label = CLASSES[predicted_index]
        
        # Return results
        result = {
            'predicted_label': predicted_label,
            'confidence': round(confidence, 3),
            'all_probabilities': {
                CLASSES[i]: round(float(predictions[0][i]), 3) 
                for i in range(len(CLASSES))
            }
        }
        
        print(f"Prediction: {predicted_label} (confidence: {confidence:.3f})")
        return result
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {
            'error': str(e),
            'predicted_label': None,
            'confidence': 0.0
        }

def is_tumor_detected(prediction_result: dict) -> bool:
    """
    Check if a tumor was detected (i.e., prediction is not 'No Tumor')
    
    Args:
        prediction_result (dict): Result from predict_image function
        
    Returns:
        bool: True if tumor detected, False otherwise
    """
    if 'error' in prediction_result:
        return False
    
    predicted_label = prediction_result.get('predicted_label', '')
    return predicted_label != 'No Tumor' and predicted_label is not None
