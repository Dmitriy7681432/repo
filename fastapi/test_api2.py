# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field

app = FastAPI()

class Payment(BaseModel):
    amount: float =Field(..., gt=0, description='Неверная сумма платежа')
    currency: str
    recipient: str

# @app.post('/process_payment/{transaction_id}')
@app.post('/')
async def process_payment(
        transaction_id: int,
        payment: Payment
):
    if payment.amount <=0:
        raise HTTPException(status_code=400,detail='Неверная сумма платежа')

    return {"status": "Транзакция прошла успешно", "transaction_id":transaction_id,"payment":payment}