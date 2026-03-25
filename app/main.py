from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers.asset_router import router as asset_router
from routers.dashboard_router import router as dashboard_router


# ✅ FIRST create app
app = FastAPI()


# ✅ THEN middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ THEN DB
Base.metadata.create_all(bind=engine)


# ✅ THEN routers (AFTER app is defined)
app.include_router(asset_router)
app.include_router(dashboard_router)


# ✅ THEN routes
@app.get("/")
def root():
    return {"message": "IMS API Running"}
