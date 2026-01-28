import asyncio
import os
from deltamemory import DeltaMemory, IngestOptions
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DELTA_API_KEY")
CONN_URL = os.getenv("DELTA_CONN_URL")

# The SDK wants the API key in the 'headers' dictionary
headers_dict = {
    "Authorization": f"Bearer {API_KEY}"
}

# Now we initialize exactly as your VS Code hover box showed:
db = DeltaMemory(
    base_url=CONN_URL,
    headers=headers_dict,
    default_collection="sarah_hospital_test"
)

async def main():
    print("Connecting to live Patient Memory Bank...")

    patient_note = """
    PATIENT CASE: Sarah Miller, 45 years old. 
    MEDICAL HISTORY: She has been living with Type 2 Diabetes since 2018. 
    ALLERGIES: Severe anaphylactic reaction to Latex and Penicillin.
    SURGERY: Had an ACL reconstruction in her left knee in 2022.
    CURRENT COMPLAINT: Patient reports sharp chest pain and shortness of breath starting 2 hours ago.
    """
    
    try:
        # 1. Ingest
        print(" Ingesting...")
        ingest_response = await db.ingest(
            patient_note, 
            options=IngestOptions(speaker="patient")
        )
        print(f"Success! Facts: {ingest_response.facts}")

        # 2. Recall
        print("Recalling...")
        briefing = await db.recall("Summarize Sarah's history.")
        print(f"\n--- BRIEF ---\n{briefing.context}")
        
    except Exception as e:
        print(f" An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())