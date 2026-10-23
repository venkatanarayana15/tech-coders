import { useCallback, useEffect, useState } from 'react';
import { api, classNames, currentPath, go } from './lib.js';
import {
  Avatar,
  Brand,
  Button,
  Icon,
  IconButton,
  Spinner,
  Toast,
} from './ui.jsx';
import SignIn from './pages/SignIn.jsx';
import Dashboard from './pages/Dashboard.jsx';
import DraftDetail from './pages/DraftDetail.jsx';
import NewReview from './pages/NewReview.jsx';
import Approvals from './pages/Approvals.jsx';
import Insights from './pages/Insights.jsx';
import Kit from './pages/Kit.jsx';

const WORKSPACE_NAV = [
  { path: '/', label: 'Overview', icon: 'grid' },
  { path: '/new', label: 'New review', icon: 'plus', creatorOnly: true },
  { path: '/approvals', label: 'Approvals', icon: 'shield', queue: true },
  { path: '/insights', label: 'Insights', icon: 'chart' },
  { path: '/kit', label: 'Brand kit', icon: 'book' },
];

function pageTitle(path) {
  if (path === '/') return 'Overview';
  if (path === '/new') return 'New review';
  if (path === '/approvals') return 'Approvals';
  if (path === '/insights') return 'Insights';
  if (path === '/kit') return 'Brand kit';
  if (path.startsWith('/drafts/')) return 'Draft review';
  return 'Not found';
}

function isActive(path, itemPath) {
  if (itemPath === '/') return path === '/';
  return path === itemPath || path.startsWith(`${itemPath}/`);
}

function modelLabel(model) {
  if (!model) return 'Review engine';
  if (model.engine === 'gemini') return model.model || 'Gemini';
  if (model.engine === 'ollama') return model.model || 'Ollama';
  return 'Local rules engine';
}

function BootScreen({ label = 'Opening the workspace…' }) {
  return (
    <div className="boot-screen">
      <div className="boot-mark">
        <Brand />
      </div>
      <div className="boot-loader">
        <Spinner size={19} />
        <span>{label}</span>
      </div>
      <p>Every finding gets a source.</p>
    </div>
  );
}

function NavItem({ item, path, pending, onNavigate }) {
  const active = isActive(path, item.path);
  return (
    <button
      type="button"
      className={classNames('nav-item', active && 'is-active')}
      aria-current={active ? 'page' : undefined}
      onClick={() => onNavigate(item.path)}
    >
      <span className="nav-icon">
        <Icon name={item.icon} size={18} />
      </span>
      <span>{item.label}</span>
      {item.queue && pending ? <span className="nav-badge">{pending}</span> : null}
    </button>
  );
}

function Sidebar({ user, bootstrap, path, pending, onNavigate, onSignOut }) {
  const model = bootstrap?.model;
  const showNew = user.role !== 'reviewer';
  return (
    <aside className="sidebar">
      <button type="button" className="sidebar-brand" onClick={() => onNavigate('/')} aria-label="PrismCheck home">
        <Brand />
      </button>

      <div className="sidebar-section">
        <p className="sidebar-label">Workspace</p>
        <nav className="sidebar-nav" aria-label="Workspace">
          {WORKSPACE_NAV.filter((item) => !item.creatorOnly || showNew).map((item) => (
            <NavItem
              key={item.path}
              item={item}
              path={path}
              pending={pending}
              onNavigate={onNavigate}
            />
          ))}
        </nav>
      </div>

      <div className="sidebar-spacer" />

      <div className="engine-card">
        <div className="engine-card-head">
          <span className="engine-dot" />
          <span>Review engine</span>
          <span className="engine-state">{model?.status === 'fallback' ? 'Fallback' : 'Ready'}</span>
        </div>
        <strong>{modelLabel(model)}</strong>
        <p>
          {model?.engine === 'local'
            ? 'Deterministic checks · Citation Lock on'
            : 'Model suggestions · Citation Lock on'}
        </p>
      </div>

      <div className="sidebar-user">
        <Avatar name={user.name} size={36} tone={user.id?.length || 0} />
        <div>
          <strong>{user.name}</strong>
          <span>{user.role}</span>
        </div>
        <IconButton label="Sign out" icon="logout" onClick={onSignOut} />
      </div>
    </aside>
  );
}

function Topbar({ user, path, pending, onNavigate, onMenu, onSignOut }) {
  const title = pageTitle(path);
  return (
    <header className="topbar">
      <div className="topbar-left">
        <button type="button" className="mobile-menu" onClick={onMenu} aria-label="Open navigation">
          <Icon name="menu" size={20} />
        </button>
        <span className="breadcrumb">
          <span>PrismCheck</span>
          <Icon name="chevronRight" size={13} />
          <strong>{title}</strong>
        </span>
      </div>
      <div className="topbar-right">
        <span className="topbar-badge">
          <span className="pulse-dot" /> Demo workspace
        </span>
        {user.role !== 'reviewer' ? (
          <Button size="sm" icon="plus" onClick={() => onNavigate('/new')}>
            New review
          </Button>
        ) : (
          <Button size="sm" variant="secondary" icon="shield" onClick={() => onNavigate('/approvals')}>
            Queue{pending ? ` · ${pending}` : ''}
          </Button>
        )}
        <button type="button" className="topbar-user" onClick={onSignOut} title="Sign out">
          <Avatar name={user.name} size={32} tone={user.id?.length || 0} />
        </button>
      </div>
    </header>
  );
}

