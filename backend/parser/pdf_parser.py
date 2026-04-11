import pikepdf
import fitz  # PyMuPDF
import tempfile
import os

def unlock_and_extract_text(pdf_bytes: bytes, password: str | None = None) -> str:
    """
    Unlock a password-protected PDF and extract raw text.
    Password is used only in-memory and never persisted.
    
    Args:
        pdf_bytes: Raw PDF file content
        password: Optional password string (can be None for unlocked PDFs)
    
    Returns:
        Full extracted text as a string
    """
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    unlocked_path = tmp_path + "_unlocked.pdf"

    try:
        # Step 1: Unlock with pikepdf if password provided
        if password:
            with pikepdf.open(tmp_path, password=password) as pdf:
                pdf.save(unlocked_path)
            read_path = unlocked_path
        else:
            read_path = tmp_path

        # Step 2: Extract text with PyMuPDF
        doc = fitz.open(read_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        return full_text.strip()

    except pikepdf.PasswordError:
        raise ValueError("Incorrect PDF password. Please try again.")
    except Exception as e:
        raise RuntimeError(f"PDF parsing failed: {str(e)}")
    finally:
        # Always clean up temp files — password never touches disk storage
        for path in [tmp_path, unlocked_path]:
            if os.path.exists(path):
                os.remove(path)
