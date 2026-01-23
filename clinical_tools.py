# clinical_tools.py
import json

async def triage_symptoms(db, patient_id, symptoms, severity):
    """
    Tool: Categorizes symptoms and saves them to the patient's event timeline.
    """
    triage_map = {
        "low": "Schedule Routine Appointment",
        "medium": "Urgent Care Recommended",
        "high": "Immediate ER/Specialist Referral"
    }
    
    result = {
        "action": triage_map.get(severity, "Consult Doctor"),
        "symptoms_logged": symptoms,
        "severity": severity
    }
    
    # Save structured data to the 'Shared Brain'
    await db.ingest(f"CLINICAL_TRIAGE: {json.dumps(result)}")
    return result

async def record_vitals(db, patient_id, heart_rate, blood_pressure):
    """
    Tool: Records physical vitals into the memory graph.
    """
    vitals = {
        "hr": heart_rate,
        "bp": blood_pressure,
        "timestamp": "2026-01-23 10:00" # Example timestamp
    }
    
    await db.ingest(f"VITALS_LOG: {json.dumps(vitals)}")
    return {"status": "Vitals recorded successfully"}