from fastapi import FastAPI
from app.api.routes import router as api_router
from app.auth.auth_routes import router as auth_router
from app.core.database import engine  # ensures DB tables are created

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CoverCraft AI",
    description="Backend API for CoverCraft AI",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    print("Application is starting up...")

@app.get("/")
def health_check():
    return {"status": "Backend is running 🚀"}
