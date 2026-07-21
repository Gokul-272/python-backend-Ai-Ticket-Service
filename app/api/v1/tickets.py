from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.ticket import (TicketCreate,TicketUpdate)
from app.services.ticket_service import (create_ticket,get_all_tickets,get_ticket,update_ticket,delete_ticket)

router = APIRouter(prefix="/tickets",tags=["Tickets"])
@router.post("/raise", status_code=status.HTTP_201_CREATED)
def raise_ticket(ticket: TicketCreate):
    return create_ticket(ticket)

@router.get("/view", status_code=status.HTTP_200_OK)
def view_all_tickets(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None)

):
    return get_all_tickets(status, priority)

@router.get("/get/{ticket_id}", status_code=status.HTTP_200_OK)
def view_ticket(ticket_id: int):
    ticket = get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404,detail="Ticket not found")
    return ticket

@router.put("/update/{ticket_id}", status_code=status.HTTP_200_OK)
def update_existing_ticket(ticket_id: int, ticket: TicketUpdate):
    updated_ticket = update_ticket(ticket_id, ticket)
    if not updated_ticket:
        raise HTTPException(status_code=404,detail="Ticket not found")
    return updated_ticket

@router.delete("/delete/{ticket_id}", status_code=status.HTTP_200_OK)
def remove_ticket(ticket_id: int):
    deleted_ticket = delete_ticket(ticket_id)
    if not deleted_ticket:
        raise HTTPException(status_code=404,detail="Ticket not found")
    return {
        "message": "Ticket deleted successfully"
    }