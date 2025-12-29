import os
from ultralytics import YOLO
from target_classes import target_classes

def check_for_knee(image_path):
    """Checks if the image contains a knee X-ray or not using YOLO"""
    if not os.path.exists(image_path):
        return "File does not exist."

    try:
        
        model = YOLO('yolov10s.pt')  
        
        
        results = model(image_path)
        detected_labels = results[0].boxes.cls.tolist()
        detected_classes = [model.names[label] for label in detected_labels]

        
        for detected_class in detected_classes:
            if detected_class in target_classes:
                return "Please upload only knee images"
        
        return "Knee detected! Proceeding with prediction."
    
    except Exception as e:
        return f"Error: {str(e)}"
