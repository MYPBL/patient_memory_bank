# app.py
import asyncio
from mock_sdk import MockDeltaMemory # Switch to 'from deltamemory import DeltaMemory' once you have the key

async def main():
    # Initialize the mock database
    db = MockDeltaMemory()

    # --- PATIENT SIDE ---
    print("--- PATIENT CHECK-IN ---")
    patient_note = "I'm Sarah. I'm allergic to Penicillin and have chest pain."
    await db.ingest(patient_note)

    # --- HOSPITAL SIDE ---
    print("\n--- DOCTOR VIEW ---")
    briefing = await db.recall("What is Sarah's history?")
    print(briefing.context) 

if __name__ == "__main__":
    asyncio.run(main())