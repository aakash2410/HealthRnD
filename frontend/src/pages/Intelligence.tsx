const Intelligence = () => {
  return (
    <div className="flex-1 overflow-y-auto p-margin-desktop pb-32 w-full">
      <div className="max-w-[1440px] mx-auto space-y-gutter">
        {/* Page Header */}
        <div className="mb-8">
          <h2 className="font-headline-lg text-headline-lg text-primary flex items-center gap-3">
            <span className="material-symbols-outlined text-[32px] text-tertiary-container">hub</span>
            Biomedical Knowledge Graph Overview
          </h2>
          <p className="text-on-surface-variant font-body-lg text-body-lg mt-1">Live instrumentation of global clinical pipelines and patent landscapes.</p>
        </div>

        {/* Metrics Bento Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-gutter">
          {/* Tech Merit */}
          <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <span className="material-symbols-outlined text-[80px]">article</span>
            </div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded bg-secondary-container text-on-secondary-container flex items-center justify-center">
                <span className="material-symbols-outlined text-[18px]">biotech</span>
              </div>
              <h3 className="font-label-md text-label-md text-on-surface-variant uppercase tracking-widest">Technical Merit</h3>
            </div>
            <div className="font-display-lg text-display-lg text-primary mb-1">842K</div>
            <div className="flex items-center gap-2 text-on-surface-variant font-body-md text-body-md">
              <span className="material-symbols-outlined text-[16px] text-tertiary-container">trending_up</span>
              <span>PubMed / Patents Analyzed</span>
            </div>
          </div>

          {/* Clinical Readiness */}
          <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <span className="material-symbols-outlined text-[80px]">medical_services</span>
            </div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded bg-tertiary-fixed text-on-tertiary-container flex items-center justify-center">
                <span className="material-symbols-outlined text-[18px]">vaccines</span>
              </div>
              <h3 className="font-label-md text-label-md text-on-surface-variant uppercase tracking-widest">Clinical Readiness</h3>
            </div>
            <div className="font-display-lg text-display-lg text-primary mb-1">1.2K</div>
            <div className="flex items-center gap-2 text-on-surface-variant font-body-md text-body-md">
              <span className="material-symbols-outlined text-[16px] text-tertiary-container">trending_up</span>
              <span>Active CTRI Protocols</span>
            </div>
          </div>

          {/* Market Viability */}
          <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <span className="material-symbols-outlined text-[80px]">payments</span>
            </div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded bg-surface-tint text-on-primary flex items-center justify-center">
                <span className="material-symbols-outlined text-[18px]">monitoring</span>
              </div>
              <h3 className="font-label-md text-label-md text-on-surface-variant uppercase tracking-widest">Market Viability</h3>
            </div>
            <div className="font-display-lg text-display-lg text-primary mb-1">$4.2B</div>
            <div className="flex items-center gap-2 text-on-surface-variant font-body-md text-body-md">
              <span className="material-symbols-outlined text-[16px] text-error">trending_down</span>
              <span>Tracked Capital Flow (Q3)</span>
            </div>
          </div>
        </div>

        {/* Complex Modules Row */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter mt-gutter">
          {/* Scatter Plot Area */}
          <div className="lg:col-span-8 bg-surface-container-lowest border border-outline-variant rounded-lg p-6 flex flex-col h-[400px]">
            <div className="flex justify-between items-center mb-6">
              <h3 className="font-title-lg text-title-lg text-primary">Funding Velocity vs. Clinical Phase</h3>
              <button className="text-on-surface-variant hover:text-primary transition-colors flex items-center gap-1 font-label-md text-label-md">
                <span className="material-symbols-outlined text-[18px]">filter_list</span> Filter View
              </button>
            </div>
            <div className="flex-1 relative border-l border-b border-outline-variant ml-8 mb-6 mt-2">
              <div className="absolute inset-0 flex flex-col justify-between z-0 pointer-events-none opacity-20">
                <div className="w-full border-b border-outline-variant border-dashed"></div>
                <div className="w-full border-b border-outline-variant border-dashed"></div>
                <div className="w-full border-b border-outline-variant border-dashed"></div>
                <div className="w-full border-b border-outline-variant border-dashed"></div>
              </div>
              <div className="absolute bottom-[20%] left-[15%] w-3 h-3 rounded-full bg-secondary-fixed ring-2 ring-white cursor-pointer hover:scale-150 transition-transform"></div>
              <div className="absolute bottom-[35%] left-[25%] w-4 h-4 rounded-full bg-tertiary-container ring-2 ring-white cursor-pointer hover:scale-150 transition-transform"></div>
              <div className="absolute bottom-[10%] left-[40%] w-2 h-2 rounded-full bg-secondary-fixed ring-2 ring-white cursor-pointer hover:scale-150 transition-transform"></div>
              <div className="absolute bottom-[60%] left-[55%] w-5 h-5 rounded-full bg-surface-tint ring-2 ring-white cursor-pointer hover:scale-150 transition-transform"></div>
              <div className="absolute bottom-[45%] left-[70%] w-3 h-3 rounded-full bg-tertiary-container ring-2 ring-white cursor-pointer hover:scale-150 transition-transform"></div>
              <div className="absolute bottom-[80%] left-[85%] w-6 h-6 rounded-full bg-primary-container ring-2 ring-white cursor-pointer hover:scale-150 transition-transform shadow-md"></div>
              <span className="absolute -left-10 top-1/2 -translate-y-1/2 -rotate-90 font-label-md text-label-md text-on-surface-variant whitespace-nowrap">Capital Secured ($M)</span>
              <span className="absolute -bottom-8 left-1/2 -translate-x-1/2 font-label-md text-label-md text-on-surface-variant">Clinical Maturity Index</span>
            </div>
          </div>

          {/* Compliance Status */}
          <div className="lg:col-span-4 flex flex-col gap-gutter h-[400px]">
            <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 flex-1">
              <h3 className="font-title-lg text-title-lg text-primary mb-4">DPDP 2023 Compliance</h3>
              <div className="flex items-center gap-4 p-4 rounded-DEFAULT bg-surface-container-low border border-surface-variant mb-4">
                <div className="w-10 h-10 rounded-full bg-[#e6f4ea] text-[#137333] flex items-center justify-center flex-shrink-0">
                  <span className="material-symbols-outlined" style={{fontVariationSettings: "'FILL' 1"}}>verified_user</span>
                </div>
                <div>
                  <h4 className="font-label-md text-label-md text-primary">System Validated</h4>
                  <p className="font-body-md text-body-md text-on-surface-variant mt-0.5">All ingestion pipelines compliant.</p>
                </div>
              </div>
              <ul className="space-y-3 font-data-mono text-data-mono text-on-surface-variant">
                <li className="flex justify-between items-center">
                  <span>Anonymization Filter</span>
                  <span className="text-[#137333] flex items-center gap-1"><span className="material-symbols-outlined text-[14px]">check_circle</span> Active</span>
                </li>
                <li className="flex justify-between items-center">
                  <span>Consent Audit Trail</span>
                  <span className="text-[#137333] flex items-center gap-1"><span className="material-symbols-outlined text-[14px]">check_circle</span> Verified</span>
                </li>
                <li className="flex justify-between items-center">
                  <span>Data Localization</span>
                  <span className="text-tertiary-container flex items-center gap-1"><span className="material-symbols-outlined text-[14px]">sync</span> Synced</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default Intelligence;
