import datetime
import calendar

from fastapi import FastAPI, HTTPException
import logging

from sqlalchemy import func
import schemas

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal, engine, Base
from ai import call_llm
from security import get_current_user, verify_credentials


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import models
from schemas import input_data, output_data

logger = logging.getLogger(__name__)
app = FastAPI()


@app.on_event("startup")
def initialize_database() -> None:
    try:
        # Create tables if they don't exist (without dropping existing data)
        Base.metadata.create_all(bind=engine)
    except Exception as exc:
        # Keep API booting so non-DB endpoints still work while DB creds are fixed.
        logger.error("Database initialization failed: %s", exc)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/login")
def login(username: str = Depends(verify_credentials)):
    return {"message": f"Login successful for {username}"}


@app.post("/input", response_model=None)
def receive_data(
    data: input_data,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    try:
        # Create a new record in the database
        new_record = models.daily_recordbase(**data.dict())
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return {
            "message": "Data received successfully",
            "data": data.dict()
        }
    except Exception as exc:
        db.rollback()
        logger.error("Error saving data: %s", exc)
        return {
            "message": "Error saving data",
            "error": str(exc)
        }
@app.get("/records", response_model=list[schemas.output_data])
def get_records(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    records = db.query(models.daily_recordbase).all()
    return records







@app.get("/records/monthly_summary", response_model=schemas.monthly_insights_response)
def get_monthly_summary(
    month: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    try:
        # Expect format MM-YYYY
        parsed_month = datetime.datetime.strptime(month, "%m-%Y")
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid month format. Use MM-YYYY (e.g., 04-2026)",
        ) from exc

    # Get first and last day of the month
    start_date = parsed_month.replace(day=1)
    last_day = calendar.monthrange(start_date.year, start_date.month)[1]
    end_date = parsed_month.replace(day=last_day, hour=23, minute=59, second=59)

    data = (
        db.query(
            models.daily_recordbase.date,
            models.daily_recordbase.sales,
            (
                func.coalesce(models.daily_recordbase.milk_expense, 0)
                + func.coalesce(models.daily_recordbase.others_expense, 0)
            ).label("expense"),
        )
        .filter(
            models.daily_recordbase.date >= start_date,
            models.daily_recordbase.date <= end_date,
        )
        .order_by(models.daily_recordbase.date.asc())
        .all()
    )

    records = []
    for row in data:
        records.append(
            {
                "date": row.date.strftime("%Y-%m-%d"),
                "sales": float(row.sales or 0),
                "expense": float(row.expense or 0),
                "profit": float((row.sales or 0) - (row.expense or 0)),
            }
        )

    if not records:
        return {
            "insights": f"No records found for {start_date.strftime('%B %Y')}.",
            "monthly_data": [],
            "totals": {
                "total_sales": 0.0,
                "total_expense": 0.0,
                "total_profit": 0.0,
            },
        }

    total_sales = sum(r["sales"] for r in records)
    total_expense = sum(r["expense"] for r in records)
    total_profit = sum(r["profit"] for r in records)

    prompt = f"""
You are a business analyst.

Analyze this monthly data for {start_date.strftime("%B %Y")}:
{records}

Monthly totals:
- Total Sales: {total_sales}
- Total Expense: {total_expense}
- Total Profit: {total_profit}

Give concise insights on:
- overall month performance
- best and worst performing days
- unusual changes
- suggestions for next month
All values are in INR.

Keep it short and clear.
"""

    ai_output = call_llm(prompt)

    return {
        "insights": ai_output,
        "monthly_data": records,
        "totals": {
            "total_sales": total_sales,
            "total_expense": total_expense,
            "total_profit": total_profit,
        }
    }


@app.get("/records/{date}", response_model=schemas.output_data)
def get_record(
    date: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    try:
        target_day = datetime.datetime.strptime(date, "%d-%m-%Y").date()
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use DD-MM-YYYY (e.g., 21-04-2026)",
        ) from exc

    start_of_day = datetime.datetime.combine(target_day, datetime.time.min)
    start_of_next_day = start_of_day + datetime.timedelta(days=1)

    record = (
        db.query(models.daily_recordbase)
        .filter(models.daily_recordbase.date >= start_of_day)
        .filter(models.daily_recordbase.date < start_of_next_day)
        .first()
    )

    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    return record