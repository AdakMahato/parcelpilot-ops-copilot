import re
with open("backend/app/llm/gemini_provider.py", "r") as f:
    content = f.read()

import_stmt = "\nfrom app.db_logger import log_activity\n"
if "log_activity" not in content:
    content = content.replace("from app.tools import", import_stmt + "from app.tools import")

# Replace tool execution block
old_tool_exec = """                    if tool_name == "document_search":
                        result = document_search(**args)
                        for r in result:
                            src = r.get("metadata", {})
                            sources_used.append({
                                "document": src.get("document"),
                                "authority_level": src.get("authority_level"),
                                "status": src.get("status")
                            })
                    elif tool_name == "operational_data_lookup":
                        result = operational_data_lookup(**args, auth_context=auth_context)
                    elif tool_name == "sla_calculator":
                        result = sla_calculator(**args)
                    elif tool_name == "prepare_escalation":
                        result = prepare_escalation(**args)
                    else:
                        result = {"error": "Unknown tool"}"""

new_tool_exec = """                    if tool_name == "document_search":
                        result = document_search(**args)
                        for r in result:
                            src = r.get("metadata", {})
                            doc_name = src.get("document", "Unknown Document")
                            sources_used.append({
                                "document": doc_name,
                                "authority_level": src.get("authority_level"),
                                "status": src.get("status")
                            })
                            log_activity("Document retrieval", f"Retrieved {doc_name}")
                    elif tool_name == "operational_data_lookup":
                        result = operational_data_lookup(**args, auth_context=auth_context)
                        entity_id = args.get('entity_id', 'Unknown')
                        log_activity("Operational lookup", f"Retrieved {entity_id}")
                    elif tool_name == "sla_calculator":
                        result = sla_calculator(**args)
                        log_activity("SLA calculation", f"Calculated SLA for {args.get('ticket_id')}")
                    elif tool_name == "prepare_escalation":
                        result = prepare_escalation(**args)
                        log_activity("Escalation prep", f"Prepared escalation for {args.get('ticket_id')}")
                    else:
                        result = {"error": "Unknown tool"}"""

content = content.replace(old_tool_exec, new_tool_exec)

# Add success log at the end of function
old_ret = """                return {
                    "response": response.text,
                    "tool_activity": tool_activity,
                    "sources_used": unique_sources
                }"""

new_ret = """                log_activity("Agent completed", "Answer generated successfully")
                return {
                    "response": response.text,
                    "tool_activity": tool_activity,
                    "sources_used": unique_sources
                }"""

content = content.replace(old_ret, new_ret)

with open("backend/app/llm/gemini_provider.py", "w") as f:
    f.write(content)
