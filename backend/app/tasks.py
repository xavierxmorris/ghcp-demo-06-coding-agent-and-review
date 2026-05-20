from __future__ import annotations
from typing import Optional
from uuid import uuid4


class TaskStore:
    def __init__(self) -> None:
        self._items: dict[str, dict] = {}

    def list(self) -> list[dict]:
        return list(self._items.values())

    def create(self, data: dict) -> dict:
        task = {"id": str(uuid4()), **data}
        self._items[task["id"]] = task
        return task

    def update(self, task_id: str, patch: dict) -> Optional[dict]:
        if task_id not in self._items:
            return None
        self._items[task_id].update(patch)
        return self._items[task_id]

    def remove(self, task_id: str) -> bool:
        return self._items.pop(task_id, None) is not None
