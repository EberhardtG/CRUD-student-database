import pytest


# ---------------------------------------------------------
# test_create_task → POST creates a student and returns 201
# ---------------------------------------------------------
def test_create_task(client):
    payload = {
        "name": "Grant",
        "email": "grant@example.com",
        "major": "Computer Science",
        "gpa": 3.8
    }

    response = client.post("/students", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Grant"
    assert data["email"] == "grant@example.com"


# ---------------------------------------------------------
# test_list_tasks → GET returns 200 and a list
# ---------------------------------------------------------
def test_list_tasks(client):

    client.post(
        "/students",
        json={
            "name": "A",
            "email": "a@example.com",
            "major": "Computer Science",
            "gpa": 3.0
        }
    )

    response = client.get("/students")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


# ---------------------------------------------------------
# test_get_task_by_id → GET by ID returns correct student
# ---------------------------------------------------------
def test_get_task_by_id(client):

    created = client.post(
        "/students",
        json={
            "name": "Grant",
            "email": "grant2@example.com",
            "major": "Computer Science",
            "gpa": 3.9
        }
    )

    student_id = created.json()["id"]

    response = client.get(
        f"/students/{student_id}"
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Grant"


# ---------------------------------------------------------
# test_get_nonexistent_task_returns_404
# ---------------------------------------------------------
def test_get_nonexistent_task_returns_404(client):

    response = client.get("/students/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found."


# ---------------------------------------------------------
# test_patch_task → PATCH updates only specified fields
# ---------------------------------------------------------
def test_patch_task(client):

    created = client.post(
        "/students",
        json={
            "name": "PatchUser",
            "email": "patch@example.com",
            "major": "Computer Science",
            "gpa": 3.0
        }
    )

    student_id = created.json()["id"]

    response = client.patch(
        f"/students/{student_id}",
        json={
            "major": "Mathematics",
            "gpa": 3.5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["major"] == "Mathematics"
    assert data["gpa"] == 3.5
    assert data["name"] == "PatchUser"


# ---------------------------------------------------------
# test_delete_task → DELETE removes student
# ---------------------------------------------------------
def test_delete_task(client):

    created = client.post(
        "/students",
        json={
            "name": "DeleteMe",
            "email": "delete@example.com",
            "major": "Computer Science",
            "gpa": 3.0
        }
    )

    student_id = created.json()["id"]

    delete_response = client.delete(
        f"/students/{student_id}"
    )

    follow_up = client.get(
        f"/students/{student_id}"
    )

    assert delete_response.status_code == 200
    assert follow_up.status_code == 404


# ---------------------------------------------------------
# test_create_task_invalid_data_returns_422
# ---------------------------------------------------------
def test_create_task_invalid_data_returns_422(client):

    payload = {
        "name": "",
        "email": "bad@example.com",
        "major": "Computer Science",
        "gpa": 3.0
    }

    response = client.post(
        "/students",
        json=payload
    )

    assert response.status_code == 422
    assert response.json()["error"] is True


# ---------------------------------------------------------
# test_duplicate_task_title_returns_409
# ---------------------------------------------------------
def test_duplicate_task_title_returns_409(client):

    client.post(
        "/students",
        json={
            "name": "User1",
            "email": "dup@example.com",
            "major": "Math",
            "gpa": 3.0
        }
    )

    response = client.post(
        "/students",
        json={
            "name": "User2",
            "email": "dup@example.com",
            "major": "Physics",
            "gpa": 3.2
        }
    )

    assert response.status_code == 409

    assert (
        response.json()["detail"]
        == "A student with this email already exists."
    )
