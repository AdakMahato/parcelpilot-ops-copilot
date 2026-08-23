import pytest
from app.tools import document_search, operational_data_lookup, sla_calculator, prepare_escalation

def test_document_retrieval_and_deprecation():
    # It should not return deprecated docs
    results = document_search("cancellation fee", account_id=None, document_type="policy")
    assert isinstance(results, list)
    for r in results:
        assert r["metadata"].get("status") != "DEPRECATED"

def test_document_agreement_precedence():
    # If account_id is provided, it should allow that account's agreement
    results = document_search("cancellation fee", account_id="ACCT-001", document_type="agreement")
    for r in results:
        assert r["metadata"].get("source_type") == "agreement"
        assert r["metadata"].get("account_id") == "ACCT-001"

def test_structured_data_lookup():
    # Test valid order lookup
    res = operational_data_lookup("order", "get", entity_id="ORD-1001")
    assert "error" not in res
    assert res["order_id"] == "ORD-1001"
    
def test_account_authorization():
    # Test auth rejection
    auth_ctx = {"role": "support_agent", "allowed_accounts": ["ACCT-001"]}
    res = operational_data_lookup("ticket", "get", entity_id="TKT-502", account_id=None, auth_context=auth_ctx)
    # TKT-502 belongs to ACCT-002, should be unauthorized
    assert "error" in res
    assert res["error"] == "Unauthorized access to account data."
    
def test_sla_calculation():
    # TKT-501 belongs to ACCT-001 (Northstar) which has Enterprise plan (Custom 2h SLA)
    res = sla_calculator("TKT-501")
    assert "error" not in res
    assert "2 hours" in res["target"]
    
def test_action_proposal():
    res = prepare_escalation("TKT-501", "High", "Needs product ops", "Escalate")
    assert res["status"] == "ACTION_REQUIRES_CONFIRMATION"
    assert res["action"] == "execute_escalation"

