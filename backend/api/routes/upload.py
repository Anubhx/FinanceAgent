from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from parser.pdf_parser import unlock_and_extract_text
from parser.csv_parser import parse_csv
from parser.normaliser import normalise_transactions, extract_from_text
from db.sqlite_store import store_transactions, log_upload, upsert_user

router = APIRouter()

@router.post("/upload")
async def upload_statement(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    password: str = Form(default=""),  # Optional — never stored after use
):
    upsert_user(user_id)
    content = await file.read()
    filename = file.filename or "upload"
    
    try:
        if filename.lower().endswith(".pdf"):
            raw_text = unlock_and_extract_text(content, password or None)
            # Use Gemini to extract transactions from unstructured text
            raw_transactions = extract_from_text(raw_text)
            file_type = "pdf"
        elif filename.lower().endswith(".csv"):
            raw_transactions = parse_csv(content)
            file_type = "csv"
        else:
            raise HTTPException(status_code=400, detail="Only PDF and CSV files are supported.")
        
        normalised = normalise_transactions(raw_transactions)
        store_transactions(user_id, normalised, source=filename)
        log_upload(user_id, filename, file_type, len(normalised))
        
        return {
            "success": True,
            "transactions_parsed": len(normalised),
            "message": f"Successfully parsed {len(normalised)} transactions from {filename}."
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))  # e.g. Wrong password
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parse error: {str(e)}")
