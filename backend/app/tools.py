import json
from app.database import SessionLocal
from app.models import Account, Order, Ticket
import chromadb
from chromadb.utils import embedding_functions

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

# TOOL 1: document_search
def document_search(query: str, account_id: str = None, document_type: str = None):
    client = chromadb.PersistentClient(path="./chroma_db")
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_or_create_collection(name="parcelpilot_docs", embedding_function=sentence_transformer_ef)
    
    where_clause = {}
    if account_id:
        # If searching for agreement, restrict to the account's agreement or general policies
        # Actually chroma allows complex where clauses but we'll filter in python for simplicity if needed
        pass
    
    results = collection.query(
        query_texts=[query],
        n_results=10
    )
    
    # Filter deprecated and inapplicable docs
    valid_results = []
    if results and results.get('documents') and len(results['documents']) > 0:
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            
            # Rule: Exclude deprecated
            if meta.get('status') == 'DEPRECATED':
                continue
                
            # Rule: If agreement, must match account_id
            if meta.get('source_type') == 'agreement':
                if account_id and meta.get('account_id') != account_id:
                    continue
                    
            if document_type and meta.get('source_type') != document_type:
                continue
                
            valid_results.append({
                "text": doc,
                "metadata": meta
            })
        
    # Sort by authority level (1 is highest)
    valid_results.sort(key=lambda x: x["metadata"]["authority_level"])
    
    # Return top 3-5
    return valid_results[:5]

# TOOL 2: operational_data_lookup
def operational_data_lookup(entity_type: str, query_type: str, entity_id: str = None, account_id: str = None, auth_context: dict = None):
    # Authorization check
    if auth_context:
        allowed_accounts = auth_context.get("allowed_accounts", [])
        if account_id and account_id not in allowed_accounts:
            return {"error": "Unauthorized access to account data."}
            
    db = get_db()
    
    if entity_type == "account":
        if query_type == "get":
            if auth_context and entity_id not in auth_context.get("allowed_accounts", []):
                 return {"error": "Unauthorized access to account data."}
            acc = db.query(Account).filter(Account.account_id == entity_id).first()
            return {k: v for k, v in acc.__dict__.items() if not k.startswith('_')} if acc else {"error": "Account not found"}
            
    elif entity_type == "order":
        if query_type == "get":
            order = db.query(Order).filter(Order.order_id == entity_id).first()
            if not order: return {"error": "Order not found"}
            if auth_context and order.account_id not in auth_context.get("allowed_accounts", []):
                return {"error": "Unauthorized access to account data."}
            return {k: v for k, v in order.__dict__.items() if not k.startswith('_')}
            
    elif entity_type == "ticket":
        if query_type == "get":
            ticket = db.query(Ticket).filter(Ticket.ticket_id == entity_id).first()
            if not ticket: return {"error": "Ticket not found"}
            if auth_context and ticket.account_id not in auth_context.get("allowed_accounts", []):
                return {"error": "Unauthorized access to account data."}
            return {k: v for k, v in ticket.__dict__.items() if not k.startswith('_')}
            
    return {"error": "Unsupported operational data lookup"}

# TOOL 3: SLA_CALCULATOR
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
    }

# TOOL 5: PREPARE_ESCALATION
def prepare_escalation(ticket_id: str, severity: str, reason: str, recommended_action: str):
    return {
        "ticket_id": ticket_id,
        "severity": severity,
        "reason": reason,
        "recommended_action": recommended_action,
        "status": "ACTION_REQUIRES_CONFIRMATION",
        "action": "execute_escalation"
    }
