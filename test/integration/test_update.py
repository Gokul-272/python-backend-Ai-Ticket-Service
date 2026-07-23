import pytest

def test_update_ticket_all_fields_success(client):
    create_response = client.post(
        "/tickets/",
        json={
            "title": "Email server error",
            "priority": "medium",
            "email": "admin@example.com"
        }
    )
    assert create_response.status_code == 201
    ticket_id = create_response.json()["id"]
    update_response = client.patch(
        f"/tickets/update/{ticket_id}",
        json={
            "title": "Updated email server error",
            "priority": "high",
            "status": "in_progress",
            "assignee": "Jane Smith",
            "email": "lead-admin@example.com"
        }
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["id"] == ticket_id
    assert data["title"] == "Updated email server error"
    assert data["priority"] == "high"
    assert data["status"] == "in_progress"
    assert data["assignee"] == "Jane Smith"
    assert data["email"] == "lead-admin@example.com"

def test_update_ticket_status_transitions(client):
    create_response = client.post(
        "/tickets/",
        json={
            "title": "VPN connection issue",
            "priority": "low",
            "email": "user@example.com"
        }
    )
    assert create_response.status_code == 201
    ticket_id = create_response.json()["id"]

    # Transition: open -> in_progress
    resp1 = client.patch(f"/tickets/update/{ticket_id}", json={"status": "in_progress"})
    assert resp1.status_code == 200
    assert resp1.json()["status"] == "in_progress"

    # Transition: in_progress -> resolved
    resp2 = client.patch(f"/tickets/update/{ticket_id}", json={"status": "resolved"})
    assert resp2.status_code == 200
    assert resp2.json()["status"] == "resolved"

    # Transition: resolved -> resolved (should work)
    resp3 = client.patch(f"/tickets/update/{ticket_id}", json={"status": "resolved"})
    assert resp3.status_code == 200

def test_update_ticket_invalid_status_transition(client):
    create_response = client.post(
        "/tickets/",
        json={
            "title": "License key issue",
            "priority": "low",
            "email": "user@example.com"
        }
    )
    assert create_response.status_code == 201
    ticket_id = create_response.json()["id"]

    # open -> resolved
    resp_resolve = client.patch(f"/tickets/update/{ticket_id}", json={"status": "resolved"})
    assert resp_resolve.status_code == 200

    # resolved -> open (should fail)
    resp_open = client.patch(f"/tickets/update/{ticket_id}", json={"status": "open"})
    assert resp_open.status_code == 400
    assert "Cannot transition ticket" in resp_open.json()["detail"]

    #resolved -> in_progress (should fail)
    resp_progress = client.patch(f"/tickets/update/{ticket_id}", json={"status": "in_progress"})
    assert resp_progress.status_code == 400
    assert "Cannot transition ticket" in resp_progress.json()["detail"]

def test_update_ticket_not_found(client):
    response = client.patch("/tickets/update/999999", json={"title": "Doesn't exist"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket with ID 999999 not found"

