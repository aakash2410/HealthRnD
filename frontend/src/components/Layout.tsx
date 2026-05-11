import { NavLink, Outlet } from 'react-router-dom';

const Layout = () => {
  return (
    <div className="bg-background text-on-surface h-screen flex overflow-hidden flex-col">
      {/* TopAppBar */}
      <header className="bg-surface text-primary font-body-md text-body-md docked full-width top-0 z-50 border-b border-outline-variant flat no shadows flex justify-between items-center px-[32px] h-16 w-full shrink-0">
        <div className="flex items-center gap-[16px]">
          <span className="font-title-lg text-title-lg font-bold text-primary tracking-tight">BioScout AI</span>
          <div className="h-6 w-px bg-outline-variant mx-2"></div>
          <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-widest">Platform Area</span>
        </div>
        <div className="flex items-center gap-4">
          <button className="p-2 hover:bg-surface-container transition-colors rounded-DEFAULT text-on-surface-variant">
            <span className="material-symbols-outlined">account_balance</span>
          </button>
          <button className="p-2 hover:bg-surface-container transition-colors rounded-DEFAULT text-on-surface-variant">
            <span className="material-symbols-outlined">database</span>
          </button>
          <button className="p-2 hover:bg-surface-container transition-colors rounded-DEFAULT text-on-surface-variant relative">
            <span className="material-symbols-outlined">notifications</span>
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-error rounded-full"></span>
          </button>
          <img alt="User" className="w-8 h-8 rounded-full border border-outline-variant ml-2 bg-surface-variant" />
        </div>
      </header>

      {/* Main Workspace */}
      <div className="flex flex-1 overflow-hidden">
        {/* SideNavBar */}
        <nav className="bg-surface-container-low text-primary font-label-md text-label-md docked left-0 h-full w-64 border-r border-outline-variant flat no shadows flex flex-col gap-[4px] py-[16px] shrink-0">
          <div className="px-4 mb-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 bg-primary-container rounded-DEFAULT flex items-center justify-center text-on-primary-container">
                <span className="material-symbols-outlined">hub</span>
              </div>
              <div>
                <div className="font-title-lg text-title-lg font-bold text-primary">BioScout AI</div>
                <div className="font-data-mono text-data-mono text-on-surface-variant text-[10px]">Precision Intelligence</div>
              </div>
            </div>
          </div>
          <button className="mx-4 mb-6 bg-surface border border-outline-variant text-on-surface px-4 py-2 rounded-DEFAULT hover:bg-surface-container-high transition-all flex items-center justify-center gap-2 font-label-md text-label-md shadow-sm">
            <span className="material-symbols-outlined" style={{fontSize: '16px'}}>add</span>
            New Scouting Project
          </button>
          <div className="flex-1 overflow-y-auto px-2 flex flex-col gap-1">
            <NavLink to="/" className={({isActive}) => `px-4 py-2 transition-all rounded-lg flex items-center gap-3 ${isActive ? 'bg-secondary-container text-on-secondary-container font-bold' : 'text-on-surface-variant hover:text-primary hover:bg-surface-container-high'}`}>
              {({isActive}) => <><span className="material-symbols-outlined" style={isActive ? {fontVariationSettings: "'FILL' 1"} : {}}>dashboard</span> Intelligence</>}
            </NavLink>
            <NavLink to="/discovery" className={({isActive}) => `px-4 py-2 transition-all rounded-lg flex items-center gap-3 ${isActive ? 'bg-secondary-container text-on-secondary-container font-bold' : 'text-on-surface-variant hover:text-primary hover:bg-surface-container-high'}`}>
              {({isActive}) => <><span className="material-symbols-outlined" style={isActive ? {fontVariationSettings: "'FILL' 1"} : {}}>psychology</span> Discovery</>}
            </NavLink>
            <NavLink to="/orchestration" className={({isActive}) => `px-4 py-2 transition-all rounded-lg flex items-center gap-3 ${isActive ? 'bg-secondary-container text-on-secondary-container font-bold' : 'text-on-surface-variant hover:text-primary hover:bg-surface-container-high'}`}>
              {({isActive}) => <><span className="material-symbols-outlined" style={isActive ? {fontVariationSettings: "'FILL' 1"} : {}}>rule</span> Orchestration</>}
            </NavLink>
          </div>
        </nav>

        {/* Dynamic Page Content */}
        <main className="flex-1 overflow-hidden relative flex flex-col bg-surface-container-lowest">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
