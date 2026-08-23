import re
with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

# 1. Restore Sidebar Styling
# Find the sidebar container
content = content.replace('className="w-64 bg-slate-50 text-slate-800 flex flex-col border-r border-slate-200 shrink-0 hidden md:flex"', 'className="w-64 bg-slate-900 text-white flex flex-col border-r border-slate-800 shrink-0 hidden md:flex"')
content = content.replace('text-blue-700', 'text-blue-400')

# Restore Sidebar active/inactive tabs
content = re.sub(r'bg-blue-50 text-blue-400 font-semibold', 'bg-blue-600 text-white', content)
content = re.sub(r'text-slate-600 hover:bg-slate-100 hover:text-slate-900', 'text-slate-300 hover:bg-slate-800 hover:text-white', content)
content = content.replace('text-slate-500 uppercase tracking-wider', 'text-slate-400 uppercase tracking-wider')

# 2. Restore Markdown styling to be more generic (no forced uppercase headers)
markdown_components = """
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
"""
content = re.sub(r'<ReactMarkdown.*?components=\{\{.*?\}\}.*?>', markdown_components, content, flags=re.DOTALL)

# 3. Restore Tool Activity List
old_tool_strip = r'\{/\* Tool Activity Strip \*/\}[\s\S]*?<\/div>\s*\)\}'
new_tool_activity = """
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
"""
content = re.sub(old_tool_strip, new_tool_activity, content)

# 4. Restore Sources Details panel and fix src.name -> src.document
old_sources = r'\{/\* Sources / Evidence Panel \*/\}[\s\S]*?<\/div>\s*\)\}'
new_sources = """
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
"""
content = re.sub(old_sources, new_sources, content)

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
