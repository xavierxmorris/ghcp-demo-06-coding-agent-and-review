from __future__ import annotations
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .tasks import TaskStore

app = FastAPI(title="ghcp-demo-06 backend")
store = TaskStore()


class TaskIn(BaseModel):
    title: str
    done: bool = False


class TaskOut(TaskIn):
    id: str


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks() -> list[TaskOut]:
    return [TaskOut(**t) for t in store.list()]


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(task: TaskIn) -> TaskOut:
    return TaskOut(**store.create(task.model_dump()))


@app.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: str, patch: TaskIn) -> TaskOut:
    updated = store.update(task_id, patch.model_dump(exclude_unset=True))
    if updated is None:
        raise HTTPException(status_code=404, detail="not found")
    return TaskOut(**updated)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str) -> None:
    if not store.remove(task_id):
        raise HTTPException(status_code=404, detail="not found")
