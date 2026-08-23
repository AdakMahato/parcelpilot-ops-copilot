const fs = require('fs');
const path = './frontend/src/app/page.tsx';
let content = fs.readFileSync(path, 'utf8');

// Add navigation history state
content = content.replace(
  /const \[activeTab, setActiveTab\] = useState\('chat'\);/,
  `const [activeTab, setActiveTabInternal] = useState('chat');
  const [navHistory, setNavHistory] = useState<string[]>([]);
  
  const setActiveTab = (tab: string) => {
    setNavHistory(prev => [...prev, activeTab]);
    setActiveTabInternal(tab);
  };
  
  const goBack = () => {
    if (navHistory.length > 0) {
      const prev = navHistory[navHistory.length - 1];
      setNavHistory(h => h.slice(0, -1));
      setActiveTabInternal(prev);
    }
  };
  
  const goHome = () => {
    setActiveTab('chat');
  };`
);

// Update sidebar buttons to be functional
content = content.replace(
  /<button className="w-full text-left px-4 py-2 rounded-lg text-sm font-medium text-slate-500 cursor-not-allowed opacity-50">Tickets<\/button>/,
  `<button onClick={() => setActiveTab('tickets')} className={\`w-full text-left px-4 py-2 rounded-lg text-sm font-medium transition-colors \${activeTab === 'tickets' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'}\`}>Tickets</button>`
);
content = content.replace(
  /<button className="w-full text-left px-4 py-2 rounded-lg text-sm font-medium text-slate-500 cursor-not-allowed opacity-50">Orders<\/button>/,
  `<button onClick={() => setActiveTab('orders')} className={\`w-full text-left px-4 py-2 rounded-lg text-sm font-medium transition-colors \${activeTab === 'orders' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'}\`}>Orders</button>`
);
content = content.replace(
  /<button className="w-full text-left px-4 py-2 rounded-lg text-sm font-medium text-slate-500 cursor-not-allowed opacity-50">Accounts<\/button>/,
  `<button onClick={() => setActiveTab('accounts')} className={\`w-full text-left px-4 py-2 rounded-lg text-sm font-medium transition-colors \${activeTab === 'accounts' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'}\`}>Accounts</button>`
);
content = content.replace(
  /<button className="w-full text-left px-4 py-2 rounded-lg text-sm font-medium text-slate-500 cursor-not-allowed opacity-50">Activity<\/button>/,
  `<button onClick={() => setActiveTab('activity')} className={\`w-full text-left px-4 py-2 rounded-lg text-sm font-medium transition-colors \${activeTab === 'activity' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'}\`}>Activity</button>`
);
content = content.replace(
  /<button className="w-full text-left px-4 py-2 rounded-lg text-sm font-medium text-slate-500 cursor-not-allowed opacity-50">Settings<\/button>/,
  `<button onClick={() => setActiveTab('settings')} className={\`w-full text-left px-4 py-2 rounded-lg text-sm font-medium transition-colors \${activeTab === 'settings' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'}\`}>Settings</button>`
);

// Add Home and Back buttons to top bar
content = content.replace(
  /<h2 className="font-semibold text-slate-800">ParcelPilot Ops Copilot<\/h2>/,
  `<div className="flex space-x-2 mr-4">
      <button onClick={goBack} disabled={navHistory.length === 0} className="px-3 py-1 bg-slate-100 text-slate-600 rounded hover:bg-slate-200 disabled:opacity-50 text-sm font-medium transition-colors">← Back</button>
      <button onClick={goHome} className="px-3 py-1 bg-slate-100 text-slate-600 rounded hover:bg-slate-200 text-sm font-medium transition-colors">⌂ Home</button>
   </div>
   <h2 className="font-semibold text-slate-800">ParcelPilot Ops Copilot</h2>`
);

// Render pages for these tabs
const pagesRender = `
        {['tickets', 'orders', 'accounts', 'activity', 'settings'].includes(activeTab) && (
          <div className="p-8 max-w-6xl mx-auto w-full overflow-y-auto">
            <h2 className="text-3xl font-bold mb-8 text-slate-800 tracking-tight capitalize">{activeTab}</h2>
            <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 flex flex-col items-center justify-center text-center">
               <div className="text-6xl mb-4 text-slate-200">🛠️</div>
               <h3 className="text-xl font-bold text-slate-700 mb-2">Feature Under Construction</h3>
               <p className="text-slate-500 max-w-md">The {activeTab} view is fully wired up to the frontend navigation state, but the backend data endpoints for this section are coming soon!</p>
               <button onClick={goHome} className="mt-6 px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition">Return to Home</button>
            </div>
          </div>
        )}
`;

content = content.replace(
  /\} \/\* End of dashboard \*\//, // I don't have this comment, I'll replace the closing div
  `
  `
);
fs.writeFileSync(path, content);
