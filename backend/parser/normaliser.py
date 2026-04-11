import json
from agent.gemini_client import call_gemini

CATEGORIES = [
    "Food & Dining", "Transport", "Shopping", "Entertainment",
    "Utilities", "Healthcare", "Rent", "Salary/Income",
    "Investment", "ATM/Cash", "Transfer", "EMI/Loan", "Other"
]

def normalise_transactions(raw_transactions: list[dict]) -> list[dict]:
    """
    Use Gemini to categorise and clean raw transaction records.
    Returns a list of normalised transactions with category assigned.
    """
    if not raw_transactions:
        return []

    sample = raw_transactions[:30]  # Process in chunks to stay within token limits
    prompt = f"""
You are a bank statement parser. Given these raw transactions, return ONLY a valid JSON array.
Each object must have: date (string), name (string), amount (float, negative=expense), category (one of: {', '.join(CATEGORIES)}).
Do not include any explanation or markdown. Only return the JSON array.

Raw transactions:
{json.dumps(sample, indent=2)}
"""
    response = call_gemini(prompt)
    
    try:
        cleaned = response.strip().replace("```json", "").replace("```", "")
        normalised = json.loads(cleaned)
        return normalised
    except json.JSONDecodeError:
        # Fallback: return raw with "Other" category
        return [{"date": t["date"], "name": t["description"], 
                 "amount": t["amount"], "category": "Other"} for t in sample]

def extract_from_text(raw_text: str) -> list[dict]:
    """
    Use Gemini to extract structured transactions from unstructured PDF text.
    """
    prompt = f"""
You are a bank statement extractor. Extract all transactions from the following text and return them as a JSON array.
Each object should have: date, description, amount (negative for debit, positive for credit).
Only return the JSON array. No explanation.

Text:
{raw_text[:4000]} # Limit text length for token safety
"""
    response = call_gemini(prompt)
    try:
        cleaned = response.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned)
    except:
        return []
