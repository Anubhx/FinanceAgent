from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.chat import router as chat_router
from api.routes.upload import router as upload_router
from api.routes.transactions import router as transactions_router

app = FastAPI(title="FinanceAgent API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-vercel-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(chat_router, prefix="/api")
app.include_router(upload_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}
