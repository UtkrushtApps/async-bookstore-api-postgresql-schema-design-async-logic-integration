from fastapi import FastAPI
from app.routes import api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Bookstore API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(api.router)
