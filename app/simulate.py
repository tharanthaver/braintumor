"""
Tumor Simulation Module
Simulates tumor size, growth, and potential symptoms
"""

import random
from typing import List

def estimate_size(img_path: str) -> float:
    """
    Simulate tumor size based on image analysis (mocked).
    
    Args:
        img_path (str): Path to the image (not used, for API consistency)
        
    Returns:
        float: Simulated tumor size in cm²
    """
    # Simulate a tumor size between 2.0 and 5.0 cm²
    simulated_size = round(random.uniform(2.0, 5.0), 2)
    print(f"Simulated tumor size for {img_path}: {simulated_size} cm²")
    return simulated_size

def predict_growth(current_size: float, months: int = 3) -> float:
    """
    Predict future tumor size based on a fixed growth rate.
    
    Args:
        current_size (float): The current size of the tumor in cm²
        months (int): The number of months to forecast growth
        
    Returns:
        float: Predicted size in cm² after the specified duration
    """
    # Use a fixed growth rate (e.g., 0.4 cm²/month)
    growth_rate_per_month = 0.4
    predicted_size = current_size + (growth_rate_per_month * months)
    return round(predicted_size, 2)

def get_symptoms(size: float) -> List[str]:
    """
    Determine potential symptoms based on tumor size.
    
    Args:
        size (float): The size of the tumor in cm²
        
    Returns:
        List[str]: A list of possible symptoms
    """
    if size < 2.0:
        return ["Mild headache"]
    elif 2.0 <= size <= 4.0:
        return ["Fatigue", "Blurred vision"]
    elif 4.0 < size <= 6.0:
        return ["Memory loss", "Speech difficulty"]
    else:  # size > 6.0
        return ["Seizures", "Cognitive decline"]

