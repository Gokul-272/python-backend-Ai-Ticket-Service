import { useState } from 'react';
import { deleteTicket, getTicketById, updateTicket } from '../api/ticketApi';

function TicketsPage() {
  const [ticket, setTicket] = useState(null); // Will hold the single searched ticket
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [editTicket, setEditTicket] = useState(null);
  const [searchId, setSearchId] = useState('');
  const [searchError, setSearchError] = useState('');
  const [searchLoading, setSearchLoading] = useState(false);
  const [updateError, setUpdateError] = useState('');
  const [updateSuccess, setUpdateSuccess] = useState('');

  const handleSearchById = async (event) => {
    event.preventDefault();
    setUpdateError('');
    setUpdateSuccess('');
    setSearchError('');
    setSelectedTicket(null);
    setEditTicket(null);

    const queryId = searchId.trim();
    if (!queryId) {
      setSearchError('Please enter a ticket ID.');
      setTicket(null);
      return;
    }

    setSearchLoading(true);
    try {
      const response = await getTicketById(queryId);
      setTicket(response);
    } catch (requestError) {
      setSearchError(requestError.message || 'Ticket not found.');
      setTicket(null);
    } finally {
      setSearchLoading(false);
    }
  };

  const handleSelectTicket = async (id) => {
    setUpdateError('');
    setUpdateSuccess('');
    try {
      const response = await getTicketById(id);
      setSelectedTicket(response);
    } catch (requestError) {
      setUpdateError(requestError.message || 'Unable to load ticket details.');
    }
  };

  const handleDeleteTicket = async (id) => {
    const confirmDelete = window.confirm('Are you sure you want to delete this ticket?');
    if (!confirmDelete) {
      return;
    }

    setUpdateError('');
    setUpdateSuccess('');
    try {
      await deleteTicket(id);
      setTicket(null);
      setSelectedTicket(null);
      setEditTicket(null);
      setUpdateSuccess('Ticket deleted successfully.');
    } catch (requestError) {
      setUpdateError(requestError.message || 'Unable to delete ticket.');
    }
  };

  const handleSaveTicket = async () => {
    if (!editTicket) {
      return;
    }

    setUpdateError('');
    setUpdateSuccess('');
    try {
      const response = await updateTicket(editTicket.id, {
        title: editTicket.title,
        priority: editTicket.priority,
        status: editTicket.status,
        assignee: editTicket.assignee || null,
        email: editTicket.email,
      });

      setTicket(response);
      if (selectedTicket?.id === editTicket.id) {
        setSelectedTicket(response);
      }
      setEditTicket(null);
      setUpdateSuccess('Ticket updated successfully.');
    } catch (requestError) {
      setUpdateError(requestError.message || 'Unable to update ticket.');
    }
  };

  const handleBeginEdit = (t) => {
    setUpdateError('');
    setUpdateSuccess('');
    setEditTicket({ ...t });
  };

  return (
    <div className="tickets-page">
      <h2 style={{ margin: '0 0 20px', color: '#374151' }}>Search Ticket</h2>

      {/* Search Input Box */}
      <div className="crud-panel" style={{ marginBottom: '20px', padding: '14px' }}>
        <form onSubmit={handleSearchById}>
          <label style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <span style={{ fontWeight: 600, fontSize: '0.85rem' }}>Enter Ticket ID</span>
            <div className="search-row" style={{ display: 'flex', gap: '10px' }}>
              <input
                className="search-input"
                type="number"
                value={searchId}
                onChange={(event) => setSearchId(event.target.value)}
                placeholder="e.g. 1"
                style={{ flex: 1, padding: '8px 12px' }}
                required
              />
              <button className="btn-primary" type="submit" disabled={searchLoading} style={{ padding: '8px 16px' }}>
                {searchLoading ? 'Searching...' : 'Search'}
              </button>
            </div>
          </label>
        </form>
        {searchError ? <p className="message error" style={{ margin: '10px 0 0' }}>{searchError}</p> : null}
      </div>

      {updateSuccess ? <p className="message success" style={{ marginBottom: '14px' }}>{updateSuccess}</p> : null}
      {updateError ? <p className="message error" style={{ marginBottom: '14px' }}>{updateError}</p> : null}

      {/* Ticket Result Table */}
      {ticket ? (
        <div className="table-wrap" style={{ border: '1px solid var(--border)', borderRadius: '4px' }}>
          <table>
            <thead>
              <tr>
                <th style={{ width: '80px' }}>ID</th>
                <th>Title</th>
                <th style={{ width: '110px' }}>Priority</th>
                <th style={{ width: '130px' }}>Status</th>
                <th>Email</th>
                <th>Created</th>
                <th style={{ width: '220px' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>#{ticket.id}</td>
                <td style={{ fontWeight: 500 }}>{ticket.title}</td>
                <td>
                  <span className={`priority-badge priority-${ticket.priority}`}>
                    {ticket.priority}
                  </span>
                </td>
                <td>
                  <span className={`status-badge status-${ticket.status}`}>
                    {ticket.status.replace('_', ' ')}
                  </span>
                </td>
                <td>{ticket.email ?? '-'}</td>
                <td style={{ fontSize: '0.85rem', color: 'var(--muted)' }}>
                  {new Date(ticket.created_at).toLocaleString()}
                </td>
                <td>
                  <div className="row-actions">
                    <button className="btn-secondary" style={{ padding: '4px 8px', minWidth: 'auto' }} type="button" onClick={() => handleSelectTicket(ticket.id)}>
                      View
                    </button>
                    <button className="btn-warning" style={{ padding: '4px 8px', minWidth: 'auto' }} type="button" onClick={() => handleBeginEdit(ticket)}>
                      Edit
                    </button>
                    <button className="btn-danger" style={{ padding: '4px 8px', minWidth: 'auto' }} type="button" onClick={() => handleDeleteTicket(ticket.id)}>
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      ) : (
        <div className="empty-state" style={{ textAlign: 'center', padding: '30px', border: '1px dashed var(--border)', borderRadius: '4px', color: 'var(--muted)' }}>
          No ticket currently loaded. Enter a valid ID above and search.
        </div>
      )}

      {/* Details & Edit Panel Grid */}
      {ticket && (selectedTicket || editTicket) && (
        <div className="details-grid" style={{ marginTop: '20px' }}>
          {selectedTicket ? (
            <div className="plain-box" style={{ margin: 0 }}>
              <h3>Ticket Details</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.92rem' }}>
                <p><strong>Title:</strong> {selectedTicket.title}</p>
                <p><strong>Priority:</strong> <span className={`priority-badge priority-${selectedTicket.priority}`}>{selectedTicket.priority}</span></p>
                <p><strong>Status:</strong> <span className={`status-badge status-${selectedTicket.status}`}>{selectedTicket.status.replace('_', ' ')}</span></p>
                <p><strong>Assignee:</strong> {selectedTicket.assignee ?? <em className="meta">Unassigned</em>}</p>
                <p><strong>Email:</strong> {selectedTicket.email ?? '-'}</p>
                <p><strong>Created at:</strong> {new Date(selectedTicket.created_at).toLocaleString()}</p>
              </div>
            </div>
          ) : (
            <div className="plain-box" style={{ margin: 0, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', minHeight: '160px', color: 'var(--muted)' }}>
              <h3>Ticket Details</h3>
              <p className="meta">Click "View" on the ticket row to inspect details.</p>
            </div>
          )}

          {editTicket ? (
            <div className="plain-box" style={{ margin: 0 }}>
              <h3>Edit Ticket #{editTicket.id}</h3>
              <div className="form-grid">
                <label className="full">
                  Title
                  <input
                    value={editTicket.title ?? ''}
                    onChange={(event) => setEditTicket((current) => ({ ...current, title: event.target.value }))}
                    required
                  />
                </label>

                <label>
                  Priority
                  <select
                    value={editTicket.priority ?? 'low'}
                    onChange={(event) => setEditTicket((current) => ({ ...current, priority: event.target.value }))}
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </label>

                <label>
                  Status
                  <select
                    value={editTicket.status ?? 'open'}
                    onChange={(event) => setEditTicket((current) => ({ ...current, status: event.target.value }))}
                  >
                    <option value="open">Open</option>
                    <option value="in_progress">In Progress</option>
                    <option value="resolved">Resolved</option>
                  </select>
                </label>

                <label className="full">
                  Assignee
                  <input
                    value={editTicket.assignee ?? ''}
                    onChange={(event) => setEditTicket((current) => ({ ...current, assignee: event.target.value }))}
                    placeholder="Optional assignee"
                  />
                </label>

                <label className="full">
                  Email
                  <input
                    type="email"
                    value={editTicket.email ?? ''}
                    onChange={(event) => setEditTicket((current) => ({ ...current, email: event.target.value }))}
                  />
                </label>
              </div>

              <div className="form-actions" style={{ marginTop: '14px' }}>
                <button className="btn-primary" type="button" onClick={handleSaveTicket}>
                  Save
                </button>
                <button className="btn-secondary" type="button" onClick={() => setEditTicket(null)}>
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div className="plain-box" style={{ margin: 0, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', minHeight: '160px', color: 'var(--muted)' }}>
              <h3>Edit Ticket</h3>
              <p className="meta">Click "Edit" on the ticket row to modify fields.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default TicketsPage;
