import { useState, useEffect } from 'react';
import axios from 'axios';
import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, ZAxis, Tooltip, CartesianGrid } from 'recharts';

const Intelligence = () => {
  const [metrics, setMetrics] = useState<any>({
    publications: 0,
    trials: 0,
    funding: 0,
    companies: 0,
    plot_data: []
  });
  const [signals, setSignals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchDashboardData = async () => {
    try {
      const [mRes, sRes] = await Promise.all([
        axios.get('http://localhost:8000/api/dashboard/metrics'),
        axios.get('http://localhost:8000/api/dashboard/signals')
      ]);
      setMetrics(mRes.data);
      setSignals(sRes.data);
    } catch (err) {
      console.error("Dashboard refresh failed:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
    // Real-time polling every 10 seconds to show ingestion progress
    const interval = setInterval(fetchDashboardData, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex-1 overflow-y-auto p-margin-desktop pb-32 w-full">
      <div className="max-w-full mx-auto mb-10 mt-8">
        <div className="flex items-center gap-3 mb-6">
          <span className="material-symbols-outlined text-secondary" style={{fontVariationSettings: "'FILL' 1"}}>hub</span>
          <h1 className="font-headline-md text-headline-md text-primary tracking-tight">Biomedical Knowledge Graph Overview</h1>
          <span className="ml-auto flex items-center gap-2 bg-secondary-container text-on-secondary-container px-3 py-1 rounded-full font-data-mono text-[11px] shadow-sm animate-pulse">
            <span className="w-2 h-2 rounded-full bg-secondary"></span>
            Real-Time Ingestion Active
          </span>
        </div>
        <p className="font-body-lg text-body-lg text-on-surface-variant max-w-2xl mb-8">
          Live instrumentation of official Indian clinical pipelines, patent landscapes, and sovereign grant funding.
        </p>

        {/* High Level Metrics Row */}
        <div className="grid grid-cols-4 gap-gutter mb-10">
          <div className="bg-surface-container-lowest border border-outline-variant rounded p-5 flex flex-col gap-2 relative overflow-hidden group hover:border-primary transition-all">
            <div className="absolute top-0 right-0 p-3 opacity-10 group-hover:opacity-20 transition-opacity">
              <span className="material-symbols-outlined text-6xl">menu_book</span>
            </div>
            <div className="flex items-center gap-2 text-secondary font-label-md text-label-md uppercase tracking-wider">
              <span className="material-symbols-outlined text-[18px]">biotech</span>
              Technical Merit
            </div>
            <div className="font-headline-lg text-headline-lg text-on-surface">{metrics.publications}</div>
            <div className="text-on-surface-variant font-body-sm text-[12px] flex items-center gap-1">
              <span className="material-symbols-outlined text-[14px]">trending_up</span>
              Patents Analyzed
            </div>
          </div>

          <div className="bg-surface-container-lowest border border-outline-variant rounded p-5 flex flex-col gap-2 relative overflow-hidden group hover:border-primary transition-all">
            <div className="absolute top-0 right-0 p-3 opacity-10 group-hover:opacity-20 transition-opacity">
              <span className="material-symbols-outlined text-6xl">medical_services</span>
            </div>
            <div className="flex items-center gap-2 text-tertiary font-label-md text-label-md uppercase tracking-wider">
              <span className="material-symbols-outlined text-[18px]">clinical_notes</span>
              Clinical Readiness
            </div>
            <div className="font-headline-lg text-headline-lg text-on-surface">{metrics.trials}</div>
            <div className="text-on-surface-variant font-body-sm text-[12px] flex items-center gap-1">
              <span className="material-symbols-outlined text-[14px]">show_chart</span>
              Active Protocols
            </div>
          </div>

          <div className="bg-surface-container-lowest border border-outline-variant rounded p-5 flex flex-col gap-2 relative overflow-hidden group hover:border-primary transition-all">
            <div className="absolute top-0 right-0 p-3 opacity-10 group-hover:opacity-20 transition-opacity">
              <span className="material-symbols-outlined text-6xl">payments</span>
            </div>
            <div className="flex items-center gap-2 text-primary font-label-md text-label-md uppercase tracking-wider">
              <span className="material-symbols-outlined text-[18px]">account_balance</span>
              Market Viability
            </div>
            <div className="font-headline-lg text-headline-lg text-on-surface">
              ${(metrics.funding / 1000000).toFixed(1)}M
            </div>
            <div className="text-on-surface-variant font-body-sm text-[12px] flex items-center gap-1">
              <span className="material-symbols-outlined text-[14px]">history_edu</span>
              Sovereign Capital Flow
            </div>
          </div>

          <div className="bg-surface-container-lowest border border-outline-variant rounded p-5 flex flex-col gap-2 relative overflow-hidden group hover:border-primary transition-all">
            <div className="absolute top-0 right-0 p-3 opacity-10 group-hover:opacity-20 transition-opacity">
              <span className="material-symbols-outlined text-6xl">corporate_fare</span>
            </div>
            <div className="flex items-center gap-2 text-on-surface-variant font-label-md text-label-md uppercase tracking-wider">
              <span className="material-symbols-outlined text-[18px]">groups</span>
              Network Size
            </div>
            <div className="font-headline-lg text-headline-lg text-on-surface">{metrics.companies}</div>
            <div className="text-on-surface-variant font-body-sm text-[12px] flex items-center gap-1">
              <span className="material-symbols-outlined text-[14px]">hub</span>
              Tracked Entities
            </div>
          </div>
        </div>

        {/* Charts and Signals Section */}
        <div className="grid grid-cols-12 gap-gutter">
          <div className="col-span-12 lg:col-span-8 bg-surface-container-lowest border border-outline-variant rounded flex flex-col min-h-[400px]">
            <div className="border-b border-outline-variant px-4 py-3 flex justify-between items-center bg-surface-container-low/30">
              <h3 className="font-title-lg text-title-lg text-primary">Funding Velocity vs. Clinical Phase</h3>
              <button className="flex items-center gap-1 text-xs font-label-md text-on-surface-variant hover:text-primary transition-colors">
                <span className="material-symbols-outlined text-[18px]">filter_list</span>
                Filter View
              </button>
            </div>
            <div className="flex-1 p-6 relative">
               {metrics.plot_data.length > 0 ? (
                 <ResponsiveContainer width="100%" height="100%">
                   <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                     <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                     <XAxis 
                       type="number" 
                       dataKey="x" 
                       name="Clinical Maturity" 
                       unit="%" 
                       axisLine={false}
                       tickLine={false}
                       tick={{fontSize: 10, fill: '#64748b'}}
                       label={{ value: 'Clinical Maturity Index', position: 'bottom', offset: 0, fontSize: 12, fill: '#64748b' }}
                     />
                     <YAxis 
                       type="number" 
                       dataKey="y" 
                       name="Capital" 
                       unit="M" 
                       axisLine={false}
                       tickLine={false}
                       tick={{fontSize: 10, fill: '#64748b'}}
                       label={{ value: 'Capital Secured ($M)', angle: -90, position: 'left', fontSize: 12, fill: '#64748b' }}
                     />
                     <ZAxis type="number" dataKey="size" range={[50, 400]} />
                     <Tooltip 
                        cursor={{ strokeDasharray: '3 3' }} 
                        contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                     />
                     <Scatter name="Startups" data={metrics.plot_data} fill="#006495" fillOpacity={0.6} stroke="#006495" />
                   </ScatterChart>
                 </ResponsiveContainer>
               ) : (
                 <div className="absolute inset-0 flex items-center justify-center text-outline font-data-mono text-[13px] opacity-60">
                   Awaiting multi-hop graph data for scatter visualization.
                 </div>
               )}
            </div>
          </div>

          <div className="col-span-12 lg:col-span-4 bg-surface-container-lowest border border-outline-variant rounded flex flex-col">
            <div className="border-b border-outline-variant px-4 py-3 flex justify-between items-center">
              <h3 className="font-title-lg text-title-lg text-primary flex items-center gap-2">
                Scouting Signals
                <span className="material-symbols-outlined text-secondary animate-pulse text-[18px]">sensors</span>
              </h3>
            </div>
            <div className="p-4 flex flex-col gap-3">
              {signals.map((signal, idx) => (
                <div key={idx} className="bg-surface-container-low border border-outline-variant rounded p-3 hover:bg-surface-container transition-colors group cursor-pointer">
                  <div className="flex justify-between items-start mb-1">
                    <span className="font-title-md text-title-md text-on-surface group-hover:text-primary transition-colors">{signal.name}</span>
                    <span className="material-symbols-outlined text-[16px] text-outline opacity-0 group-hover:opacity-100 transition-opacity">open_in_new</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="font-data-mono text-[10px] text-secondary uppercase bg-secondary-container px-1.5 py-0.5 rounded">{signal.type}</span>
                    <span className="font-body-sm text-[11px] text-on-surface-variant">Impact Score: {signal.score}</span>
                  </div>
                </div>
              ))}
              {loading && <div className="text-center py-10 animate-pulse text-outline">Listening for signals...</div>}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Intelligence;
