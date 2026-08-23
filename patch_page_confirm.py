import re
with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

# Replace the text-based check with a tool-based check
replacement = """
                    {/* Action Confirmation Card */}
                    {m.role === 'agent' && m.toolActivity?.some(t => t.tool === 'prepare_escalation') && (
                       <div className="mt-5 p-5 border rounded-xl bg-orange-50 border-orange-200">
                         <div className="flex items-center gap-2 mb-3">
                           <span className="text-orange-600 text-lg">⚠️</span>
                           <h4 className="font-bold text-orange-900">Prepare Escalation</h4>
                         </div>
                         <div className="bg-white p-3 rounded border border-orange-100 mb-4 text-sm text-orange-800 space-y-1">
                           <div><strong>Ticket:</strong> {m.toolActivity.find(t => t.tool === 'prepare_escalation')?.args?.ticket_id || 'Identified from context'}</div>
                           <div><strong>Action:</strong> Escalate to Product Operations</div>
                           <div><strong>Reason:</strong> {m.toolActivity.find(t => t.tool === 'prepare_escalation')?.args?.reason || 'Review required'}</div>
                         </div>
                         <div className="flex space-x-3">
                           <button onClick={() => handleConfirm('execute_escalation', {ticket_id: m.toolActivity.find(t => t.tool === 'prepare_escalation')?.args?.ticket_id})} className="bg-blue-600 text-white px-5 py-2 rounded-lg font-semibold hover:bg-blue-700 shadow-sm">Confirm Escalation</button>
                           <button className="bg-white border border-slate-300 text-slate-700 px-5 py-2 rounded-lg font-semibold hover:bg-slate-50">Cancel</button>
                         </div>
                       </div>
                    )}
"""
content = re.sub(
    r'\{/\* Action Confirmation Card \*/\}[\s\S]*?(?=\{/\* Sources / Evidence Panel \*/\})',
    replacement,
    content
)

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
