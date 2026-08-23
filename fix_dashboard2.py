with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

start_idx = content.find("{activeTab === 'dashboard' && (")
end_idx = content.find("{['tickets', 'orders', 'accounts'].includes(activeTab) && !selectedItem && (")

if start_idx != -1 and end_idx != -1:
    old_block = content[start_idx:end_idx]
    
    new_dash = """{activeTab === 'dashboard' && (
          <div className="p-8 max-w-6xl mx-auto w-full overflow-y-auto h-full bg-slate-50">
            {/* Show health warning if backend is offline */}
            {backendHealth?.status === 'error' && (
               <div className="bg-red-50 text-red-700 p-4 rounded-lg mb-6 text-sm border border-red-200">
                  <strong>AI backend unavailable.</strong> Start the FastAPI server (<code>uvicorn app.main:app</code>) and try again.
               </div>
            )}

            {dashboardData ? (
              <div className="space-y-6">
                {/* Compact KPI Cards */}
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex flex-col">
                    <div className="text-slate-500 font-semibold uppercase tracking-wider text-xs mb-2">SLA Breached</div>
                    <div className="text-3xl font-bold text-red-600">{dashboardData.sla_metrics.breached}</div>
                  </div>
                  <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex flex-col">
                    <div className="text-slate-500 font-semibold uppercase tracking-wider text-xs mb-2">Approaching SLA</div>
                    <div className="text-3xl font-bold text-yellow-600">{dashboardData.sla_metrics.approaching}</div>
                  </div>
                  <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm flex flex-col">
                    <div className="text-slate-500 font-semibold uppercase tracking-wider text-xs mb-2">Healthy Tickets</div>
                    <div className="text-3xl font-bold text-emerald-600">{dashboardData.sla_metrics.healthy}</div>
                  </div>
                </div>

                {/* Professional Two-Column Layout */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  
                  {/* Left Column: Recurring Issues */}
                  <div>
                    <h3 className="text-sm font-bold text-slate-800 mb-4 border-b border-slate-200 pb-2">Recurring Issues</h3>
                    <div className="space-y-3">
                      {dashboardData.recurring_issues.map((iss: any, i: number) => (
                        <div key={i} className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
                          <div className="flex justify-between items-start mb-2">
                            <span className="text-xs font-semibold px-2 py-0.5 bg-blue-50 text-blue-700 rounded border border-blue-100">{iss.issue_id}</span>
                            <span className="text-xs font-medium px-2 py-0.5 bg-orange-50 text-orange-700 rounded border border-orange-100">{iss.severity} Severity</span>
                          </div>
                          <h4 className="font-bold text-slate-800 text-sm mb-3">{iss.title}</h4>
                          <div className="text-xs text-slate-600 mb-1"><span className="font-semibold">Affected:</span> {iss.affected_customers.join(', ')}</div>
                          <div className="text-xs text-slate-600"><span className="font-semibold">Related:</span> {iss.related_tickets.join(', ')}</div>
                        </div>
                      ))}
                      {dashboardData.recurring_issues.length === 0 && (
                        <div className="text-sm text-slate-500 p-4 bg-slate-50 rounded border border-slate-100">No recurring issues detected.</div>
                      )}
                    </div>
                  </div>

                  {/* Right Column: SLA Risk */}
                  <div>
                    <h3 className="text-sm font-bold text-slate-800 mb-4 border-b border-slate-200 pb-2">SLA Risk</h3>
                    <div className="bg-white border border-slate-200 rounded-lg shadow-sm overflow-hidden">
                      <table className="w-full text-left text-sm">
                        <thead className="bg-slate-50 border-b border-slate-200">
                          <tr>
                            <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Ticket</th>
                            <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Account</th>
                            <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase">Status</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                          {dashboardData.sla_risks.map((r: any, i: number) => (
                            <tr key={i} className="hover:bg-slate-50 cursor-pointer" onClick={() => handleInvestigate(`Investigate ${r.ticket_id} for SLA risk.`)}>
                              <td className="px-4 py-3 font-medium text-blue-600 text-xs hover:underline">{r.ticket_id}</td>
                              <td className="px-4 py-3 text-slate-700 text-xs truncate max-w-[120px]">{r.account}</td>
                              <td className="px-4 py-3">
                                <span className={`text-xs font-semibold px-2 py-0.5 rounded border ${
                                  r.status === 'Breached' ? 'bg-red-50 text-red-700 border-red-100' : 'bg-yellow-50 text-yellow-700 border-yellow-100'
                                }`}>
                                  {r.status}
                                </span>
                              </td>
                            </tr>
                          ))}
                          {dashboardData.sla_risks.length === 0 && (
                            <tr>
                              <td colSpan={3} className="px-4 py-6 text-center text-sm text-slate-500">All tickets are healthy.</td>
                            </tr>
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>

                </div>
              </div>
            ) : (
              <div className="animate-pulse flex space-x-4">
                <div className="flex-1 space-y-4 py-1">
                  <div className="h-4 bg-slate-200 rounded w-3/4"></div>
                  <div className="space-y-2">
                    <div className="h-4 bg-slate-200 rounded"></div>
                    <div className="h-4 bg-slate-200 rounded w-5/6"></div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        """
    content = content[:start_idx] + new_dash + content[end_idx:]
    
    with open("frontend/src/app/page.tsx", "w") as f:
        f.write(content)
else:
    print("Could not find bounds")
