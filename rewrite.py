import re

with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

# 1. Update Typography & Shell
# Remove the old floating back button entirely
content = re.sub(r'\{\/\* Floating Top Left Back Button \*\/\}.*?<\/button>', '', content, flags=re.DOTALL)

# Insert a consistent top header in the flex-1 container
top_header = """
        {/* Consistent Top Header */}
        <header className="h-14 flex items-center justify-between px-6 border-b border-slate-200 bg-white shrink-0">
          <div className="flex items-center gap-4">
            <button 
              onClick={goBack} 
              disabled={navHistory.length === 0} 
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
"""
content = content.replace('{/* Main Content */}\n      <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">\n        \n        ', 
                          '{/* Main Content */}\n      <div className="flex-1 flex flex-col min-w-0 overflow-hidden bg-white">\n' + top_header)

# 2. Update Sidebar styles
content = content.replace('bg-slate-900 text-white flex flex-col border-r border-slate-800', 'bg-slate-50 text-slate-800 flex flex-col border-r border-slate-200')
content = content.replace('text-blue-400', 'text-blue-600')
content = content.replace('bg-blue-600 text-white', 'bg-blue-50 text-blue-700 font-semibold')
content = content.replace('text-slate-300 hover:bg-slate-800 hover:text-white', 'text-slate-600 hover:bg-slate-100 hover:text-slate-900')

# 3. Fix Dashboard
content = content.replace('text-3xl font-bold mb-8 text-slate-800 tracking-tight', 'text-xl font-semibold mb-6 text-slate-800')
# KPI cards from 5xl -> 3xl, p-6 -> p-4
content = content.replace('text-5xl font-extrabold text-slate-900', 'text-3xl font-bold text-slate-800')
content = content.replace('bg-white p-6 rounded-2xl shadow-sm', 'bg-white p-4 rounded-lg shadow-sm border border-slate-200')

# 4. Redesign Markdown
markdown_components = """
     <ReactMarkdown 
       components={{
         h3: ({...props}: any) => <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mt-6 mb-2" {...props} />,
         h4: ({...props}: any) => <h4 className="text-sm font-semibold text-slate-800 mt-4 mb-1" {...props} />,
         p: ({...props}: any) => <p className="mb-3 text-sm leading-relaxed text-slate-700" {...props} />,
         ul: ({...props}: any) => <ul className="list-none space-y-1 mb-3 text-sm text-slate-700" {...props} />,
         li: ({...props}: any) => <li className="relative pl-3 before:content-['•'] before:absolute before:left-0 before:text-slate-400" {...props} />,
         strong: ({...props}: any) => <strong className="font-semibold text-slate-900" {...props} />,
         hr: ({...props}: any) => <hr className="my-5 border-slate-100" {...props} />
       }}
     >
"""
content = re.sub(r'<ReactMarkdown.*?components=\{\{.*?\}\}.*?>', markdown_components, content, flags=re.DOTALL)

# 5. Fix tool activity (compact strip)
old_tool_activity = r'\{/\* Tool Activity \*/\}[\s\S]*?<\/div>[\s\S]*?<\/div>[\s\S]*?<\/div>'
new_tool_activity = """
                    {/* Tool Activity Strip */}
                    {m.toolActivity && m.toolActivity.length > 0 && (
                       <div className="mb-3 flex flex-wrap items-center gap-2 text-xs text-slate-500 font-medium">
                         <span className="text-blue-600">⚡ Agent activity:</span>
                         {m.toolActivity.map((t, i) => (
                           <span key={i} className="bg-slate-50 border border-slate-200 px-2 py-0.5 rounded text-slate-600">
                             ✓ {toolNameMapping[t.tool] || t.tool}
                           </span>
                         ))}
                       </div>
                    )}
"""
content = re.sub(old_tool_activity, new_tool_activity, content)

# 6. Fix Sources Panel
old_sources = r'\{/\* Sources / Evidence Panel \*/\}[\s\S]*?<\/details>'
new_sources = """
                    {/* Sources / Evidence Panel */}
                    {m.role === 'agent' && m.sourcesUsed && m.sourcesUsed.length > 0 && (
                      <div className="mt-6 border-t border-slate-100 pt-4">
                        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">Sources Used</h4>
                        <div className="space-y-2">
                          {m.sourcesUsed.map((src, i) => (
                            <div key={i} className="flex items-center justify-between text-xs p-2 rounded border border-slate-100 bg-slate-50">
                              <div>
                                <span className="font-semibold text-slate-700">{src.name || 'Unknown Source'}</span>
                                <span className="text-slate-400 ml-2">{src.type || 'Document'}</span>
                              </div>
                              {src.authority_level && (
                                <span className="px-2 py-0.5 bg-blue-50 text-blue-700 rounded font-medium border border-blue-100">Auth Lvl {src.authority_level}</span>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
"""
content = re.sub(old_sources, new_sources, content)

# 7. Redesign Settings and Activity Empty States
old_empty = r"\{\['activity', 'settings'\].includes\(activeTab\)[\s\S]*?<\/div>\s*<\/div>\s*\)}"
new_empty = """
        {activeTab === 'activity' && (
          <div className="p-6 max-w-4xl mx-auto w-full h-full">
            <h2 className="text-xl font-semibold mb-6 text-slate-800">Activity Log</h2>
            <div className="bg-white border border-slate-200 rounded-lg p-12 text-center">
               <div className="text-slate-300 text-3xl mb-3">≡</div>
               <h3 className="text-sm font-semibold text-slate-700 mb-1">No recent activity</h3>
               <p className="text-xs text-slate-500">Activity will appear here as operational actions occur.</p>
            </div>
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
"""
content = re.sub(old_empty, new_empty, content)

# 8. Tighter table styles
content = content.replace('px-5 py-4', 'px-4 py-3')
content = content.replace('px-5 py-3', 'px-4 py-2')
content = content.replace('text-2xl font-bold', 'text-lg font-semibold')
content = content.replace('text-3xl font-bold', 'text-xl font-semibold')

# 9. Drawer blur
content = content.replace('backdrop-blur-sm', 'backdrop-blur-none bg-slate-900/40')

# Write back
with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)

