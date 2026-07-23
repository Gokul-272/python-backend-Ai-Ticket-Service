import pytest

def test_delete_ticket_success(client):
    # Create ticket
    create_response = client.post(
        "/tickets/",
        json={
            "title": "Old unused ticket",
            "priority": "low",
            "email": "user@example.com"
        }
    )
    assert create_response.status_code == 201
    ticket_id = create_response.json()["id"]

    # Delete ticket
    delete_response = client.delete(f"/tickets/delete/{ticket_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Ticket deleted successfully"}

    # Verify ticket is gone
    get_response = client.get(f"/tickets/get/{ticket_id}")
    assert get_response.status_code == 404

def test_delete_ticket_not_found(client):
    response = client.delete("/tickets/delete/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket with ID 999999 not found"
