"""Tests for the Tasks API. Run with: pytest -q"""
import os
import tempfile

import main
from fastapi.testclient import TestClient


def setup_module(_):
    # Use a throwaway database file for the test run.
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    main.DB_PATH = path
    main.init_db()


client = TestClient(main.app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_create_list_get_update_delete():
    # create
    r = client.post("/tasks", json={"title": "Write proposal"})
    assert r.status_code == 201
    task = r.json()
    assert task["title"] == "Write proposal" and task["done"] is False
    tid = task["id"]

    # list
    assert any(t["id"] == tid for t in client.get("/tasks").json())

    # get
    assert client.get(f"/tasks/{tid}").json()["title"] == "Write proposal"

    # update
    r = client.put(f"/tasks/{tid}", json={"title": "Write proposal", "done": True})
    assert r.status_code == 200 and r.json()["done"] is True

    # filter by done
    assert all(t["done"] for t in client.get("/tasks?done=true").json())

    # delete
    assert client.delete(f"/tasks/{tid}").status_code == 204
    assert client.get(f"/tasks/{tid}").status_code == 404


def test_validation_rejects_empty_title():
    assert client.post("/tasks", json={"title": ""}).status_code == 422
