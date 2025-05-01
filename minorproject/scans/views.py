import os
import json
from django.shortcuts import render,redirect
from django.core.files.storage import default_storage
from django.conf import settings
from .models import ScanResult
from .utils import predict_image
from .fhir_utils import create_patient, create_observation
from .image_utils import compress_image


MRI_SCANS_DIR = os.path.join(settings.MEDIA_ROOT, "mriscans")
os.makedirs(MRI_SCANS_DIR, exist_ok=True)

def home(request):
    if request.method == "POST" and request.FILES.get("scan"):
        patient_name = request.POST.get("patient_name", "Unknown")
        uploaded_file = request.FILES["scan"]

        file_name = f"{patient_name}_{uploaded_file.name}"
        file_path = os.path.join(MRI_SCANS_DIR, file_name)
        with open(file_path, "wb") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        label, confidence = predict_image(file_path)

        # Save to local DB

        result = ScanResult.objects.create(
            patient_name=patient_name,
            file_name=file_name,
            prediction=label,
            confidence=round(confidence, 2)
        )

# Push to FHIR
        try:
            fhir_patient_id = create_patient(patient_name)
            fhir_observation_id = create_observation(fhir_patient_id, label, confidence)

            # Save FHIR IDs to that result
            result.fhir_patient_id = fhir_patient_id
            result.fhir_observation_id = fhir_observation_id
            result.save()

        except Exception as e:
            print("FHIR upload failed:", str(e))


        return render(request, "result.html", {"result": result})

    return render(request, "home.html")

def classify_scan(request):
    if request.method == "POST" and request.FILES.get("scan"):
        patient_name = request.POST.get("patient_name", "Unknown")
        uploaded_file = request.FILES["scan"]

        # Save uploaded file
        file_name = f"{patient_name}_{uploaded_file.name}"
        file_path = os.path.join(MRI_SCANS_DIR, file_name)
        with open(file_path, "wb") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Run prediction
        label, confidence = predict_image(file_path)

        # Save to DB
        result = ScanResult.objects.create(
            patient_name=patient_name,
            file_name=file_name,
            prediction=label,
            confidence=round(confidence, 2)
        )

        return render(request, "result.html", {"result": result})

    return render(request, "upload.html")

def scan_history(request):
    results = ScanResult.objects.order_by('-uploaded_at')  # latest first
    return render(request, "history.html", {"results": results})

from .models import ScanResult

def compress_and_save(request):
    if request.method == "POST":
        result_id = request.POST.get("result_id")
        result = ScanResult.objects.get(id=result_id)

        original_path = os.path.join(settings.MEDIA_ROOT, "mriscans", result.file_name)
        compressed_path = compress_image(original_path, delete_original=True)

        result.file_name = os.path.basename(compressed_path)
        result.save()

        return redirect("history")  # or render a success page

def delete_scan(request, scan_id):
    result = ScanResult.objects.get(id=scan_id)

    # Delete file
    file_path = os.path.join(settings.MEDIA_ROOT, "mriscans", result.file_name)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete record
    result.delete()

    return redirect("history")



