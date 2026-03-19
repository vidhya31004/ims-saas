import uuid
from sqlalchemy import Column, String, Float, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


# BUSINESS TABLE
class Business(Base):
    __tablename__ = "businesses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="business")
    assets = relationship("Asset", back_populates="business")


# USERS TABLE
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"))

    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    role = Column(String)

    business = relationship("Business", back_populates="users")


# ASSETS TABLE
class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"))

    asset_code = Column(String, unique=True)
    asset_name = Column(String)

    category = Column(String)
    location = Column(String)
    department = Column(String)

    purchase_date = Column(Date)
    purchase_cost = Column(Float)

    expected_life = Column(Float)

    daily_operating_hours = Column(Float)
    hourly_run_cost = Column(Float)

    maintenance_threshold = Column(Float)

    business = relationship("Business", back_populates="assets")
    usage_logs = relationship("UsageLog", back_populates="asset")


# USAGE LOG TABLE
class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"))
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"))

    date = Column(Date)
    hours_used = Column(Float)

    operator = Column(String)
    notes = Column(String)

    asset = relationship("Asset", back_populates="usage_logs")
