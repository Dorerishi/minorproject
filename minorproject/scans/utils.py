import torch
from transformers import ViTFeatureExtractor, ViTForImageClassification
from PIL import Image
import os
import subprocess

# Labels
CLASS_LABELS = ["Normal", "glioma_tumor", "meningioma_tumor", "pituitary_tumor"]

# Model path
MODEL_PATH = os.path.join(os.path.dirname(__file__), "best_vit_model.pth")

def download_model_if_needed():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model from Kaggle...")

        kaggle_username = os.environ.get("KAGGLE_USERNAME")
        kaggle_key = os.environ.get("KAGGLE_KEY")

        if not kaggle_username or not kaggle_key:
            raise Exception("KAGGLE_USERNAME and KAGGLE_KEY environment variables must be set")

        # Save kaggle.json
        os.makedirs(os.path.expanduser("~/.kaggle"), exist_ok=True)
        kaggle_json_path = os.path.expanduser("~/.kaggle/kaggle.json")
        with open(kaggle_json_path, "w") as f:
            f.write(f"""{{
  "username": "{kaggle_username}",
  "key": "{kaggle_key}"
}}""")
        os.chmod(kaggle_json_path, 0o600)

        # Run Kaggle CLI to download the model
        subprocess.run([
            "kaggle", "kernels", "output", "hri0123/brain-tumor-using-vit", "-p", os.path.dirname(MODEL_PATH)
        ], check=True)

def load_model():
    download_model_if_needed()

    model = ViTForImageClassification.from_pretrained(
        'google/vit-base-patch16-224-in21k',
        num_labels=len(CLASS_LABELS)
    )
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
    model.eval()
    return model

# Feature extractor
feature_extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch16-224-in21k")

# Predict function
def predict_image(image_path):
    model = load_model()

    image = Image.open(image_path).convert("RGB")
    inputs = feature_extractor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=-1)

    predicted_class = torch.argmax(probabilities, dim=-1).item()
    confidence = probabilities[0, predicted_class].item()

    return CLASS_LABELS[predicted_class], confidence
