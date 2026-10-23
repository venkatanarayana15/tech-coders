import { useEffect, useMemo, useState } from 'react';
import { api, classNames, firstName, formatShortDate, greeting, plural, statusMeta, timeAgo, todayLabel, truncate } from '../lib.js';
import {
  Avatar,
  Badge,
  Button,
  EmptyState,
  ErrorBlock,
  Icon,
  LoadingBlock,
  ProgressRing,
  StatusBadge,
} from '../ui.jsx';

const FILTERS = [
  { id: 'all', label: 'All drafts' },
  { id: 'attention', label: 'Needs work' },
  { id: 'review', label: 'In review' },
  { id: 'approved', label: 'Approved' },
];

function DraftThumb({ draft }) {
  return (
    <span className="draft-thumb">
      <span className="draft-thumb-fallback">
        <Icon name="image" size={18} />
      </span>
      {draft.image_url ? (
        <img
          src={draft.image_url}
          alt=""
          loading="lazy"
          onError={(event) => {
            event.currentTarget.style.display = 'none';
          }}
        />
      ) : null}
    </span>
  );
}

function DraftRow({ draft, onOpen }) {
  const meta = statusMeta(draft.status, draft.status_label);
  return (
    <button type="button" className="draft-row" onClick={() => onOpen(draft.id)}>
      <span className="draft-identity">
        <DraftThumb draft={draft} />
        <span className="draft-main">
          <span className="draft-title">{draft.title}</span>
          <span className="draft-snippet">{truncate(draft.caption || 'Document review', 94)}</span>
        </span>
      </span>
      <span className="draft-owner">
        <Avatar name={draft.creator} size={24} tone={draft.creator_id?.length || 0} />
        <span>{draft.creator}</span>
      </span>
      <span className="draft-status">
        <StatusBadge status={draft.status} label={draft.status_label || meta.label} />
      </span>
      <span className="draft-findings">
        <span className={classNames('finding-count', draft.open_count > 0 && 'has-open')}>
          {draft.open_count > 0 ? `${draft.open_count} open` : 'Clear'}
        </span>
        <span className="finding-total">{draft.finding_count} total</span>
      </span>
      <span className="draft-updated">{timeAgo(draft.updated_at)}</span>
      <span className="draft-chevron">
        <Icon name="chevronRight" size={16} />
      </span>
    </button>
  );
}

