from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import date

app = FastAPI()

class Task(BaseModel):
    date: str
    title: str
    description: str

tasks = []

@app.get('/tasks', response_model=List[Task])
async  def get_tasks():
    return tasks

@app.post('/tasks', response_model=Task)
async def create_task(task: Task):
    tasks.append(task)
    return task
