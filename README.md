# Patient Memory Bank (AI-Powered Healthcare Context)
This project aims to eliminate repetitive paperwork and prevent context loss during medical handoffs.

## The Problem
- **Repitative Paperwork :** Patients fill out the same "case papers" for every department visit.
- **Context Loss:** Critical patient details are often lost during shift changes or department transfers.
- **Fragmented Care:** Specialists often lack the full history recorded by general practitioners.

## The Solution: "Shared Brain" Architecture
By using **DeltaMemory** as a centralized cognitive layer, this project connects two specialized AI agents:

1. **Intake Agent (Patient Side):** Greets the patient via mobile/kiosk and "ingests" their history, automatically extracting facts like allergies and past surgeries.
2. **Doctor Agent (Hospital Side):** Recalls the patient's centralized history to provide a "30-second medical brief" before a consultation starts.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Memory Engine:** DeltaMemory Python SDK
- **Environment:** VS Code + Virtual Environment (venv)

## Project Structure
- `app.py`: Main application logic for the Intake and Doctor agents.
- `mock_sdk.py`: Simulation layer to test logic .
- `requirements.txt`: List of necessary Python libraries.
- `.env`: (Configuration) Stores the DeltaMemory API key and Base URL.

## ⚙️ Setup & Installation

1. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: .\venv\Scripts\activate