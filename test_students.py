"""
WHY
----
These tests verify that the Student CRUD API behaves correctly and consistently.
Each test follows the AAA (Arrange/Act/Assert) pattern so behavior is clear,
isolated, and easy to reason about. The goal is to confirm that the API returns
the correct status codes, enforces validation rules, and handles edge cases
like nonexistent IDs and duplicate emails.

DESIGN
------
1. Arrange: Set up input data or create a student when needed.
2. Act: Call the corresponding endpoint using the TestClient.
3. Assert: Check status codes and response bodies to confirm correct behavior.

The suite covers all required CRUD behaviors:
- Creating students (valid and invalid)
- Listing students
- Fetching by ID (valid and invalid)
- Updating only specified fields
- Deleting students and verifying removal
- Rejecting duplicate emails

This ensures the API is predictable, validated, and aligned with assignment requirements.
"""



import pytest

# ---------------------------------------------------------
# test_create_task → POST creates a student and returns 201
# ---------------------------------------------------------
def test_create_task(client):
    # Arrange
    payload = {
        "username": "Grant",
        "email": "grant@example.com",
        "major": "CS",
        "gpa": 3.8
    }

    # Act
    response = client.post("/students", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "Grant"
    assert data["email"] == "grant@example.com"


# ---------------------------------------------------------
# test_list_tasks → GET returns 200 and a list
# ---------------------------------------------------------
def test_list_tasks(client):
    # Arrange
    client.post("/students", json={
        "username": "A",
        "email": "a@example.com",
        "major": "CS",
        "gpa": 3.0
    })

    # Act
    response = client.get("/students")

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


# ---------------------------------------------------------
# test_get_task_by_id → GET by ID returns correct student
# ---------------------------------------------------------
def test_get_task_by_id(client):
    # Arrange
    created = client.post("/students", json={
        "username": "Grant",
        "email": "grant2@example.com",
        "major": "CS",
        "gpa": 3.9
    })
    student_id = created.json()["id"]

    # Act
    response = client.get(f"/students/{student_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["username"] == "Grant"


# ---------------------------------------------------------
# test_get_nonexistent_task_returns_404
# ---------------------------------------------------------
def test_get_nonexistent_task_returns_404(client):
    # Arrange / Act
    response = client.get("/students/999")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found."


# ---------------------------------------------------------
# test_patch_task → PATCH updates only specified fields
# ---------------------------------------------------------
def test_patch_task(client):
    # Arrange
    created = client.post("/students", json={
        "username": "PatchUser",
        "email": "patch@example.com",
        "major": "CS",
        "gpa": 3.0
    })
    student_id = created.json()["id"]

    # Act
    response = client.patch(f"/students/{student_id}", json={"major": "Math"})

    # Assert
    assert response.status_code == 200
    assert response.json()["major"] == "Math"
    assert response.json()["username"] == "PatchUser"  # unchanged


# ---------------------------------------------------------
# test_delete_task → DELETE removes student (verify with GET)
# ---------------------------------------------------------
def test_delete_task(client):
    # Arrange
    created = client.post("/students", json={
        "username": "DeleteMe",
        "email": "delete@example.com",
        "major": "CS",
        "gpa": 3.0
    })
    student_id = created.json()["id"]

    # Act
    delete_response = client.delete(f"/students/{student_id}")
    follow_up = client.get(f"/students/{student_id}")

    # Assert
    assert delete_response.status_code == 200
    assert follow_up.status_code == 404


# ---------------------------------------------------------
# test_create_task_invalid_data_returns_422
# ---------------------------------------------------------
def test_create_task_invalid_data_returns_422(client):
    # Arrange — empty username is invalid
    payload = {
        "username": "",
        "email": "bad@example.com",
        "major": "CS",
        "gpa": 3.0
    }

    # Act
    response = client.post("/students", json=payload)

    # Assert
    assert response.status_code == 422
    assert response.json()["error"] is True


# ---------------------------------------------------------
# test_duplicate_task_title_returns_409 → duplicate email
# ---------------------------------------------------------
def test_duplicate_task_title_returns_409(client):
    # Arrange
    client.post("/students", json={
        "username": "User1",
        "email": "dup@example.com",
        "major": "Math",
        "gpa": 3.0
    })

    # Act
    response = client.post("/students", json={
        "username": "User2",
        "email": "dup@example.com",
        "major": "Physics",
        "gpa": 3.2
    })

    # Assert
    assert response.status_code == 409
    assert response.json()["detail"] == "A student with this email already exists."
