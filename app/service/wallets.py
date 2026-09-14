from decimal import Decimal

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.enum import CurrencyEnum
from app.models import User
from app.repository import wallets as wallets_repository
from app.schemas import CreateWalletRequest, TotalBalance, WalletResponse
from app.service import exchange_service

async def get_balance(db: Session, current_user: User, wallet_name: str | None = None):
    if wallet_name is None:
        wallets = wallets_repository.get_all_wallets(db, current_user.id)
        return {"total_balance": sum([w.balance for w in wallets])}
    if not wallets_repository.is_wallet_exist(db, current_user.id, wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet `{wallet_name}` not found"
        )
    wallet = wallets_repository.get_wallet_balance_by_name(db, current_user.id, wallet_name)

    if not wallet_name:
        total_balance = Decimal(0)

        for wallet in wallets:
            if wallet.currency == CurrencyEnum.RUB:
                total_balance += wallet.balance
            else:
                exchange_rate = await exchange_service.get_exchange_rate(wallet.currency, CurrencyEnum.RUB)
                total_balance += exchange_service * wallet.balance
        return TotalBalance(total_balance=total_balance)

    return {"wallet": wallet_name, "balance": wallet.balance}

def create_wallet(db: Session, current_user: User, wallet: CreateWalletRequest) -> WalletResponse:
    if wallets_repository.is_wallet_exist(db, current_user.id, wallet.name):
        raise HTTPException(
            status_code=400,
            detail=f"Wallet '{wallet.name}' already exists"
        )
    new_wallet = wallets_repository.create_wallet(db, current_user.id, wallet.name, wallet.initial_balance, wallet.currency)
    db.commit()
    return WalletResponse.model_validate(new_wallet)

def get_all_wallets(db: Session, current_user: User) -> list[WalletResponse]:
    wallets = wallets_repository.get_all_wallets(db, current_user.id)
    return [WalletResponse.model_validate(wallet) for wallet in wallets]