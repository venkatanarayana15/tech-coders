export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

async function request(path, options = {}) {
  const response = await fetch(path, {
    credentials: 'include',
    ...options,
  });
  const text = await response.text();
  let data = null;
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }
  }
  if (!response.ok) {
    let message = 'Something went wrong. Please try again.';
    if (typeof data === 'string' && data.trim()) {
      message = data;
    } else if (data && typeof data.detail === 'string') {
      message = data.detail;
    } else if (data && Array.isArray(data.detail)) {
      message = data.detail.map((item) => item.msg || String(item)).join(', ');
    }
    throw new ApiError(message, response.status);
  }
  return data;
}

const json = (body) => ({
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
});

export const api = {
  session: () => request('/api/session'),
  users: () => request('/api/users'),
  signIn: (credentials) => request('/api/session', json(credentials)),
  signOut: () => request('/api/session', { method: 'DELETE' }),
  bootstrap: () => request('/api/bootstrap'),
  drafts: () => request('/api/drafts'),
  draft: (id) => request(`/api/drafts/${encodeURIComponent(id)}`),
  createDraft: (formData) => request('/api/drafts', { method: 'POST', body: formData }),
  decide: (id, payload) =>
    request(`/api/drafts/${encodeURIComponent(id)}/decisions`, json(payload)),
  submit: (id) => request(`/api/drafts/${encodeURIComponent(id)}/submit`, { method: 'POST' }),
  approve: (id, note) =>
    request(`/api/drafts/${encodeURIComponent(id)}/approve`, json({ note })),
  requestChanges: (id, note) =>
    request(`/api/drafts/${encodeURIComponent(id)}/request-changes`, json({ note })),
  rerun: (id) => request(`/api/drafts/${encodeURIComponent(id)}/rerun`, { method: 'POST' }),
  insights: () => request('/api/insights'),
  kit: () => request('/api/kit'),
  updateKit: (payload) => request('/api/kit', { ...json(payload), method: 'PATCH' }),
};

export function go(path) {
  if (window.location.pathname === path) return;
  window.history.pushState({}, '', path);
  window.dispatchEvent(new PopStateEvent('popstate'));
  window.scrollTo({ top: 0, behavior: 'instant' });
}

export function currentPath() {
  const path = window.location.pathname.replace(/\/+$/, '');
  return path || '/';
}

export function classNames(...values) {
  return values.filter(Boolean).join(' ');
}

export function firstName(name = '') {
  return name.trim().split(/\s+/)[0] || 'there';
}

export function initials(name = '') {
  return (
    name
      .trim()
      .split(/\s+/)
      .slice(0, 2)
      .map((part) => part[0])
      .join('')
      .toUpperCase() || '?'
  );
}

const RELATIVE = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });
const DATE = new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
const DATE_SHORT = new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short' });
const TIME = new Intl.DateTimeFormat('en-IN', { hour: 'numeric', minute: '2-digit' });

export function formatDate(value) {
  if (!value) return '—';
  return DATE.format(new Date(value));
}

export function formatShortDate(value) {
  if (!value) return '—';
  return DATE_SHORT.format(new Date(value));
}

export function formatDateTime(value) {
  if (!value) return '—';
  const date = new Date(value);
  return `${DATE_SHORT.format(date)} · ${TIME.format(date)}`;
}

export function timeAgo(value) {
  if (!value) return '—';
  const date = new Date(value);
  const seconds = (date.getTime() - Date.now()) / 1000;
  const ranges = [
    ['year', 31536000],
    ['month', 2592000],
    ['week', 604800],
    ['day', 86400],
    ['hour', 3600],
    ['minute', 60],
  ];
  for (const [unit, size] of ranges) {
    if (Math.abs(seconds) >= size) {
      return RELATIVE.format(Math.round(seconds / size), unit);
    }
  }
  return 'just now';
}

export function todayLabel() {
  return new Intl.DateTimeFormat('en-IN', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  }).format(new Date());
}

export function greeting() {
  const hour = new Date().getHours();
  if (hour < 12) return 'morning';
  if (hour < 17) return 'afternoon';
  return 'evening';
}

export function plural(count, singular, pluralForm = `${singular}s`) {
  return `${count} ${count === 1 ? singular : pluralForm}`;
}

export function statusMeta(status, label) {
  const map = {
    draft: { label: 'Draft', tone: 'neutral' },
    in_review: { label: 'In review', tone: 'purple' },
    changes_requested: { label: 'Changes requested', tone: 'amber' },
    approved: { label: 'Approved', tone: 'green' },
  };
  return map[status] || { label: label || status || 'Unknown', tone: 'neutral' };
}

export const CHECK_META = {
  claims: { label: 'Claims', tone: 'purple', color: '#6A4CF0' },
  tone: { label: 'Tone', tone: 'amber', color: '#C07A18' },
  visual: { label: 'Visual', tone: 'teal', color: '#0C766E' },
  accessibility: { label: 'Accessibility', tone: 'red', color: '#B42318' },
  document: { label: 'Document', tone: 'neutral', color: '#736F66' },
};

export function checkMeta(check) {
  return CHECK_META[check] || { label: check || 'Review', tone: 'neutral', color: '#736F66' };
}

export function truncate(text = '', limit = 120) {
  if (text.length <= limit) return text;
  return `${text.slice(0, limit).trimEnd()}…`;
}

export function percent(value, total) {
  if (!total) return 0;
  return Math.round((value / total) * 100);
}

export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
