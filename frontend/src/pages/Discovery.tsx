const Discovery = () => {
  return (
    <div className="flex-1 overflow-y-auto p-margin-desktop pb-32 w-full">
      <div className="max-w-5xl mx-auto mb-10 mt-8">
        <div className="flex items-center gap-3 mb-6">
          <span className="material-symbols-outlined text-secondary" style={{fontVariationSettings: "'FILL' 1"}}>graphic_eq</span>
          <h1 className="font-headline-md text-headline-md text-primary tracking-tight">RAG Knowledge Query</h1>
          <span className="ml-auto flex items-center gap-2 bg-tertiary-fixed text-on-tertiary-fixed px-3 py-1 rounded-full font-data-mono text-data-mono text-[11px] shadow-sm border border-tertiary-fixed-dim">
            <span className="w-2 h-2 rounded-full bg-on-tertiary-container animate-pulse"></span>
            Graph Sync: Live
          </span>
        </div>
        
        {/* Prominent Search Box */}
        <div className="relative bg-surface-container-lowest border border-outline-variant rounded-xl shadow-[0_4px_12px_rgba(15,23,42,0.05)] overflow-hidden focus-within:ring-2 focus-within:ring-primary focus-within:border-transparent transition-all">
          <div className="flex items-start p-4">
            <span className="material-symbols-outlined text-outline mt-1 mr-3">travel_explore</span>
            <textarea 
              className="w-full bg-transparent border-none outline-none focus:ring-0 p-0 font-body-lg text-body-lg text-on-surface placeholder:text-outline resize-none min-h-[60px]" 
              placeholder="Query the knowledge graph... (e.g., 'CRISPR startups in India working on agritech')"
              defaultValue="CRISPR startups in India working on agritech"
            />
          </div>
          <div className="bg-surface-container-low border-t border-outline-variant px-4 py-2 flex justify-between items-center">
            <div className="flex gap-2">
              <button className="text-xs font-label-md text-on-surface-variant bg-surface border border-outline-variant px-2 py-1 rounded hover:bg-surface-container transition-colors flex items-center gap-1">
                <span className="material-symbols-outlined text-[14px]">tune</span> Parameters
              </button>
              <button className="text-xs font-label-md text-on-surface-variant bg-surface border border-outline-variant px-2 py-1 rounded hover:bg-surface-container transition-colors flex items-center gap-1">
                <span className="material-symbols-outlined text-[14px]">history</span> Recent
              </button>
            </div>
            <button className="bg-primary text-on-primary font-label-md text-label-md px-4 py-1.5 rounded flex items-center gap-2 hover:opacity-90 transition-opacity">
              <span className="material-symbols-outlined text-[16px]">send</span> Execute
            </button>
          </div>
        </div>
        
        <div className="flex gap-2 mt-3 overflow-x-auto pb-2 scrollbar-hide">
          <span className="text-xs font-label-md text-outline-variant py-1 px-2">Suggestions:</span>
          <span className="text-xs font-data-mono text-secondary bg-surface-container border border-outline-variant rounded px-2 py-1 cursor-pointer hover:bg-surface-container-high whitespace-nowrap">CAR-T therapies in Phase II</span>
          <span className="text-xs font-data-mono text-secondary bg-surface-container border border-outline-variant rounded px-2 py-1 cursor-pointer hover:bg-surface-container-high whitespace-nowrap">Emerging IP landscape for solid-state batteries</span>
        </div>
      </div>

      {/* Dashboard Layout Grid */}
      <div className="grid grid-cols-12 gap-gutter max-w-full">
        {/* Left Column: Results */}
        <div className="col-span-12 lg:col-span-9 flex flex-col gap-gutter">
          <div className="bg-surface-container-lowest border border-outline-variant rounded flex flex-col relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-tertiary-fixed to-secondary-fixed"></div>
            <div className="border-b border-outline-variant px-4 py-3 flex justify-between items-center bg-surface-container-low/50">
              <h2 className="font-title-lg text-title-lg text-primary flex items-center gap-2">
                <span className="material-symbols-outlined text-secondary">lightbulb</span>
                Synthesized Insight
              </h2>
            </div>
            <div className="p-5 font-body-lg text-body-lg text-on-surface leading-relaxed">
              <p className="mb-4">
                The ecosystem for CRISPR applications in Indian agritech is currently characterized by early-stage academic spin-offs and mid-cap biopharma entities pivoting to agricultural verticals. Analysis of recent patent filings and funding rounds indicates a strong focus on drought-resistance and enhanced yield metrics in staple crops.
              </p>
              <p>
                Leading entities such as <span className="border-b border-dashed border-primary cursor-pointer hover:bg-surface-container px-1">AgriGenomix India</span> and <span className="border-b border-dashed border-primary cursor-pointer hover:bg-surface-container px-1">Tierra Seed Science</span> have secured significant Series A funding in the past 18 months, primarily backed by domestic venture capital focused on sustainable agriculture.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-gutter">
            <div className="col-span-2 bg-surface-container-lowest border border-outline-variant rounded flex flex-col">
              <div className="border-b border-outline-variant px-4 py-2 flex justify-between items-center">
                <h3 className="font-label-md text-label-md text-on-surface uppercase tracking-wider">Identified Entities</h3>
                <button className="text-xs font-data-mono text-primary flex items-center hover:underline">View Full Graph <span className="material-symbols-outlined text-[14px] ml-1">arrow_forward</span></button>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-surface-container-low border-b border-outline-variant text-xs font-label-md text-on-surface-variant">
                      <th className="py-2 px-4 font-semibold w-1/3">Entity Name</th>
                      <th className="py-2 px-4 font-semibold w-1/4">Type</th>
                      <th className="py-2 px-4 font-semibold">Resolution ID</th>
                      <th className="py-2 px-4 font-semibold text-right">Confidence</th>
                    </tr>
                  </thead>
                  <tbody className="font-data-mono text-[12px] text-on-surface">
                    <tr className="border-b border-outline-variant/50 hover:bg-surface-container-low/50 transition-colors">
                      <td className="py-2.5 px-4 font-medium flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-tertiary-container"></div>
                        AgriGenomix India
                      </td>
                      <td className="py-2.5 px-4"><span className="bg-surface-container border border-outline-variant rounded px-1.5 py-0.5 text-[10px]">Startup</span></td>
                      <td className="py-2.5 px-4 text-outline">CB-ORG-9821</td>
                      <td className="py-2.5 px-4 text-right text-secondary">0.98</td>
                    </tr>
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
              <span className="material-symbols-outlined text-[18px] text-on-surface-variant">filter_list</span>
              <h3 className="font-title-lg text-[16px] font-semibold text-primary">Entity Resolution</h3>
            </div>
            <div className="p-4 flex flex-col gap-5 overflow-y-auto">
              <div className="flex flex-col gap-2">
                <label className="font-label-md text-[11px] text-outline uppercase tracking-wider flex justify-between">
                  Ontologies <span className="material-symbols-outlined text-[14px] cursor-pointer">add_circle</span>
                </label>
                <div className="flex flex-col gap-1.5">
                  <label className="flex items-center gap-2 cursor-pointer group">
                    <input type="checkbox" defaultChecked className="rounded-sm border-outline-variant text-primary focus:ring-primary w-3.5 h-3.5 bg-surface" />
                    <span className="font-data-mono text-[12px] text-on-surface group-hover:text-primary transition-colors">UMLS CUIs</span>
                  </label>
                </div>
              </div>
              <div className="w-full h-px bg-outline-variant/30"></div>
              <div className="flex flex-col gap-2">
                <div className="flex justify-between items-center">
                  <label className="font-label-md text-[11px] text-outline uppercase tracking-wider">Confidence Threshold</label>
                  <span className="font-data-mono text-[10px] text-secondary">0.85</span>
                </div>
                <input type="range" min="0" max="100" defaultValue="85" className="w-full h-1 bg-surface-container-high rounded-lg appearance-none cursor-pointer accent-primary" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Discovery;
