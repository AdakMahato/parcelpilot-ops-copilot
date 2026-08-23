import re
with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

# 1. Remove duplicate border
content = content.replace('border border-slate-200 border border-slate-200', 'border border-slate-200')

# 2. Remove inline back button in Details View
content = re.sub(r'<button onClick=\{.*?setSelectedItem\(null\).*?← Back to list<\/button>', '', content)

# 3. Change AI investigate button to be more professional (no emoji, less huge)
content = content.replace('🤖 Investigate with AI', 'Analyze')
content = content.replace('className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold shadow-sm w-full"', 'className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded font-medium shadow-sm w-full text-sm"')

# 4. Clear chat button - make it less of a giant rounded pill
content = content.replace('rounded-full text-xs font-bold uppercase tracking-wider', 'rounded text-xs font-medium')

# 5. Fix double background in backdrop
content = content.replace('bg-slate-900/20 backdrop-blur-none bg-slate-900/40', 'bg-slate-900/40')

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
