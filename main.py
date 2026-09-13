from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.exceptions import HTTPException

app = FastAPI()

BALANCE = {}

@app.get("/balance")
def get_balance(wallet_name: str | None = None):
    if wallet_name is None:
        return {"total_balance": sum(BALANCE.values())}
    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet `{wallet_name}` not found"
        )
    return {"wallet": wallet_name, "balance": BALANCE[wallet_name]}

@app.post("/wallets/{name}")
def receive_money(name: str, amount: int):
    if name not in BALANCE:
        BALANCE[name] = 0
    BALANCE[name] += amount

    return {
        "message": f"Added {amount} to {name}",
        "wallet": name,
        "new_balance": BALANCE[name]
    }


@app.get("/health")
def health_check():
    return Response(status_code=200)

