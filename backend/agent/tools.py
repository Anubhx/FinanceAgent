from langchain.tools import tool
from db.sqlite_store import get_user_transactions
from agent.gemini_client import call_gemini
import json

@tool
def get_spending_summary(user_id: str) -> str:
    """Summarise a user's spending by category from their stored transactions.
    
    Args:
        user_id: The unique ID of the user.
    """
    transactions = get_user_transactions(user_id, limit=100)
    if not transactions:
        return "No transactions found. Ask the user to upload a bank statement."
    
    by_category = {}
    for t in transactions:
        cat = t["category"]
        by_category[cat] = by_category.get(cat, 0) + abs(t["amount"])
    
    lines = [f"- {cat}: ₹{amt:,.0f}" for cat, amt in sorted(by_category.items(), key=lambda x: -x[1])]
    return "Spending by category:\n" + "\n".join(lines)

@tool
def detect_anomalies(user_id: str) -> str:
    """Detect unusually large or suspicious transactions for the user.
    
    Args:
        user_id: The unique ID of the user.
    """
    transactions = get_user_transactions(user_id, limit=100)
    if not transactions:
        return "No transactions to analyse."
    
    expenses = [t for t in transactions if t["amount"] < 0]
    if not expenses:
        return "No expense transactions found."
    
    amounts = [abs(t["amount"]) for t in expenses]
    mean = sum(amounts) / len(amounts)
    std = (sum((a - mean)**2 for a in amounts) / len(amounts)) ** 0.5
    threshold = mean + 2 * std
    
    flagged = [t for t in expenses if abs(t["amount"]) > threshold]
    if not flagged:
        return "No anomalies detected. All transactions look normal."
    
    lines = [f"- {t['date']} | {t['name']} | ₹{abs(t['amount']):,.0f}" for t in flagged]
    return f"⚠️ Flagged {len(flagged)} unusual transactions (threshold ₹{threshold:,.0f}):\n" + "\n".join(lines)

@tool
def generate_savings_plan(user_id: str) -> str:
    """Generate a personalised savings plan based on the user's spending patterns.
    
    Args:
        user_id: The unique ID of the user.
    """
    transactions = get_user_transactions(user_id, limit=100)
    if not transactions:
        return "No transaction data available to create a savings plan."
    
    income = sum(t["amount"] for t in transactions if t["amount"] > 0)
    expenses = sum(abs(t["amount"]) for t in transactions if t["amount"] < 0)
    
    by_category = {}
    for t in transactions:
        if t["amount"] < 0:
            cat = t["category"]
            by_category[cat] = by_category.get(cat, 0) + abs(t["amount"])
    
    top_3 = sorted(by_category.items(), key=lambda x: -x[1])[:3]
    top_str = ", ".join([f"{c} (₹{a:,.0f})" for c, a in top_3])
    
    prompt = f"""
You are a personal finance advisor for a young Indian professional.
Income this period: ₹{income:,.0f}
Total expenses: ₹{expenses:,.0f}
Net savings: ₹{income - expenses:,.0f}
Top spending categories: {top_str}

Give a concise, actionable savings plan in 4-5 bullet points. Be specific with amounts. 
Keep it under 200 words. No markdown headers.
"""
    return call_gemini(prompt)

@tool
def answer_finance_question(question: str, user_id: str) -> str:
    """Answer a general personal finance question using Gemini.
    
    Args:
        question: The financial question from the user.
        user_id: The unique ID of the user.
    """
    transactions = get_user_transactions(user_id, limit=20)
    context = json.dumps(transactions[:10], indent=2) if transactions else "No transactions uploaded yet."
    
    prompt = f"""
You are a personal finance assistant for a young Indian professional.
User's recent transactions context:
{context}

Answer this question concisely and practically:
{question}

Keep response under 150 words.
"""
    return call_gemini(prompt)
