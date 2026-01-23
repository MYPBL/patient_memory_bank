import React from 'react';
import { PatientChat } from './components/PatientChat';
import { MedicalGraph } from './components/MedicalGraph';

function App() {
  const patientId = "sarah_001";

  return (
    <div style={{ height: '100vh', width: '100vw', backgroundColor: '#f1f5f9', padding: '32px', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: '24px', fontFamily: 'sans-serif' }}>
      <header style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '24px', fontWeight: 900, color: '#1e3a8a', letterSpacing: '-1px' }}>PATIENT MEMORY BANK</h1>
          <p style={{ margin: 0, fontSize: '12px', color: '#64748b', fontWeight: 500 }}>Multi-Agent Shared Cognitive Memory System</p>
        </div>
        <div style={{ backgroundColor: 'white', padding: '4px 12px', borderRadius: '20px', border: '1px solid #e2e8f0', fontSize: '10px', fontWeight: 'bold', color: '#94a3b8 shadow-sm' }}>
          PATIENT ID: {patientId}
        </div>
      </header>

      <main style={{ flex: 1, display: 'flex', gap: '32px', minHeight: 0 }}>
        <div style={{ width: '30%', minWidth: '350px' }}>
          <PatientChat patientId={patientId} />
        </div>
        <div style={{ flex: 1 }}>
          <MedicalGraph patientId={patientId} />
        </div>
      </main>
    </div>
  );
}

export default App;