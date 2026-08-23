import os
import json
import time
import random
from google import genai
from google.genai import types

from app.db_logger import log_activity
from app.tools import document_search, operational_data_lookup, sla_calculator, prepare_escalation

class GeminiProvider:
    def __init__(self, api_key=None, model=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is missing.")
        self.client = genai.Client(api_key=self.api_key)
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-3.7-flash")

    def _send_with_retry(self, chat, payload):
        max_retries = 3
        delays = [1.0, 2.0, 4.0]
        
        for attempt in range(max_retries + 1):
            try:
                return chat.send_message(payload)
            except Exception as e:
                err_str = str(e).lower()
                status_code = getattr(e, 'code', getattr(e, 'status_code', 'unknown'))
                print(f"Gemini API Error (Attempt {attempt+1}): HTTP {status_code} - {e}")
                
                
                # Log to a local file so the sandbox can read it
                with open("gemini_error.txt", "w") as f_err:
                    f_err.write(f"HTTP Status: {status_code}\nError: {e}\n")
                    
                # If daily quota is exhausted
                if ("quota" in err_str and "exceeded" in err_str) or "exhausted" in err_str:
                    return {"type": "llm_unavailable", "recoverable": True, "response": "Gemini quota has been reached. Please try again later."}
                
                # Check for transient rate limit (429 but not quota) or overloaded (503)
                if "429" in err_str or "503" in err_str or "overloaded" in err_str or "unavailable" in err_str:
                    if attempt < max_retries:
                        sleep_time = delays[attempt] + random.uniform(0, 0.5)
                        print(f"Retrying in {sleep_time:.2f} seconds...")
                        time.sleep(sleep_time)
                        continue
                    else:
                        return {"type": "llm_unavailable", "recoverable": True, "response": "Gemini is temporarily unavailable. Please try again in a moment."}
                        
                # Any other error, raise it
                raise e

    def generate_with_tools(self, system_prompt: str, user_message: str, tools_schema: list, auth_context: dict) -> dict:
        gemini_tools = []
        for t in tools_schema:
            fn = t["function"]
            gemini_tools.append(
                types.Tool(
                    function_declarations=[
                        types.FunctionDeclaration(
                            name=fn["name"],
                            description=fn["description"],
                            parameters=fn["parameters"]
                        )
                    ]
                )
            )

        chat = self.client.chats.create(
            model=self.model,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.0,
                tools=gemini_tools
            )
        )
        
        tool_activity = []
        sources_used = []
        
        response = self._send_with_retry(chat, user_message)
        if isinstance(response, dict) and response.get("type") == "llm_unavailable":
            return response

        for _ in range(5):
            if response.function_calls:
                parts_to_return = []
                for tool_call in response.function_calls:
                    tool_name = tool_call.name
                    args = tool_call.args
                    tool_activity.append({"tool": tool_name, "args": args})
                    
                    if tool_name == "document_search":
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
                        result = {"error": "Unknown tool"}
                        
                    if not isinstance(result, dict):
                        result = {"result": result}
                        
                    parts_to_return.append(
                        types.Part.from_function_response(
                            name=tool_name,
                            response=result
                        )
                    )
                
                response = self._send_with_retry(chat, parts_to_return)
                if isinstance(response, dict) and response.get("type") == "llm_unavailable":
                    return response
            else:
                unique_sources = []
                seen = set()
                for s in sources_used:
                    if s["document"] not in seen:
                        seen.add(s["document"])
                        unique_sources.append(s)
                        
                log_activity("Agent completed", "Answer generated successfully")
                return {
                    "response": response.text,
                    "tool_activity": tool_activity,
                    "sources_used": unique_sources
                }

        return {
            "response": "Error: Agent reached maximum steps.",
            "tool_activity": tool_activity,
            "sources_used": []
        }
