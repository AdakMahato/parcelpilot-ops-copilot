from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from app.agent import OpsAgent
from app.database import engine, SessionLocal
from app.models import Base, ActivityLog
from fastapi.middleware.cors import CORSMiddleware
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ParcelPilot Ops Copilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    
class ActionConfirmRequest(BaseModel):
    action: str
    payload: dict

def get_auth_context(x_user_role: str = Header("support_agent"), x_allowed_accounts: str = Header("ACCT-001,ACCT-002,ACCT-003,ACCT-004")):
    return {
        "role": x_user_role,
        "allowed_accounts": [acc.strip() for acc in x_allowed_accounts.split(",")]
    }

@app.get("/api/health")
def health_check():
    db_ok = os.path.exists("./parcelpilot.db")
    docs_ok = os.path.exists("./chroma_db")
    agent_ok = bool(os.getenv("GEMINI_API_KEY"))
    return {
        "status": "ok" if (db_ok and docs_ok and agent_ok) else "degraded",
        "llm_provider": "gemini",
        "llm_available": agent_ok,
        "database": db_ok,
        "documents": docs_ok
    }

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest, auth=Depends(get_auth_context)):
    try:
        agent = OpsAgent()
        result = agent.run(req.message, auth_context=auth)
        
        # Check if the result was a dict indicating a quota error
        if isinstance(result, dict) and result.get("type") == "llm_unavailable":
            return result

        if isinstance(result, str):
            return {"response": result, "tool_activity": [], "sources_used": []}
        return result
    except Exception as e:
        print("CHAT ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/action/confirm")
def confirm_action_endpoint(req: ActionConfirmRequest, auth=Depends(get_auth_context)):
    if auth["role"] == "read_only_analyst":
        raise HTTPException(status_code=403, detail="Analysts cannot execute state-changing actions.")
        
    if req.action == "execute_escalation":
        return {"status": "success", "message": f"Escalated ticket {req.payload.get('ticket_id', 'unknown')} successfully."}
    
    raise HTTPException(status_code=400, detail="Unknown action")

@app.get("/api/dashboard")
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
@app.get("/api/tickets")
def get_tickets(auth=Depends(get_auth_context)):
    db = SessionLocal()
    from app.models import Ticket
    tickets = db.query(Ticket).all()
    # Apply basic auth filtering if needed
    if auth["allowed_accounts"] and "all" not in auth["allowed_accounts"]:
        tickets = [t for t in tickets if t.account_id in auth["allowed_accounts"] or "all" in auth["allowed_accounts"]]
    return [{k:v for k,v in t.__dict__.items() if k != '_sa_instance_state'} for t in tickets]

@app.get("/api/tickets/{ticket_id}")
def get_ticket(ticket_id: str, auth=Depends(get_auth_context)):
    db = SessionLocal()
    from app.models import Ticket
    t = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {k:v for k,v in t.__dict__.items() if k != '_sa_instance_state'}

@app.get("/api/orders")
def get_orders(auth=Depends(get_auth_context)):
    db = SessionLocal()
    from app.models import Order
    orders = db.query(Order).all()
    if auth["allowed_accounts"] and "all" not in auth["allowed_accounts"]:
        orders = [o for o in orders if o.account_id in auth["allowed_accounts"] or "all" in auth["allowed_accounts"]]
    return [{k:v for k,v in o.__dict__.items() if k != '_sa_instance_state'} for o in orders]

@app.get("/api/accounts")
def get_accounts(auth=Depends(get_auth_context)):
    db = SessionLocal()
    from app.models import Account
    accounts = db.query(Account).all()
    if auth["allowed_accounts"] and "all" not in auth["allowed_accounts"]:
        accounts = [a for a in accounts if a.account_id in auth["allowed_accounts"] or "all" in auth["allowed_accounts"]]
    return [{k:v for k,v in a.__dict__.items() if k != '_sa_instance_state'} for a in accounts]


@app.get("/api/activity")
def get_activity_log(auth=Depends(get_auth_context)):
    db = SessionLocal()
    try:
        logs = db.query(ActivityLog).order_by(ActivityLog.id.desc()).limit(50).all()
        return [
            {
                "id": log.id,
                "timestamp": log.timestamp,
                "event_type": log.event_type,
                "description": log.description,
                "actor": log.actor
            } for log in logs
        ]
    finally:
        db.close()
