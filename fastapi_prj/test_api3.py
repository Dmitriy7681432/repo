# -*- coding: utf-8 -*-
from fastapi import FastAPI
import requests

app = FastAPI()


# @app.get("/api/kurs/{currency_code}")
@app.get("/")
def get_currency_rate(currency_code: str):
    url = f"https://api.exchangerate-api.com/v4/latest/{currency_code.upper()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "base_currency": data["base"],
            "date": data["date"],
            "rates": data["rates"]
        }
    else:
        return {"error": "Курсы валют в данное время недоступны"}