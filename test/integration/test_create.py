import pytest

def test_create_ticket_success(client):
    response = client.post(
        "/tickets/",
        json={
            "title": "Database connection error",
            "priority": "high",
            "email": "user@example.com"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Database connection error"
    assert data["priority"] == "high"
    assert data["status"] == "open"
    assert data["email"] == "user@example.com"
    assert data["assignee"] is None
    assert "created_at" in data
    assert data["is_resolved"] is False

def test_create_ticket_strips_title_whitespace(client):
    response = client.post(
        "/tickets/",
        json={
            "title": "  Database connection error  ",
            "priority": "high",
            "email": "user@example.com"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Database connection error"

