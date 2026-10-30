import { useEffect, useMemo, useState } from 'react';
import { api, checkMeta, classNames, formatDate } from '../lib.js';
import {
  Badge,
  Button,
  CopyButton,
  ErrorBlock,
  Icon,
  LoadingBlock,
  PageHeader,
  SeverityBadge,
} from '../ui.jsx';

const TABS = [
  { id: 'rules', label: 'Rules' },
  { id: 'facts', label: 'Fact bank' },
  { id: 'palette', label: 'Palette' },
  { id: 'language', label: 'Language' },
];

export default function Kit({ user, navigate, notify }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [tab, setTab] = useState('rules');
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(null);
  const [saving, setSaving] = useState(false);

  async function load() {
    setLoading(true);
    setError('');
    try {
      setData(await api.kit());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  const kit = data?.kit;
  const counts = useMemo(
    () => ({
      rules: kit?.rules?.length || 0,
      facts: kit?.facts?.length || 0,
      palette: kit?.palette?.length || 0,
      language: (kit?.banned?.length || 0) + (kit?.preferred?.length || 0),
    }),
    [kit],
  );

  function beginEdit() {
    setDraft(JSON.parse(JSON.stringify(kit)));
    setEditing(true);
  }

  function patchPart(part, index, field, value) {
    setDraft((current) => {
      const next = JSON.parse(JSON.stringify(current));
      next[part][index][field] = value;
      return next;
    });
  }

  function patchTop(field, value) {
    setDraft((current) => ({ ...current, [field]: value }));
  }

  async function saveEdit() {
    if (!draft) return;
    setSaving(true);
    setError('');
    try {
      const payload = {
        audience: draft.audience,
        tone: draft.tone,
        tolerance: draft.tolerance,
        palette: draft.palette,
        rules: draft.rules,
        facts: draft.facts,
        banned: draft.banned,
        preferred: draft.preferred,
      };
      const result = await api.updateKit(payload);
      setData({ kit: result.kit });
      setEditing(false);
      setDraft(null);
      notify('Brand kit saved. New version recorded.');
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="page kit-page">
      <PageHeader
        eyebrow="Brand library"
        title={kit ? `${kit.client} · ${kit.name}` : 'Brand kit'}
        description={
          kit
            ? `Version ${kit.version} · updated ${formatDate(kit.updated)}. This is the single source every finding resolves to.`
            : 'The single source every finding resolves to.'
        }
        actions={
          <>
            {user?.role === 'admin' ? (
              editing ? (
                <>
                  <Button variant="secondary" onClick={() => { setEditing(false); setDraft(null); }}>
                    Cancel
                  </Button>
                  <Button onClick={saveEdit} disabled={saving}>
                    {saving ? 'Saving…' : 'Save kit'}
                  </Button>
                </>
              ) : (
                <Button variant="secondary" onClick={beginEdit}>
                  Edit kit
                </Button>
              )
            ) : null}
            <Button variant="secondary" icon="shield" onClick={() => navigate('/insights')}>
              View signals
            </Button>
            {kit ? (
              <Button icon="plus" onClick={() => navigate('/new')}>
                Review a draft
              </Button>
            ) : null}
          </>
        }
      />

      {loading ? (
        <LoadingBlock label="Opening the brand kit…" />
      ) : error || !kit ? (
        <ErrorBlock message={error || 'The brand kit is unavailable.'} onRetry={load} />
      ) : (
        <>
          <section className="kit-summary">
            <div className="kit-summary-main">
              <span className="kit-seal">
                <Icon name="book" size={22} />
              </span>
              <div>
                <p className="eyebrow">Controlled document</p>
                <h2>{kit.name}</h2>
                <p>
                  Owned by {kit.owner} for {kit.audience.replace(/\.+$/, '')}. Every rule, fact, and colour below is
                  addressable by ID.
                </p>
              </div>
            </div>
            <div className="kit-summary-stats">
              <div>
                <strong>{counts.rules}</strong>
                <span>rules</span>
              </div>
              <div>
                <strong>{counts.facts}</strong>
                <span>facts</span>
              </div>
              <div>
                <strong>{counts.palette}</strong>
                <span>colours</span>
              </div>
              <div>
                <strong>{counts.language}</strong>
                <span>language entries</span>
              </div>
            </div>
          </section>

          {editing ? (
            <section className="kit-edit-settings">
              <label>
                <span>Audience</span>
                <textarea
                  value={draft.audience || ''}
                  onChange={(event) => patchTop('audience', event.target.value)}
                  rows={2}
                />
              </label>
              <label>
                <span>Colour tolerance ΔE</span>
                <input
                  type="number"
                  step="0.5"
                  value={draft.tolerance?.delta_e ?? 12}
                  onChange={(event) =>
                    patchTop('tolerance', {
                      ...draft.tolerance,
                      delta_e: Number(event.target.value),
                    })
                  }
                />
              </label>
              <label>
                <span>Minimum contrast</span>
                <input
                  type="number"
                  step="0.1"
                  value={draft.tolerance?.min_contrast ?? 4.5}
                  onChange={(event) =>
                    patchTop('tolerance', {
                      ...draft.tolerance,
                      min_contrast: Number(event.target.value),
                    })
                  }
                />
              </label>
            </section>
          ) : null}

          <div className="kit-tabs" role="tablist" aria-label="Brand kit sections">
            {TABS.map((item) => (
              <button
                key={item.id}
                type="button"
                role="tab"
                aria-selected={tab === item.id}
                className={classNames('kit-tab', tab === item.id && 'is-active')}
                onClick={() => setTab(item.id)}
              >
                {item.label}
                <span>{counts[item.id]}</span>
              </button>
            ))}
          </div>

          {tab === 'rules' ? (
            <section className="kit-section">
              <div className="kit-section-head">
                <div>
                  <p className="eyebrow">The checks</p>
                  <h2>Seven rules, one source each.</h2>
                </div>
                <p>
                  Hard stops block a clean submit. Soft notes are judgment calls for the creator.
                </p>
              </div>
              <div className="rule-grid">
                {kit.rules.map((rule, index) => {
                  const meta = checkMeta(rule.check);
                  return (
                    <article className="rule-card" key={rule.id}>
                      <div className="rule-top">
                        <code>{rule.id}</code>
                        <div>
                          <SeverityBadge severity={rule.severity} />
                          <Badge tone={meta.tone}>{meta.label}</Badge>
                        </div>
                      </div>
                      {editing ? (
                        <div className="kit-edit-fields">
                          <label>
                            <span>Label</span>
                            <input
                              value={draft.rules[index].label}
                              onChange={(event) => patchPart('rules', index, 'label', event.target.value)}
                            />
                          </label>
                          <label>
                            <span>Severity</span>
                            <select
                              value={draft.rules[index].severity}
                              onChange={(event) => patchPart('rules', index, 'severity', event.target.value)}
                            >
                              <option value="hard">Hard stop</option>
                              <option value="soft">Soft note</option>
                            </select>
                          </label>
                          <label>
                            <span>Rule text</span>
                            <textarea
                              value={draft.rules[index].text}
                              onChange={(event) => patchPart('rules', index, 'text', event.target.value)}
                              rows={3}
                            />
                          </label>
                        </div>
                      ) : (
                        <>
                          <h3>{rule.label}</h3>
                          <p>{rule.text}</p>
                        </>
                      )}
                      <span className="rule-foot">
                        <Icon name="shield" size={14} />
                        Resolvable source
                      </span>
                    </article>
                  );
                })}
              </div>
            </section>
          ) : null}

          {tab === 'facts' ? (
            <section className="kit-section">
              <div className="kit-section-head">
                <div>
                  <p className="eyebrow">Approved claims</p>
                  <h2>The fact bank.</h2>
                </div>
                <p>A finding can only suggest wording that already exists here.</p>
              </div>
              <div className="fact-grid">
                {kit.facts.map((fact, index) => (
                  <article className="fact-card" key={fact.id}>
                    <div className="fact-top">
                      <code>{fact.id}</code>
                      <Badge tone="neutral">{fact.category}</Badge>
                    </div>
                    {editing ? (
                      <div className="kit-edit-fields">
                        <label>
                          <span>Approved fact</span>
                          <textarea
                            value={draft.facts[index].text}
                            onChange={(event) => patchPart('facts', index, 'text', event.target.value)}
                            rows={3}
                          />
                        </label>
                      </div>
                    ) : (
                      <p>{fact.text}</p>
                    )}
                    <span className="fact-foot">
                      <Icon name="check" size={14} /> Approved wording
                    </span>
                  </article>
                ))}
              </div>
            </section>
          ) : null}

          {tab === 'palette' ? (
            <section className="kit-section">
              <div className="kit-section-head">
                <div>
                  <p className="eyebrow">Visual system</p>
                  <h2>The approved palette.</h2>
                </div>
                <p>
                  Artwork is sampled and compared with CIELAB ΔE. ΔE ≤ {kit.tolerance?.delta_e} is
                  on-brand; text contrast must reach {kit.tolerance?.min_contrast}:1.
                </p>
              </div>
              <div className="palette-grid">
                {kit.palette.map((colour, index) => (
                  <article className="palette-card" key={colour.id}>
                    <span className="swatch" style={{ background: colour.hex }} />
                    {editing ? (
                      <div className="kit-edit-fields">
                        <label>
                          <span>Name</span>
                          <input
                            value={draft.palette[index].name}
                            onChange={(event) => patchPart('palette', index, 'name', event.target.value)}
                          />
                        </label>
                        <label>
                          <span>Hex</span>
                          <input
                            value={draft.palette[index].hex}
                            onChange={(event) => patchPart('palette', index, 'hex', event.target.value)}
                          />
                        </label>
                        <label>
                          <span>Role</span>
                          <input
                            value={draft.palette[index].role}
                            onChange={(event) => patchPart('palette', index, 'role', event.target.value)}
                          />
                        </label>
                      </div>
                    ) : (
                      <div className="palette-info">
                        <div>
                          <strong>{colour.name}</strong>
                          <code>{colour.hex}</code>
                        </div>
                        <Badge tone="neutral">{colour.role}</Badge>
                      </div>
                    )}
                    <div className="palette-foot">
                      <span>{colour.id}</span>
                      <CopyButton
                        value={colour.hex}
                        onCopy={(value) =>
                          notify(
                            value.startsWith('Copy failed')
                              ? value
                              : `${colour.hex} copied to the clipboard.`,
                            value.startsWith('Copy failed') ? 'error' : 'info',
                          )
                        }
                      />
                    </div>
                  </article>
                ))}
              </div>
            </section>
          ) : null}

          {tab === 'language' ? (
            <section className="kit-section">
              <div className="kit-section-head">
                <div>
                  <p className="eyebrow">Words that carry risk</p>
                  <h2>Banned and preferred language.</h2>
                </div>
                <p>Banned terms are hard stops. Preferred swaps keep the meaning in plainer words.</p>
              </div>
              <div className="language-grid">
                <div className="panel language-panel">
                  <div className="panel-head compact">
                    <div>
                      <p className="eyebrow">Hard stops</p>
                      <h2>Banned terms</h2>
                    </div>
                    <Badge tone="red">{kit.banned.length}</Badge>
                  </div>
                  <div className="language-list">
                    {kit.banned.map((entry, index) => (
                      <div className="language-row" key={entry.id}>
                        {editing ? (
                          <>
                            <input
                              className="kit-edit-inline"
                              value={draft.banned[index].term}
                              onChange={(event) => patchPart('banned', index, 'term', event.target.value)}
                            />
                            <input
                              className="kit-edit-inline code"
                              value={draft.banned[index].rule_id}
                              onChange={(event) => patchPart('banned', index, 'rule_id', event.target.value)}
                            />
                          </>
                        ) : (
                          <>
                            <span className="language-term">{entry.term}</span>
                            <code>{entry.rule_id}</code>
                          </>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="panel language-panel">
                  <div className="panel-head compact">
                    <div>
                      <p className="eyebrow">Soft guidance</p>
                      <h2>Preferred swaps</h2>
                    </div>
                    <Badge tone="amber">{kit.preferred.length}</Badge>
                  </div>
                  <div className="language-list">
                    {kit.preferred.map((entry, index) => (
                      <div className="language-row swap" key={entry.id}>
                        {editing ? (
                          <>
                            <input
                              className="kit-edit-inline"
                              value={draft.preferred[index].from}
                              onChange={(event) => patchPart('preferred', index, 'from', event.target.value)}
                            />
                            <Icon name="arrowRight" size={14} />
                            <input
                              className="kit-edit-inline"
                              value={draft.preferred[index].to}
                              onChange={(event) => patchPart('preferred', index, 'to', event.target.value)}
                            />
                            <input
                              className="kit-edit-inline code"
                              value={draft.preferred[index].rule_id}
                              onChange={(event) => patchPart('preferred', index, 'rule_id', event.target.value)}
                            />
                          </>
                        ) : (
                          <>
                            <span className="swap-from">{entry.from}</span>
                            <Icon name="arrowRight" size={14} />
                            <span className="swap-to">{entry.to}</span>
                            <code>{entry.rule_id}</code>
                          </>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </section>
          ) : null}
        </>
      )}
    </div>
  );
}
