# AI-Based Brain Tumor Detection and Growth Forecasting System

This project is a FastAPI-based backend system that uses a pretrained model to detect and classify brain tumors from MRI images. It also simulates tumor growth and forecasts potential symptoms.

## Features

- **Tumor Detection**: Detects if a brain tumor is present in MRI images
- **Tumor Classification**: Classifies tumors into types: Glioma, Meningioma, or Pituitary
- **Size Estimation**: Simulates tumor size in cm²
- **Growth Prediction**: Forecasts tumor size after 3 months (0.4 cm²/month growth rate)
- **Symptom Forecasting**: Predicts potential symptoms based on tumor size

## Project Structure

```
brain_tumor_project/
├── app/
│   ├── main.py            # FastAPI entry point
│   ├── predict.py         # Tumor detection & classification logic
│   ├── simulate.py        # Growth rate logic + symptom forecasting
│   ├── utils/
│   │   └── image_utils.py # Save uploaded images
│   └── model/
│       └── tumor_model.h5 # Pretrained Keras model (place your model here)
├── data/                  # Folder for uploaded images & dataset
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Prerequisites

⚠️ **IMPORTANT**: You need to place your pretrained model file at `app/model/tumor_model.h5` before running the application.

## Installation & Setup

1.  **Clone or navigate to the project directory:**

    ```bash
    cd brain_tumor_project
    ```

2.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Place your pretrained model:**

    Ensure your `tumor_model.h5` file is located at `app/model/tumor_model.h5`

4.  **Run the FastAPI server:**

    ```bash
    uvicorn app.main:app --reload
    ```

5.  **Access the API:**

    - **Interactive Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
    - **API Root**: [http://localhost:8000](http://localhost:8000)
    - **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

## API Endpoints

### `POST /predict`
Upload an MRI image for tumor detection and analysis.

**Response for No Tumor:**
```json
{
  "tumor_detected": false,
  "message": "No tumor detected",
  "confidence": 0.95,
  "timestamp": "2024-01-01T12:00:00"
}
```

**Response for Tumor Detected:**
```json
{
  "tumor_detected": true,
  "tumor_type": "Glioma",
  "confidence": 0.91,
  "current_size_cm2": 3.2,
  "predicted_size_after_3_months": 4.4,
  "growth_rate_cm2_per_month": 0.4,
  "current_expected_symptoms": ["Fatigue", "Blurred vision"],
  "future_expected_symptoms": ["Memory loss", "Speech difficulty"],
  "timestamp": "2024-01-01T12:00:00"
}
```

### `POST /predict-batch`
Upload multiple MRI images for batch processing (max 10 files).

## How to Test

1.  **Via Swagger UI (Recommended):**
    - Go to [http://localhost:8000/docs](http://localhost:8000/docs)
    - Expand the `POST /predict` endpoint
    - Click "Try it out"
    - Choose an MRI image file
    - Click "Execute"

2.  **Via cURL:**
    ```bash
    curl -X POST "http://localhost:8000/predict" \
         -H "accept: application/json" \
         -H "Content-Type: multipart/form-data" \
         -F "file=@path/to/your/mri_image.jpg"
    ```

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)

## Model Classes

The pretrained model classifies images into these categories:
- **Glioma**: A type of brain tumor
- **Meningioma**: A type of brain tumor
- **Pituitary**: A type of brain tumor
- **No Tumor**: No tumor detected

## Symptom Mapping

| Tumor Size (cm²) | Expected Symptoms |
|------------------|-------------------|
| < 2.0 | Mild headache |
| 2.0 - 4.0 | Fatigue, Blurred vision |
| 4.0 - 6.0 | Memory loss, Speech difficulty |
| > 6.0 | Seizures, Cognitive decline |

## Notes

- Size estimation is simulated (2.0-5.0 cm²)
- Growth rate is fixed at 0.4 cm²/month
- Symptom predictions are based on size correlations
- This is a demonstration system - not for actual medical diagnosis

