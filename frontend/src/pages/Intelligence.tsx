import { useState, useEffect } from 'react';
import axios from 'axios';

const Intelligence = () => {
  const [metrics, setMetrics] = useState<any>({ publications: 0, trials: 0, funding: 0, companies: 0, plot_data: [] });
  const [signals, setSignals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [mRes, sRes] = await Promise.all([
          axios.get('http://localhost:8000/api/dashboard/metrics'),
          axios.get('http://localhost:8000/api/dashboard/signals')
        ]);
        setMetrics(mRes.data);
        setSignals(sRes.data);
      } catch (err) {
        console.error("Failed to fetch dashboard data:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const formatCurrency = (val: number) => {
    if (val >= 1000000000) return `$${(val / 1000000000).toFixed(1)}B`;
    if (val >= 1000000) return `$${(val / 1000000).toFixed(1)}M`;
    return `$${val.toLocaleString()}`;
  };

  const formatCount = (val: number) => {
    if (val >= 1000) return `${(val / 1000).toFixed(1)}K`;
    return val.toString();
  };

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
        <div className="grid grid-cols-1 md:grid-cols-4 gap-gutter">
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
            <div className="font-display-lg text-display-lg text-primary mb-1">{loading ? '...' : formatCount(metrics.publications)}</div>
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
            <div className="font-display-lg text-display-lg text-primary mb-1">{loading ? '...' : formatCount(metrics.trials)}</div>
            <div className="flex items-center gap-2 text-on-surface-variant font-body-md text-body-md">
              <span className="material-symbols-outlined text-[16px] text-tertiary-container">trending_up</span>
              <span>Active Protocols</span>
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
            <div className="font-display-lg text-display-lg text-primary mb-1">{loading ? '...' : formatCurrency(metrics.funding)}</div>
            <div className="flex items-center gap-2 text-on-surface-variant font-body-md text-body-md">
              <span className="material-symbols-outlined text-[16px] text-tertiary-container">trending_up</span>
              <span>Tracked Capital Flow</span>
            </div>
          </div>

          {/* Companies */}
          <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <span className="material-symbols-outlined text-[80px]">domain</span>
            </div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded bg-primary-container text-on-primary-container flex items-center justify-center">
                <span className="material-symbols-outlined text-[18px]">business</span>
              </div>
              <h3 className="font-label-md text-label-md text-on-surface-variant uppercase tracking-widest">Network Size</h3>
            </div>
            <div className="font-display-lg text-display-lg text-primary mb-1">{loading ? '...' : metrics.companies}</div>
            <div className="flex items-center gap-2 text-on-surface-variant font-body-md text-body-md">
              <span className="material-symbols-outlined text-[16px] text-tertiary-container">hub</span>
              <span>Total Tracked Entities</span>
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
              
              {!loading && metrics.plot_data && metrics.plot_data.map((point: any, idx: number) => (
                <div 
                  key={idx}
                  className="absolute rounded-full bg-primary-container ring-2 ring-white cursor-pointer hover:scale-150 transition-transform shadow-sm group"
                  style={{
                    bottom: `${point.y}%`,
                    left: `${point.x}%`,
                    width: `${point.size * 2}px`,
                    height: `${point.size * 2}px`,
                    backgroundColor: `hsl(${180 + (point.x)}, 60%, 50%)`
                  }}
                  title={`${point.name}: $${point.y}M`}
                >
                   <div className="absolute hidden group-hover:block bg-surface border border-outline-variant p-2 rounded text-[10px] whitespace-nowrap z-50 -top-10 left-1/2 -translate-x-1/2">
                      {point.name}
                   </div>
                </div>
              ))}

              {(!metrics.plot_data || metrics.plot_data.length === 0) && !loading && (
                <div className="absolute inset-0 flex items-center justify-center text-on-surface-variant opacity-40 font-body-md">
                  Awaiting multi-hop graph data for scatter visualization.
                </div>
              )}

              <span className="absolute -left-10 top-1/2 -translate-y-1/2 -rotate-90 font-label-md text-label-md text-on-surface-variant whitespace-nowrap">Capital Secured ($M)</span>
              <span className="absolute -bottom-8 left-1/2 -translate-x-1/2 font-label-md text-label-md text-on-surface-variant">Clinical Maturity Index</span>
            </div>
          </div>

          {/* Compliance Status */}
          <div className="lg:col-span-4 flex flex-col gap-gutter min-h-[400px]">
             {/* Signals Feed in Bento Column */}
             <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 flex-1 overflow-hidden flex flex-col">
              <h3 className="font-title-lg text-title-lg text-primary mb-4 flex items-center justify-between">
                Scouting Signals
                <span className="material-symbols-outlined text-[18px] text-secondary animate-pulse">sensors</span>
              </h3>
              <div className="flex-1 overflow-y-auto space-y-3">
                {loading ? (
                  <div className="animate-pulse space-y-2">
                    <div className="h-10 bg-surface-container rounded"></div>
                    <div className="h-10 bg-surface-container rounded"></div>
                  </div>
                ) : signals.map((s, idx) => (
                  <div key={idx} className="p-3 bg-surface-container-low rounded border border-surface-variant flex items-center gap-3">
                    <div className="w-8 h-8 rounded bg-surface border border-outline-variant flex items-center justify-center text-primary">
                      <span className="material-symbols-outlined text-[16px]">{s.type === 'Company' ? 'business' : 'hub'}</span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="font-label-md text-label-md text-on-surface truncate">{s.name}</div>
                      <div className="text-[10px] font-data-mono text-secondary">Impact: {s.score}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 h-[180px]">
              <h3 className="font-title-lg text-title-lg text-primary mb-3">DPDP Compliance</h3>
              <ul className="space-y-2 font-data-mono text-[11px] text-on-surface-variant">
                <li className="flex justify-between items-center">
                  <span>Anonymization</span>
                  <span className="text-[#137333] flex items-center gap-1"><span className="material-symbols-outlined text-[14px]">check_circle</span> Active</span>
                </li>
                <li className="flex justify-between items-center">
                  <span>Audit Trail</span>
                  <span className="text-[#137333] flex items-center gap-1"><span className="material-symbols-outlined text-[14px]">check_circle</span> Verified</span>
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
