import os
import json
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
from .utils import predict_image 


MRI_SCANS_DIR = os.path.join(settings.MEDIA_ROOT, "mriscans")
os.makedirs(MRI_SCANS_DIR, exist_ok=True)

def home(request):
    if request.method == "POST" and request.FILES.get("scan"):
        patient_name = request.POST.get("patient_name", "Unknown")
        uploaded_file = request.FILES["scan"]

        # Save uploaded file
        file_name = f"{patient_name}_{uploaded_file.name}"
        file_path = os.path.join(MRI_SCANS_DIR, file_name)
        with open(file_path, "wb") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Run AI prediction
        label, confidence = predict_image(file_path)

        # Save output as JSON
        result_json = {
            "patient_name": patient_name,
            "file_name": file_name,
            "prediction": label,
            "confidence": round(confidence, 2)
        }
        json_path = os.path.join(MRI_SCANS_DIR, f"{patient_name}.json")
        with open(json_path, "w") as json_file:
            json.dump(result_json, json_file, indent=4)

        return render(request, "result.html", {"result": result_json})

    return render(request, "home.html")

def classify_scan(request):
    if request.method == "POST" and request.FILES.get("scan"):
        uploaded_file = request.FILES["scan"]
        file_path = default_storage.save("uploads/" + uploaded_file.name, uploaded_file)

        label, confidence = predict_image(default_storage.path(file_path))

        return render(request, "result.html", {"label": label, "confidence": confidence})

    return render(request, "upload.html")

