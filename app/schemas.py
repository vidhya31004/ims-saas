from pydantic import BaseModel
from typing import Optional
from datetime import date


class BusinessSignup(BaseModel):
    business_name: str
    owner_name: str
    owner_email: str
    owner_password: str


class LoginRequest(BaseModel):
    email: str
    password: str

class AssetCreate(BaseModel):
    asset_code: str
    asset_name: str
    category: str
    location: str
    department: str
    daily_operating_hours: int
    hourly_run_cost: float
    maintenance_threshold: int

class UsageLogCreate(BaseModel):

    asset_id: str
    date: date
    hours_used: float

    operator: Optional[str] = None
    notes: Optional[str] = None
