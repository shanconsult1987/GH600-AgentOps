# Software Cevelopment Agent

A lightweight task-management REST API built with Python's standard library. The
application lets clients create, list, retrieve, and delete development tasks.
Tasks are stored in memory and include a title, description, and priority.

## Application details

- Runs locally at `http://127.0.0.1:8000`
- Uses Python's built-in `http.server` module
- Returns JSON responses
- Supports `low`, `medium`, and `high` task priorities
- Assigns an incrementing numeric ID to each task
- Stores data in memory, so all tasks are cleared when the server stops
- Reserves an AI suggestion endpoint for a future implementation

## Endpoints

| Method | Endpoint | Description | Success status |
| --- | --- | --- | --- |
| `GET` | `/` | Check the application status | `200 OK` |
| `GET` | `/tasks` | List all tasks | `200 OK` |
| `GET` | `/tasks/{id}` | Retrieve one task by ID | `200 OK` |
| `POST` | `/tasks` | Create a task | `201 Created` |
| `DELETE` | `/tasks/{id}` | Delete a task by ID | `200 OK` |
| `POST` | `/tasks/{id}/suggest` | Request an AI suggestion (not yet implemented) | `501 Not Implemented` |

### Create-task request

The `title` field is required. `description` defaults to an empty string, and
`priority` defaults to `medium`.

```json
{
  "title": "Add authentication",
  "description": "Protect task-management endpoints",
  "priority": "high"
}
```

## Run locally

### Prerequisites

- Python 3.8 or later

### Start the server

Clone the repository, enter the project directory, and run:

```powershell
python app.py
```

The API will be available at `http://127.0.0.1:8000`. The current implementation
uses only the Python standard library, so no package installation is required to
start it.

## Usage

Check the service:

```powershell
curl.exe http://127.0.0.1:8000/
```

Create a task:

```powershell
$body = @{
  title = "Add authentication"
  description = "Protect the API"
  priority = "high"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/tasks `
  -ContentType "application/json" `
  -Body $body
```

List all tasks:

```powershell
curl.exe http://127.0.0.1:8000/tasks
```

Get a task:

```powershell
curl.exe http://127.0.0.1:8000/tasks/1
```

Delete a task:

```powershell
curl.exe -X DELETE http://127.0.0.1:8000/tasks/1
```

### Error responses

Errors are returned as JSON. Common responses include:

- `400 Bad Request` for a missing title, invalid task ID, or unsupported priority
- `404 Not Found` when a route or task does not exist
- `501 Not Implemented` for the planned AI suggestion endpoint

## License

No license has been specified for this project. Unless a license is added, the
repository's contents remain protected by applicable copyright law and may not
be copied, modified, or distributed without permission from the copyright
holder.
