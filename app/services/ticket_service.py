from app.models.ticket_store import ticket_db

def create_ticket(ticket):
    ticket_id = len(ticket_db) + 1
    new_ticket = {
        "id": ticket_id,
        "title": ticket.title,
        "priority": ticket.priority,
        "status": "open"
    }
    ticket_db[ticket_id] = new_ticket
    return new_ticket


def get_all_tickets(status=None, priority=None):
    tickets = list(ticket_db.values())
    if status:
        tickets = [
            ticket
            for ticket in tickets
            if ticket["status"] == status
        ]
    if priority:
        tickets = [
            ticket
            for ticket in tickets
            if ticket["priority"] == priority
        ]
    return { "tickets": tickets ,"message": "Tickets retrieved successfully" }

def get_ticket(ticket_id):
    return ticket_db.get(ticket_id)

def update_ticket(ticket_id, ticket):
    existing_ticket = ticket_db.get(ticket_id)
    if not existing_ticket:
        return None
    existing_ticket["status"] = ticket.status
    return existing_ticket

def delete_ticket(ticket_id):
    return ticket_db.pop(ticket_id, None)