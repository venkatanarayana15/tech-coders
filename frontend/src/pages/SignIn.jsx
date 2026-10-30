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
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [formError, setFormError] = useState('');

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

  async function signInWith(credentials) {
    setFormError('');
    setActive(credentials.email || '');
    try {
      await onSignIn({
        email: credentials.email,
        password: credentials.password,
      });
    } catch (err) {
      setFormError(err.message);
      setActive('');
    }
  }

  function pick(user) {
    setEmail(user.email);
    setPassword(user.password);
    signInWith(user);
  }

  function handleSubmit(event) {
    event.preventDefault();
    if (!email.trim() || !password) {
      setFormError('Enter the demo email and password.');
      return;
    }
    signInWith({ email: email.trim(), password });
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
          Tech Circuit Round 3 <span>·</span> Northwind Bank demo workspace
        </p>
      </section>

      <section className="signin-panel">
        <div className="signin-card">
          <div className="signin-card-head">
            <p className="eyebrow">Demo access</p>
            <h2>Step into the workspace</h2>
            <p>Use any demo account. Email and password are shown below.</p>
          </div>

          <form className="signin-form" onSubmit={handleSubmit}>
            <label className="signin-field">
              <span>Email</span>
              <input
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="you@northwind.example"
                autoComplete="username"
              />
            </label>
            <label className="signin-field">
              <span>Password</span>
              <input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="demo123"
                autoComplete="current-password"
              />
            </label>
            <button type="submit" className="signin-submit" disabled={Boolean(active)}>
              {active ? <Spinner size={17} /> : 'Sign in'}
            </button>
            {formError ? <p className="form-error">{formError}</p> : null}
            <p className="signin-hint">One-click demo accounts below.</p>
          </form>

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
                    <span className="role-creds">
                      {user.email} · password {user.password}
                    </span>
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
