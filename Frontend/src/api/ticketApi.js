const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers ?? {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const errorBody = await response.json();
      message = errorBody.detail ?? errorBody.message ?? message;
    } catch {
      const text = await response.text();
      if (text) {
        message = text;
      }
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export function getTickets(filters = {}) {
  const params = new URLSearchParams();

  if (filters.status) {
    params.set('status', filters.status);
  }
  if (filters.priority) {
    params.set('priority', filters.priority);
  }

  const query = params.toString();
  return request(`/tickets/view${query ? `?${query}` : ''}`);
}

export function getTicketById(id) {
  return request(`/tickets/get/${id}`);
}

export function createTicket(payload) {
  return request('/tickets/', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function updateTicket(id, payload) {
  return request(`/tickets/update/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });
}

export function deleteTicket(id) {
  return request(`/tickets/delete/${id}`, {
    method: 'DELETE',
  });
}

export function summarizeTicket(ticketDescription) {
  return request('/ai/summarize', {
    method: 'POST',
    body: JSON.stringify({ ticket_description: ticketDescription }),
  });
}