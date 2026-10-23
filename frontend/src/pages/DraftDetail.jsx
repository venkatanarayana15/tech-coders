import { useEffect, useMemo, useState } from 'react';
import {
  api,
  checkMeta,
  classNames,
  formatDateTime,
  percent,
  plural,
  timeAgo,
} from '../lib.js';
import {
  Avatar,
  Badge,
  Button,
  Callout,
  EmptyState,
  ErrorBlock,
  Icon,
  LoadingBlock,
  PageHeader,
  ProgressRing,
  SeverityBadge,
  StatusBadge,
} from '../ui.jsx';

function PreviewCard({ draft }) {
  return (
    <section className="panel preview-panel">
      <div className="panel-head">
        <div>
          <p className="eyebrow">Submitted draft</p>
          <h2>Preview</h2>
        </div>
        {draft.image_url ? <Badge tone="neutral">Artwork supplied</Badge> : <Badge tone="neutral">Text only</Badge>}
      </div>

      <div className="preview-art">
        {draft.image_url ? (
          <img src={draft.image_url} alt={draft.alt_text || `Artwork for ${draft.title}`} />
        ) : (
          <div className="preview-placeholder">
            <span>
              <Icon name="image" size={24} />
            </span>
            <strong>No artwork attached</strong>
            <p>Caption-only drafts still get claims, tone, and document review.</p>
          </div>
        )}
        <span className="preview-tag">
          <Icon name="eye" size={13} /> 1:1.91 crop
        </span>
      </div>

      <div className="preview-copy">
        <div className="copy-block">
          <span className="copy-label">Caption</span>
          <p className={draft.caption ? '' : 'is-empty'}>
            {draft.caption || 'No caption supplied.'}
          </p>
        </div>
        <div className="copy-block alt-block">
          <span className="copy-label">Alt text</span>
          <p className={draft.alt_text ? '' : 'is-empty'}>
            {draft.alt_text || 'No alt text supplied — the accessibility check will flag this.'}
          </p>
        </div>

        {draft.doc_name ? (
          <details className="doc-block">
            <summary>
              <span>
                <Icon name="doc" size={17} />
                {draft.doc_name}
              </span>
              <Icon name="chevronDown" size={15} />
            </summary>
            <pre>{draft.doc_text || 'No extractable text in this document.'}</pre>
          </details>
        ) : null}
      </div>
    </section>
  );
}

function SourceCard({ source }) {
  if (!source) return null;
  return (
    <div className="source-card">
      <span className="source-icon">
        <Icon name={source.type === 'rule' ? 'shield' : source.type === 'asset' ? 'palette' : 'book'} size={17} />
      </span>
      <div>
        <span className="source-label">
          {source.type === 'rule' ? 'Rule' : source.type === 'asset' ? 'Asset' : 'Approved fact'} ·{' '}
          {source.id}
        </span>
        <p>{source.quote}</p>
      </div>
      <span className="source-verified">
        <Icon name="check" size={12} /> Cited
      </span>
    </div>
  );
}

