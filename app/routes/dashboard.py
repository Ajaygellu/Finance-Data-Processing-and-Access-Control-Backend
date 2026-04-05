from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app.models.transaction import Transaction
from app.core.deps import require_analyst, require_viewer, get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/summary")
def get_summary(current_user=Depends(require_viewer), db: Session = Depends(get_db)):
    total_income = db.query(func.sum(Transaction.amount))\
        .filter(
            Transaction.type == "income",
            Transaction.user_id == current_user["user_id"]   
        ).scalar() or 0

    total_expense = db.query(func.sum(Transaction.amount))\
        .filter(
            Transaction.type == "expense",
            Transaction.user_id == current_user["user_id"]   
        ).scalar() or 0

    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "net_balance": round(total_income - total_expense, 2)
    }


@router.get("/category")
def category_summary(current_user=Depends(require_viewer), db: Session = Depends(get_db)):
    result = db.query(
        Transaction.category,
        func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == current_user["user_id"]   
    ).group_by(Transaction.category).all()

    return [
        {"category": r[0], "total": round(r[1], 2)}
        for r in result
    ]


@router.get("/recent")
def recent_transactions(current_user=Depends(require_viewer), db: Session = Depends(get_db)):
    return db.query(Transaction)\
        .filter(Transaction.user_id == current_user["user_id"])\
        .order_by(Transaction.date.desc())\
        .limit(5).all()

@router.get("/monthly")
def monthly_summary(current_user=Depends(require_viewer), db: Session = Depends(get_db)):
    result = db.query(
        func.date_format(Transaction.date, "%Y-%m"),
        func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == current_user["user_id"]   
    ).group_by(func.date_format(Transaction.date, "%Y-%m")).all()

    return [
        {"month": r[0], "total": round(r[1], 2)}
        for r in result
    ]
