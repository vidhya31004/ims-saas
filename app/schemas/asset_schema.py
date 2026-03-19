from pydantic import BaseModel


class AssetCreate(BaseModel):

    asset_code: str
    asset_name: str
    category: str
    location: str
    department: str
    daily_operating_hours: int
    hourly_run_cost: float
    maintenance_threshold: int
