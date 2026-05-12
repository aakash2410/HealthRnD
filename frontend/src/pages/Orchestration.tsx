import { useState, FormEvent } from 'react';
import axios from 'axios';

const Orchestration = () => {
  const [query, setQuery] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [aiResponse, setAiResponse] = useState('');
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

  const handleSearch = async (e: FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setIsTyping(true);
    setAiResponse('');
    setGraphData({ nodes: [], links: [] });
    
    try {
      const res = await axios.post('http://localhost:8000/api/rag', { query, mode: 'orchestration' });
      if (res.data.status === 'success') {
        setAiResponse(res.data.response);
        if (res.data.graph_data) {
          setGraphData(res.data.graph_data);
        }
      } else {
        setAiResponse("System Error: Could not parse Knowledge Graph.");
      }
    } catch (err) {
      setAiResponse("Network Error: Cannot connect to Nexus API Bridge.");
    } finally {
      setIsTyping(false);
    }
  };

  const formatMarkdown = (text: string) => {
    let formatted = text.replace(/## (.*?)\n/g, '<h2 class="font-title-lg text-title-lg text-on-surface border-b border-surface-variant pb-2 mb-4 mt-8">$1</h2>');
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<b class="text-primary font-semibold">$1</b>');
    formatted = formatted.replace(/\n\n/g, '</p><p class="font-body-md text-body-md text-on-surface-variant leading-relaxed mb-4">');
    formatted = '<p class="font-body-md text-body-md text-on-surface-variant leading-relaxed mb-4">' + formatted + '</p>';
    formatted = formatted.replace(/<p[^>]*><\/p>/g, '');
    return { __html: formatted };
  };

  return (
    <>
      <div className="flex-[3] flex flex-col border-r border-outline-variant overflow-hidden">
        <div className="h-12 border-b border-surface-variant bg-surface flex items-center justify-between px-4 shrink-0">
          <div className="flex items-center gap-3">
            <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-widest">Draft Investment Memo</span>
            {aiResponse && (
              <div className="px-2 py-0.5 bg-secondary-container text-on-secondary-container font-data-mono text-data-mono rounded-DEFAULT text-[11px] flex items-center gap-1">
                <span className="material-symbols-outlined" style={{fontSize: '12px'}}>auto_awesome</span>
                AI Generated
              </div>
            )}
          </div>
          <div className="flex items-center gap-2">
            <button className="p-1.5 text-on-surface-variant hover:bg-surface-container rounded-DEFAULT"><span className="material-symbols-outlined" style={{fontSize: '18px'}}>format_bold</span></button>
            <button className="p-1.5 text-on-surface-variant hover:bg-surface-container rounded-DEFAULT"><span className="material-symbols-outlined" style={{fontSize: '18px'}}>format_italic</span></button>
            <button className="p-1.5 text-on-surface-variant hover:bg-surface-container rounded-DEFAULT"><span className="material-symbols-outlined" style={{fontSize: '18px'}}>format_list_bulleted</span></button>
          </div>
        </div>
        
        <div className="flex-1 overflow-y-auto p-8 max-w-4xl mx-auto w-full">
          <form onSubmit={handleSearch} className="mb-6">
             <div className="flex items-center bg-surface-container-low border border-outline-variant rounded-DEFAULT px-3 py-2 w-full">
                <span className="material-symbols-outlined text-on-surface-variant mr-2">search</span>
                <input 
                  className="bg-transparent border-none outline-none focus:ring-0 p-0 font-body-md text-body-md w-full placeholder-on-surface-variant/70 text-on-surface" 
                  placeholder="Instruct the Analyst Agent (e.g. 'Draft memo for nutrition startups')..." 
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
             </div>
          </form>

          {isTyping ? (
            <div className="font-data-mono text-on-surface-variant animate-pulse">Analyst Agent is drafting investment memo...</div>
          ) : aiResponse ? (
            <div>
              <h1 className="font-headline-lg text-headline-lg text-primary mb-6 outline-none" contentEditable>Automated Intelligence Memo</h1>
              <div dangerouslySetInnerHTML={formatMarkdown(aiResponse)} />
              <div className="bg-surface-container-low border border-surface-variant p-3 rounded-DEFAULT font-data-mono text-data-mono text-xs flex items-start gap-2 mt-8">
                <span className="material-symbols-outlined text-tertiary-container" style={{fontSize: '16px'}}>info</span>
                <span className="text-on-surface-variant">AI Confidence: High | Sourced directly from {graphData.nodes.length} entities in the Neo4j Knowledge Graph.</span>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-[60%] text-on-surface-variant">
              <span className="material-symbols-outlined mb-4" style={{fontSize: '48px'}}>edit_document</span>
              <p className="font-title-lg">Awaiting Execution</p>
              <p className="font-body-md mt-2">Use the search bar to generate a memo.</p>
            </div>
          )}
        </div>
      </div>

      <div className="flex-[2] bg-surface-container flex flex-col overflow-hidden">
        <div className="h-12 border-b border-surface-variant bg-surface flex items-center justify-between px-4 shrink-0">
          <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-widest flex items-center gap-2">
            <span className="material-symbols-outlined" style={{fontSize: '16px'}}>account_tree</span>
            Evidence Graph Nodes ({graphData.nodes.length})
          </span>
          <button className="text-on-surface-variant hover:text-primary p-1 rounded-DEFAULT"><span className="material-symbols-outlined" style={{fontSize: '18px'}}>filter_list</span></button>
        </div>
        <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4">
          
          {graphData.nodes.length === 0 && !isTyping && (
            <p className="text-on-surface-variant font-body-md text-center mt-10">No nodes extracted.</p>
          )}

          {graphData.nodes.map((node: any, idx: number) => (
            <div key={idx} className="bg-surface border border-outline-variant rounded-DEFAULT p-4 shadow-sm relative">
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className="w-6 h-6 rounded-full bg-secondary-container text-on-secondary-container flex items-center justify-center">
                    <span className="material-symbols-outlined" style={{fontSize: '12px'}}>
                      {node.label === 'Patent' ? 'description' : node.label === 'Company' ? 'domain' : 'person'}
                    </span>
                  </div>
                  <span className="font-label-md text-label-md text-primary">{node.label}</span>
                </div>
                <span className="font-data-mono text-data-mono text-[10px] text-on-surface-variant">ID: {node.id}</span>
              </div>
              <p className="font-body-md text-[13px] text-on-surface-variant mb-3">
                Extracted from Neo4j multi-hop query. Used as ground-truth context for the generated memo.
              </p>
            </div>
          ))}

        </div>
      </div>

      {/* Footer Orchestration Action */}
      <footer className="bg-primary-container text-on-primary-container font-data-mono text-data-mono fixed bottom-0 w-[calc(100%-16rem)] right-0 z-40 border-t border-tertiary-container shadow-lg flex justify-between items-center px-[32px] py-2 h-12">
        <div className="flex items-center gap-4">
          <span className="font-label-md text-label-md uppercase tracking-widest text-secondary-fixed flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-secondary-fixed animate-pulse"></span>
            HITL Authorization Layer v4.2 | Active
          </span>
        </div>
        <div className="flex items-center gap-3">
          <button className="text-on-primary-container/80 hover:bg-primary transition-colors px-4 py-1.5 rounded-DEFAULT font-label-md border border-on-primary-container/30">
            View Evidence Graph
          </button>
          <button 
            className="text-on-primary-container/80 hover:bg-primary transition-colors px-4 py-1.5 rounded-DEFAULT font-label-md border border-on-primary-container/30"
            onClick={() => setAiResponse('')}
          >
            Reject with Feedback
          </button>
          <button 
            className="text-on-tertiary-container bg-tertiary-fixed font-bold hover:brightness-110 px-6 py-1.5 rounded-DEFAULT font-label-md ml-2 transition-all shadow-md"
            onClick={() => alert("Memo Authorized. Dispatched to Foundation Foundry Database.")}
          >
            Approve Memo
          </button>
        </div>
      </footer>
    </>
  );
};

export default Orchestration;
