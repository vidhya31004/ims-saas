from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.asset_schema import AssetCreate
from models.asset import Asset

router = APIRouter()


@router.post("/assets")
def create_asset(asset: AssetCreate, business_id: str, db: Session = Depends(get_db)):

    new_asset = Asset(
        business_id=business_id,
        asset_code=asset.asset_code,
        asset_name=asset.asset_name,
        category=asset.category,
        location=asset.location,
        department=asset.department,
        daily_operating_hours=asset.daily_operating_hours,
        hourly_run_cost=asset.hourly_run_cost,
        maintenance_threshold=asset.maintenance_threshold
    )

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset


@router.get("/assets")
def get_assets(business_id: str, db: Session = Depends(get_db)):

    return db.query(Asset).filter(Asset.business_id == business_id).all()
