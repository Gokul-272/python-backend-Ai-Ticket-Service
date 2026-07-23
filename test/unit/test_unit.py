import pytest
from pydantic import ValidationError
from app.core.exceptions import InvalidTicketStatusTransitionException, TicketNotFoundException
from app.models.ticket import Ticket, StatusEnum
from app.schemas.ticket import CreateTicketRequest, UpdateTicketRequest, TicketResponse

@pytest.fixture
def base_ticket_data():
    return {
        "title": "Database connection failing",
        "priority": "high",
        "email": "admin@example.com"
    }

@pytest.mark.parametrize("email", [
    "test@example.com",
    "abcd@efgh.com",
    "123@456.com"
])
def test_create_ticket_request_valid_email(email, base_ticket_data):
    base_ticket_data["email"] = email
    req = CreateTicketRequest(**base_ticket_data)
    assert req.email == email

@pytest.mark.parametrize("email", [
    "invalid-email",
    "@domain.com",
    "test@.com",
    "test@domain.",
])
def test_create_ticket_request_invalid_email(email, base_ticket_data):
    base_ticket_data["email"] = email
    with pytest.raises(ValidationError):
        CreateTicketRequest(**base_ticket_data)

def test_create_ticket_request_title_too_long(base_ticket_data):
    base_ticket_data["title"] = "goml" * 101
    with pytest.raises(ValidationError):
        CreateTicketRequest(**base_ticket_data)

@pytest.mark.parametrize("title", [
    "Valid title",
    "Another valid title",
    "ABC"
])
def test_update_ticket_request_valid_title(title):
    req = UpdateTicketRequest(title=title)
    assert req.title == title

@pytest.mark.parametrize("title", [
    "",
    "   ",
    "a",
    "ab"
])
def test_update_ticket_request_invalid_title(title):
    with pytest.raises(ValidationError):
        UpdateTicketRequest(title=title)

def test_invalid_status_transition_exception_format():
    exc = InvalidTicketStatusTransitionException(1, "resolved", "open")
    assert exc.status_code == 400
    assert exc.message == "Cannot transition ticket 1 from 'resolved' to 'open'"

def test_ticket_not_found_exception_format():
    exc = TicketNotFoundException(999)
    assert exc.status_code == 404
    assert exc.message == "Ticket with ID 999 not found"

@pytest.mark.parametrize("priority,expected", [
    ("low", True),
    ("medium", True),
    ("high", True),
    ("urgent", False)
])
def test_validate_priority_values(priority, expected):
    if expected:
        req = CreateTicketRequest(title="Valid title", priority=priority, email="test@test.com")
        assert req.priority == priority
    else:
        with pytest.raises(ValidationError):
            CreateTicketRequest(title="Valid title", priority=priority, email="test@test.com")

@pytest.mark.parametrize("status,expected_resolved", [
    (StatusEnum.OPEN, False),
    (StatusEnum.IN_PROGRESS, False),
    (StatusEnum.RESOLVED, True)
])
def test_ticket_response_resolved_property(status, expected_resolved):
    response = TicketResponse(
        id=1,
        title="Valid ticket title",
        priority="medium",
        status=status,
        created_at="2026-07-22T20:00:00Z"
    )
    assert response.is_resolved == expected_resolved
