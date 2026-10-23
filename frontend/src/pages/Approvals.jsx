import { useEffect, useMemo, useState } from 'react';
import { api, formatShortDate, plural, timeAgo, truncate } from '../lib.js';
import {
  Avatar,
  Badge,
  Button,
  EmptyState,
  ErrorBlock,
  Icon,
  LoadingBlock,
  PageHeader,
  StatusBadge,
} from '../ui.jsx';

function QueueCard({ draft, onOpen }) {
  return (
    <article className="queue-card">
      <div className="queue-thumb">
        {draft.image_url ? (
          <img src={draft.image_url} alt="" />
        ) : (
          <span>
            <Icon name="image" size={19} />
          </span>
        )}
      </div>
      <div className="queue-main">
        <div className="queue-top">
          <StatusBadge status={draft.status} label={draft.status_label} />
          <span className="queue-age">
            <Icon name="clock" size={13} /> {timeAgo(draft.updated_at)}
          </span>
        </div>
        <h3>{draft.title}</h3>
        <p>{truncate(draft.caption || 'Document review', 112)}</p>
        <div className="queue-meta">
          <span>
            <Avatar name={draft.creator} size={22} tone={draft.creator_id?.length || 0} />
            {draft.creator}
          </span>
          <span>
            <Icon name="alert" size={14} /> {plural(draft.finding_count, 'finding')}
          </span>
          <span>
            <Icon name="calendar" size={14} /> {formatShortDate(draft.updated_at)}
          </span>
        </div>
      </div>
      <div className="queue-action">
        <Button variant="secondary" size="sm" iconRight="arrowRight" onClick={() => onOpen(draft.id)}>
          Open review
        </Button>
      </div>
    </article>
  );
}

export default function Approvals({ navigate }) {
  const [drafts, setDrafts] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  async function load() {
    setLoading(true);
    setError('');
    try {
      const data = await api.drafts();
      setDrafts(data.drafts || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  const queue = useMemo(
    () =>
      (drafts || [])
        .filter((draft) => draft.status === 'in_review')
        .sort((a, b) => new Date(a.updated_at) - new Date(b.updated_at)),
    [drafts],
  );

  const hard = queue.reduce((sum, draft) => sum + (draft.hard_count || 0), 0);
  const oldest = queue[0];

  return (
    <div className="page approvals-page">
      <PageHeader
        eyebrow="Review queue"
        title="Approvals, without the guesswork."
        description="Every draft here has been submitted by its creator. Open the receipt, check the citations, then approve or send it back."
        actions={
          <Button variant="secondary" icon="refresh" onClick={load} loading={loading}>
            Refresh queue
          </Button>
        }
      />

      <section className="stat-strip approvals-stats">
        <div className="stat-cell">
          <span className="stat-label">Waiting on you</span>
          <strong>{queue.length}</strong>
          <span className="stat-note">{queue.length === 1 ? 'draft' : 'drafts'} in review</span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">Hard findings</span>
          <strong>{hard}</strong>
          <span className="stat-note">across the queue</span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">Oldest</span>
          <strong className="stat-text">{oldest ? timeAgo(oldest.updated_at) : 'Clear'}</strong>
          <span className="stat-note">{oldest ? oldest.title : 'Nothing waiting'}</span>
        </div>
      </section>

      <div className="approvals-grid">
        <section className="queue-list-wrap">
          <div className="section-heading">
            <div>
              <p className="eyebrow">In review</p>
              <h2>{queue.length ? `${queue.length} ready to read` : 'Queue clear'}</h2>
            </div>
            {queue.length ? <Badge tone="purple">{queue.length} waiting</Badge> : null}
          </div>

          {loading ? (
            <LoadingBlock label="Loading the review queue…" />
          ) : error ? (
            <ErrorBlock message={error} onRetry={load} />
          ) : queue.length === 0 ? (
            <EmptyState
              icon="check"
              title="Nothing waiting."
              body="Submitted drafts will appear here. Creators see the same review receipt before they submit."
              action={
                <Button variant="secondary" size="sm" icon="grid" onClick={() => navigate('/')}>
                  Back to workspace
                </Button>
              }
            />
          ) : (
            <div className="queue-list">
              {queue.map((draft) => (
                <QueueCard key={draft.id} draft={draft} onOpen={(id) => navigate(`/drafts/${id}`)} />
              ))}
            </div>
          )}
        </section>

        <aside className="approvals-rail">
          <section className="panel rail-card">
            <p className="eyebrow">Reviewer checklist</p>
            <ol className="numbered-list">
              <li>
                <span>01</span>
                <div>
                  <strong>Open the receipt</strong>
                  <p>Check that every displayed finding carries a rule, fact, or palette source.</p>
                </div>
              </li>
              <li>
                <span>02</span>
                <div>
                  <strong>Read the decisions</strong>
                  <p>Accepted fixes and kept wording both include a creator note.</p>
                </div>
              </li>
              <li>
                <span>03</span>
                <div>
                  <strong>Approve or send back</strong>
                  <p>A note is required to request changes. Approval locks the trail.</p>
                </div>
              </li>
            </ol>
          </section>

          <section className="panel rail-card quiet-card">
            <span className="quiet-icon">
              <Icon name="shield" size={17} />
            </span>
            <h3>Citation Lock is enforced</h3>
            <p>
              Reviewers never see an uncited model suggestion. The counter in each draft is the
              audit trail.
            </p>
            <button type="button" className="text-link" onClick={() => navigate('/insights')}>
              See the signals <Icon name="arrowRight" size={14} />
            </button>
          </section>
        </aside>
      </div>
    </div>
  );
}
