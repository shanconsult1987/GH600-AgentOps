import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


tasks = {}
next_id = 1


def create_task(title, description="", priority="medium"):
    global next_id

    if priority not in ["low", "medium", "high"]:
        raise ValueError(
            "Priority must be low, medium, or high"
        )

    task = {
        "id": next_id,
        "title": title,
        "description": description,
        "priority": priority
    }

    tasks[next_id] = task
    next_id += 1

    return task


def get_task(task_id):
    return tasks.get(task_id)


def get_tasks():
    return list(tasks.values())


def delete_task(task_id):
    return tasks.pop(task_id, None)


class Handler(BaseHTTPRequestHandler):

    def send_json(self, status, data):

        body = json.dumps(data).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.send_header(
            "Content-Length",
            str(len(body))
        )

        self.end_headers()

        self.wfile.write(body)

    def read_json(self):

        length = int(
            self.headers.get(
                "Content-Length",
                0
            )
        )

        if length == 0:
            return {}

        body = self.rfile.read(length)

        return json.loads(body)

    def do_GET(self):

        path = urlparse(self.path).path

        if path == "/":

            self.send_json(
                200,
                {
                    "name": "Software Development Agent",
                    "status": "running"
                }
            )

            return

        if path == "/tasks":

            self.send_json(
                200,
                get_tasks()
            )

            return

        if path.startswith("/tasks/"):

            try:

                task_id = int(
                    path.split("/")[-1]
                )

            except ValueError:

                self.send_json(
                    400,
                    {"error": "Invalid task ID"}
                )

                return

            task = get_task(task_id)

            if task is None:

                self.send_json(
                    404,
                    {"error": "Task not found"}
                )

                return

            self.send_json(
                200,
                task
            )

            return

        self.send_json(
            404,
            {"error": "Not found"}
        )

    def do_POST(self):

        path = urlparse(self.path).path

        if path == "/tasks":

            data = self.read_json()

            try:

                task = create_task(
                    title=data["title"],
                    description=data.get(
                        "description",
                        ""
                    ),
                    priority=data.get(
                        "priority",
                        "medium"
                    )
                )

                self.send_json(
                    201,
                    task
                )

            except KeyError:

                self.send_json(
                    400,
                    {
                        "error":
                        "title is required"
                    }
                )

            except ValueError as error:

                self.send_json(
                    400,
                    {
                        "error": str(error)
                    }
                )

            return

        if (
            path.startswith("/tasks/")
            and path.endswith("/suggest")
        ):

            self.send_json(
                501,
                {
                    "error":
                    "AI suggestion will be added in Stage 7"
                }
            )

            return

        self.send_json(
            404,
            {"error": "Not found"}
        )

    def do_DELETE(self):

        path = urlparse(self.path).path

        if path.startswith("/tasks/"):

            try:

                task_id = int(
                    path.split("/")[-1]
                )

            except ValueError:

                self.send_json(
                    400,
                    {"error": "Invalid task ID"}
                )

                return

            task = delete_task(task_id)

            if task is None:

                self.send_json(
                    404,
                    {"error": "Task not found"}
                )

                return

            self.send_json(
                200,
                task
            )

            return

        self.send_json(
            404,
            {"error": "Not found"}
        )


if __name__ == "__main__":

    server = HTTPServer(
        ("127.0.0.1", 8000),
        Handler
    )

    print(
        "Software Development Agent running at:"
    )

    print(
        "http://127.0.0.1:8000"
    )

    server.serve_forever()