import requests

FHIR_BASE_URL = "https://hapi.fhir.org/baseR4"

def create_patient(patient_name):
    name_parts = patient_name.strip().split()
    given = name_parts[:-1] if len(name_parts) > 1 else name_parts
    family = name_parts[-1] if len(name_parts) > 1 else ""

    patient_resource = {
        "resourceType": "Patient",
        "name": [{
            "given": given,
            "family": family
        }]
    }

    response = requests.post(f"{FHIR_BASE_URL}/Patient", json=patient_resource)
    response.raise_for_status()
    return response.json()["id"]  # FHIR patient ID

def create_observation(patient_id, prediction, confidence):
    observation_resource = {
        "resourceType": "Observation",
        "status": "final",
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "LA9633-4",
                "display": "Tumor classification"
            }],
            "text": "Brain MRI Classification"
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "valueString": f"{prediction} ({round(confidence, 2)})"
    }

    response = requests.post(f"{FHIR_BASE_URL}/Observation", json=observation_resource)
    response.raise_for_status()
    return response.json()["id"]  # FHIR observation ID
