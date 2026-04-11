import os
import time
from itertools import cycle
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Ensure absolute path for .env loading
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
env_path = os.path.join(backend_dir, ".env")
load_dotenv(env_path)

def get_keys():
    """Dynamically load keys from environment."""
    keys = [
        os.getenv("GEMINI_API_KEY_1"),
        os.getenv("GEMINI_API_KEY_2"),
        os.getenv("GEMINI_API_KEY_3"),
    ]
    return [k for k in keys if k and len(str(k)) > 10]

def call_gemini(prompt: str) -> str:
    """
    Safe Gemini call using the modern google-genai SDK.
    Rotates across API keys on 429 quota errors.
    """
    keys = get_keys()
    if not keys:
        return f"Error: No valid Gemini API keys found in {env_path}."

    key_cycle = cycle(keys)

    for _ in range(len(keys)):
        key = next(key_cycle)
        try:
            client = genai.Client(api_key=key)
            
            # Using gemini-2.0-flash which was verified in models.list()
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=4096,
                    temperature=0.1,
                ),
            )
            return response.text or ""
        except Exception as e:
            err = str(e)
            print(f"Gemini API Error with key {key[:10]}...: {err}")
            if "429" in err or "quota" in err.lower() or "RESOURCE_EXHAUSTED" in err:
                time.sleep(1)
                continue
            raise e

    return "Error: All Gemini API keys exhausted or rate limited."
