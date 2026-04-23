from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float
from database import Base
class daily_recordbase(Base):
    __tablename__ = "daily_records"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True, default=datetime.utcnow)
    sales = Column(Float)
    milk_expense = Column(Float)
    others_expense = Column(Integer)
    