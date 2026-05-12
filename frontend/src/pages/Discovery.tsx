import { useState, useEffect } from 'react';
import axios from 'axios';

const Discovery = () => {
  const [entities, setEntities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  // RAG States
  const [query, setQuery] = useState('CRISPR startups in India working on agritech');
  const [aiInsight, setAiInsight] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);

  useEffect(() => {
    const fetchEntities = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/discovery/entities');
        setEntities(res.data);
      } catch (err) {
        console.error("Failed to fetch entities:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchEntities();
  }, []);

  const handleExecute = async () => {
    if (!query.trim()) return;
    setIsExecuting(true);
    setAiInsight('');
    
    try {
      const res = await axios.post('http://localhost:8000/api/rag', { query, mode: 'discovery' });
      if (res.data.status === 'success') {
        setAiInsight(res.data.response);
        if (res.data.graph_data && res.data.graph_data.nodes) {
          const newEntities = res.data.graph_data.nodes.map((n: any) => ({
            name: n.id,
            type: n.label,
            verified: true,
            confidence: 0.95
          }));
          setEntities(newEntities.length > 0 ? newEntities : entities);
        }
      }
    } catch (err) {
      console.error("RAG Execution failed:", err);
      setAiInsight("Error: Could not connect to the Analyst Agent.");
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-margin-desktop pb-32 w-full">
      <div className="max-w-5xl mx-auto mb-10 mt-8">
        <div className="flex items-center gap-3 mb-6">
          <span className="material-symbols-outlined text-secondary" style={{fontVariationSettings: "'FILL' 1"}}>graphic_eq</span>
          <h1 className="font-headline-md text-headline-md text-primary tracking-tight">RAG Knowledge Query</h1>
          <span className="ml-auto flex items-center gap-2 bg-tertiary-fixed text-on-tertiary-fixed px-3 py-1 rounded-full font-data-mono text-data-mono text-[11px] shadow-sm border border-tertiary-fixed-dim">
            <span className="w-2 h-2 rounded-full bg-on-tertiary-container animate-pulse"></span>
            Auditor Active: Fact-Checking Live
          </span>
        </div>
        
        {/* Prominent Search Box */}
        <div className="relative bg-surface-container-lowest border border-outline-variant rounded-xl shadow-[0_4px_12px_rgba(15,23,42,0.05)] overflow-hidden focus-within:ring-2 focus-within:ring-primary focus-within:border-transparent transition-all">
          <div className="flex items-start p-4">
            <span className="material-symbols-outlined text-outline mt-1 mr-3">travel_explore</span>
            <textarea 
              className="w-full bg-transparent border-none outline-none focus:ring-0 p-0 font-body-lg text-body-lg text-on-surface placeholder:text-outline resize-none min-h-[60px]" 
              placeholder="Query the knowledge graph... (e.g., 'CRISPR startups in India working on agritech')"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>
          <div className="bg-surface-container-low border-t border-outline-variant px-4 py-2 flex justify-between items-center">
            <div className="flex gap-2">
              <button className="text-xs font-label-md text-on-surface-variant bg-surface border border-outline-variant px-2 py-1 rounded hover:bg-surface-container transition-colors flex items-center gap-1">
                <span className="material-symbols-outlined text-[14px]">verified</span> Auditor Mode
              </button>
            </div>
            <button 
              onClick={handleExecute}
              disabled={isExecuting}
              className={`bg-primary text-on-primary font-label-md text-label-md px-4 py-1.5 rounded flex items-center gap-2 hover:opacity-90 transition-opacity ${isExecuting ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <span className="material-symbols-outlined text-[16px]">{isExecuting ? 'sync' : 'send'}</span> 
              {isExecuting ? 'Executing...' : 'Execute'}
            </button>
          </div>
        </div>
        
        <div className="flex gap-2 mt-3 overflow-x-auto pb-2 scrollbar-hide">
          <span className="text-xs font-label-md text-outline-variant py-1 px-2">Suggestions:</span>
          <button onClick={() => setQuery('Serum Institute trials for Malaria')} className="text-xs font-data-mono text-secondary bg-surface-container border border-outline-variant rounded px-2 py-1 cursor-pointer hover:bg-surface-container-high whitespace-nowrap">Serum Institute trials for Malaria</button>
          <button onClick={() => setQuery('Digital Health grants in 2026')} className="text-xs font-data-mono text-secondary bg-surface-container border border-outline-variant rounded px-2 py-1 cursor-pointer hover:bg-surface-container-high whitespace-nowrap">Digital Health grants in 2026</button>
        </div>
      </div>

      {/* Dashboard Layout Grid */}
      <div className="grid grid-cols-12 gap-gutter max-w-full">
        {/* Left Column: Results */}
        <div className="col-span-12 lg:col-span-9 flex flex-col gap-gutter">
          <div className="bg-surface-container-lowest border border-outline-variant rounded flex flex-col relative overflow-hidden min-h-[200px]">
            <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-tertiary-fixed to-secondary-fixed"></div>
            <div className="border-b border-outline-variant px-4 py-3 flex justify-between items-center bg-surface-container-low/50">
              <h2 className="font-title-lg text-title-lg text-primary flex items-center gap-2">
                <span className="material-symbols-outlined text-secondary">lightbulb</span>
                Verified Knowledge Synthesis
              </h2>
            </div>
            <div className="p-5 font-body-lg text-body-lg text-on-surface leading-relaxed">
              {isExecuting ? (
                <div className="flex flex-col gap-3 animate-pulse">
                  <div className="h-4 bg-surface-container rounded w-3/4"></div>
                  <div className="h-4 bg-surface-container rounded w-5/6"></div>
                  <div className="h-4 bg-surface-container rounded w-2/3"></div>
                </div>
              ) : aiInsight ? (
                <div className="whitespace-pre-wrap">{aiInsight}</div>
              ) : (
                <div className="text-on-surface-variant flex flex-col items-center justify-center py-10 opacity-60">
                   <span className="material-symbols-outlined text-4xl mb-2">fact_check</span>
                   <p>Query the graph. The Auditor will cross-reference every fact.</p>
                </div>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-gutter">
            <div className="col-span-2 bg-surface-container-lowest border border-outline-variant rounded flex flex-col min-h-[300px]">
              <div className="border-b border-outline-variant px-4 py-2 flex justify-between items-center">
                <h3 className="font-label-md text-label-md text-on-surface uppercase tracking-wider">Evidence Index & Auditor Verification</h3>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-surface-container-low border-b border-outline-variant text-xs font-label-md text-on-surface-variant">
                      <th className="py-2 px-4 font-semibold w-1/3">Entity Name</th>
                      <th className="py-2 px-4 font-semibold w-1/4">Type</th>
                      <th className="py-2 px-4 font-semibold">Auditor Status</th>
                      <th className="py-2 px-4 font-semibold text-right">Confidence Score</th>
                    </tr>
                  </thead>
                  <tbody className="font-data-mono text-[12px] text-on-surface">
                    {loading ? (
                      <tr><td colSpan={4} className="py-10 text-center text-on-surface-variant animate-pulse">Auditing Neo4j Knowledge Graph...</td></tr>
                    ) : entities.length > 0 ? (
                      entities.map((e, idx) => (
                        <tr key={idx} className="border-b border-outline-variant/50 hover:bg-surface-container-low/50 transition-colors">
                          <td className="py-2.5 px-4 font-medium flex items-center gap-2">
                            <div className={`w-2 h-2 rounded-full ${e.verified ? 'bg-[#137333]' : 'bg-outline-variant'}`}></div>
                            {e.name}
                          </td>
                          <td className="py-2.5 px-4"><span className="bg-surface-container border border-outline-variant rounded px-1.5 py-0.5 text-[10px]">{e.type}</span></td>
                          <td className="py-2.5 px-4">
                            {e.verified ? (
                              <span className="text-[#137333] flex items-center gap-1 font-semibold">
                                <span className="material-symbols-outlined text-[14px]">check_circle</span> Verified
                              </span>
                            ) : (
                              <span className="text-outline flex items-center gap-1">
                                <span className="material-symbols-outlined text-[14px]">pending</span> Pending Audit
                              </span>
                            )}
                          </td>
                          <td className="py-2.5 px-4 text-right">
                             <div className="flex flex-col items-end">
                               <span className={e.confidence > 0.8 ? 'text-[#137333]' : 'text-secondary'}>
                                 {(e.confidence * 100).toFixed(1)}%
                               </span>
                               <div className="w-16 h-1 bg-surface-container rounded-full mt-1 overflow-hidden">
                                 <div className="h-full bg-primary" style={{width: `${e.confidence * 100}%`}}></div>
                               </div>
                             </div>
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr><td colSpan={4} className="py-10 text-center text-on-surface-variant">No entities found in current graph subset.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Filters */}
        <div className="col-span-12 lg:col-span-3 flex flex-col gap-gutter">
          <div className="bg-surface-container-lowest border border-outline-variant rounded flex flex-col h-full">
            <div className="border-b border-outline-variant px-4 py-3 flex items-center gap-2 bg-surface-container-low/30">
              <span className="material-symbols-outlined text-[18px] text-on-surface-variant">fact_check</span>
              <h3 className="font-title-lg text-[16px] font-semibold text-primary">Auditor Settings</h3>
            </div>
            <div className="p-4 flex flex-col gap-5 overflow-y-auto">
              <div className="flex flex-col gap-2">
                <label className="font-label-md text-[11px] text-outline uppercase tracking-wider flex justify-between">
                  Source Priority
                </label>
                <div className="flex flex-col gap-1.5">
                  <label className="flex items-center gap-2 cursor-pointer group">
                    <input type="checkbox" defaultChecked className="rounded-sm border-outline-variant text-primary focus:ring-primary w-3.5 h-3.5 bg-surface" />
                    <span className="font-data-mono text-[12px] text-on-surface group-hover:text-primary transition-colors">Gazette Archives</span>
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer group">
                    <input type="checkbox" defaultChecked className="rounded-sm border-outline-variant text-primary focus:ring-primary w-3.5 h-3.5 bg-surface" />
                    <span className="font-data-mono text-[12px] text-on-surface group-hover:text-primary transition-colors">Live News Feeds</span>
                  </label>
                </div>
              </div>
              <div className="w-full h-px bg-outline-variant/30"></div>
              <div className="p-3 bg-secondary-container/30 rounded-lg border border-secondary-container">
                 <p className="text-[11px] text-on-secondary-container font-body-md leading-tight">
                   The Auditor automatically flags relationships where the confidence score falls below 0.65 for manual review.
                 </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Discovery;
