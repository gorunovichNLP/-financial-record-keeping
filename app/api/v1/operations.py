from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.models import User
from app.schemas import OperationRequest, OperationResponse
from app.service import operations as operations_service
from app.dependency import get_current_user, get_db

router = APIRouter()

@router.post("/operations/income", response_model=OperationResponse)
def add_income(operation: OperationRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return operations_service.add_income(db, current_user, operation)

@router.post("/operations/expense", response_model=OperationResponse)
def add_expense(operation: OperationRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return operations_service.add_expense(db, current_user, operation)

@router.get("/operations", response_model=list[OperationResponse])
def get_operations_list(
    wallet_id: int | None = Query(None),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return operations_service.get_operations_list(db, current_user, wallet_id, date_from, date_to)