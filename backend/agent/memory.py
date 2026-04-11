import os
from mem0 import Memory

# Configuration for Mem0 with Pinecone and Gemini
config = {
    "vector_store": {
        "provider": "pinecone",
        "config": {
            "api_key": os.getenv("PINECONE_API_KEY"),
            "environment": os.getenv("PINECONE_ENV", "us-east-1"),
            "index_name": os.getenv("PINECONE_INDEX_NAME", "finance-agent-memory"),
            "dimension": 768,  # Gemini embedding dimension
        },
    },
    "llm": {
        "provider": "google",
        "config": {
            "model": "gemini-1.5-flash", # Using 1.5-flash as 2.5 is not stable/available
            "api_key": os.getenv("GEMINI_API_KEY_1"),
        },
    },
    "embedder": {
        "provider": "google",
        "config": {
            "model": "models/embedding-001",
            "api_key": os.getenv("GEMINI_API_KEY_1"),
        },
    },
}

# Lazy initialization to avoid crash if env vars are missing during setup
_memory = None

def get_memory_client():
    global _memory
    if _memory is None:
        _memory = Memory.from_config(config)
    return _memory

def save_memory(user_id: str, content: str) -> None:
    """Save a conversation turn or fact to the user's persistent memory."""
    try:
        mem = get_memory_client()
        mem.add(content, user_id=user_id)
    except Exception as e:
        print(f"Memory save error: {e}")

def get_memories(user_id: str, query: str) -> str:
    """Retrieve top-5 relevant memories for a user given the current query."""
    try:
        mem = get_memory_client()
        results = mem.search(query, user_id=user_id, limit=5)
        if not results:
            return "No prior context found."
        return "\n".join([r["memory"] for r in results])
    except Exception as e:
        print(f"Memory retrieval error: {e}")
        return "Memory retrieval unavailable."
