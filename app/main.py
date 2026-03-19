from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers.asset_router import router as asset_router
from app.routers.dashboard_router import router as dashboard_router


app = FastAPI()


# CORS (so frontend can talk to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Include routers
app.include_router(asset_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {"message": "IMS API Running"}
