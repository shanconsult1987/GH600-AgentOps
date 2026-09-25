# Software Development Agent

## Repository

This is a small Python application used for the GH-600 workshop.

The main application is:

app.py

Tests are located in:

tests/

GitHub Actions workflows are located in:

.github/workflows/

## Development Philosophy

Keep the application simple.

Do not introduce unnecessary architecture.

Do not introduce:

- FastAPI
- Flask
- uvicorn
- databases
- Docker
- Kubernetes
- unnecessary frameworks

Prefer Python standard library functionality.

## Code Changes

Before changing code:

1. Understand the requirement.
2. Inspect the existing implementation.
3. Identify the smallest change.
4. Implement the change.
5. Add or update tests.
6. Run the tests.

## Testing

Always run:

python -m pytest -q

Do not consider a change complete until the tests pass.

## API

Do not intentionally break existing endpoints.

If an API change is required:

- explain the change
- update tests
- update README.md when appropriate

## GitHub

Development should normally happen through:

Issue
→ Branch
→ Pull Request
→ GitHub Actions
→ Review
→ Merge

Do not modify unrelated files.

## Pull Requests

A pull request should explain:

### What changed

Describe the implementation.

### Why

Describe the requirement.

### Tests

Describe the tests that were executed.

### Risks

Describe any known limitations.

## AI Development

When acting as an AI developer:

- inspect the repository before changing it
- make small changes
- avoid unnecessary dependencies
- add tests
- run tests
- explain what changed