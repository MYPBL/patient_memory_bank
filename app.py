# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS # Run: pip install flask-cors
import asyncio

# Import your supporting modules
from mock_sdk import MockDeltaMemory
from prompts import RECEPTION_SYSTEM, DIAGNOSIS_SYSTEM, SPECIALIST_SYSTEM, DISCHARGE_SYSTEM
from clinical_tools import triage_symptoms, record_vitals

app = Flask(__name__)
CORS(app) # Allows your React frontend to connect to this Python backend
db = MockDeltaMemory()

# Map agent types to their system prompts from prompts.py
AGENT_PROMPTS = {
    "reception": RECEPTION_SYSTEM,
    "diagnosis": DIAGNOSIS_SYSTEM,
    "specialist": SPECIALIST_SYSTEM,
    "discharge": DISCHARGE_SYSTEM
}

@app.route('/chat', methods=['POST'])
async def chat():
    """
    Handles Multi-Agent switching and memory-driven conversations.
    Mirrors the logic in learning-tutor/src/app/api/chat/route.ts.
    """
    data = request.json
    patient_id = data.get('patient_id', 'sarah_001')
    agent_type = data.get('agent_type', 'reception')
    message = data.get('message', '')

    # 1. CENTRALIZED CONTINUITY: Recall shared history for this specific patient
    memory = await db.recall(f"History for {patient_id}")
    
    # 2. AGENT SWITCHING: Select the specialized "brain" for this hospital phase
    system_prompt = AGENT_PROMPTS.get(agent_type, RECEPTION_SYSTEM)
    
    # 3. CLINICAL TOOLS: If in diagnosis phase, automatically trigger the triage tool
    tool_results = None
    if agent_type == "diagnosis":
        # Simulate identifying a symptom to triage
        tool_results = await triage_symptoms(db, patient_id, message, "high")

    # 4. UPDATE SHARED BRAIN: Store the interaction so the NEXT agent sees it
    await db.ingest(f"[{agent_type.upper()}] Patient said: {message}")

    # Return the response (In a real app, you would call an LLM here with the system_prompt)
    return jsonify({
        "agent": agent_type,
        "context_recalled": memory.context,
        "tool_used": tool_results,
        "response": f"The {agent_type} agent has processed your message and updated your memory bank."
    })

@app.route('/api/graph', methods=['GET'])
async def get_graph():
    """
    Exposes the memory graph for the D3 visualization component.
    Mirrors learning-tutor/src/app/api/graph/route.ts.
    """
    patient_id = request.args.get('patientId')
    if not patient_id:
        return jsonify({"error": "patientId required"}), 400
    
    # Retrieve the Nodes and Edges from DeltaMemory
    graph_data = await db.graph(patient_id)
    return jsonify(graph_data)

if __name__ == "__main__":
    # Use 'threaded=True' to handle the async calls properly in Flask
    app.run(port=5000, debug=True)