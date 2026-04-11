from fastapi import APIRouter, Query
from db.sqlite_store import get_user_transactions

router = APIRouter()

@router.get("/transactions")
async def get_transactions(user_id: str = Query(...), limit: int = 100):
    transactions = get_user_transactions(user_id, limit=limit)
    return transactions

@router.get("/summary")
async def get_summary(user_id: str = Query(...)):
    transactions = get_user_transactions(user_id, limit=1000)
    if not transactions:
        return {"total_expense": 0, "total_income": 0, "categories": {}}
    
    total_expense = sum(abs(t["amount"]) for t in transactions if t["amount"] < 0)
    total_income = sum(t["amount"] for t in transactions if t["amount"] > 0)
    
    categories = {}
    for t in transactions:
        if t["amount"] < 0:
            cat = t["category"]
            categories[cat] = categories.get(cat, 0) + abs(t["amount"])
            
    return {
        "total_expense": total_expense,
        "total_income": total_income,
        "categories": categories
    }
