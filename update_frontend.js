const fs = require('fs');
const path = './frontend/src/app/page.tsx';
let content = fs.readFileSync(path, 'utf8');

// Add states for data
content = content.replace(
  /const \[dashboardData, setDashboardData\] = useState<any>\(null\);/,
  `const [dashboardData, setDashboardData] = useState<any>(null);
  const [ticketsData, setTicketsData] = useState<any[]>([]);
  const [ordersData, setOrdersData] = useState<any[]>([]);
  const [accountsData, setAccountsData] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedItem, setSelectedItem] = useState<any>(null);`
);

// Add fetch calls
content = content.replace(
  /const loadDashboard = async \(\) => \{/,
  `const loadData = async (endpoint: string, setter: any) => {
    try {
      const res = await fetch(\`\${apiUrl}/api/\${endpoint}\`, {
        headers: {
          'x-user-role': 'support_agent',
          'x-allowed-accounts': 'ACCT-001,ACCT-002,ACCT-003,ACCT-004'
        }
      });
      const data = await res.json();
      setter(data);
    } catch (e) {
      console.error(e);
    }
  };

  const loadDashboard = async () => {`
);

// Add useEffects for loading data
content = content.replace(
  /if \(activeTab === 'dashboard'\) \{\n\s*loadDashboard\(\);\n\s*\}/,
  `if (activeTab === 'dashboard') {
      loadDashboard();
    } else if (activeTab === 'tickets') {
      loadData('tickets', setTicketsData);
    } else if (activeTab === 'orders') {
      loadData('orders', setOrdersData);
    } else if (activeTab === 'accounts') {
      loadData('accounts', setAccountsData);
    }
    setSelectedItem(null);
    setSearchQuery('');`
);

// Function to handle "Investigate with AI"
content = content.replace(
  /const handleSendClick = \(\) => \{/,
  `const handleInvestigate = (query: string) => {
    setActiveTab('chat');
    sendMessage(query);
  };
  
  const handleSendClick = () => {`
);

// We need to replace the "Feature Under Construction" block
const newPagesRender = `
        {['tickets', 'orders', 'accounts'].includes(activeTab) && !selectedItem && (
          <div className="p-8 max-w-6xl mx-auto w-full overflow-y-auto">
            <h2 className="text-3xl font-bold mb-6 text-slate-800 tracking-tight capitalize">{activeTab}</h2>
            
            <div className="mb-6">
               <input 
                 type="text"
                 placeholder={\`Search \${activeTab}...\`}
                 className="w-full p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                 value={searchQuery}
                 onChange={e => setSearchQuery(e.target.value)}
               />
            </div>

            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
               {activeTab === 'tickets' && (
                 <table className="w-full text-left text-sm">
                   <thead className="bg-slate-50 text-slate-500 font-semibold text-xs uppercase">
                     <tr>
                       <th className="px-5 py-3">ID</th>
                       <th className="px-5 py-3">Account</th>
                       <th className="px-5 py-3">Subject</th>
                       <th className="px-5 py-3">Status</th>
                     </tr>
                   </thead>
                   <tbody className="divide-y divide-slate-100">
                     {ticketsData.filter(t => (t.ticket_id+' '+t.account_id+' '+t.subject).toLowerCase().includes(searchQuery.toLowerCase())).map((t, i) => (
                       <tr key={i} className="hover:bg-slate-50 cursor-pointer" onClick={() => setSelectedItem(t)}>
                         <td className="px-5 py-4 font-medium text-blue-600">{t.ticket_id}</td>
                         <td className="px-5 py-4 text-slate-700">{t.account_id}</td>
                         <td className="px-5 py-4 text-slate-700">{t.subject}</td>
                         <td className="px-5 py-4">
                            <span className={\`px-2 py-1 rounded text-xs font-bold uppercase \${t.status === 'open' ? 'bg-yellow-100 text-yellow-700' : 'bg-slate-100 text-slate-700'}\`}>{t.status}</span>
                         </td>
                       </tr>
                     ))}
                   </tbody>
                 </table>
               )}

               {activeTab === 'orders' && (
                 <table className="w-full text-left text-sm">
                   <thead className="bg-slate-50 text-slate-500 font-semibold text-xs uppercase">
                     <tr>
                       <th className="px-5 py-3">ID</th>
                       <th className="px-5 py-3">Account</th>
                       <th className="px-5 py-3">Carrier</th>
                       <th className="px-5 py-3">Status</th>
                     </tr>
                   </thead>
                   <tbody className="divide-y divide-slate-100">
                     {ordersData.filter(o => (o.order_id+' '+o.account_id+' '+o.carrier).toLowerCase().includes(searchQuery.toLowerCase())).map((o, i) => (
                       <tr key={i} className="hover:bg-slate-50 cursor-pointer" onClick={() => setSelectedItem(o)}>
                         <td className="px-5 py-4 font-medium text-blue-600">{o.order_id}</td>
                         <td className="px-5 py-4 text-slate-700">{o.account_id}</td>
                         <td className="px-5 py-4 text-slate-700">{o.carrier}</td>
                         <td className="px-5 py-4 text-slate-700">{o.status}</td>
                       </tr>
                     ))}
                   </tbody>
                 </table>
               )}

               {activeTab === 'accounts' && (
                 <table className="w-full text-left text-sm">
                   <thead className="bg-slate-50 text-slate-500 font-semibold text-xs uppercase">
                     <tr>
                       <th className="px-5 py-3">ID</th>
                       <th className="px-5 py-3">Name</th>
                       <th className="px-5 py-3">Plan</th>
                       <th className="px-5 py-3">Status</th>
                     </tr>
                   </thead>
                   <tbody className="divide-y divide-slate-100">
                     {accountsData.filter(a => (a.account_id+' '+a.account_name).toLowerCase().includes(searchQuery.toLowerCase())).map((a, i) => (
                       <tr key={i} className="hover:bg-slate-50 cursor-pointer" onClick={() => setSelectedItem(a)}>
                         <td className="px-5 py-4 font-medium text-blue-600">{a.account_id}</td>
                         <td className="px-5 py-4 text-slate-700">{a.account_name}</td>
                         <td className="px-5 py-4 text-slate-700">{a.plan}</td>
                         <td className="px-5 py-4 text-slate-700">{a.status}</td>
                       </tr>
                     ))}
                   </tbody>
                 </table>
               )}
            </div>
          </div>
        )}

        {/* Details View */}
        {selectedItem && (
          <div className="p-8 max-w-4xl mx-auto w-full overflow-y-auto">
            <button onClick={() => setSelectedItem(null)} className="mb-4 text-blue-600 font-medium hover:underline">← Back to list</button>
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
               <h2 className="text-2xl font-bold mb-4 text-slate-800">
                  {selectedItem.ticket_id || selectedItem.order_id || selectedItem.account_id} Details
               </h2>
               
               <div className="grid grid-cols-2 gap-4 mb-6">
                 {Object.entries(selectedItem).map(([key, val]) => (
                   <div key={key} className="border-b pb-2">
                     <div className="text-xs text-slate-400 uppercase font-semibold">{key.replace(/_/g, ' ')}</div>
                     <div className="text-sm font-medium text-slate-800">{String(val)}</div>
                   </div>
                 ))}
               </div>

               {selectedItem.ticket_id && (
                 <button onClick={() => handleInvestigate(\`Investigate \${selectedItem.ticket_id} and identify the likely issue.\`)} className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold shadow-sm w-full">
                    🤖 Investigate with AI
                 </button>
               )}
               {selectedItem.order_id && (
                 <button onClick={() => handleInvestigate(\`Investigate order \${selectedItem.order_id}.\`)} className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold shadow-sm w-full">
                    🤖 Investigate with AI
                 </button>
               )}
            </div>
          </div>
        )}

        {['activity', 'settings'].includes(activeTab) && (
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
  /\{(\['tickets', 'orders', 'accounts', 'activity', 'settings'\].includes\(activeTab\))[\s\S]*?<\/button>\n\s*<\/div>\n\s*<\/div>\n\s*\)}/,
  newPagesRender.trim()
);

fs.writeFileSync(path, content);
