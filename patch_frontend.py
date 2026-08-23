import re
with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

# Add state
if "const [activityData, setActivityData]" not in content:
    content = content.replace("const [accountsData, setAccountsData] = useState<any[]>([]);", "const [accountsData, setAccountsData] = useState<any[]>([]);\n  const [activityData, setActivityData] = useState<any[]>([]);")

# Add to useEffect
load_logic = """    } else if (activeTab === 'accounts') {
      loadData('accounts', setAccountsData);
    } else if (activeTab === 'activity') {
      loadData('activity', setActivityData);
    }"""
content = content.replace("""    } else if (activeTab === 'accounts') {
      loadData('accounts', setAccountsData);
    }""", load_logic)

# Replace empty state with map
old_activity = r"\{activeTab === 'activity' && \([\s\S]*?<\/div>\s*<\/div>\s*\)\}"
new_activity = """        {activeTab === 'activity' && (
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
        )}"""
content = re.sub(old_activity, new_activity, content)

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
