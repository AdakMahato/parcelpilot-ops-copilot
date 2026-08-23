import os
import json
from app.llm.gemini_provider import GeminiProvider
from app.db_logger import log_activity


class OpsAgent:
    def __init__(self):
        self.provider = GeminiProvider()

    def run(self, user_message: str, auth_context: dict):
        log_activity("Agent query", f"User query: {user_message}", actor=auth_context.get("role", "System"))

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
            "5. Structure your output exactly like this:\n\n"
            "### Answer\n"
            "[Clear, concise answer generated from the actual retrieved data and documents]\n\n"
            "### Analysis & Details\n"
            "[Bullet points explaining the policy vs agreement, statuses, etc]\n\n"
            "### Evidence\n"
            "[Nested bullet points of evidence from records and clauses]\n\n"
            "### Sources\n"
            "1. [actual document filename] (Authority Level X)\n"
            "2. [actual document filename] (Authority Level X)"
        )

        return self.provider.generate_with_tools(system_prompt, user_message, tools, auth_context)
