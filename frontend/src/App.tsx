import { useState } from 'react';
import { Activity, Database, Network, Search, Send, Zap, Bot, Microscope, Target } from 'lucide-react';
import './index.css';

function App() {
  const [query, setQuery] = useState('');

  return (
    <div className="dashboard-container">
      
      {/* LEFT PANEL: NAVIGATION & METRICS */}
      <aside className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '32px' }}>
        <div>
          <h1 className="text-gradient-cyan" style={{ fontSize: '24px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Network size={28} color="var(--neon-cyan)" />
            Nexus Health
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginTop: '4px' }}>
            Agentic Knowledge Graph
          </p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <h3 style={{ color: 'var(--text-muted)', fontSize: '12px', textTransform: 'uppercase', letterSpacing: '1px' }}>
            Live Intelligence
          </h3>
          
          <div className="glass-card flex-between" style={{ padding: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ padding: '8px', borderRadius: '8px', background: 'rgba(0, 240, 255, 0.1)' }}>
                <Microscope size={20} color="var(--neon-cyan)" />
              </div>
              <div>
                <div style={{ color: 'var(--text-primary)', fontSize: '18px', fontWeight: '600' }}>2,405</div>
                <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Patents Scraped</div>
              </div>
            </div>
          </div>

          <div className="glass-card flex-between" style={{ padding: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ padding: '8px', borderRadius: '8px', background: 'rgba(138, 43, 226, 0.1)' }}>
                <Activity size={20} color="var(--neon-purple)" />
              </div>
              <div>
                <div style={{ color: 'var(--text-primary)', fontSize: '18px', fontWeight: '600' }}>8,192</div>
                <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Clinical Trials</div>
              </div>
            </div>
          </div>

          <div className="glass-card flex-between" style={{ padding: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ padding: '8px', borderRadius: '8px', background: 'rgba(0, 255, 135, 0.1)' }}>
                <Target size={20} color="var(--neon-green)" />
              </div>
              <div>
                <div style={{ color: 'var(--text-primary)', fontSize: '18px', fontWeight: '600' }}>1,104</div>
                <div style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>Regulatory Licenses</div>
              </div>
            </div>
          </div>
        </div>

        <div style={{ marginTop: 'auto' }}>
          <div className="glass-card" style={{ padding: '16px', display: 'flex', alignItems: 'center', gap: '12px' }}>
            <Database size={16} color="var(--neon-green)" />
            <span style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>Neo4j Status: <span style={{ color: 'var(--neon-green)' }}>Simulated</span></span>
          </div>
        </div>
      </aside>

      {/* CENTER PANEL: KNOWLEDGE GRAPH VISUALIZER */}
      <main className="glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '24px', borderBottom: '1px solid var(--border-glass)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ fontSize: '18px', fontWeight: '500' }}>Biomedical Graph Explorer</h2>
          <div style={{ position: 'relative' }}>
            <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
            <input 
              type="text" 
              placeholder="Search Entities..." 
              style={{
                background: 'rgba(0,0,0,0.3)',
                border: '1px solid var(--border-glass)',
                borderRadius: '20px',
                padding: '8px 16px 8px 36px',
                color: 'white',
                outline: 'none',
                width: '250px'
              }}
            />
          </div>
        </div>
        
        <div style={{ flex: 1, position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          {/* Placeholder for 3D Force Graph */}
          <div style={{ textAlign: 'center', color: 'var(--text-muted)' }}>
            <Network size={64} style={{ opacity: 0.2, margin: '0 auto 16px' }} />
            <p>Graph Visualizer Initializing...</p>
          </div>
        </div>
      </main>

      {/* RIGHT PANEL: RAG AI ASSISTANT */}
      <aside className="glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '24px', borderBottom: '1px solid var(--border-glass)', display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Bot size={24} color="var(--neon-purple)" />
          <h2 style={{ fontSize: '18px', fontWeight: '500' }} className="text-gradient-purple">A.I. Intelligence</h2>
        </div>
        
        <div style={{ flex: 1, padding: '24px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Example AI Message */}
          <div style={{ display: 'flex', gap: '12px' }}>
            <div style={{ background: 'rgba(138, 43, 226, 0.2)', padding: '8px', borderRadius: '8px', height: 'fit-content' }}>
              <Zap size={16} color="var(--neon-purple)" />
            </div>
            <div className="glass-card" style={{ padding: '16px', flex: 1 }}>
              <p style={{ fontSize: '14px', lineHeight: '1.6', color: 'var(--text-primary)' }}>
                System Online. I am connected to the Neo4j Knowledge Graph. You can ask me questions about patents, clinical trials, or regulatory licenses.
              </p>
            </div>
          </div>
        </div>

        <div style={{ padding: '24px', borderTop: '1px solid var(--border-glass)' }}>
          <div style={{ position: 'relative' }}>
            <input 
              type="text" 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask the Graph..." 
              style={{
                width: '100%',
                background: 'rgba(0,0,0,0.4)',
                border: '1px solid var(--border-glass)',
                borderRadius: '12px',
                padding: '16px 48px 16px 16px',
                color: 'white',
                outline: 'none',
                fontSize: '14px'
              }}
            />
            <button 
              style={{
                position: 'absolute',
                right: '8px',
                top: '50%',
                transform: 'translateY(-50%)',
                background: 'var(--neon-purple)',
                border: 'none',
                borderRadius: '8px',
                width: '32px',
                height: '32px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer'
              }}
            >
              <Send size={16} color="white" />
            </button>
          </div>
        </div>
      </aside>

    </div>
  );
}

export default App;
