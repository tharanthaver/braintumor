"""
Brain Tumor Detection FastAPI Application
Main entry point for the tumor detection and growth forecasting system.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from datetime import datetime

# Import our custom modules
from .predict import predict_image, is_tumor_detected
from .simulate import estimate_size, predict_growth, get_symptoms
from .utils.image_utils import save_upload_image

# Initialize FastAPI app
app = FastAPI(
    title="Brain Tumor Detection & Growth Forecasting API",
    description="AI-powered system to detect brain tumors from MRI images and forecast their growth",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration
UPLOAD_DIR = "data"
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]

@app.on_event("startup")
async def startup_event():
    """Ensure upload directory exists on startup."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    print("Brain Tumor Detection API started successfully!")

@app.get("/")
async def root():
    """Serve the main HTML page."""
    return FileResponse('static/index.html')

@app.get("/api")
async def api_info():
    """API information endpoint."""
    return {
        "message": "Brain Tumor Detection & Growth Forecasting API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict - Upload MRI image for tumor detection",
            "docs": "/docs - Interactive API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Brain Tumor Detection API"
    }

@app.post("/predict")
async def predict_tumor(file: UploadFile = File(...)):
    """
    Predict tumor presence, type, size, and growth from uploaded MRI image.
    
    Args:
        file (UploadFile): The MRI image file to analyze
        
    Returns:
        JSONResponse: Prediction results including tumor detection, classification, 
                     size estimation, growth forecast, and potential symptoms
    """
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file format. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Generate unique filename to avoid conflicts
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save the uploaded file
        save_upload_image(file, file_path)
        
        # Predict tumor type using the pretrained model
        prediction_result = predict_image(file_path)
        
        # Check if there was an error in prediction
        if 'error' in prediction_result:
            raise HTTPException(status_code=500, detail=f"Prediction error: {prediction_result['error']}")
        
        # Check if tumor is detected
        tumor_detected = is_tumor_detected(prediction_result)
        
        if not tumor_detected:
            # No tumor detected
            response = {
                "tumor_detected": False,
                "message": "No tumor detected",
                "confidence": prediction_result['confidence'],
                "all_probabilities": prediction_result['all_probabilities'],
                "timestamp": datetime.now().isoformat()
            }
        else:
            # Tumor detected - perform full analysis
            tumor_type = prediction_result['predicted_label']
            confidence = prediction_result['confidence']
            
            # Estimate current tumor size
            current_size = estimate_size(file_path)
            
            # Predict growth after 3 months
            predicted_size_3_months = predict_growth(current_size, months=3)
            
            # Get potential symptoms based on current size
            current_symptoms = get_symptoms(current_size)
            
            # Get potential symptoms based on predicted size
            future_symptoms = get_symptoms(predicted_size_3_months)
            
            response = {
                "tumor_detected": True,
                "tumor_type": tumor_type,
                "confidence": confidence,
                "current_size_cm2": current_size,
                "predicted_size_after_3_months": predicted_size_3_months,
                "growth_rate_cm2_per_month": 0.4,
                "current_expected_symptoms": current_symptoms,
                "future_expected_symptoms": future_symptoms,
                "all_probabilities": prediction_result['all_probabilities'],
                "timestamp": datetime.now().isoformat(),
                "analysis_notes": {
                    "size_estimation": "Simulated based on typical tumor characteristics",
                    "growth_model": "Fixed rate of 0.4 cm²/month (simplified model)",
                    "symptoms": "Based on tumor size correlation studies"
                }
            }
        
        # Clean up: remove the uploaded file after processing
        try:
            os.remove(file_path)
        except OSError:
            pass  # File deletion is not critical
        
        return JSONResponse(content=response, status_code=200)
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected error in predict_tumor: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/predict-batch")
async def predict_batch(files: list[UploadFile] = File(...)):
    """
    Predict tumors for multiple MRI images at once.
    
    Args:
        files (list[UploadFile]): List of MRI image files to analyze
        
    Returns:
        JSONResponse: Batch prediction results
    """
    if len(files) > 10:  # Limit batch size
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed per batch")
    
    results = []
    
    for i, file in enumerate(files):
        try:
            # Process each file individually using the same logic as single prediction
            file_result = await predict_tumor(file)
            results.append({
                "file_index": i,
                "filename": file.filename,
                "result": file_result.body.decode() if hasattr(file_result, 'body') else file_result
            })
        except Exception as e:
            results.append({
                "file_index": i,
                "filename": file.filename,
                "error": str(e)
            })
    
    return JSONResponse(content={
        "batch_results": results,
        "total_files": len(files),
        "timestamp": datetime.now().isoformat()
    }, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
