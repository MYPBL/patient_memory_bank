import React, { useState, useEffect } from 'react';
import { PatientChat } from './components/PatientChat';
import { MedicalGraph } from './components/MedicalGraph';

// 1. Separate component for the Recovery Plan
// This fulfills the "Discharge Agent" requirement in your UI
const PatientPlan = ({ patientName }: { patientName: string }) => {
  const [plan, setPlan] = useState("");

  useEffect(() => {
    // Fetches the recovery plan from your FastAPI backend
    fetch(`http://localhost:8000/api/discharge/${patientName}`)
      .then(response => response.json())
      .then(data => setPlan(data.recovery_plan))
      .catch(err => console.error("FastAPI not running:", err));
  }, [patientName]);

  return (
    <div style={{ backgroundColor: 'white', padding: '16px', borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', marginTop: '24px' }}>
      <h2 style={{ margin: 0, fontSize: '16px', fontWeight: 800, color: '#1e3a8a' }}>🏥 YOUR RECOVERY PLAN</h2>
      <p style={{ marginTop: '8px', fontSize: '14px', color: '#475569', lineHeight: '1.5' }}>
        {plan || "Waiting for Doctor's Discharge..."}
      </p>
    </div>
  );
};

function App() {
  // Matches the ID and collection used in your Python app
  const patientId = "Sarah Miller"; 

  return (
    <div style={{ height: '100vh', width: '100vw', backgroundColor: '#f1f5f9', padding: '32px', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: '24px', fontFamily: 'sans-serif' }}>
      
      {/* HEADER SECTION */}
      <header style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '24px', fontWeight: 900, color: '#1e3a8a', letterSpacing: '-1px' }}>PATIENT MEMORY BANK</h1>
          <p style={{ margin: 0, fontSize: '12px', color: '#64748b', fontWeight: 500 }}>Multi-Agent Shared Cognitive Memory System</p>
        </div>
        <div style={{ backgroundColor: 'white', padding: '6px 12px', borderRadius: '20px', border: '1px solid #e2e8f0', fontSize: '10px', fontWeight: 'bold', color: '#64748b', boxShadow: '0 1px 2px rgba(0,0,0,0.05)' }}>
          PATIENT NAME: {patientId}
        </div>
      </header>

      {/* MAIN CONTENT AREA */}
      <main style={{ flex: 1, display: 'flex', gap: '32px', minHeight: 0 }}>
        
        {/* LEFT COL: Chat & Discharge Plan */}
        <div style={{ width: '30%', minWidth: '350px', display: 'flex', flexDirection: 'column' }}>
          <div style={{ flex: 1, minHeight: 0 }}>
            <PatientChat patientId={patientId} />
          </div>
          <PatientPlan patientName={patientId} />
        </div>

        {/* RIGHT COL: Knowledge Graph */}
        <div style={{ flex: 1, backgroundColor: 'white', borderRadius: '16px', border: '1px solid #e2e8f0', overflow: 'hidden', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}>
          <MedicalGraph patientId={patientId} />
        </div>

      </main>
    </div>
  );
}

export default App;