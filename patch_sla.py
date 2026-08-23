import re
with open("backend/app/tools.py", "r") as f:
    content = f.read()

new_sla = """# TOOL 3: SLA_CALCULATOR
def sla_calculator(ticket_id: str):
    db = get_db()
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not ticket:
        return {"error": "Ticket not found"}
        
    account = db.query(Account).filter(Account.account_id == ticket.account_id).first()
    
    snapshot_time = "2026-08-16 11:00"
    
    plan = account.plan
    if plan == "Enterprise":
        target = "4 hours"
        if account.account_name == "Northstar Logistics":
            target = "2 hours (Custom Agreement)"
    elif plan == "Growth":
        target = "12 hours"
    else:
        target = "24 hours"
        
    return {
        "target": target,
        "status": "CALCULATED",
        "snapshot_time": snapshot_time,
        "created_at": ticket.created_at
    }"""
content = re.sub(r'# TOOL 3: SLA_CALCULATOR[\s\S]*?(?=# TOOL 5: PREPARE_ESCALATION)', new_sla + "\n\n", content)

with open("backend/app/tools.py", "w") as f:
    f.write(content)
