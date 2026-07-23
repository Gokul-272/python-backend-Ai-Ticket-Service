from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import Ticket, StatusEnum, PriorityEnum
from app.repositories.ticket_store import TicketRepository
from app.schemas.ticket import CreateTicketRequest, UpdateTicketRequest
from app.core.exceptions import TicketNotFoundException, InvalidTicketStatusTransitionException

repository = TicketRepository()


async def create_ticket(db: AsyncSession,request: CreateTicketRequest)-> Ticket:
    ticket = Ticket(title=request.title,priority=request.priority,status=StatusEnum.OPEN,email=request.email)
    return await repository.create(db, ticket)


async def get_all_tickets(db: AsyncSession,status: StatusEnum | None = None,priority: PriorityEnum | None = None,)-> list[Ticket]:
    return await repository.get_all(db=db,status=status,priority=priority,)


async def get_ticket(db: AsyncSession,ticket_id: int,) -> Ticket:
    ticket = await repository.get_by_id(db, ticket_id)
    if ticket is None:
        raise TicketNotFoundException(ticket_id)
    return ticket


async def update_ticket(db: AsyncSession,ticket_id: int,request: UpdateTicketRequest,) -> Ticket:
    ticket = await repository.get_by_id(db, ticket_id)
    if ticket is None:
        raise TicketNotFoundException(ticket_id)

    if request.status is not None and ticket.status == StatusEnum.RESOLVED and request.status != StatusEnum.RESOLVED:
        raise InvalidTicketStatusTransitionException(ticket_id, ticket.status.value, request.status)

    if request.title is not None:
        ticket.title = request.title

    if request.priority is not None:
        ticket.priority = request.priority

    if request.status is not None:
        ticket.status = request.status

    if request.assignee is not None:
        ticket.assignee = request.assignee

    if request.email is not None:
        ticket.email = request.email

    return await repository.update(db, ticket)


async def delete_ticket(db: AsyncSession,ticket_id: int,) -> None:
    ticket = await repository.get_by_id(db, ticket_id)
    if ticket is None:
        raise TicketNotFoundException(ticket_id)

    await repository.delete(db, ticket)