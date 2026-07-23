from typing import Optional, List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.models.ticket import StatusEnum, PriorityEnum
from app.schemas.ticket import (
    CreateTicketRequest,
    UpdateTicketRequest,
    TicketResponse,
)
from app.services.ticket_service import (create_ticket,get_all_tickets,get_ticket,update_ticket,delete_ticket,)

router = APIRouter(prefix="/tickets",tags=["Tickets"],)

@router.post(
    "/",
    response_model=TicketResponse,
    status_code=201,
)
async def raise_ticket(
    ticket: CreateTicketRequest,
    db: AsyncSession = Depends(get_db),
):
    return await create_ticket(db, ticket)


@router.get("/view",response_model=List[TicketResponse],status_code=200)
async def view_all_tickets(
    status: Optional[StatusEnum] = Query(None),
    priority: Optional[PriorityEnum] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await get_all_tickets(db, status, priority)


@router.get( "/get/{ticket_id}",response_model=TicketResponse,status_code=200)
async def view_ticket(ticket_id: int,db: AsyncSession = Depends(get_db),):
    return await get_ticket(db, ticket_id)


@router.patch("/update/{ticket_id}",response_model=TicketResponse,status_code=200)
async def update_existing_ticket(ticket_id: int,ticket: UpdateTicketRequest,db: AsyncSession = Depends(get_db),):
    return await update_ticket(db,ticket_id,ticket,)


@router.delete("/delete/{ticket_id}",status_code=200)
async def remove_ticket(ticket_id: int,db: AsyncSession = Depends(get_db),):
    await delete_ticket(db, ticket_id)
    return {
        "message": "Ticket deleted successfully"
    }    