function NotFound({ navigate }) {
  return (
    <div className="page not-found">
      <p className="eyebrow">404</p>
      <h1>This page is off the palette.</h1>
      <p>The route does not exist in the workspace.</p>
      <Button icon="arrowLeft" onClick={() => navigate('/')}>
        Back to overview
      </Button>
    </div>
  );
}

export default function App() {
  const [session, setSession] = useState(undefined);
  const [bootstrap, setBootstrap] = useState(null);
  const [bootError, setBootError] = useState('');
  const [path, setPath] = useState(currentPath());
  const [navOpen, setNavOpen] = useState(false);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    let cancelled = false;
    api
      .session()
      .then((data) => {
        if (!cancelled) setSession(data.user || null);
      })
      .catch(() => {
        if (!cancelled) setSession(null);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    function onPop() {
      setPath(currentPath());
      setNavOpen(false);
    }
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, []);

  useEffect(() => {
    if (!session) {
      setBootstrap(null);
      return;
    }
    let cancelled = false;
    setBootError('');
    api
      .bootstrap()
      .then((data) => {
        if (!cancelled) setBootstrap(data);
      })
      .catch((err) => {
        if (!cancelled) {
          if (err.status === 401) setSession(null);
          else setBootError(err.message);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [session]);

  useEffect(() => {
    document.title =
      path === '/'
        ? 'Overview · PrismCheck AI'
        : `${pageTitle(path)} · PrismCheck AI`;
  }, [path]);

  const notify = useCallback((message, tone = 'success') => {
    setToast({ message, tone, id: Date.now() });
  }, []);

  const closeToast = useCallback(() => setToast(null), []);

  const refreshBootstrap = useCallback(async () => {
    try {
      const data = await api.bootstrap();
      setBootstrap(data);
    } catch {
      /* The next action will surface a useful error. */
    }
  }, []);

  const navigate = useCallback((to) => {
    setNavOpen(false);
    go(to);
  }, []);

  async function signIn(userId) {
    const data = await api.signIn(userId);
    setSession(data.user);
    go('/');
  }

  async function signOut() {
    setSession(null);
    setBootstrap(null);
    setToast(null);
    go('/');
    try {
      await api.signOut();
    } catch {
      /* The local session is already cleared. */
    }
  }

  if (session === undefined) return <BootScreen />;
  if (session === null) {
    return (
      <>
        <SignIn onSignIn={signIn} />
        <Toast toast={toast} onClose={closeToast} />
      </>
    );
  }

  if (!bootstrap && !bootError) return <BootScreen label="Loading the brand kit…" />;

  if (bootError) {
    return (
      <div className="boot-screen boot-error">
        <Brand />
        <h1>The workspace did not open.</h1>
        <p>{bootError}</p>
        <div className="boot-actions">
          <Button icon="refresh" onClick={() => setSession({ ...session })}>
            Try again
          </Button>
          <Button variant="secondary" icon="logout" onClick={signOut}>
            Sign out
          </Button>
        </div>
      </div>
    );
  }

  const user = bootstrap.user;
  const pending = bootstrap.stats?.pending_review || 0;

  let content;
  if (path === '/') {
    content = (
      <Dashboard
        bootstrap={bootstrap}
        user={user}
        navigate={navigate}
        notify={notify}
      />
    );
  } else if (path === '/new') {
    content = <NewReview user={user} navigate={navigate} notify={notify} />;
  } else if (path === '/approvals') {
    content = <Approvals navigate={navigate} notify={notify} />;
  } else if (path === '/insights') {
    content = <Insights navigate={navigate} />;
  } else if (path === '/kit') {
    content = <Kit navigate={navigate} notify={notify} />;
  } else {
    const match = path.match(/^\/drafts\/([^/]+)$/);
    if (match) {
      content = (
        <DraftDetail
          id={decodeURIComponent(match[1])}
          user={user}
          navigate={navigate}
          notify={notify}
          refreshBootstrap={refreshBootstrap}
        />
      );
    } else {
      content = <NotFound navigate={navigate} />;
    }
  }

  return (
    <div className={classNames('app-shell', navOpen && 'nav-open')}>
      <div className="nav-scrim" onClick={() => setNavOpen(false)} aria-hidden="true" />
      <Sidebar
        user={user}
        bootstrap={bootstrap}
        path={path}
        pending={pending}
        onNavigate={navigate}
        onSignOut={signOut}
      />
      <div className="app-body">
        <Topbar
          user={user}
          path={path}
          pending={pending}
          onNavigate={navigate}
          onMenu={() => setNavOpen(true)}
          onSignOut={signOut}
        />
        <main className="page-shell">{content}</main>
        <footer className="app-footer">
          <span>
            PrismCheck AI <span className="footer-dot">·</span> Tech Circuit 2026
          </span>
          <span>Every finding has a source.</span>
        </footer>
      </div>
      <Toast toast={toast} onClose={closeToast} />
    </div>
  );
}
