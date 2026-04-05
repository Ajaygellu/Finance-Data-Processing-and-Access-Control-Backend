from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import SessionLocal
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.core.deps import require_admin, require_viewer, get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/filter", response_model=list[TransactionResponse])
def filter_transactions(
    type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Transaction).filter(
        Transaction.user_id == current_user["user_id"]   
    )

    if type:
        query = query.filter(Transaction.type == type)
    if category:
        query = query.filter(Transaction.category == category)

    return query.all()



@router.post("/", response_model=TransactionResponse)
def create_transaction(
    data: TransactionCreate,
    current_user=Depends(require_admin),   
    db: Session = Depends(get_db)
):
    tx = Transaction(
        **data.model_dump(),
        user_id=current_user["user_id"]  
    )

    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


@router.get("/", response_model=list[TransactionResponse])
def get_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Transaction).filter(
        Transaction.user_id == current_user["user_id"]   
    ).offset(skip).limit(limit).all()


@router.get("/{id}", response_model=TransactionResponse)
def get_transaction(
    id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tx = db.query(Transaction).filter(
        Transaction.id == id,
        Transaction.user_id == current_user["user_id"]  
    ).first()

    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return tx


@router.put("/{id}", response_model=TransactionResponse)
def update_transaction(
    id: int,
    data: TransactionUpdate,
    current_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    tx = db.query(Transaction).filter(
        Transaction.id == id,
        Transaction.user_id == current_user["user_id"]   
    ).first()

    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tx, field, value)

    db.commit()
    db.refresh(tx)
    return tx


@router.delete("/{id}")
def delete_transaction(
    id: int,
    current_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    tx = db.query(Transaction).filter(
        Transaction.id == id,
        Transaction.user_id == current_user["user_id"]   
    ).first()

    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(tx)
    db.commit()

    return {"message": "Transaction deleted successfully"}