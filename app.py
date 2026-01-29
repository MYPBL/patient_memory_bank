import asyncio
import os
from deltamemory import DeltaMemory, IngestOptions
from dotenv import load_dotenv
from prompts import RECEPTION_SYSTEM #

load_dotenv()
API_KEY = os.getenv("DELTA_API_KEY")
CONN_URL = os.getenv("DELTA_CONN_URL")

headers_dict = {
    "Authorization": f"Bearer {API_KEY}"
}

db = DeltaMemory(
    base_url=CONN_URL,
    headers=headers_dict,
    default_collection="sarah_hospital_test"
)

async def reception_check_in(db, patient_name):
    print(f"\n--- [Reception Agent] Checking in: {patient_name} ---")
    
    # 1. Identity Recognition: Fetch existing profile
    search_query = f"Find basic profile, insurance, and blood type for {patient_name}"
    recognition_data = await db.recall(search_query) #
    
    if recognition_data.context:
        print("✅ Identity Recognized!")
        print(f"Agent Greeting: 'Welcome back, {patient_name}. I see you are still with your current provider. Has your address changed?'")
    else:
        print("🆕 New Patient Detected. Starting first-time registration.")
        await db.ingest(f"New Patient Registration: {patient_name}") #

        from clinical_tools import triage_symptoms

async def diagnose_and_triage(db, patient_id, symptoms):
    print(f"\n--- [Diagnosis Agent] Analyzing Symptoms for: {patient_id} ---")
    
    # 1. Pull History: The Agent looks at past surgeries and chronic conditions
    # This fulfills the "Initial Diagnosis" part of your use case
    history_brief = await db.recall(f"Does {patient_id} have history of heart disease or major surgeries?")
    print(f"Historical Context Found: {history_brief.context}")

    # 2. Triage: Use your clinical tool to determine severity
    # We'll set it to 'high' because Sarah has chest pain + Diabetes history
    triage_result = await triage_symptoms(db, patient_id, symptoms, severity="high")
    
    print(f" Triage Action: {triage_result['action']}")
    print(f" Diagnosis logged to Shared Brain.")

async def discharge_and_followup(db, patient_id, doctor_notes):
    print(f"\n--- [Discharge Agent] Processing Exit for: {patient_id} ---")
    
    # Action 1: Ingest the Doctor's notes so the next doctor sees them
    # This closes the loop and ensures continuity of care
    print("📝 Saving doctor's diagnosis to Event Timeline...")
    await db.ingest(
        f"FINAL DIAGNOSIS for {patient_id}: {doctor_notes}",
        options=IngestOptions(speaker="doctor")
    )

    # Action 2: Query the memory for a "Recovery Plan"
    # This pulls from the newly saved notes to create a patient to-do list
    print("📋 Generating Patient Recovery Plan...")
    followup_query = f"Based on the diagnosis '{doctor_notes}', what are the recovery steps for {patient_id}?"
    recovery_data = await db.recall(followup_query)
    
    print("\n--- PATIENT FOLLOW-UP PLAN ---")
    print(recovery_data.context)
    print("------------------------------")
    print("✅ Discharge complete. Visit coded for insurance.")

async def main():
    print(" System Online: Patient Memory Bank")

    patient_note = """
    PATIENT CASE: Sarah Miller, 45 years old. 
    MEDICAL HISTORY: She has been living with Type 2 Diabetes since 2018. 
    ALLERGIES: Severe anaphylactic reaction to Latex and Penicillin.
    SURGERY: Had an ACL reconstruction in her left knee in 2022.
    CURRENT COMPLAINT: Patient reports sharp chest pain and shortness of breath starting 2 hours ago.
    """
    
    try:
        # STEP 1: Reception (Identity Recognition)
        await reception_check_in(db, "Sarah Miller")

        # STEP 2: Record Current Visit Symptoms
        print("\nIngesting Current Visit...")
        ingest_response = await db.ingest(
            patient_note, 
            options=IngestOptions(speaker="patient")
        )
        print(f"Success! Facts Extracted: {ingest_response.facts}") #

        current_symptoms = "sharp chest pain and shortness of breath"
        await diagnose_and_triage(db, "Sarah Miller", current_symptoms)

        # STEP 3: Generate Doctor's Briefing
        print("\n Recalling for Doctor...")
        briefing = await db.recall("Summarize Sarah's history.") #
        print(f"\n--- BRIEF ---\n{briefing.context}")
        
        print("\n✅ Reception process complete. Data synced to Shared Brain.")
        print("\n👨‍⚕️ Specialist is reviewing the case...")
        await db.recall("Summarize Sarah's history for the Cardiologist.")

        # STEP 4: Discharge & Follow-up (The New Part)
        # This simulates the doctor's actual findings at the end of the appointment
        final_doctor_notes = "Suspected Angina. Prescribed Nitroglycerin. Patient advised to avoid heavy lifting for 2 weeks."
        
        await discharge_and_followup(db, "Sarah Miller", final_doctor_notes)
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())