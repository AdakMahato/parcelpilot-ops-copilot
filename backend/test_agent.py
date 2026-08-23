from app.llm.gemini_provider import GeminiProvider
import os

print(f"API_KEY present: {bool(os.getenv('GEMINI_API_KEY'))}")
provider = GeminiProvider()
res = provider.generate_with_tools(
    system_prompt="Test",
    user_message="Reply with exactly: ParcelPilot test successful.",
    tools_schema=[],
    auth_context={}
)
print("Result:", res)