function FindingCard({ finding, canDecide, onDecide, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen);
  const [fixIndex, setFixIndex] = useState(0);
  const [note, setNote] = useState('');
  const [busy, setBusy] = useState('');
  const [error, setError] = useState('');
  const meta = checkMeta(finding.check);
  const decided = Boolean(finding.decision);

  async function decide(action) {
    setError('');
    if (action === 'keep' && !note.trim()) {
      setError('Add a short note before keeping your own wording.');
      return;
    }
    setBusy(action);
    try {
      await onDecide(finding.id, action, { fixIndex, note: note.trim() });
      setOpen(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy('');
    }
  }

  return (
    <article className={classNames('finding-card', decided && 'is-decided', `finding-${finding.severity}`)}>
      <button
        type="button"
        className="finding-summary"
        onClick={() => setOpen((value) => !value)}
        aria-expanded={open}
      >
        <span className={classNames('check-chip', `check-${meta.tone}`)}>
          <Icon
            name={
              finding.check === 'claims'
                ? 'alert'
                : finding.check === 'tone'
                  ? 'message'
                  : finding.check === 'visual'
                    ? 'palette'
                    : finding.check === 'accessibility'
                      ? 'eye'
                      : 'doc'
            }
            size={17}
          />
        </span>
        <span className="finding-title-wrap">
          <span className="finding-kicker">
            <code>{finding.rule_id}</code>
            <span>{meta.label}</span>
          </span>
          <span className="finding-title">{finding.title}</span>
        </span>
        <span className="finding-state">
          {decided ? (
            <Badge tone={finding.decision === 'accepted' ? 'green' : 'amber'} dot>
              {finding.decision === 'accepted' ? 'Accepted fix' : 'Kept wording'}
            </Badge>
          ) : (
            <SeverityBadge severity={finding.severity} />
          )}
        </span>
        <span className={classNames('finding-chevron', open && 'is-open')}>
          <Icon name="chevronDown" size={16} />
        </span>
      </button>

      {open ? (
        <div className="finding-body">
          <blockquote className="finding-quote">
            <Icon name="quote" size={16} />
            <span>{finding.quote}</span>
          </blockquote>
          <p className="finding-detail">{finding.detail}</p>
          <SourceCard source={finding.source} />

          {decided ? (
            <div className="decision-record">
              <span className="decision-check">
                <Icon name="check" size={16} />
              </span>
              <div>
                <strong>
                  {finding.decision === 'accepted' ? 'Fix accepted' : 'Wording kept'}
                  {finding.decided_at ? ` · ${timeAgo(finding.decided_at)}` : ''}
                </strong>
                <p>{finding.note || 'No note added.'}</p>
              </div>
            </div>
          ) : !canDecide ? (
            <Callout tone="neutral" icon="lock">
              Switch to the creator account to decide on this finding.
            </Callout>
          ) : (
            <div className="decision-form">
              {finding.fixes?.length ? (
                <div className="fix-list" role="radiogroup" aria-label="Suggested fixes">
                  {finding.fixes.map((fix, index) => (
                    <label
                      key={`${fix.label}-${index}`}
                      className={classNames('fix-option', fixIndex === index && 'is-selected')}
                    >
                      <input
                        type="radio"
                        name={`fix-${finding.id}`}
                        checked={fixIndex === index}
                        onChange={() => setFixIndex(index)}
                      />
                      <span className="fix-radio" aria-hidden="true" />
                      <span className="fix-copy">
                        <span className="fix-label">{fix.label}</span>
                        <span className={classNames('fix-text', !fix.text && 'is-empty')}>
                          {fix.text || 'Remove this claim from the draft.'}
                        </span>
                        {fix.kind === 'guidance' ? (
                          <span className="fix-kind">Design guidance · no text rewrite</span>
                        ) : null}
                      </span>
                    </label>
                  ))}
                </div>
              ) : null}

              <label className="field">
                <span className="field-label">
                  Decision note <span className="optional">optional for accept, required to keep</span>
                </span>
                <textarea
                  rows={2}
                  value={note}
                  onChange={(event) => setNote(event.target.value)}
                  placeholder="Why this is the right call…"
                />
              </label>

              {error ? <p className="form-error">{error}</p> : null}

              <div className="decision-actions">
                <Button
                  size="sm"
                  icon="check"
                  loading={busy === 'accept'}
                  onClick={() => decide('accept')}
                  disabled={Boolean(busy)}
                >
                  {finding.field === 'image'
                    ? 'Accept guidance'
                    : finding.fixes?.length
                      ? 'Apply fix'
                      : 'Accept finding'}
                </Button>
                <Button
                  size="sm"
                  variant="secondary"
                  icon="block"
                  loading={busy === 'keep'}
                  onClick={() => decide('keep')}
                  disabled={Boolean(busy) || !note.trim()}
                  title={!note.trim() ? 'Add a note before keeping your wording' : undefined}
                >
                  Keep as is
                </Button>
                <span className="decision-hint">
                  {finding.severity === 'hard' ? 'Hard stop' : 'Soft note'} · source required
                </span>
              </div>
            </div>
          )}
        </div>
      ) : null}
    </article>
  );
}

function IntegrityCard({ draft }) {
  const lock = draft.review_meta?.citation_lock || {};
  const received = lock.received ?? 0;
  const kept = lock.kept ?? 0;
  const dropped = lock.dropped ?? 0;
  const coverage = received ? Math.round((kept / received) * 1000) / 10 : 100;
  return (
    <section className="panel integrity-card">
      <div className="panel-head compact">
        <div>
          <p className="eyebrow">Audit trail</p>
          <h2>Review integrity</h2>
        </div>
        <span className="integrity-lock">
          <Icon name="lock" size={15} />
        </span>
      </div>
      <div className="integrity-ring">
        <ProgressRing value={coverage} size={92} stroke={8} caption="cited" />
        <div>
          <strong>{coverage}% citation coverage</strong>
          <p>
            {kept} of {received || 0} findings resolve to a rule, fact, or palette entry.
          </p>
        </div>
      </div>
      <div className="integrity-grid">
        <div>
          <span>Received</span>
          <strong>{received}</strong>
        </div>
        <div>
          <span>Cited</span>
          <strong>{kept}</strong>
        </div>
        <div>
          <span>Dropped</span>
          <strong className={dropped ? 'is-danger' : ''}>{dropped}</strong>
        </div>
        <div>
          <span>Review time</span>
          <strong>{draft.review_meta?.duration_ms ? `${draft.review_meta.duration_ms} ms` : '—'}</strong>
        </div>
      </div>
      <div className="integrity-engine">
        <span className="engine-dot" />
        <span>
          {draft.review_meta?.model || 'PrismCheck Review Engine'} ·{' '}
          {draft.review_meta?.engine || 'local'}
        </span>
      </div>
    </section>
  );
}

function Timeline({ revisions }) {
  const list = [...(revisions || [])].reverse().slice(0, 8);
  return (
    <section className="panel timeline-card">
      <div className="panel-head compact">
        <div>
          <p className="eyebrow">History</p>
          <h2>Timeline</h2>
        </div>
        <Badge tone="neutral">{revisions?.length || 0}</Badge>
      </div>
      {list.length ? (
        <ol className="timeline">
          {list.map((revision) => (
            <li key={revision.id}>
              <span
                className={classNames(
                  'timeline-dot',
                  revision.action.includes('approved') && 'is-green',
                  revision.action.includes('changes') && 'is-amber',
                  revision.action.includes('finding') && 'is-purple',
                )}
              />
              <div>
                <p>{revision.summary}</p>
                <span>
                  {revision.actor} · {formatDateTime(revision.created_at)}
                </span>
              </div>
            </li>
          ))}
        </ol>
      ) : (
        <p className="muted-copy">No revisions yet.</p>
      )}
    </section>
  );
}

function ReviewPanel({ openCount, onApprove, onRequestChanges }) {
  const [note, setNote] = useState('');
  const [busy, setBusy] = useState('');
  const [error, setError] = useState('');

  async function act(action) {
    setError('');
    if (action === 'changes' && !note.trim()) {
      setError('Tell the creator what needs changing.');
      return;
    }
    setBusy(action);
    try {
      if (action === 'approve') {
        await onApprove(note.trim());
      } else {
        await onRequestChanges(note.trim());
      }
      setNote('');
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy('');
    }
  }

  return (
    <section className="panel review-panel" id="review-actions">
      <div className="panel-head compact">
        <div>
          <p className="eyebrow">Reviewer action</p>
          <h2>Ready to decide?</h2>
        </div>
        <span className="reviewer-badge">
          <Icon name="shield" size={15} />
        </span>
      </div>
      <p className="review-copy">
        Approving locks the draft and its decision trail. Requesting changes sends it back with
        your note.
      </p>
      {openCount ? (
        <p className="review-hint">
          <Icon name="alert" size={14} />
          Resolve {plural(openCount, 'open finding')} before approving.
        </p>
      ) : null}
      <label className="field">
        <span className="field-label">
          Review note <span className="optional">required to request changes</span>
        </span>
        <textarea
          rows={3}
          value={note}
          onChange={(event) => setNote(event.target.value)}
          placeholder="What should the creator know?"
        />
      </label>
      {error ? <p className="form-error">{error}</p> : null}
      <div className="review-actions">
        <Button
          icon="check"
          loading={busy === 'approve'}
          onClick={() => act('approve')}
          disabled={Boolean(busy) || openCount > 0}
        >
          Approve draft
        </Button>
        <Button
          variant="secondary"
          icon="message"
          loading={busy === 'changes'}
          onClick={() => act('changes')}
          disabled={Boolean(busy) || !note.trim()}
        >
          Request changes
        </Button>
      </div>
    </section>
  );
}

export default function DraftDetail({ id, user, navigate, notify, refreshBootstrap }) {
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [tab, setTab] = useState('open');

  async function load({ quiet = false } = {}) {
    if (!quiet) setLoading(true);
    setError('');
    try {
      const data = await api.draft(id);
      setDetail(data);
    } catch (err) {
      setError(err.message);
    } finally {
      if (!quiet) setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [id]);

  const draft = detail?.draft;
  const findings = detail?.findings || [];
  const openFindings = useMemo(() => findings.filter((finding) => !finding.decision), [findings]);
  const resolvedFindings = useMemo(() => findings.filter((finding) => finding.decision), [findings]);
  const accepted = findings.filter((finding) => finding.decision === 'accepted').length;
  const kept = findings.filter((finding) => finding.decision === 'kept').length;

  useEffect(() => {
    if (!detail) return;
    if (openFindings.length === 0 && resolvedFindings.length > 0) {
      setTab('resolved');
    }
  }, [detail, openFindings.length, resolvedFindings.length]);

  async function decide(findingId, action, payload) {
    await api.decide(id, {
      finding_id: findingId,
      action,
      note: payload.note,
      fix_index: payload.fixIndex,
    });
    await load({ quiet: true });
    await refreshBootstrap();
    notify(action === 'accept' ? 'Fix applied and recorded.' : 'Wording kept with a note.');
  }

  async function submit() {
    try {
      await api.submit(id);
      await load({ quiet: true });
      await refreshBootstrap();
      notify('Draft submitted for review.');
    } catch (err) {
      notify(err.message, 'error');
    }
  }

  async function approve(note) {
    await api.approve(id, note);
    await load({ quiet: true });
    await refreshBootstrap();
    notify('Draft approved. The decision trail is locked.');
  }

  async function requestChanges(note) {
    await api.requestChanges(id, note);
    await load({ quiet: true });
    await refreshBootstrap();
    notify('Changes requested and sent back to the creator.', 'info');
  }

  async function rerun() {
    if (!window.confirm('Re-run the review? This clears the current findings and decisions.')) {
      return;
    }
    try {
      await api.rerun(id);
      await load({ quiet: true });
      notify('Review re-run against the current brand kit.');
    } catch (err) {
      notify(err.message, 'error');
    }
  }

  if (loading) {
    return (
      <div className="page">
        <LoadingBlock label="Opening the review…" />
      </div>
    );
  }

  if (error || !detail) {
    return (
      <div className="page">
        <ErrorBlock
          message={error || 'This draft could not be found.'}
          onRetry={() => load()}
          title="Draft unavailable"
        />
      </div>
    );
  }

  const canDecide = detail.permissions?.can_decide;
  const canReview = detail.permissions?.can_review;
  const canSubmit = detail.permissions?.can_submit;
  const canRerun = detail.permissions?.can_rerun && findings.every((finding) => !finding.decision);
  const visible =
    tab === 'open' ? openFindings : tab === 'resolved' ? resolvedFindings : findings;

  const actions = (
    <>
      {canRerun ? (
        <Button variant="ghost" size="sm" icon="refresh" onClick={rerun}>
          Re-run
        </Button>
      ) : null}
      {canSubmit ? (
        <Button
          icon={openFindings.length ? 'alert' : 'send'}
          disabled={openFindings.length > 0}
          onClick={submit}
          title={
            openFindings.length
              ? `Resolve ${plural(openFindings.length, 'open finding')} before submitting`
              : 'Submit for review'
          }
        >
          {openFindings.length ? `Resolve ${openFindings.length} first` : 'Submit for review'}
        </Button>
      ) : null}
      {canReview ? (
        <Button
          icon="shield"
          onClick={() =>
            document.getElementById('review-actions')?.scrollIntoView({ behavior: 'smooth' })
          }
        >
          Review actions
        </Button>
      ) : null}
      {draft.status === 'approved' ? (
        <Badge tone="green" dot>
          Approved {draft.approved_at ? timeAgo(draft.approved_at) : ''}
        </Badge>
      ) : null}
    </>
  );

  return (
    <div className="page draft-detail">
      <PageHeader
        back={() => navigate(user.role === 'reviewer' ? '/approvals' : '/')}
        backLabel={user.role === 'reviewer' ? 'Approvals' : 'Workspace'}
        eyebrow={`Draft · ${draft.id}`}
        title={draft.title}
        description={
          <span className="draft-meta">
            <StatusBadge status={draft.status} label={draft.status_label} />
            <span className="meta-divider" />
            <Avatar name={draft.creator} size={22} tone={draft.creator_id?.length || 0} />
            <span>{draft.creator}</span>
            <span className="meta-divider" />
            <span>{formatDateTime(draft.updated_at)}</span>
            <span className="meta-divider" />
            <span>
              {plural(findings.length, 'finding')} · {openFindings.length} open
            </span>
          </span>
        }
        actions={actions}
      />

      {draft.status === 'changes_requested' ? (
        <Callout tone="amber" icon="message" title="Changes requested">
          {detail.revisions?.filter((revision) => revision.action === 'draft.changes_requested').slice(-1)[0]
            ?.summary || 'The reviewer sent this draft back with a note.'}
        </Callout>
      ) : null}

      <div className="detail-grid">
        <div className="detail-main">
          <PreviewCard draft={draft} />

          <section className="findings-panel">
            <div className="findings-head">
              <div>
                <p className="eyebrow">Review receipt</p>
                <h2>
                  {findings.length === 0
                    ? 'No findings'
                    : openFindings.length
                      ? `${openFindings.length} ${openFindings.length === 1 ? 'finding needs' : 'findings need'} a decision`
                      : 'Every finding has a decision'}
                </h2>
                <p>
                  {findings.length
                    ? `${accepted} accepted · ${kept} kept · ${openFindings.length} open`
                    : 'The deterministic checks did not find anything against this kit.'}
                </p>
              </div>
              <div className="finding-tabs" role="tablist" aria-label="Finding status">
                <button
                  type="button"
                  role="tab"
                  aria-selected={tab === 'open'}
                  className={classNames('finding-tab', tab === 'open' && 'is-active')}
                  onClick={() => setTab('open')}
                >
                  Open <span>{openFindings.length}</span>
                </button>
                <button
                  type="button"
                  role="tab"
                  aria-selected={tab === 'resolved'}
                  className={classNames('finding-tab', tab === 'resolved' && 'is-active')}
                  onClick={() => setTab('resolved')}
                >
                  Resolved <span>{resolvedFindings.length}</span>
                </button>
                <button
                  type="button"
                  role="tab"
                  aria-selected={tab === 'all'}
                  className={classNames('finding-tab', tab === 'all' && 'is-active')}
                  onClick={() => setTab('all')}
                >
                  All <span>{findings.length}</span>
                </button>
              </div>
            </div>

            {visible.length === 0 ? (
              <EmptyState
                icon={tab === 'open' ? 'check' : 'file'}
                title={tab === 'open' ? 'No open findings' : 'Nothing here yet'}
                body={
                  tab === 'open'
                    ? 'Every finding has a decision. Submit when you are ready — or keep reviewing the resolved trail.'
                    : 'Findings will appear here as the review runs.'
                }
                action={
                  tab === 'open' && canSubmit ? (
                    <Button size="sm" icon="send" onClick={submit} disabled={openFindings.length > 0}>
                      Submit for review
                    </Button>
                  ) : null
                }
              />
            ) : (
              <div className="findings-list">
                {visible.map((finding, index) => (
                  <FindingCard
                    key={finding.id}
                    finding={finding}
                    canDecide={canDecide}
                    onDecide={decide}
                    defaultOpen={tab === 'open' && index === 0 && !finding.decision}
                  />
                ))}
              </div>
            )}
          </section>
        </div>

        <aside className="detail-rail">
          <IntegrityCard draft={draft} />

          <section className="panel summary-card">
            <div className="panel-head compact">
              <div>
                <p className="eyebrow">Summary</p>
                <h2>Decision mix</h2>
              </div>
            </div>
            <div className="decision-mix">
              <div>
                <span className="mix-label">
                  <span className="mix-dot accepted" /> Accepted
                </span>
                <strong>{accepted}</strong>
                <span className="mix-bar">
                  <span style={{ width: `${percent(accepted, findings.length)}%` }} />
                </span>
              </div>
              <div>
                <span className="mix-label">
                  <span className="mix-dot kept" /> Kept
                </span>
                <strong>{kept}</strong>
                <span className="mix-bar kept">
                  <span style={{ width: `${percent(kept, findings.length)}%` }} />
                </span>
              </div>
              <div>
                <span className="mix-label">
                  <span className="mix-dot open" /> Open
                </span>
                <strong>{openFindings.length}</strong>
                <span className="mix-bar open">
                  <span style={{ width: `${percent(openFindings.length, findings.length)}%` }} />
                </span>
              </div>
            </div>
            {findings.length ? (
              <div className="severity-split">
                <span>
                  <span className="sev-dot hard" /> {findings.filter((f) => f.severity === 'hard').length}{' '}
                  hard
                </span>
                <span>
                  <span className="sev-dot soft" /> {findings.filter((f) => f.severity === 'soft').length}{' '}
                  soft
                </span>
              </div>
            ) : null}
          </section>

          {canReview ? (
            <ReviewPanel
              openCount={openFindings.length}
              onApprove={approve}
              onRequestChanges={requestChanges}
            />
          ) : null}

          {draft.status === 'approved' ? (
            <section className="panel approved-card">
              <span className="approved-seal">
                <Icon name="check" size={22} />
              </span>
              <div>
                <h3>Approved</h3>
                <p>
                  Locked {draft.approved_at ? formatDateTime(draft.approved_at) : ''}. The decision
                  trail is immutable.
                </p>
              </div>
            </section>
          ) : null}

          <Timeline revisions={detail.revisions} />
        </aside>
      </div>
    </div>
  );
}
