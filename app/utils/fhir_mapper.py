import re

def clean_text(text):
    return text.strip().replace("\n", " ").replace("  ", " ")

def extract_fields(text):
    fields = {
        "patient_name": None,
        "diagnosis": None,
        "medications": None,
        "follow_up": None
    }

    # 👤 Patient Name (EN or DE)
    name_match = re.search(r"(?:Name:|Name des Patienten:)\s*(.*?)(?:DOB|Geburtsdatum)", text)
    if name_match:
        fields["patient_name"] = name_match.group(1).strip()

    # 🧠 Diagnosis (EN or DE)
    diagnosis_match = re.search(
        r"(?:Diagnosis:|Diagnose:)\s*(.*?)(?:Treatment Given:|Medikation|Medications on Discharge:|Discharge Instructions:|Empfehlungen:|$)",
        text, re.DOTALL
    )
    if diagnosis_match:
        fields["diagnosis"] = diagnosis_match.group(1).strip()

    # 💊 Medications (EN or DE)
    meds_match = re.search(
        r"(?:Medications on Discharge:|Medikation.*?:)\s*(.*?)(?:Discharge Instructions:|Empfehlungen:|$)",
        text, re.DOTALL
    )
    if meds_match:
        fields["medications"] = meds_match.group(1).strip()

    # 📋 Follow-up / Instructions (EN or DE)
    follow_match = re.search(
        r"(?:Discharge Instructions:|Empfehlungen:|Follow-up:)\s*(.*)", text, re.DOTALL
    )
    if follow_match:
        fields["follow_up"] = follow_match.group(1).strip()

    return fields

def map_to_fhir(text):
    clean = clean_text(text)
    extracted = extract_fields(clean)

    fhir_output = {
        "resourceType": "DischargeSummary",
        "patient": {
            "name": extracted["patient_name"]
        },
        "diagnosis": {
            "text": extracted["diagnosis"]
        },
        "medications": extracted["medications"],
        "follow_up": extracted["follow_up"],
        "raw_text": clean
    }

    return fhir_output
