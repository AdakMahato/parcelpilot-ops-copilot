import re

with open("backend/app/main.py", "r") as f:
    content = f.read()

endpoints = """
@app.get("/api/tickets")
def get_tickets(auth=Depends(get_auth_context)):
    db = SessionLocal()
    from app.models import Ticket
    tickets = db.query(Ticket).all()
    # Apply basic auth filtering if needed
    if auth["allowed_accounts"] and "all" not in auth["allowed_accounts"]:
        tickets = [t for t in tickets if t.account_id in auth["allowed_accounts"] or "all" in auth["allowed_accounts"]]
    return [t.__dict__ for t in tickets]

@app.get("/api/tickets/{ticket_id}")
def get_ticket(ticket_id: str, auth=Depends(get_auth_context)):
    db = SessionLocal()
    from app.models import Ticket
    t = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return t.__dict__

@app.get("/api/orders")
def get_orders(auth=Depends(get_auth_context)):
    db = SessionLocal()
    from app.models import Order
    orders = db.query(Order).all()
    if auth["allowed_accounts"] and "all" not in auth["allowed_accounts"]:
        orders = [o for o in orders if o.account_id in auth["allowed_accounts"] or "all" in auth["allowed_accounts"]]
    return [o.__dict__ for o in orders]

@app.get("/api/accounts")
def get_accounts(auth=Depends(get_auth_context)):
    db = SessionLocal()
    from app.models import Account
    accounts = db.query(Account).all()
    if auth["allowed_accounts"] and "all" not in auth["allowed_accounts"]:
        accounts = [a for a in accounts if a.account_id in auth["allowed_accounts"] or "all" in auth["allowed_accounts"]]
    return [a.__dict__ for a in accounts]
"""

content = content + "\n" + endpoints

# Because __dict__ has SQLAlchemy internal state _sa_instance_state, let's fix it by deleting it
content = content.replace("return [t.__dict__ for t in tickets]", "return [{k:v for k,v in t.__dict__.items() if k != '_sa_instance_state'} for t in tickets]")
content = content.replace("return t.__dict__", "return {k:v for k,v in t.__dict__.items() if k != '_sa_instance_state'}")
content = content.replace("return [o.__dict__ for o in orders]", "return [{k:v for k,v in o.__dict__.items() if k != '_sa_instance_state'} for o in orders]")
content = content.replace("return [a.__dict__ for a in accounts]", "return [{k:v for k,v in a.__dict__.items() if k != '_sa_instance_state'} for a in accounts]")

with open("backend/app/main.py", "w") as f:
    f.write(content)
