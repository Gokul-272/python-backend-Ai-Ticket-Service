import pytest


def create_ticket(
    client,
    title="Test Ticket",
    priority="low",
    email="test@example.com",
):
    response = client.post(
        "/tickets/",
        json={
            "title": title,
            "priority": priority,
            "email": email,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_get_ticket_success(client):
    ticket = create_ticket(
        client,
        title="Printer connectivity failure",
        email="tech@example.com",
    )

    response = client.get(f"/tickets/get/{ticket['id']}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == ticket["id"]
    assert data["title"] == "Printer connectivity failure"
    assert data["priority"] == "low"
    assert data["status"] == "open"
    assert data["email"] == "tech@example.com"


def test_get_ticket_not_found(client):
    response = client.get("/tickets/get/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket with ID 999999 not found"


def test_get_all_tickets(client):
    t1 = create_ticket(client, "High Ticket", "high")
    t2 = create_ticket(client, "Low Ticket", "low")
    t3 = create_ticket(client, "Another High", "high")
    response = client.get("/tickets/view")
    assert response.status_code == 200
    ids = [ticket["id"] for ticket in response.json()]
    assert t1["id"] in ids
    assert t2["id"] in ids
    assert t3["id"] in ids

def test_filter_by_priority(client):
    create_ticket(client, "High Ticket", "high")
    create_ticket(client, "Low Ticket", "low")
    create_ticket(client, "Another High", "high")
    response = client.get("/tickets/view?priority=high")
    assert response.status_code == 200

    tickets = response.json()
    assert len(tickets) > 0
    assert all(ticket["priority"] == "high" for ticket in tickets)

def test_filter_by_status_and_priority(client):
    create_ticket(client, "Low Ticket", "low")
    response = client.get("/tickets/view?status=open&priority=low")
    assert response.status_code == 200
    tickets = response.json()

    assert all(
        ticket["status"] == "open"
        and ticket["priority"] == "low"
        for ticket in tickets
    )


def test_filter_in_progress_returns_empty(client):
    create_ticket(client)
    response = client.get("/tickets/view?status=in_progress")
    assert response.status_code == 200
    assert response.json() ==[]