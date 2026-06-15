"""Tasks API - a small, production-shaped FastAPI service.

A self-contained REST API for managing tasks, backed by SQLite. Demonstrates
clean routing, Pydantic validation, correct HTTP status codes, and a tiny data
layer with no heavyweight ORM. Run locally with:

    pip install -r requirements.txt
    uvicorn main:app --reload

Then open http://127.0.0.1:8000/docs for interactive API documentation.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

DB_PATH = "tasks.db"
app = FastAPI(title="Tasks API", version="1.0.0",
              description="A small CRUD API for managing tasks.")


@contextmanager
def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()


def init_db() -> None:
    with get_db() as con:
        con.execute(
            """CREATE TABLE IF NOT EXISTS tasks (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   done INTEGER NOT NULL DEFAULT 0,
                   created_at TEXT NOT NULL
               )"""
        )


class TaskIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    done: bool = False


class Task(TaskIn):
    id: int
    created_at: str


def _row_to_task(row: sqlite3.Row) -> Task:
    return Task(id=row["id"], title=row["title"],
               done=bool(row["done"]), created_at=row["created_at"])


@app.on_event("startup")
def _startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task])
def list_tasks(done: Optional[bool] = None) -> list[Task]:
    query = "SELECT * FROM tasks"
    params: tuple = ()
    if done is not None:
        query += " WHERE done = ?"
        params = (1 if done else 0,)
    query += " ORDER BY id"
    with get_db() as con:
        rows = con.execute(query, params).fetchall()
    return [_row_to_task(r) for r in rows]


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskIn) -> Task:
    with get_db() as con:
        cur = con.execute(
            "INSERT INTO tasks (title, done, created_at) VALUES (?, ?, ?)",
            (task.title, int(task.done), datetime.now(timezone.utc).isoformat()),
        )
        row = con.execute("SELECT * FROM tasks WHERE id = ?",
                          (cur.lastrowid,)).fetchone()
    return _row_to_task(row)


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    with get_db() as con:
        row = con.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return _row_to_task(row)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskIn) -> Task:
    with get_db() as con:
        cur = con.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
            (task.title, int(task.done), task_id),
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        row = con.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return _row_to_task(row)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    with get_db() as con:
        cur = con.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
