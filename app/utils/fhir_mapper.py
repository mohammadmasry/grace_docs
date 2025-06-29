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

    if "Name:" in text:
        match = re.search(r"Name:\s*(.*)", text)
        if match:
            fields["patient_name"] = " ".join(match.group(1).split()[0:3])

    if "Diagnosis:" in text:
        match = re.search(r"Diagnosis:\s*(.*)", text)
        if match:
            fields["diagnosis"] = match.group(1).strip()

    if "Medications:" in text:
        match = re.search(r"Medications:\s*(.*)", text)
        if match:
            fields["medications"] = match.group(1).strip()

    if "Follow-up:" in text:
        match = re.search(r"Follow-up:\s*(.*)", text)
        if match:
            fields["follow_up"] = match.group(1).strip()

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
