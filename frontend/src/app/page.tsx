"use client";
import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

type Message = {
  role: string;
  content: string;
  toolActivity?: any[];
  sourcesUsed?: any[];
};

export default function Home() {
  const [activeTab, setActiveTabInternal] = useState('chat');
  const [navHistory, setNavHistory] = useState<string[]>([]);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  
  const setActiveTab = (tab: string) => {
    setSelectedItem(null);
    setNavHistory(prev => [...prev, activeTab]);
    setActiveTabInternal(tab);
  };
  
  const goBack = () => {
    setSelectedItem(null);
    if (navHistory.length > 0) {
      const prev = navHistory[navHistory.length - 1];
      setNavHistory(h => h.slice(0, -1));
      setActiveTabInternal(prev);
    }
  };
  
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setIsDrawerOpen(false);
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, []);

  const goHome = () => {
    setSelectedItem(null);
    setActiveTab('chat');
  };
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [ticketsData, setTicketsData] = useState<any[]>([]);
  const [ordersData, setOrdersData] = useState<any[]>([]);
  const [accountsData, setAccountsData] = useState<any[]>([]);
  const [activityData, setActivityData] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedItem, setSelectedItem] = useState<any>(null);
  const [backendHealth, setBackendHealth] = useState<any>(null);

  const snapshotTime = "2026-08-16 11:00 Asia/Kolkata";
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  useEffect(() => {
    fetch(`${apiUrl}/api/health`)
      .then(res => res.json())
      .then(data => setBackendHealth(data))
      .catch(err => setBackendHealth({ status: 'error', error: err.message }));
  }, []);

  const loadData = async (endpoint: string, setter: any) => {
    try {
      const res = await fetch(`${apiUrl}/api/${endpoint}`, {
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

  const loadDashboard = async () => {
    try {
      const res = await fetch(`${apiUrl}/api/dashboard`, {
        headers: {
          'x-user-role': 'support_agent',
          'x-allowed-accounts': 'ACCT-001,ACCT-002,ACCT-003,ACCT-004'
        }
      });
      const data = await res.json();
      if (data.type === 'llm_unavailable' && data.recoverable) {
        setMessages(prev => [...prev, {role: 'agent', content: data.response || 'Gemini API is temporarily unavailable (quota or rate limit reached).'}]);
        setIsLoading(false);
        return;
      }
      setDashboardData(data);
    } catch (e) {
      console.error("Dashboard error:", e);
    }
  };

  useEffect(() => {
    if (activeTab === 'dashboard') {
      loadDashboard();
    } else if (activeTab === 'tickets') {
      loadData('tickets', setTicketsData);
    } else if (activeTab === 'orders') {
      loadData('orders', setOrdersData);
    } else if (activeTab === 'accounts') {
      loadData('accounts', setAccountsData);
    } else if (activeTab === 'activity') {
      loadData('activity', setActivityData);
    }
    setSelectedItem(null);
    setSearchQuery('');
  }, [activeTab]);

  const sendMessage = async (textToSubmit: string) => {
    if(!textToSubmit.trim()) return;
    setInput('');
    setMessages(prev => [...prev, {role: 'user', content: textToSubmit}]);
    setIsLoading(true);

    try {
      const res = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-role': 'support_agent',
          'x-allowed-accounts': 'ACCT-001,ACCT-002,ACCT-003,ACCT-004'
        },
        body: JSON.stringify({ message: textToSubmit })
      });
      
      if (!res.ok) {
        let errMsg = `Server returned ${res.status}`;
        try {
          const errData = await res.json();
          errMsg = errData.detail || errData.message || errMsg;
        } catch(e) {}
        throw new Error(errMsg);
      }

      const data = await res.json();
      setMessages(prev => [...prev, {
        role: 'agent', 
        content: data.response || data,
        toolActivity: data.tool_activity || [],
        sourcesUsed: data.sources_used || []
      }]);
    } catch (e) {
      console.error(e);
      setMessages(prev => [...prev, {role: 'agent', content: 'Agent Error: ' + (e as Error).message}]);
    }
    setIsLoading(false);
  };

  const handleConfirm = async (action: string, payload: any) => {
    try {
      const res = await fetch(`${apiUrl}/api/action/confirm`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-role': 'support_agent',
          'x-allowed-accounts': 'ACCT-001,ACCT-002,ACCT-003,ACCT-004'
        },
        body: JSON.stringify({ action, payload })
      });
      const data = await res.json();
      alert(data.message || data.detail);
    } catch (e) {
      alert("Execution failed.");
    }
  };

  const toolNameMapping: Record<string, string> = {
    'document_search': 'Searching documents...',
    'operational_data_lookup': 'Querying operational data...',
    'sla_calculator': 'Calculating SLA...',
    'prepare_escalation': 'Evaluating action prerequisites...'
  };

  const handleInvestigate = (query: string) => {
    setActiveTab('chat');
    sendMessage(query);
  };
  
  const handleSendClick = () => {
    sendMessage(input);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 font-sans text-slate-800">
      {/* Sidebar */}
      <div className="w-64 bg-slate-50 text-slate-800 flex flex-col border-r border-slate-200">
        <div className="p-6">
          <h1 className="text-xl font-bold tracking-tight">ParcelPilot</h1>
          <h2 className="text-sm font-medium text-blue-600">Ops Copilot</h2>
        </div>
        
        <nav className="flex-1 px-4 space-y-1">
          <button 
            onClick={() => setActiveTab('chat')}
            className={`w-full text-left px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-3 transition-colors ${activeTab === 'chat' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'}`}>
            <span className="text-lg">▣</span> Chat
          </button>
          <button 
            onClick={() => setActiveTab('dashboard')}
            className={`w-full text-left px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-3 transition-colors ${activeTab === 'dashboard' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'}`}>
            <span className="text-lg">◉</span> Issue Intelligence
          </button>
          
          <div className="pt-8 pb-2 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Operations</div>
          <button onClick={() => setActiveTab('tickets')} className={`w-full text-left px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'tickets' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'}`}>Tickets</button>
          <button onClick={() => setActiveTab('orders')} className={`w-full text-left px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'orders' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'}`}>Orders</button>
          <button onClick={() => setActiveTab('accounts')} className={`w-full text-left px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'accounts' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'}`}>Accounts</button>

          <div className="pt-8 pb-2 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">System</div>
          <button onClick={() => setActiveTab('activity')} className={`w-full text-left px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'activity' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'}`}>Activity</button>
          <button onClick={() => setActiveTab('settings')} className={`w-full text-left px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'settings' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'}`}>Settings</button>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden bg-white">

        {/* Consistent Top Header */}
        <header className="h-14 flex items-center justify-between px-6 border-b border-slate-200 bg-white shrink-0">
          <div className="flex items-center gap-4">
            <button 
              onClick={goBack} 
              disabled={navHistory.length === 0 && !selectedItem} 
              className="text-slate-500 hover:text-slate-800 disabled:opacity-30 text-sm font-medium transition-colors flex items-center gap-1"
            >
              <span>←</span> Back
            </button>
            <div className="h-4 w-px bg-slate-300"></div>
            <h2 className="text-sm font-semibold text-slate-800 capitalize">
              {selectedItem ? 'Details' : activeTab}
            </h2>
          </div>
          <button 
            onClick={() => setIsDrawerOpen(true)}
            className="md:hidden text-slate-500 hover:text-slate-800"
          >
            ☰ Menu
          </button>
        </header>

        

        {/* Floating Top Right Menu Button */}
        <button 
          onClick={() => setIsDrawerOpen(true)}
          aria-label="Open menu"
          className="absolute top-4 right-4 z-20 w-8 h-8 flex items-center justify-center bg-white border border-slate-200 shadow-sm text-slate-600 rounded-md hover:bg-slate-50 transition-colors text-lg"
        >
          ☰
        </button>


        {activeTab === 'chat' && (
          <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full p-6 relative min-h-0 h-full">
            
            {/* Show health warning if backend is offline */}
            {backendHealth?.status === 'error' && (
               <div className="bg-red-50 text-red-700 p-4 rounded-lg mb-4 text-sm border border-red-200">
                  <strong>AI backend unavailable.</strong> Start the FastAPI server (<code>uvicorn app.main:app</code>) and try again.
               </div>
            )}
            {backendHealth?.status === 'degraded' && (
               <div className="bg-yellow-50 text-yellow-800 p-4 rounded-lg mb-4 text-sm border border-yellow-200">
                  <strong>Backend degraded.</strong> Check if GEMINI_API_KEY is exported and if SQLite/Chroma DB files exist.
               </div>
            )}

            <div className="flex-1 overflow-y-auto space-y-6 pb-24 hide-scrollbar">
              
              {messages.length > 0 && (
                <div className="flex justify-center mb-4">
                  <button onClick={() => setMessages([])} className="px-4 py-1 bg-slate-200 text-slate-600 rounded text-xs font-medium hover:bg-slate-300 transition-colors">Clear Chat</button>
                </div>
              )}
              {messages.length === 0 && (
                <div className="flex flex-col h-full mt-12">
                  <div className="mb-10 text-center">
                    <h2 className="text-xl font-semibold text-slate-800 mb-3">ParcelPilot Ops Copilot</h2>
                    <p className="text-slate-500 text-lg">Investigate support issues, orders, policies and customer agreements using ParcelPilot's operational data.</p>
                  </div>
                  
                  <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4 px-2">What can I help investigate?</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {[
                      {title: "Investigate an order", desc: "Can Northstar cancel ORD-1001 without a fee?"},
                      {title: "Investigate a ticket", desc: "Investigate TKT-502 and identify the likely issue."},
                      {title: "Check service credit", desc: "Does this delayed pickup qualify for a service credit?"},
                      {title: "Check SLA", desc: "Which tickets are currently approaching SLA?"},
                      {title: "Find known issues", desc: "Are multiple customers reporting the same product issue?"},
                      {title: "Prepare escalation", desc: "Prepare an escalation for a high-severity ticket."}
                    ].map((c, i) => (
                      <button 
                        key={i} 
                        onClick={() => sendMessage(c.desc)}
                        className="text-left p-4 rounded-xl border bg-white hover:border-blue-400 hover:shadow-md transition-all group">
                        <div className="font-semibold text-slate-800 mb-1 group-hover:text-blue-600">{c.title}</div>
                        <div className="text-sm text-slate-500">{c.desc}</div>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {messages.map((m, idx) => (
                <div key={idx} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  {m.role === 'agent' && (
                    <div className="w-8 h-8 rounded-full bg-slate-900 text-white flex items-center justify-center mr-3 flex-shrink-0 mt-1">🤖</div>
                  )}
                  
                  <div className={`rounded-xl px-4 py-3 shadow-sm border ${
                    m.role === 'user' 
                      ? 'bg-blue-600 text-white border-blue-700 max-w-[80%]' 
                      : 'bg-white border-slate-200 max-w-[90%] w-full'
                  }`}>
                    
                    
                    
                    {/* Tool Activity */}
                    {m.toolActivity && m.toolActivity.length > 0 && (
                       <div className="mb-4 space-y-1">
                         <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Agent Activity</div>
                         {m.toolActivity.map((t, i) => (
                           <div key={i} className="text-sm text-slate-600 flex items-center">
                             <span className="text-green-500 mr-2">✓</span> 
                             {t.tool === 'document_search' ? 'Searching documents...' : 
                              t.tool === 'operational_data_lookup' ? 'Querying operational data...' : 
                              t.tool === 'sla_calculator' ? 'Calculating SLA risk...' :
                              t.tool === 'prepare_escalation' ? 'Preparing escalation...' : t.tool}
                           </div>
                         ))}
                       </div>
                    )}


                    
                    
                    
                    {/* Message Content */}
                    {m.role === 'user' ? (
                      <div className="text-sm whitespace-pre-wrap leading-relaxed">{m.content}</div>
                    ) : (
                      <div className="text-slate-800 leading-relaxed text-sm">
                        
                        <ReactMarkdown 
                           components={{
                             h3: ({...props}: any) => <h3 className="text-lg font-bold mt-4 mb-2" {...props} />,
                             h4: ({...props}: any) => <h4 className="text-base font-bold mt-3 mb-1" {...props} />,
                             p: ({...props}: any) => <p className="mb-2" {...props} />,
                             ul: ({...props}: any) => <ul className="list-disc pl-5 space-y-1 mb-2" {...props} />,
                             ol: ({...props}: any) => <ol className="list-decimal pl-5 space-y-1 mb-2" {...props} />,
                             strong: ({...props}: any) => <strong className="font-bold text-slate-900" {...props} />,
                             hr: ({...props}: any) => <hr className="my-4 border-slate-200" {...props} />
                           }}
                        >

                          {m.content}
                        </ReactMarkdown>
                      </div>
                    )}

                    {/* Action Confirmation Card */}
                    {m.role === 'agent' && m.toolActivity?.some(t => t.tool === 'prepare_escalation') && (
                       <div className="mt-5 p-5 border rounded-xl bg-orange-50 border-orange-200">
                         <div className="flex items-center gap-2 mb-3">
                           <span className="text-orange-600 text-lg">⚠️</span>
                           <h4 className="font-bold text-orange-900">Prepare Escalation</h4>
                         </div>
                         <div className="bg-white p-3 rounded border border-orange-100 mb-4 text-sm text-orange-800 space-y-1">
                           <div><strong>Ticket:</strong> {m.toolActivity?.find(t => t.tool === 'prepare_escalation')?.args?.ticket_id || 'Identified from context'}</div>
                           <div><strong>Action:</strong> Escalate to Product Operations</div>
                           <div><strong>Reason:</strong> {m.toolActivity?.find(t => t.tool === 'prepare_escalation')?.args?.reason || 'Review required'}</div>
                         </div>
                         <div className="flex space-x-3">
                           <button onClick={() => handleConfirm('execute_escalation', {ticket_id: m.toolActivity?.find(t => t.tool === 'prepare_escalation')?.args?.ticket_id})} className="bg-blue-600 text-white px-5 py-2 rounded-lg font-semibold hover:bg-blue-700 shadow-sm">Confirm Escalation</button>
                           <button className="bg-white border border-slate-300 text-slate-700 px-5 py-2 rounded-lg font-semibold hover:bg-slate-50">Cancel</button>
                         </div>
                       </div>
                    )}

                    
                    {/* Sources / Evidence Panel */}
                    {m.role === 'agent' && m.sourcesUsed && m.sourcesUsed.length > 0 && (
                      <details className="mt-4 border-t pt-3 group">
                        <summary className="text-sm font-semibold text-slate-500 cursor-pointer flex items-center hover:text-slate-800 outline-none">
                          <span className="mr-1 group-open:rotate-90 transition-transform">▶</span> View Evidence & Sources
                        </summary>
                        <div className="mt-3 space-y-2 pl-4 border-l-2 border-slate-200">
                          {m.sourcesUsed.map((src, i) => (
                            <div key={i} className="text-sm text-slate-600 bg-slate-50 p-2 rounded">
                              <div className="font-semibold">{src.document || src.name || 'Unknown Source'}</div>
                              <div className="text-xs text-slate-500 mt-1">
                                {src.type || 'Document'} {src.authority_level ? `· Authority Level ${src.authority_level}` : ''}
                              </div>
                            </div>
                          ))}
                        </div>
                      </details>
                    )}


                  </div>
                </div>
              ))}
              
              {isLoading && (
                <div className="flex justify-start">
                  <div className="w-8 h-8 rounded-full bg-slate-900 text-white flex items-center justify-center mr-3 mt-1">🤖</div>
                  <div className="p-4 bg-white border border-slate-200 shadow-sm max-w-[90%] rounded-xl flex items-center space-x-3">
                    <span className="text-slate-500 font-medium text-sm">Agent is investigating...</span>
                  </div>
                </div>
              )}
            </div>
            
            {/* Input Area */}
            <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-gray-50 via-gray-50 to-transparent pt-10">
              <div className="relative max-w-4xl mx-auto">
                <textarea 
                  className="w-full pl-5 pr-24 py-4 bg-white border border-slate-300 rounded-2xl shadow-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all text-base resize-none"
                  rows={1}
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask about orders, tickets, policies, agreements or SLAs..."
                  disabled={isLoading}
                />
                <button 
                  onClick={handleSendClick} 
                  disabled={isLoading || !input.trim()}
                  className="absolute right-2 top-2 bottom-2 px-6 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white rounded-xl font-semibold transition-colors">
                  Send
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'dashboard' && (
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
                            <span className="text-xs font-semibold px-2 py-0.5 bg-blue-50 text-blue-400 rounded border border-blue-100">{iss.issue_id}</span>
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

        {['tickets', 'orders', 'accounts'].includes(activeTab) && !selectedItem && (
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
                            <span className={`px-2 py-0.5 text-xs font-semibold rounded border ${o.status === 'DELIVERED' ? 'bg-green-50 text-green-700 border-green-200' : o.status === 'BOOKED' ? 'bg-blue-50 text-blue-400 border-blue-200' : 'bg-yellow-50 text-yellow-700 border-yellow-200'}`}>{o.status}</span>
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

        {/* Details View */}
        {selectedItem && (
          <div className="p-8 max-w-4xl mx-auto w-full overflow-y-auto h-full">
            
            <div className="bg-white p-4 rounded-lg shadow-sm border border-slate-200">
               <h2 className="text-lg font-semibold mb-4 text-slate-800">
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
                 <button onClick={() => handleInvestigate(`Investigate ${selectedItem.ticket_id} and identify the likely issue.`)} className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded font-medium shadow-sm w-full text-sm">
                    Analyze
                 </button>
               )}
               {selectedItem.order_id && (
                 <button onClick={() => handleInvestigate(`Investigate order ${selectedItem.order_id}.`)} className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded font-medium shadow-sm w-full text-sm">
                    Analyze
                 </button>
               )}
            </div>
          </div>
        )}

        
                {activeTab === 'activity' && (
          <div className="p-6 max-w-4xl mx-auto w-full overflow-y-auto h-full">
            <h2 className="text-xl font-semibold mb-6 text-slate-800">Activity Log</h2>
            
            {activityData.length === 0 ? (
                <div className="bg-white border border-slate-200 rounded-lg p-12 text-center">
                   <div className="text-slate-300 text-3xl mb-3">≡</div>
                   <h3 className="text-sm font-semibold text-slate-700 mb-1">No recent activity</h3>
                   <p className="text-xs text-slate-500">Activity will appear here as operational actions occur.</p>
                </div>
            ) : (
                <div className="bg-white border border-slate-200 rounded-lg shadow-sm overflow-hidden">
                    <div className="divide-y divide-slate-100">
                        {activityData.map((act: any, i: number) => (
                            <div key={i} className="p-4 hover:bg-slate-50 transition-colors">
                                <div className="flex items-center justify-between mb-1">
                                    <span className="text-xs font-semibold text-blue-600 tracking-wider uppercase">{act.event_type}</span>
                                    <span className="text-xs text-slate-400 font-mono">{act.timestamp}</span>
                                </div>
                                <div className="text-sm text-slate-800 font-medium">{act.description}</div>
                                <div className="text-xs text-slate-500 mt-1">Actor: {act.actor}</div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
          </div>
        )}

        {activeTab === 'settings' && (
          <div className="p-6 max-w-4xl mx-auto w-full h-full">
            <h2 className="text-xl font-semibold mb-6 text-slate-800">Settings</h2>
            <div className="bg-white border border-slate-200 rounded-lg overflow-hidden">
               <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center">
                 <span className="text-sm font-medium text-slate-600">Application</span>
                 <span className="text-sm font-semibold text-slate-900">ParcelPilot Ops Copilot</span>
               </div>
               <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center">
                 <span className="text-sm font-medium text-slate-600">AI Provider</span>
                 <span className="text-sm font-semibold text-slate-900">Gemini 3.7 Flash</span>
               </div>
               <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center">
                 <span className="text-sm font-medium text-slate-600">Connection</span>
                 <span className="text-sm font-semibold text-green-600 flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-green-500"></span> Connected</span>
               </div>
               <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center">
                 <span className="text-sm font-medium text-slate-600">Environment</span>
                 <span className="text-sm font-semibold text-slate-900">Local</span>
               </div>
               <div className="px-6 py-4 flex justify-between items-center bg-slate-50">
                 <span className="text-sm font-medium text-slate-600">Data Snapshot</span>
                 <span className="text-xs font-mono text-slate-500">{snapshotTime || '2026-08-16 11:00'}</span>
               </div>
            </div>
          </div>
        )}

      </div>

      {/* Right-Side Drawer Overlay & Panel */}
      {isDrawerOpen && (
        <div className="fixed inset-0 z-50 flex justify-end">
          {/* Backdrop */}
          <div 
            className="absolute inset-0 bg-slate-900/40 transition-opacity" 
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
                  className="flex items-center w-full px-4 py-3 bg-blue-50 text-blue-400 rounded-xl hover:bg-blue-100 transition-colors text-base font-semibold"
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
    </div>
  );
}