export default function Dashboard({ bootstrap, user, navigate, notify }) {
  const [drafts, setDrafts] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [query, setQuery] = useState('');

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

  const stats = useMemo(() => {
    const list = drafts || [];
    const open = list.reduce((sum, draft) => sum + (draft.open_count || 0), 0);
    const pending = list.filter((draft) => draft.status === 'in_review').length;
    const approved = list.filter((draft) => draft.status === 'approved').length;
    const received = list.reduce(
      (sum, draft) => sum + (draft.review_meta?.citation_lock?.received || 0),
      0,
    );
    const kept = list.reduce(
      (sum, draft) => sum + (draft.review_meta?.citation_lock?.kept || 0),
      0,
    );
    return {
      open,
      pending,
      approved,
      coverage: received ? Math.round((kept / received) * 1000) / 10 : 100,
    };
  }, [drafts]);

  const focus = useMemo(() => {
    if (!drafts) return null;
    if (user.role === 'reviewer' || user.role === 'admin') {
      return (
        drafts
          .filter((draft) => draft.status === 'in_review')
          .sort((a, b) => new Date(a.updated_at) - new Date(b.updated_at))[0] || null
      );
    }
    return (
      drafts
        .filter((draft) => draft.open_count > 0 || draft.status === 'changes_requested')
        .sort((a, b) => b.open_count - a.open_count)[0] || null
    );
  }, [drafts, user.role]);

  const filtered = useMemo(() => {
    let list = drafts || [];
    if (filter === 'attention') {
      list = list.filter((draft) => draft.open_count > 0 || draft.status === 'changes_requested');
    } else if (filter === 'review') {
      list = list.filter((draft) => draft.status === 'in_review');
    } else if (filter === 'approved') {
      list = list.filter((draft) => draft.status === 'approved');
    }
    const needle = query.trim().toLowerCase();
    if (needle) {
      list = list.filter((draft) =>
        [draft.title, draft.caption, draft.creator, draft.status_label]
          .filter(Boolean)
          .some((value) => value.toLowerCase().includes(needle)),
      );
    }
    return list;
  }, [drafts, filter, query]);

  const counts = useMemo(() => {
    const list = drafts || [];
    return {
      all: list.length,
      attention: list.filter((draft) => draft.open_count > 0 || draft.status === 'changes_requested')
        .length,
      review: list.filter((draft) => draft.status === 'in_review').length,
      approved: list.filter((draft) => draft.status === 'approved').length,
    };
  }, [drafts]);

  const failing = Boolean(error) && !drafts;

  return (
    <div className="page dashboard">
      <section className="dashboard-hero">
        <div className="hero-copy">
          <p className="eyebrow">{todayLabel()}</p>
          <h1>
            Good {greeting()}, {firstName(user.name)}.
            <br />
            <span className="hero-accent">Here’s what needs you.</span>
          </h1>
          <p className="hero-lede">
            {stats.open > 0
              ? `${plural(stats.open, 'finding')} still open across the workspace. Every one has a source, a fix, and a decision to make.`
              : 'Every finding has a decision and a source. The workspace is clear.'}
          </p>
          <div className="hero-actions">
            {user.role !== 'reviewer' ? (
              <Button icon="plus" onClick={() => navigate('/new')}>
                New review
              </Button>
            ) : null}
            <Button
              variant="secondary"
              icon="shield"
              iconRight="arrowRight"
              onClick={() => navigate('/approvals')}
            >
              Review queue
              {stats.pending ? <span className="btn-count">{stats.pending}</span> : null}
            </Button>
          </div>
        </div>

        <div className="focus-card">
          <div className="focus-head">
            <span>
              <span className="pulse-dot" />
              {user.role === 'reviewer' || user.role === 'admin' ? 'Oldest in queue' : 'Needs attention'}
            </span>
            <Icon name="spark" size={16} />
          </div>
          {loading ? (
            <div className="focus-skeleton">
              <span />
              <span />
              <span />
            </div>
          ) : focus ? (
            <>
              <div className="focus-body">
                <StatusBadge status={focus.status} label={focus.status_label} />
                <h3>{focus.title}</h3>
                <p>{truncate(focus.caption || 'Document review', 104)}</p>
              </div>
              <div className="focus-foot">
                <span>
                  <Icon name="alert" size={15} />
                  {focus.open_count > 0 ? `${focus.open_count} open` : 'Ready to review'}
                </span>
                <button type="button" onClick={() => navigate(`/drafts/${focus.id}`)}>
                  Open draft <Icon name="arrowRight" size={15} />
                </button>
              </div>
            </>
          ) : (
            <div className="focus-clear">
              <span className="focus-check">
                <Icon name="check" size={22} />
              </span>
              <h3>Nothing waiting.</h3>
              <p>The queue is clear. New work will land here.</p>
            </div>
          )}
        </div>
      </section>

      <section className="stat-strip" aria-label="Workspace statistics">
        <div className="stat-cell">
          <span className="stat-label">Open findings</span>
          <strong>{stats.open}</strong>
          <span className="stat-note">across {plural(counts.all, 'draft')}</span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">In review</span>
          <strong>{stats.pending}</strong>
          <span className="stat-note">waiting on a reviewer</span>
        </div>
        <div className="stat-cell stat-cell-accent">
          <span className="stat-label">
            Citation lock <Icon name="shield" size={14} />
          </span>
          <strong>{stats.coverage}%</strong>
          <span className="stat-note">of findings resolve to the kit</span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">Approved</span>
          <strong>{stats.approved}</strong>
          <span className="stat-note">locked with a decision trail</span>
        </div>
      </section>

      <section className="drafts-section">
        <div className="drafts-head">
          <div>
            <p className="eyebrow">Workspace</p>
            <h2>Drafts</h2>
          </div>
          <div className="drafts-tools">
            <label className="search-box">
              <Icon name="search" size={16} />
              <input
                type="search"
                placeholder="Search drafts"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                aria-label="Search drafts"
              />
            </label>
          </div>
        </div>

        <div className="filter-tabs" role="tablist" aria-label="Filter drafts">
          {FILTERS.map((item) => (
            <button
              key={item.id}
              type="button"
              role="tab"
              aria-selected={filter === item.id}
              className={classNames('filter-tab', filter === item.id && 'is-active')}
              onClick={() => setFilter(item.id)}
            >
              {item.label}
              <span>{counts[item.id] ?? 0}</span>
            </button>
          ))}
        </div>

        {loading ? (
          <LoadingBlock label="Loading drafts…" />
        ) : failing ? (
          <ErrorBlock message={error} onRetry={load} />
        ) : filtered.length === 0 ? (
          <EmptyState
            icon={query ? 'search' : 'file'}
            title={query ? 'No drafts match that search' : 'No drafts here yet'}
            body={
              query
                ? 'Try a different title, creator, or status.'
                : filter === 'attention'
                  ? 'Everything in this view is resolved or approved.'
                  : 'Start a review and PrismCheck will build the receipt.'
            }
            action={
              !query && user.role !== 'reviewer' ? (
                <Button size="sm" icon="plus" onClick={() => navigate('/new')}>
                  New review
                </Button>
              ) : null
            }
          />
        ) : (
          <div className="draft-table">
            <div className="draft-table-head" aria-hidden="true">
              <span>Draft</span>
              <span>Owner</span>
              <span>Status</span>
              <span>Findings</span>
              <span>Updated</span>
              <span />
            </div>
            {filtered.map((draft) => (
              <DraftRow key={draft.id} draft={draft} onOpen={(id) => navigate(`/drafts/${id}`)} />
            ))}
          </div>
        )}
      </section>

      <section className="dashboard-footnote">
        <div className="footnote-mark">
          <Icon name="lock" size={17} />
        </div>
        <div>
          <strong>Every displayed finding has a source.</strong>
          <p>
            PrismCheck drops uncited model output before it reaches the screen. The Citation Lock
            counter on each draft is the audit trail.
          </p>
        </div>
        <button type="button" onClick={() => navigate('/kit')}>
          View brand kit <Icon name="arrowRight" size={15} />
        </button>
      </section>
    </div>
  );
}
