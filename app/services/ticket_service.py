from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket, StatusEnum
from app.repositories.ticket_store import TicketRepository
from app.schemas.ticket import (
    CreateTicketRequest,
    UpdateTicketRequest,
)

repository = TicketRepository()

async def create_ticket(
    db: AsyncSession,
    ticket: CreateTicketRequest,
):
    new_ticket = Ticket(
        title=ticket.title,
        priority=ticket.priority,
        status=StatusEnum.OPEN,
    )
    return await repository.create(db, new_ticket)


async def get_all_tickets(
    db: AsyncSession,
    status: str | None = None,
    priority: str | None = None,
):
    tickets = await repository.get_all(db)

    if status:
        tickets = [
            ticket for ticket in tickets
            if ticket.status.value == status
        ]

    if priority:
        tickets = [
            ticket for ticket in tickets
            if ticket.priority.value == priority
        ]

    return tickets


async def get_ticket(
    db: AsyncSession,
    ticket_id: int,
):
    return await repository.get_by_id(
        db,
        ticket_id,
    )


async def update_ticket(
    db: AsyncSession,
    ticket_id: int,
    request: UpdateTicketRequest,
):
    ticket = await repository.get_by_id(
        db,
        ticket_id,
    )

    if ticket is None:
        return None

    if request.title is not None:
        ticket.title = request.title

    if request.priority is not None:
        ticket.priority = request.priority

    if request.status is not None:
        ticket.status = request.status

    if request.assignee is not None:
        ticket.assignee = request.assignee

    return await repository.update(
        db,
        ticket,
    )


async def delete_ticket(
    db: AsyncSession,
    ticket_id: int,
):
    ticket = await repository.get_by_id(
        db,
        ticket_id,
    )

    if ticket is None:
        return False

    await repository.delete(
        db,
        ticket,
    )

    return True