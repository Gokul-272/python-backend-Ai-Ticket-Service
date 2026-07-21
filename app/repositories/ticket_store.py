from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket


class TicketRepository:

    async def create(self,db: AsyncSession,ticket: Ticket,) -> Ticket:
        db.add(ticket)
        await db.flush()
        await db.refresh(ticket)
        return ticket

    async def get_by_id(self,db: AsyncSession,ticket_id: int,) -> Ticket | None:
        result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
        return result.scalar_one_or_none()

    async def get_all(self,db: AsyncSession,) -> list[Ticket]:
        result = await db.execute(select(Ticket))
        return list(result.scalars().all())

    async def update(self,db: AsyncSession,ticket: Ticket,) -> Ticket:
        await db.flush()
        await db.refresh(ticket)
        return ticket

    async def delete(self,db: AsyncSession,ticket: Ticket,) -> None:
        await db.delete(ticket)