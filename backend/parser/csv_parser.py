import pandas as pd
import io

def parse_csv(csv_bytes: bytes) -> list[dict]:
    """
    Parse a bank statement CSV into a list of raw transaction dicts.
    Handles common Indian bank CSV formats (SBI, HDFC, ICICI patterns).
    """
    df = pd.read_csv(io.BytesIO(csv_bytes), encoding="utf-8", on_bad_lines="skip")
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    
    # Try to find common column name patterns
    date_col = next((c for c in df.columns if "date" in c), None)
    desc_col = next((c for c in df.columns if any(x in c for x in ["narration", "description", "particulars", "remarks"])), None)
    debit_col = next((c for c in df.columns if "debit" in c or "withdrawal" in c), None)
    credit_col = next((c for c in df.columns if "credit" in c or "deposit" in c), None)
    amount_col = next((c for c in df.columns if "amount" in c), None)

    records = []
    for _, row in df.iterrows():
        amount = 0.0
        if debit_col and pd.notna(row.get(debit_col)):
            try:
                amount = -float(str(row[debit_col]).replace(",", ""))
            except: pass
        elif credit_col and pd.notna(row.get(credit_col)):
            try:
                amount = float(str(row[credit_col]).replace(",", ""))
            except: pass
        elif amount_col:
            try:
                amount = float(str(row[amount_col]).replace(",", ""))
            except: pass

        records.append({
            "date": str(row.get(date_col, "Unknown")),
            "description": str(row.get(desc_col, "Unknown")),
            "amount": amount,
        })
    return [r for r in records if r["amount"] != 0.0]
