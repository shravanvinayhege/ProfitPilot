from pydantic import BaseModel
from typing import Optional
from datetime import datetime

 
 
 
class input_data(BaseModel):
    date: datetime
    sales: float
    milk_expense: float
    others_expense: float
    
class Config:
    from_attributes = True

class output_data(BaseModel):
    id: int
    date: datetime
    sales: float
    milk_expense: float
    others_expense: int

    class Config:
        from_attributes = True

class summary_data(BaseModel):
    date: datetime
    sales: float
    milk_expense: float
    others_expense: int
    net_profit: float

    class Config:
        from_attributes = True


class weekly_summary_data(BaseModel):
    date: str
    sales: float
    expense: float
    profit: float
class Config:
    from_attributes = True

class weekly_insights_response(BaseModel):
    insights: str
    weekly_data: list[weekly_summary_data]

class Config:
    from_attributes = True




class monthly_totals_data(BaseModel):
    total_sales: float
    total_expense: float
    total_profit: float

class Config:
    from_attributes = True
    


class monthly_insights_response(BaseModel):
    insights: str
    monthly_data: list[weekly_summary_data]
    totals: monthly_totals_data

class Config:
    from_attributes = True