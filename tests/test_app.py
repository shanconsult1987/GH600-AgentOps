import json
import threading
from typing import Any, Tuple
from http.client import HTTPConnection
from http.server import HTTPServer

from app import (
    Handler,
    create_task,
    delete_task,
    get_task,
    get_tasks,
    tasks
)


def setup_function():

    tasks.clear()


def start_server() -> Tuple[HTTPServer, threading.Thread]:

    server = HTTPServer(
        ("127.0.0.1", 0),
        Handler
    )

    thread = threading.Thread(
        target=server.serve_forever
    )

    thread.daemon = True

    thread.start()

    return server, thread


def stop_server(
    server: HTTPServer,
    thread: threading.Thread
) -> None:

    server.shutdown()

    server.server_close()

    thread.join()


def request(
    server: HTTPServer,
    method: str,
    path: str
) -> Tuple[int, Any]:

    connection = HTTPConnection(
        "127.0.0.1",
        server.server_address[1]
    )

    try:

        connection.request(
            method,
            path
        )

        response = connection.getresponse()

        body = response.read()

        return (
            response.status,
            json.loads(body)
        )

    finally:

        connection.close()


def test_create_task():

    task = create_task(
        "Learn GH-600",
        "Build a GitHub agent",
        "high"
    )

    assert task["id"] == 1

    assert task["title"] == (
        "Learn GH-600"
    )

    assert task["priority"] == "high"


def test_get_task():

    task = create_task(
        "Test task"
    )

    result = get_task(
        task["id"]
    )

    assert result["title"] == (
        "Test task"
    )


def test_get_tasks():

    create_task("Task 1")

    create_task("Task 2")

    result = get_tasks()

    assert len(result) == 2


def test_delete_task():

    task = create_task(
        "Delete me"
    )

    result = delete_task(
        task["id"]
    )

    assert result["title"] == (
        "Delete me"
    )

    assert get_task(
        task["id"]
    ) is None


def test_invalid_priority():

    try:

        create_task(
            "Bad task",
            priority="urgent"
        )

        assert False

    except ValueError:

        assert True


def test_missing_task():

    result = get_task(9999)

    assert result is None


def test_delete_missing_task():

    result = delete_task(9999)

    assert result is None


def test_delete_task_endpoint():

    task = create_task(
        "Delete via API"
    )

    server, thread = start_server()

    try:

        status, body = request(
            server,
            "DELETE",
            "/tasks/{0}".format(
                task["id"]
            )
        )

        assert status == 200

        assert body["title"] == (
            "Delete via API"
        )

        status, body = request(
            server,
            "DELETE",
            "/tasks/{0}".format(
                task["id"]
            )
        )

        assert status == 404

        assert body["error"] == (
            "Task not found"
        )

        status, body = request(
            server,
            "DELETE",
            "/tasks/abc"
        )

        assert status == 400

        assert body["error"] == (
            "Invalid task ID"
        )

    finally:

        stop_server(
            server,
            thread
        )
