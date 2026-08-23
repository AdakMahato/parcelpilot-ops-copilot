from typing import Protocol, List, Dict, Any

class LLMProvider(Protocol):
    def generate_with_tools(self, system_prompt: str, user_message: str, tools: List[Dict[str, Any]], auth_context: dict) -> dict:
        ...
