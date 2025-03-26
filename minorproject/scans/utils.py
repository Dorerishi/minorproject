import torch
from transformers import ViTFeatureExtractor, ViTForImageClassification
from PIL import Image
import os

# Load model (update model path)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "best_vit_model.pth")
CLASS_LABELS = ["Normal", "glioma_tumor", "meningioma_tumor", "pituitary_tumor"] 

# Load model function
def load_model():
    model = ViTForImageClassification.from_pretrained(
        'google/vit-base-patch16-224-in21k',
        num_labels=len(CLASS_LABELS)
    )
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
    model.eval()
    return model

# Load feature extractor
feature_extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch16-224-in21k")

# Predict function
def predict_image(image_path):
    model = load_model()

    # Load and preprocess image
    image = Image.open(image_path).convert("RGB")
    inputs = feature_extractor(images=image, return_tensors="pt")

    # Get model predictions
    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits  # Get raw logits
    probabilities = torch.nn.functional.softmax(logits, dim=-1)  # Convert to probabilities

    predicted_class = torch.argmax(probabilities, dim=-1).item()  # Get highest confidence class
    confidence = probabilities[0, predicted_class].item()  # Extract confidence

    return CLASS_LABELS[predicted_class], confidence
