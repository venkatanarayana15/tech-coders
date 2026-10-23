import { useEffect, useMemo, useState } from 'react';
import { api, checkMeta, percent, plural } from '../lib.js';
import {
  Badge,
  Button,
  EmptyState,
  ErrorBlock,
  Icon,
  LoadingBlock,
  PageHeader,
  ProgressRing,
} from '../ui.jsx';

function StatCard({ label, value, note, icon, tone = 'neutral' }) {
  return (
    <div className="signal-card">
      <span className={`signal-icon signal-${tone}`}>
        <Icon name={icon} size={18} />
      </span>
      <span className="signal-label">{label}</span>
      <strong>{value}</strong>
      <span className="signal-note">{note}</span>
    </div>
  );
}

export default function Insights({ navigate }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  async function load() {
    setLoading(true);
    setError('');
    try {
      setData(await api.insights());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  const totals = data?.totals;
  const maxFlagged = useMemo(
    () => Math.max(1, ...(data?.most_flagged || []).map((row) => row.count)),
    [data],
  );
  const totalChecks = useMemo(
    () => (data?.by_check || []).reduce((sum, row) => sum + row.count, 0),
    [data],
  );
  const decidedRate = totals?.findings ? Math.round((totals.decided / totals.findings) * 100) : 0;

  return (
    <div className="page insights-page">
      <PageHeader
        eyebrow="Signals"
        title="What the workspace is learning."
        description="A live read on where the kit is catching work, and which rules creators keep overriding. Overrides are a product signal, not a failure."
        actions={
          <Button variant="secondary" icon="book" onClick={() => navigate('/kit')}>
            Open brand kit
          </Button>
        }
      />

      {loading ? (
        <LoadingBlock label="Reading the workspace signals…" />
      ) : error || !data ? (
        <ErrorBlock message={error || 'Signals are unavailable.'} onRetry={load} />
      ) : (
        <>
          <section className="signal-grid">
            <StatCard
              label="Citation coverage"
              value={`${totals.citation_coverage}%`}
              note={`${totals.citation_kept} of ${totals.citation_received} findings cited`}
              icon="shield"
              tone="purple"
            />
            <StatCard
              label="Findings reviewed"
              value={totals.findings}
              note={`${totals.decided} with a recorded decision`}
              icon="file"
              tone="teal"
            />
            <StatCard
              label="Decision rate"
              value={`${decidedRate}%`}
              note={`${totals.accepted} accepted · ${totals.kept} kept`}
              icon="check"
              tone="green"
            />
            <StatCard
              label="Average review"
              value={totals.avg_review_ms ? `${totals.avg_review_ms} ms` : '—'}
              note={`${plural(totals.approved, 'draft')} approved`}
              icon="clock"
              tone="amber"
            />
          </section>

          <div className="insights-grid">
            <section className="panel chart-panel">
              <div className="panel-head">
                <div>
                  <p className="eyebrow">Where the kit catches work</p>
                  <h2>Most flagged rules</h2>
                </div>
                <Badge tone="neutral">{plural(totals.findings, 'finding')}</Badge>
              </div>
              {data.most_flagged.length ? (
                <div className="bar-chart">
                  {data.most_flagged.map((row) => (
                    <div className="bar-row" key={row.rule_id}>
                      <span className="bar-label">
                        <code>{row.rule_id}</code>
                        <span>{row.label}</span>
                      </span>
                      <span className="bar-track">
                        <span
                          className="bar-fill"
                          style={{ width: `${(row.count / maxFlagged) * 100}%` }}
                        />
                      </span>
                      <strong>{row.count}</strong>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyState icon="check" title="No findings yet" body="Run a review to start the signal." />
              )}
              <p className="chart-note">
                Counts include findings across every draft, including ones later accepted or kept.
              </p>
            </section>

            <section className="panel chart-panel">
              <div className="panel-head">
                <div>
                  <p className="eyebrow">Where judgment diverges</p>
                  <h2>Most overridden rules</h2>
                </div>
                <Icon name="sliders" size={18} />
              </div>
              {data.most_overridden.length ? (
                <div className="override-list">
                  {data.most_overridden.map((row) => (
                    <div className="override-row" key={row.rule_id}>
                      <div className="override-head">
                        <span className="override-name">
                          <code>{row.rule_id}</code> {row.label}
                          {row.ambiguous ? <Badge tone="amber">Ambiguous</Badge> : null}
                        </span>
                        <span className="override-rate">{row.rate}% kept</span>
                      </div>
                      <span className="override-track">
                        <span style={{ width: `${row.rate}%` }} />
                      </span>
                      <span className="override-meta">
                        {row.count} kept of {row.decided} decisions
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyState
                  icon="check"
                  title="No overrides yet"
                  body="When creators keep their wording twice at a 40% rate, the rule is marked ambiguous."
                />
              )}
              <p className="chart-note">
                A rule is <strong>ambiguous</strong> when it is kept at least twice and at a rate of
                40% or more. That is a cue to rewrite the guideline.
              </p>
            </section>

            <section className="panel coverage-panel">
              <div className="panel-head">
                <div>
                  <p className="eyebrow">Receipt health</p>
                  <h2>Citation Lock</h2>
                </div>
                <span className="integrity-lock">
                  <Icon name="lock" size={15} />
                </span>
              </div>
              <div className="coverage-body">
                <ProgressRing
                  value={totals.citation_coverage}
                  size={128}
                  stroke={10}
                  caption="cited"
                />
                <div className="coverage-copy">
                  <strong>Every displayed finding resolves.</strong>
                  <p>
                    {totals.citation_kept} of {totals.citation_received} model and deterministic
                    findings resolved to the kit. {totals.citation_dropped} were dropped before
                    display.
                  </p>
                  <div className="coverage-pills">
                    <Badge tone="green">Cited · {totals.citation_kept}</Badge>
                    <Badge tone={totals.citation_dropped ? 'red' : 'neutral'}>
                      Dropped · {totals.citation_dropped}
                    </Badge>
                  </div>
                </div>
              </div>
              <div className="coverage-engine">
                <span className="engine-dot" />
                {data.model?.model || 'PrismCheck Review Engine'} · {data.model?.engine || 'local'}
              </div>
            </section>

            <section className="panel checks-panel">
              <div className="panel-head">
                <div>
                  <p className="eyebrow">Coverage</p>
                  <h2>Findings by check</h2>
                </div>
                <Badge tone="neutral">{plural(totalChecks, 'finding')}</Badge>
              </div>
              {data.by_check.length ? (
                <>
                  <div className="check-bar" aria-hidden="true">
                    {data.by_check.map((row) => (
                      <span
                        key={row.check}
                        style={{
                          width: `${percent(row.count, totalChecks)}%`,
                          background: checkMeta(row.check).color,
                        }}
                      />
                    ))}
                  </div>
                  <div className="check-legend">
                    {data.by_check.map((row) => (
                      <div key={row.check}>
                        <span
                          className="legend-dot"
                          style={{ background: checkMeta(row.check).color }}
                        />
                        <span>{checkMeta(row.check).label}</span>
                        <strong>{row.count}</strong>
                        <span className="legend-percent">
                          {percent(row.count, totalChecks)}%
                        </span>
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <EmptyState icon="chart" title="No check data" body="Findings will populate this view." />
              )}
            </section>
          </div>

          <section className="insight-footnote">
            <span>
              <Icon name="info" size={17} />
            </span>
            <p>
              These numbers are demo-workspace data. In production, the same ledger can be exported
              per campaign or per rule for an audit.
            </p>
            <button type="button" onClick={() => navigate('/approvals')}>
              Review queue <Icon name="arrowRight" size={14} />
            </button>
          </section>
        </>
      )}
    </div>
  );
}
