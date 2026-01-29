import React, { useState } from 'react';
import { Send, Activity } from 'lucide-react';

export function PatientChat({ patientId }: { patientId: string }) {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [agentType, setAgentType] = useState("reception");

  const onSend = async () => {
    if (!input) return;
    const userMsg = { role: "patient", text: input };
    setMessages([...messages, userMsg]);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ patient_id: patientId, agent_type: agentType, message: input })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: agentType, text: data.response, tool: data.tool_used }]);
      setInput("");
    } catch (err) {
      console.error("Chat error:", err);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', border: '1px solid #e2e8f0', borderRadius: '8px', backgroundColor: 'white', overflow: 'hidden' }}>
      <div style={{ backgroundColor: '#1d4ed8', padding: '16px', color: 'white', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ margin: 0, fontSize: '16px' }}>Hospital Agent Network</h2>
        <select 
          style={{ backgroundColor: '#1e40af', color: 'white', fontSize: '12px', border: 'none', borderRadius: '4px', padding: '4px' }}
          value={agentType} 
          onChange={(e) => setAgentType(e.target.value)}
        >
          <option value="reception">Receptionist</option>
          <option value="diagnosis">Diagnosis/Triage</option>
          <option value="specialist">Specialist</option>
        </select>
      </div>
      
      <div style={{ flex: 1, padding: '16px', overflowY: 'auto', backgroundColor: '#f8fafc' }}>
        {messages.map((m, i) => (
          <div key={i} style={{ display: 'flex', justifyContent: m.role === 'patient' ? 'flex-end' : 'flex-start', marginBottom: '16px' }}>
            <div style={{ padding: '12px', borderRadius: '12px', maxWidth: '85%', backgroundColor: m.role === 'patient' ? '#2563eb' : 'white', color: m.role === 'patient' ? 'white' : '#1e293b', boxShadow: '0 1px 2px rgba(0,0,0,0.05)', border: m.role === 'patient' ? 'none' : '1px solid #e2e8f0' }}>
              <p style={{ margin: 0, fontSize: '14px' }}>{m.text}</p>
              {m.tool && (
                <div style={{ marginTop: '8px', paddingTop: '8px', borderTop: '1px solid #fee2e2', fontSize: '10px', display: 'flex', alignItems: 'center', gap: '4px', color: '#ef4444', fontWeight: 'bold' }}>
                  <Activity size={12} /> TOOL: {m.tool.action}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div style={{ padding: '16px', borderTop: '1px solid #e2e8f0', display: 'flex', gap: '8px' }}>
        <input 
          style={{ flex: 1, border: '1px solid #cbd5e1', borderRadius: '20px', padding: '8px 16px', fontSize: '14px' }}
          value={input} onChange={(e) => setInput(e.target.value)}
          placeholder="Type here..."
          onKeyDown={(e) => e.key === 'Enter' && onSend()}
        />
        <button onClick={onSend} style={{ backgroundColor: '#2563eb', color: 'white', border: 'none', borderRadius: '50%', width: '36px', height: '36px', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer' }}>
          <Send size={18} />
        </button>
      </div>
    </div>
  );
}