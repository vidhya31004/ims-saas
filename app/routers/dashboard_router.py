from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.asset import Asset

router = APIRouter()


@router.get("/underutilized-assets")
def get_underutilized_assets(business_id: str, db: Session = Depends(get_db)):

    assets = db.query(Asset).filter(
        Asset.business_id == business_id
    ).all()

    underutilized = []

    for asset in assets:

        # Skip assets with no data
        if asset.daily_operating_hours is None:
            continue

        if asset.daily_operating_hours < 4:

            underutilized.append({
                "asset_code": asset.asset_code,
                "asset_name": asset.asset_name,
                "department": asset.department,
                "daily_operating_hours": asset.daily_operating_hours
            })

    return underutilized


@router.get("/maintenance-alerts")
def get_maintenance_alerts(business_id: str, db: Session = Depends(get_db)):

    assets = db.query(Asset).filter(
        Asset.business_id == business_id
    ).all()

    alerts = []

    for asset in assets:

        if asset.daily_operating_hours is None:
            continue

        if asset.maintenance_threshold is None:
            continue

        usage_score = asset.daily_operating_hours * 30

        if usage_score > asset.maintenance_threshold:

            alerts.append({
                "asset_code": asset.asset_code,
                "asset_name": asset.asset_name,
                "maintenance_threshold": asset.maintenance_threshold,
                "usage_score": usage_score
            })

    return alerts
