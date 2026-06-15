# Tasks API (FastAPI + SQLite)

A small, production-shaped REST API for managing tasks. It shows how I build
lightweight backends: clean routes, input validation, correct HTTP status
codes, a simple SQLite data layer, and tests — no unnecessary frameworks.

## Endpoints

| Method | Path           | Purpose                          |
|--------|----------------|----------------------------------|
| GET    | `/health`      | Liveness check                   |
| GET    | `/tasks`       | List tasks (optional `?done=`)   |
| POST   | `/tasks`       | Create a task                    |
| GET    | `/tasks/{id}`  | Get one task                     |
| PUT    | `/tasks/{id}`  | Update a task                    |
| DELETE | `/tasks/{id}`  | Delete a task                    |

## Run it

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open <http://127.0.0.1:8000/docs> for interactive, auto-generated API docs.

## Example

```bash
curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" \
     -d '{"title": "Send invoice"}'
# -> {"id": 1, "title": "Send invoice", "done": false, "created_at": "..."}
```

## Tests

```bash
pytest -q
```

The tests cover the full create/read/update/delete cycle, the `done` filter,
404 handling, and input validation.
