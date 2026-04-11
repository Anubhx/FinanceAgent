import json
import re
from agent.gemini_client import call_gemini

CATEGORIES = [
    "Food & Dining", "Transport", "Shopping", "Entertainment",
    "Utilities", "Healthcare", "Rent", "Salary/Income",
    "Investment", "ATM/Cash", "Transfer", "EMI/Loan", "Other"
]

def _safe_parse_json(text: str) -> list:
    """Robustly parse a potentially truncated JSON array from a string."""
    cleaned = re.sub(r"```json\s*|```", "", text).strip()

    # Full parse first
    try:
        result = json.loads(cleaned)
        if isinstance(result, list):
            return result
    except json.JSONDecodeError:
        pass

    # Recover truncated array: find last complete object
    try:
        last_obj_end = cleaned.rfind("},")
        if last_obj_end == -1:
            last_obj_end = cleaned.rfind("}")
        if last_obj_end > 0:
            recovered = cleaned[:last_obj_end + 1] + "\n]"
            result = json.loads(recovered)
            if isinstance(result, list):
                return result
    except (json.JSONDecodeError, ValueError):
        pass

    return []


def normalise_transactions(raw_transactions: list[dict]) -> list[dict]:
    """Use Gemini to categorise and clean raw transaction records."""
    if not raw_transactions:
        return []

    sample = raw_transactions[:30]
    prompt = f"""Categorize these bank transactions. Return ONLY a JSON array.
Each item must have: date (string), name (string), amount (float, negative=expense), category (one of: {', '.join(CATEGORIES)}).
No explanation, no markdown.

Transactions:
{json.dumps(sample, indent=2)}
"""
    response = call_gemini(prompt)
    result = _safe_parse_json(response)

    if result:
        return result

    # Fallback: passthrough with "Other" category
    return [{"date": t.get("date", ""), "name": t.get("description", t.get("name", "")),
             "amount": t.get("amount", 0), "category": "Other"} for t in sample]


def extract_from_text(raw_text: str) -> list[dict]:
    """
    Use Gemini to extract structured transactions from unstructured PDF text.
    Uses two-pass extraction to handle large statements.
    """
    all_transactions = []
    chunk_size = 2500  # ~600 tokens, well within limits
    chunks = [raw_text[i:i+chunk_size] for i in range(0, min(len(raw_text), 10000), chunk_size)]

    for chunk in chunks:
        prompt = f"""Extract bank transactions from this text. Return ONLY a JSON array.
Each item: date (string), description (string), amount (float, negative=debit, positive=credit).
No explanation, no markdown fences.

Text:
{chunk}
"""
        response = call_gemini(prompt)
        transactions = _safe_parse_json(response)
        all_transactions.extend(transactions)

    # Deduplicate by (date, description, amount)
    seen = set()
    unique = []
    for t in all_transactions:
        key = (t.get("date"), t.get("description"), t.get("amount"))
        if key not in seen:
            seen.add(key)
            unique.append(t)

    return unique
