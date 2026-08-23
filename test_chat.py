import requests
import json

payload = {
    "message": "Can Northstar cancel ORD-1001 without a fee?",
    "history": []
}

headers = {
    "x-user-role": "support_agent",
    "x-allowed-accounts": "ACCT-001,ACCT-002,ACCT-003,ACCT-004"
}

try:
    res = requests.post("http://127.0.0.1:8000/api/chat", json=payload, headers=headers)
    print(json.dumps(res.json(), indent=2))
except Exception as e:
    print(e)
