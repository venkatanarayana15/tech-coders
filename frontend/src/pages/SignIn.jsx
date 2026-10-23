import { useEffect, useState } from 'react';
import { api } from '../lib.js';
import { Avatar, Brand, Button, ErrorBlock, Icon, LoadingBlock, Spinner } from '../ui.jsx';

const ROLE_COPY = {
  creator: 'Draft, resolve, and submit work.',
  reviewer: 'Approve work or send it back.',
  admin: 'See every workspace and rule.',
};

export default function SignIn({ onSignIn }) {
  const [users, setUsers] = useState(null);
  const [error, setError] = useState('');
  const [active, setActive] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    api
      .users()
      .then((data) => {
        if (!cancelled) setUsers(data.users || []);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  async function pick(user) {
    setError('');
    setActive(user.id);
    try {
      await onSignIn(user.id);
    } catch (err) {
      setError(err.message);
      setActive('');
    }
  }

  return (
    <main className="signin">
      <div className="signin-glow" aria-hidden="true" />
      <section className="signin-story">
        <Brand />
        <div className="signin-copy">
          <p className="eyebrow">Brand compliance, with receipts</p>
          <h1>
            Every claim,
            <br />
            <em>cleared.</em>
          </h1>
          <p className="signin-lede">
            PrismCheck reviews a draft against the brand kit, cites every finding, and keeps a
            human in the loop. No black-box approvals.
          </p>
        </div>

        <div className="receipt" aria-label="Example review receipt">
          <div className="receipt-head">
            <span>
              <span className="receipt-dot" /> Review receipt
            </span>
            <span>4 findings</span>
          </div>
          <div className="receipt-row">
            <span className="receipt-mark hard" />
            <span>Banned promise</span>
            <code>T-14</code>
          </div>
          <div className="receipt-row">
            <span className="receipt-mark hard" />
            <span>Unsupported claim</span>
            <code>C-01</code>
          </div>
          <div className="receipt-row">
            <span className="receipt-mark soft" />
            <span>Off-palette colour</span>
            <code>V-05</code>
          </div>
          <div className="receipt-source">
            <Icon name="shield" size={16} />
            <span>4 of 4 findings resolve to the kit</span>
            <span className="receipt-lock">100%</span>
          </div>
        </div>

        <p className="signin-foot">
          Tech Circuit Round 2 <span>·</span> Northwind Bank demo workspace
        </p>
      </section>

      <section className="signin-panel">
        <div className="signin-card">
          <div className="signin-card-head">
            <p className="eyebrow">Demo access</p>
            <h2>Step into the workspace</h2>
            <p>Choose a role. No password, no setup — the seeded workspace is ready.</p>
          </div>

          {loading ? (
            <LoadingBlock label="Loading demo roles…" />
          ) : error && !users ? (
            <ErrorBlock message={error} onRetry={() => window.location.reload()} />
          ) : (
            <div className="role-list">
              {(users || []).map((user, index) => (
                <button
                  key={user.id}
                  type="button"
                  className="role-card"
                  onClick={() => pick(user)}
                  disabled={Boolean(active)}
                >
                  <Avatar name={user.name} size={42} tone={index} />
                  <span className="role-copy">
                    <span className="role-name">{user.name}</span>
                    <span className="role-desc">{ROLE_COPY[user.role] || user.role}</span>
                  </span>
                  <span className="role-action">
                    {active === user.id ? <Spinner size={17} /> : <Icon name="arrowRight" size={17} />}
                  </span>
                </button>
              ))}
            </div>
          )}

          {error && users ? <p className="form-error">{error}</p> : null}

          <div className="signin-note">
            <Icon name="lock" size={15} />
            <span>Demo accounts only. Findings and decisions stay in this workspace.</span>
          </div>
        </div>

        <div className="signin-meta">
          <span>PrismCheck AI</span>
          <span>Built for Tech Circuit 2026</span>
        </div>
      </section>
    </main>
  );
}
