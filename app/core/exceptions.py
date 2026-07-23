# app/core/exceptions.py

class ServiceDeskException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

class TicketNotFoundException(ServiceDeskException):
    def __init__(self, ticket_id: int):
        super().__init__(status_code=404,message=f"Ticket with ID {ticket_id} not found")

class InvalidTicketStatusTransitionException(ServiceDeskException):
    def __init__(self, ticket_id: int, from_status, to_status):
        super().__init__(status_code=400,message=f"Cannot transition ticket {ticket_id} from '{from_status}' to '{to_status}'")