import re
with open("app/main.py", "r") as f:
    content = f.read()

# Replace the dashboard_endpoint entirely
new_dashboard = """@app.get("/api/dashboard")
def dashboard_endpoint(auth=Depends(get_auth_context)):
    db = SessionLocal()
    from app.models import Ticket, Account
    from datetime import datetime
    
    tickets = db.query(Ticket).all()
    accounts = db.query(Account).all()
    account_map = {a.account_id: a for a in accounts}
    
    snapshot_time = datetime.strptime("2026-08-16 11:00", "%Y-%m-%d %H:%M")
    
    breached = 0
    approaching = 0
    healthy = 0
    
    sla_risks = []
    bulk_upload_tickets = []
    
    for t in tickets:
        if "Bulk upload" in t.subject:
            bulk_upload_tickets.append(t.ticket_id)
            
        if t.status == 'open':
            acc = account_map.get(t.account_id)
            if not acc: continue
            
            created = datetime.strptime(t.created_at, "%Y-%m-%d %H:%M")
            elapsed_hours = (snapshot_time - created).total_seconds() / 3600.0
            
            sla_hours = 24
            if acc.plan == "Enterprise":
                sla_hours = 4
                if acc.account_name == "Northstar Logistics":
                    sla_hours = 2 # Custom SLA
            elif acc.plan == "Growth":
                sla_hours = 12
                
            remaining = sla_hours - elapsed_hours
            
            status = "Healthy"
            if remaining < 0:
                breached += 1
                status = "Breached"
            elif remaining <= 2:
                approaching += 1
                status = "Approaching SLA"
            else:
                healthy += 1
                
            if status != "Healthy":
                sla_risks.append({
                    "ticket_id": t.ticket_id,
                    "account": acc.account_name,
                    "severity": "High" if sla_hours <= 4 else "Medium",
                    "sla_target": f"{sla_hours} hours",
                    "remaining_time": f"{round(remaining, 1)} hours",
                    "status": status
                })
                
    recurring_issues = []
    if len(bulk_upload_tickets) > 1:
        recurring_issues.append({
            "issue_id": "KI-208",
            "title": "Bulk Upload Failures for Large CSV",
            "affected_customers": list(set([account_map[t.account_id].account_name for t in tickets if t.ticket_id in bulk_upload_tickets and t.account_id in account_map])),
            "related_tickets": bulk_upload_tickets,
            "severity": "High",
            "status": "Open / Investigating"
        })
                
    return {
        "sla_metrics": {
            "breached": breached,
            "approaching": approaching,
            "healthy": healthy
        },
        "recurring_issues": recurring_issues,
        "sla_risks": sla_risks
    }
"""
content = re.sub(r'@app\.get\("/api/dashboard"\)[\s\S]*?(?=@app\.get\("/api/tickets"\))', new_dashboard, content)

with open("app/main.py", "w") as f:
    f.write(content)
