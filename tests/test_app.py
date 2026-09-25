from app import (
    create_task,
    delete_task,
    get_task,
    get_tasks,
    tasks
)


def setup_function():

    tasks.clear()


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