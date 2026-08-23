import os
import json
from openai import OpenAI
from app.tools import document_search, operational_data_lookup, sla_calculator, prepare_escalation

class OpsAgent:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "gpt-4o")

    def run(self, user_message: str, auth_context: dict):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "document_search",
                    "description": "Search policies, agreements, SOPs, and product docs.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "account_id": {"type": "string"},
                            "document_type": {"type": "string", "enum": ["policy", "sop", "product_docs", "agreement"]}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "operational_data_lookup",
                    "description": "Query accounts, orders, and tickets.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "entity_type": {"type": "string", "enum": ["account", "order", "ticket"]},
                            "query_type": {"type": "string", "enum": ["get"]},
                            "entity_id": {"type": "string"},
                            "account_id": {"type": "string"}
                        },
                        "required": ["entity_type", "query_type", "entity_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "sla_calculator",
                    "description": "Calculate SLA deterministically for a ticket.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ticket_id": {"type": "string"}
                        },
                        "required": ["ticket_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "prepare_escalation",
                    "description": "Prepare a ticket escalation (does not immediately change state).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ticket_id": {"type": "string"},
                            "severity": {"type": "string"},
                            "reason": {"type": "string"},
                            "recommended_action": {"type": "string"}
                        },
                        "required": ["ticket_id", "severity", "reason", "recommended_action"]
                    }
                }
            }
        ]
        
        system_prompt = (
            "You are the ParcelPilot Ops Copilot. "
            "You help authorized users with support issues, SLAs, and escalations. "
            "IMPORTANT RULES: "
            "1. NEVER invent facts. If missing info, state INSUFFICIENT_DATA. "
            "2. State-changing actions require CONFIRMATION. "
            "3. Format your response cleanly using Markdown. DO NOT output raw JSON to the user except for tool calls. "
            "4. Resolve conflicts using source authority: 1 (Agreements) > 2 (Current Policies/SOP) > 3 (Product Docs) > 4 (History). "
            "5. Include an 'Evidence' and 'Sources' section in your response text explicitly."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        tool_activity = []
        sources_used = []

        for _ in range(5):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            msg = response.choices[0].message
            messages.append(msg)
            
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    args = json.loads(tool_call.function.arguments)
                    tool_activity.append({"tool": tool_call.function.name, "args": args})
                    
                    if tool_call.function.name == "document_search":
                        result = document_search(**args)
                        for r in result:
                            src = r.get("metadata", {})
                            sources_used.append({
                                "document": src.get("document"),
                                "authority_level": src.get("authority_level"),
                                "status": src.get("status")
                            })
                    elif tool_call.function.name == "operational_data_lookup":
                        result = operational_data_lookup(**args, auth_context=auth_context)
                    elif tool_call.function.name == "sla_calculator":
                        result = sla_calculator(**args)
                    elif tool_call.function.name == "prepare_escalation":
                        result = prepare_escalation(**args)
                    else:
                        result = {"error": "Unknown tool"}
                        
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": json.dumps(result)
                    })
            else:
                # Remove duplicates in sources
                unique_sources = []
                seen = set()
                for s in sources_used:
                    if s["document"] not in seen:
                        seen.add(s["document"])
                        unique_sources.append(s)
                        
                return {
                    "response": msg.content,
                    "tool_activity": tool_activity,
                    "sources_used": unique_sources
                }

        return {
            "response": "Error: Agent reached maximum steps.",
            "tool_activity": tool_activity,
            "sources_used": []
        }

