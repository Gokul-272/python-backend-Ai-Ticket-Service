import { useState } from 'react';
import { createTicket, summarizeTicket } from '../api/ticketApi';

const initialForm = {
  title: '',
  priority: 'low',
  email: '',
};

function CreateTicketPage() {
  const [form, setForm] = useState(initialForm);
  const [createLoading, setCreateLoading] = useState(false);
  const [createError, setCreateError] = useState('');
  const [createSuccess, setCreateSuccess] = useState('');

  // AI Summarizer states
  const [description, setDescription] = useState('');
  const [aiSummary, setAiSummary] = useState('');
  const [aiSuggestedResponse, setAiSuggestedResponse] = useState('');
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState('');

  const handleCreateSubmit = async (event) => {
    event.preventDefault();
    setCreateLoading(true);
    setCreateError('');
    setCreateSuccess('');

    // Pre-validation to match backend constraints
    if (form.title.trim().length < 3) {
      setCreateError('Title must be at least 3 characters.');
      setCreateLoading(false);
      return;
    }

    try {
      const response = await createTicket({
        title: form.title.trim(),
        priority: form.priority,
        email: form.email.trim(),
      });
      setForm(initialForm);
      setCreateSuccess(`Ticket #${response.id} raised successfully!`);
    } catch (requestError) {
      setCreateError(requestError.message || 'Unable to create ticket.');
    } finally {
      setCreateLoading(false);
    }
  };

  const handleAIAddSummary = async (event) => {
    event.preventDefault();
    setAiLoading(true);
    setAiError('');
    setAiSummary('');
    setAiSuggestedResponse('');

    if (description.trim().length < 10) {
      setAiError('Description must be at least 10 characters.');
      setAiLoading(false);
      return;
    }

    try {
      const response = await summarizeTicket(description.trim());
      setAiSummary(response.summary);
      setAiSuggestedResponse(response.suggested_response);
    } catch (requestError) {
      setAiError(requestError.message || 'Unable to summarize the ticket.');
    } finally {
      setAiLoading(false);
    }
  };

  return (
    <div className="create-ticket-page">
      <h2 style={{ margin: '0 0 20px', color: '#374151' }}>Raise Ticket & AI Copilot</h2>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '20px', alignItems: 'start' }}>
        {/* Left Column: Create Ticket Form */}
        <section className="crud-panel" style={{ margin: 0 }}>
          <div className="panel-title">New Ticket Form</div>
          <form onSubmit={handleCreateSubmit}>
            <div className="form-grid">
              <label className="full">
                Title
                <input
                  value={form.title}
                  onChange={(event) => setForm((current) => ({ ...current, title: event.target.value }))}
                  placeholder="Summarize the support issue"
                  required
                  minLength={3}
                  maxLength={100}
                />
              </label>

              <label className="full">
                Priority
                <select
                  value={form.priority}
                  onChange={(event) => setForm((current) => ({ ...current, priority: event.target.value }))}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </label>

              <label className="full">
                Customer Email
                <input
                  type="email"
                  value={form.email}
                  onChange={(event) => setForm((current) => ({ ...current, email: event.target.value }))}
                  placeholder="customer@domain.com"
                  required
                />
              </label>
            </div>

            <div className="form-actions" style={{ marginTop: '20px' }}>
              <button className="btn-primary" type="submit" disabled={createLoading}>
                {createLoading ? 'Submitting...' : 'Submit Ticket'}
              </button>
              <button className="btn-secondary" type="button" onClick={() => setForm(initialForm)} disabled={createLoading}>
                Clear
              </button>
            </div>
          </form>

          {createSuccess ? <p className="message success" style={{ marginTop: '12px' }}>{createSuccess}</p> : null}
          {createError ? <p className="message error" style={{ marginTop: '12px' }}>{createError}</p> : null}
        </section>

        {/* Right Column: AI Summarizer Copilot */}
        <section className="crud-panel" style={{ margin: 0 }}>
          <div className="panel-title">AI Ticket Copilot (Bedrock)</div>
          <form onSubmit={handleAIAddSummary}>
            <label style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              Raw Conversation Transcript / Long Description
              <textarea
                value={description}
                onChange={(event) => setDescription(event.target.value)}
                placeholder="Paste support email, chatbot transcript, or long issue description here..."
                required
                minLength={10}
                style={{ minHeight: '120px', padding: '10px', fontSize: '0.9rem' }}
              />
            </label>

            <div className="form-actions" style={{ marginTop: '14px' }}>
              <button className="btn-secondary" type="submit" disabled={aiLoading} style={{ width: '100%' }}>
                {aiLoading ? 'Summarizing...' : 'Summarize with AI'}
              </button>
            </div>
          </form>

          {aiError ? <p className="message error" style={{ marginTop: '10px' }}>{aiError}</p> : null}

          {(aiSummary || aiSuggestedResponse) ? (
            <div style={{ marginTop: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {aiSummary && (
                <div style={{ padding: '12px', border: '1px solid var(--border)', borderRadius: '4px', background: '#fafafa' }}>
                  <h4 style={{ margin: '0 0 6px', fontSize: '0.85rem', color: '#4b5563' }}>AI Summary</h4>
                  <p style={{ margin: 0, fontSize: '0.9rem', color: 'var(--text)' }}>{aiSummary}</p>
                </div>
              )}
              {aiSuggestedResponse && (
                <div style={{ padding: '12px', border: '1px solid var(--border)', borderRadius: '4px', background: '#fafafa' }}>
                  <h4 style={{ margin: '0 0 6px', fontSize: '0.85rem', color: '#4b5563' }}>Suggested Reply</h4>
                  <p style={{ margin: 0, fontSize: '0.9rem', color: 'var(--text)', whiteSpace: 'pre-wrap' }}>{aiSuggestedResponse}</p>
                </div>
              )}
            </div>
          ) : null}
        </section>
      </div>
    </div>
  );
}

export default CreateTicketPage;
