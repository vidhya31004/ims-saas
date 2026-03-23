from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database import Base


class Asset(Base):

    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    business_id = Column(UUID(as_uuid=True))

    asset_code = Column(String, unique=True)
    asset_name = Column(String)

    category = Column(String)
    location = Column(String)
    department = Column(String)

    purchase_date = Column(String)
    purchase_cost = Column(Float)
    expected_life = Column(Integer)

    daily_operating_hours = Column(Integer)
    hourly_run_cost = Column(Float)

    maintenance_threshold = Column(Integer)
