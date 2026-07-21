from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.schemas.ticket import (
    CreateTicketRequest,
    UpdateTicketRequest,
    TicketResponse,
)

from app.services.ticket_service import (
    create_ticket,
    get_all_tickets,
    get_ticket,
    update_ticket,
    delete_ticket,
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.post(
    "/raise",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
async def raise_ticket(
    ticket: CreateTicketRequest,
    db: AsyncSession = Depends(get_db),
):
    return await create_ticket(db, ticket)


@router.get(
    "/view",
    response_model=List[TicketResponse],
    status_code=status.HTTP_200_OK,
)
async def view_all_tickets(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await get_all_tickets(db, status, priority)


@router.get(
    "/get/{ticket_id}",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
)
async def view_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
):
    ticket = await get_ticket(db, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return ticket


@router.patch(
    "/update/{ticket_id}",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
)
async def update_existing_ticket(
    ticket_id: int,
    ticket: UpdateTicketRequest,
    db: AsyncSession = Depends(get_db),
):
    updated_ticket = await update_ticket(
        db,
        ticket_id,
        ticket,
    )

    if updated_ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found for update",
        )

    return updated_ticket


@router.delete(
    "/delete/{ticket_id}",
    status_code=status.HTTP_200_OK,
)
async def remove_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
):
    deleted = await delete_ticket(
        db,
        ticket_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found for deletion",
        )

    return {
        "message": "Ticket deleted successfully"
    }