import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key present: {bool(api_key)}")
if api_key:
    print(f"API Key prefix: {api_key[:5]}...")

try:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-3.7-flash',
        contents='Reply with exactly: ParcelPilot test successful.'
    )
    print("Response:", response.text)
except Exception as e:
    print("Error:", type(e).__name__)
    print("Error details:", str(e))
    import traceback
    traceback.print_exc()
