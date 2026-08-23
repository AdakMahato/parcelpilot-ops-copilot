const fs = require('fs');
const path = './frontend/src/app/page.tsx';
let content = fs.readFileSync(path, 'utf8');

// 1. Add isDrawerOpen state
if (!content.includes('isDrawerOpen')) {
  content = content.replace(
    /const \[navHistory, setNavHistory\] = useState<string\[\]>\(\[\]\);/,
    `const [navHistory, setNavHistory] = useState<string[]>([]);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);`
  );
}

// Add useEffect for Escape key
if (!content.includes('Escape')) {
  content = content.replace(
    /const goHome = \(\) => \{/,
    `useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setIsDrawerOpen(false);
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, []);

  const goHome = () => {`
  );
}

// 2. Replace the header with the floating buttons
const headerRegex = /\{\/\* Top Bar \*\/\}\s*<header[\s\S]*?<\/header>/;

const floatingButtons = `
        {/* Floating Top Left Back Button */}
        <button 
          onClick={goBack} 
          disabled={navHistory.length === 0} 
          className="absolute top-4 left-4 z-20 px-3 py-1 bg-white border border-slate-200 shadow-sm text-slate-600 rounded-md hover:bg-slate-50 disabled:opacity-50 text-sm font-medium transition-colors"
        >
          ← Back
        </button>

        {/* Floating Top Right Menu Button */}
        <button 
          onClick={() => setIsDrawerOpen(true)}
          aria-label="Open menu"
          className="absolute top-4 right-4 z-20 w-8 h-8 flex items-center justify-center bg-white border border-slate-200 shadow-sm text-slate-600 rounded-md hover:bg-slate-50 transition-colors text-lg"
        >
          ☰
        </button>
`;

content = content.replace(headerRegex, floatingButtons);

// Make Main Content relative so absolute buttons position correctly
content = content.replace(
  /<div className="flex-1 flex flex-col min-w-0 overflow-hidden">/,
  `<div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">`
);

// 3. Add Drawer JSX right before the final closing div
const drawerJSX = `
      {/* Right-Side Drawer Overlay & Panel */}
      {isDrawerOpen && (
        <div className="fixed inset-0 z-50 flex justify-end">
          {/* Backdrop */}
          <div 
            className="absolute inset-0 bg-slate-900/20 backdrop-blur-sm transition-opacity" 
            onClick={() => setIsDrawerOpen(false)}
          ></div>
          
          {/* Drawer Panel */}
          <div className="relative w-full sm:w-[340px] md:w-[380px] h-full bg-white shadow-2xl flex flex-col animate-slide-in-right">
            {/* Drawer Header */}
            <div className="flex items-center justify-between p-6 border-b border-slate-100">
              <h2 className="text-xl font-bold text-slate-800">Menu</h2>
              <button 
                onClick={() => setIsDrawerOpen(false)}
                aria-label="Close menu"
                className="w-8 h-8 flex items-center justify-center rounded-full bg-slate-100 text-slate-500 hover:bg-slate-200 hover:text-slate-700 transition-colors"
              >
                ✕
              </button>
            </div>
            
            {/* Drawer Content */}
            <div className="flex-1 overflow-y-auto p-6 space-y-8">
              
              {/* Home Navigation */}
              <div>
                <button 
                  onClick={() => { goHome(); setIsDrawerOpen(false); }} 
                  className="flex items-center w-full px-4 py-3 bg-blue-50 text-blue-700 rounded-xl hover:bg-blue-100 transition-colors text-base font-semibold"
                >
                  <span className="mr-3 text-xl">⌂</span> Home
                </button>
              </div>

              {/* Title & Snapshot */}
              <div>
                <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-2">Application</h3>
                <div className="bg-slate-50 rounded-xl p-4 border border-slate-100">
                  <h2 className="font-bold text-slate-800 mb-2">ParcelPilot Ops Copilot</h2>
                  <div className="text-xs font-medium text-slate-500">
                    Data snapshot: {snapshotTime}
                  </div>
                </div>
              </div>

              {/* System Status */}
              <div>
                <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-2">System Status</h3>
                <div className="bg-slate-50 rounded-xl p-4 border border-slate-100 space-y-3">
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-600">API Connection</span>
                    {backendHealth?.status === 'ok' ? (
                      <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded font-bold">API Online {backendHealth?.llm_provider === 'gemini' ? '• Gemini Online' : ''}</span>
                    ) : backendHealth?.status === 'degraded' ? (
                      <span className="text-xs bg-yellow-100 text-yellow-700 px-2 py-1 rounded font-bold">API Degraded</span>
                    ) : (
                      <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded font-bold">API Offline</span>
                    )}
                  </div>
                  
                  <div className="flex items-center justify-between pt-3 border-t border-slate-200">
                    <span className="text-sm font-medium text-slate-600">Current Session</span>
                    <div className="flex items-center">
                      <div className="w-2 h-2 rounded-full bg-green-500 mr-2"></div>
                      <span className="text-xs font-bold text-slate-700">Support Agent • Demo User</span>
                    </div>
                  </div>

                </div>
              </div>

            </div>
          </div>
        </div>
      )}
`;

content = content.replace(
  /    <\/div>\n  \);\n\}/,
  drawerJSX + `    </div>\n  );\n}`
);

fs.writeFileSync(path, content);
