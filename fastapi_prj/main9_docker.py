# -*- coding: utf-8 -*-
from fastapi import FastAPI
import uvicorn
# 1.Этот код необходимо запуска через venv
# 2. Созать файл с зависимостями: python -m pip freeze > requirements.txt
app = FastAPI()

@app.get("/users")
async def get_users():
    return [{"id":1, "name": "Artem"}]


if __name__ == "__main__":
    uvicorn.run("main9_docker:app", host="0.0.0.0", port=8000)