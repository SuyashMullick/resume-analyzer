from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .app.routers import match, upload  # Import your routers here

app = FastAPI()

# Allow React dev server to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Smart Resume Analyzer API is running."}

# Register endpoints via routers
app.include_router(upload.router)
app.include_router(match.router)
