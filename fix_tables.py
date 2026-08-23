with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

start_idx = content.find("{['tickets', 'orders', 'accounts'].includes(activeTab) && !selectedItem && (")
end_idx = content.find("{/* Details View */}")

if start_idx != -1 and end_idx != -1:
    new_tables = """{['tickets', 'orders', 'accounts'].includes(activeTab) && !selectedItem && (
          <div className="p-6 max-w-6xl mx-auto w-full overflow-y-auto h-full bg-slate-50">
            <div className="flex justify-between items-center mb-4 border-b border-slate-200 pb-4">
              <input 
                type="text" 
                placeholder={`Search ${activeTab}...`}
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="w-72 px-3 py-1.5 border border-slate-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-blue-500 shadow-sm"
              />
            </div>
            
            <div className="bg-white border border-slate-200 shadow-sm rounded-lg overflow-hidden">
               {activeTab === 'tickets' && (
                 <table className="w-full text-left text-sm whitespace-nowrap">
                   <thead className="bg-slate-50 border-b border-slate-200">
                     <tr>
                       <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Ticket ID</th>
                       <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Account</th>
                       <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Status</th>
                       <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Subject</th>
                       <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Created</th>
                     </tr>
                   </thead>
                   <tbody className="divide-y divide-slate-100">
                     {ticketsData.filter(t => (t.ticket_id+' '+t.subject).toLowerCase().includes(searchQuery.toLowerCase())).map((t, i) => (
                       <tr key={i} className="hover:bg-slate-50 cursor-pointer" onClick={() => setSelectedItem(t)}>
                         <td className="px-4 py-3 font-semibold text-blue-600 hover:underline">{t.ticket_id}</td>
                         <td className="px-4 py-3 text-slate-700">{t.account_id}</td>
                         <td className="px-4 py-3">
                           <span className={`px-2 py-0.5 text-xs font-semibold rounded border ${t.status === 'open' ? 'bg-green-50 text-green-700 border-green-200' : 'bg-slate-100 text-slate-600 border-slate-200'}`}>{t.status.toUpperCase()}</span>
                         </td>
                         <td className="px-4 py-3 text-slate-700 truncate max-w-xs">{t.subject}</td>
                         <td className="px-4 py-3 text-slate-500">{t.created_at}</td>
                       </tr>
                     ))}
                   </tbody>
                 </table>
               )}

               {activeTab === 'orders' && (
                 <table className="w-full text-left text-sm whitespace-nowrap">
                   <thead className="bg-slate-50 border-b border-slate-200">
                     <tr>
                       <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Order ID</th>
                       <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Account</th>
                       <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Status</th>
                       <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Service</th>
                       <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Booked</th>
                     </tr>
                   </thead>
                   <tbody className="divide-y divide-slate-100">
                     {ordersData.filter(o => (o.order_id+' '+o.status).toLowerCase().includes(searchQuery.toLowerCase())).map((o, i) => (
                       <tr key={i} className="hover:bg-slate-50 cursor-pointer" onClick={() => setSelectedItem(o)}>
                         <td className="px-4 py-3 font-semibold text-blue-600 hover:underline">{o.order_id}</td>
                         <td className="px-4 py-3 text-slate-700">{o.account_id}</td>
                         <td className="px-4 py-3">
                            <span className={`px-2 py-0.5 text-xs font-semibold rounded border ${o.status === 'DELIVERED' ? 'bg-green-50 text-green-700 border-green-200' : o.status === 'BOOKED' ? 'bg-blue-50 text-blue-700 border-blue-200' : 'bg-yellow-50 text-yellow-700 border-yellow-200'}`}>{o.status}</span>
                         </td>
                         <td className="px-4 py-3 text-slate-700">{o.service_type}</td>
                         <td className="px-4 py-3 text-slate-500">{o.booked_at}</td>
                       </tr>
                     ))}
                   </tbody>
                 </table>
               )}

               {activeTab === 'accounts' && (
                 <table className="w-full text-left text-sm whitespace-nowrap">
                   <thead className="bg-slate-50 border-b border-slate-200">
                     <tr>
                       <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">ID</th>
                       <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Name</th>
                       <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Plan</th>
                       <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Status</th>
                     </tr>
                   </thead>
                   <tbody className="divide-y divide-slate-100">
                     {accountsData.filter(a => (a.account_id+' '+a.account_name).toLowerCase().includes(searchQuery.toLowerCase())).map((a, i) => (
                       <tr key={i} className="hover:bg-slate-50 cursor-pointer" onClick={() => setSelectedItem(a)}>
                         <td className="px-4 py-3 font-semibold text-blue-600 hover:underline">{a.account_id}</td>
                         <td className="px-4 py-3 text-slate-700">{a.account_name}</td>
                         <td className="px-4 py-3 text-slate-700">{a.plan}</td>
                         <td className="px-4 py-3">
                           <span className={`px-2 py-0.5 text-xs font-semibold rounded border ${a.status === 'Active' ? 'bg-green-50 text-green-700 border-green-200' : 'bg-slate-100 text-slate-600 border-slate-200'}`}>{a.status}</span>
                         </td>
                       </tr>
                     ))}
                   </tbody>
                 </table>
               )}
            </div>
          </div>
        )}

        """
    content = content[:start_idx] + new_tables + content[end_idx:]
    with open("frontend/src/app/page.tsx", "w") as f:
        f.write(content)
