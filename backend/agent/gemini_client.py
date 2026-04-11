import os
import time
from itertools import cycle
from google import genai
from google.genai import types

# Load keys from environment
keys = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
]
keys = [k for k in keys if k]  # filter out empty/missing keys

if not keys:
    _key_cycle = cycle(["PLACEHOLDER_KEY"])
else:
    _key_cycle = cycle(keys)


def _make_client() -> genai.Client:
    """Create a new google.genai Client with the next rotated key."""
    key = next(_key_cycle)
    return genai.Client(api_key=key)


def call_gemini(prompt: str) -> str:
    """
    Safe Gemini call using the modern google-genai SDK.
    Rotates across API keys on 429 quota errors.
    Uses gemini-2.5-flash as requested in AGENT.md.
    """
    if not keys:
        return "Error: No Gemini API keys provided in .env."

    for attempt in range(len(keys)):
        try:
            client = _make_client()
            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-04-17",
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=1024,
                    temperature=0.3,
                    thinking_config=types.ThinkingConfig(thinking_budget=0),
                ),
            )
            return response.text or ""
        except Exception as e:
            err = str(e)
            if "429" in err or "quota" in err.lower() or "RESOURCE_EXHAUSTED" in err:
                time.sleep(2)
                continue
            raise e

    return "Error: All Gemini API keys exhausted or rate limited."
