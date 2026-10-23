import { useEffect, useId, useState } from 'react';
import { classNames, initials, statusMeta } from './lib.js';

const ICONS = {
  grid: (
    <>
      <rect x="3" y="3" width="7" height="7" rx="2" />
      <rect x="14" y="3" width="7" height="7" rx="2" />
      <rect x="3" y="14" width="7" height="7" rx="2" />
      <rect x="14" y="14" width="7" height="7" rx="2" />
    </>
  ),
  plus: (
    <>
      <path d="M12 5v14M5 12h14" />
    </>
  ),
  file: (
    <>
      <path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z" />
      <path d="M14 3v5h5M9 13h6M9 17h4" />
    </>
  ),
  check: <path d="m5 12 4.5 4.5L19 7" />,
  chevronRight: <path d="m9 5 7 7-7 7" />,
  chevronDown: <path d="m5 9 7 7 7-7" />,
  arrowLeft: (
    <>
      <path d="M19 12H5" />
      <path d="m11 18-6-6 6-6" />
    </>
  ),
  arrowRight: (
    <>
      <path d="M5 12h14" />
      <path d="m13 6 6 6-6 6" />
    </>
  ),
  alert: (
    <>
      <path d="M10.3 3.9 2.6 17a2 2 0 0 0 1.7 3h15.4a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z" />
      <path d="M12 9v4M12 17h.01" />
    </>
  ),
  shield: (
    <>
      <path d="M12 3 5 6v5c0 4.6 3 8 7 10 4-2 7-5.4 7-10V6z" />
      <path d="m9 12 2 2 4-4" />
    </>
  ),
  palette: (
    <>
      <path d="M12 3a9 9 0 1 0 0 18h1.5a2.5 2.5 0 0 0 0-5H12a2 2 0 0 1 0-4h4a5 5 0 0 0 0-10z" />
      <circle cx="7.5" cy="10" r="1" />
      <circle cx="9.5" cy="6.5" r="1" />
      <circle cx="14" cy="6.5" r="1" />
    </>
  ),
  chart: (
    <>
      <path d="M4 20V10M10 20V4M16 20v-7M22 20H2" />
    </>
  ),
  book: (
    <>
      <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21.5z" />
      <path d="M4 5.5v16M8 7h8M8 11h6" />
    </>
  ),
  logout: (
    <>
      <path d="M10 17l5-5-5-5M15 12H3" />
      <path d="M15 4h4a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-4" />
    </>
  ),
  upload: (
    <>
      <path d="M12 16V4M7 9l5-5 5 5" />
      <path d="M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3" />
    </>
  ),
  image: (
    <>
      <rect x="3" y="4" width="18" height="16" rx="2" />
      <circle cx="8.5" cy="9.5" r="1.5" />
      <path d="m21 15-5-5L5 20" />
    </>
  ),
  doc: (
    <>
      <path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z" />
      <path d="M14 3v5h5M9 13h6M9 17h6" />
    </>
  ),
  clock: (
    <>
      <circle cx="12" cy="12" r="9" />
      <path d="M12 7v5l3 2" />
    </>
  ),
  calendar: (
    <>
      <rect x="3" y="5" width="18" height="16" rx="2" />
      <path d="M8 3v4M16 3v4M3 10h18" />
    </>
  ),
  spark: (
    <>
      <path d="m12 3 1.4 4.6L18 9l-4.6 1.4L12 15l-1.4-4.6L6 9l4.6-1.4z" />
      <path d="m19 15 .7 2.3L22 18l-2.3.7L19 21l-.7-2.3L16 18l2.3-.7z" />
    </>
  ),
  close: <path d="M6 6l12 12M18 6 6 18" />,
  menu: <path d="M4 7h16M4 12h16M4 17h16" />,
  quote: (
    <>
      <path d="M9 11H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v7a4 4 0 0 1-4 4" />
      <path d="M19 11h-4a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v7a4 4 0 0 1-4 4" />
    </>
  ),
  lock: (
    <>
      <rect x="4" y="10" width="16" height="11" rx="2" />
      <path d="M8 10V7a4 4 0 0 1 8 0v3M12 14v3" />
    </>
  ),
  refresh: (
    <>
      <path d="M20 7v5h-5" />
      <path d="M4 17v-5h5" />
      <path d="M6.1 8.5a7 7 0 0 1 11.5-1L20 12M4 12l2.4 4.5a7 7 0 0 0 11.5-1" />
    </>
  ),
  info: (
    <>
      <circle cx="12" cy="12" r="9" />
      <path d="M12 11v5M12 8h.01" />
    </>
  ),
  user: (
    <>
      <circle cx="12" cy="8" r="3.5" />
      <path d="M4.5 20a7.5 7.5 0 0 1 15 0" />
    </>
  ),
  search: (
    <>
      <circle cx="11" cy="11" r="7" />
      <path d="m20 20-4-4" />
    </>
  ),
  external: (
    <>
      <path d="M14 4h6v6M20 4l-8 8" />
      <path d="M19 14v4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h4" />
    </>
  ),
  copy: (
    <>
      <rect x="9" y="9" width="11" height="11" rx="2" />
      <path d="M5 15H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v1" />
    </>
  ),
  message: (
    <>
      <path d="M21 12a8 8 0 0 1-8 8H4l2-3a8 8 0 1 1 15-5Z" />
      <path d="M8 11h.01M12 11h.01M16 11h.01" />
    </>
  ),
  send: (
    <>
      <path d="m22 2-7 20-4-9-9-4z" />
      <path d="M22 2 11 13" />
    </>
  ),
  eye: (
    <>
      <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z" />
      <circle cx="12" cy="12" r="3" />
    </>
  ),
  block: (
    <>
      <circle cx="12" cy="12" r="9" />
      <path d="m5.6 5.6 12.8 12.8" />
    </>
  ),
  sliders: (
    <>
      <path d="M4 7h10M18 7h2M4 17h2M10 17h10" />
      <circle cx="16" cy="7" r="2" />
      <circle cx="8" cy="17" r="2" />
    </>
  ),
  download: (
    <>
      <path d="M12 4v12M7 11l5 5 5-5" />
      <path d="M4 20h16" />
    </>
  ),
};

export function Icon({ name, size = 18, strokeWidth = 1.8, className = '' }) {
  return (
    <svg
      aria-hidden="true"
      className={className}
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      {ICONS[name] || ICONS.spark}
    </svg>
  );
}

export function BrandMark({ size = 34 }) {
  const id = useId().replace(/:/g, '');
  return (
    <svg
      aria-hidden="true"
      width={size}
      height={size}
      viewBox="0 0 40 40"
      className="brand-mark"
    >
      <defs>
        <linearGradient id={`prism-${id}`} x1="4" y1="4" x2="36" y2="36" gradientUnits="userSpaceOnUse">
          <stop stopColor="#6A4CF0" />
          <stop offset="1" stopColor="#0C766E" />
        </linearGradient>
      </defs>
      <rect width="40" height="40" rx="11" fill="#18161B" />
      <path d="M20 6 33 20 20 34 7 20Z" fill={`url(#prism-${id})`} />
      <path d="M20 6v28M7 20h26" stroke="#fff" strokeOpacity=".32" strokeWidth="1.4" />
      <circle cx="20" cy="20" r="3.2" fill="#fff" />
    </svg>
  );
}

export function Brand({ compact = false }) {
  return (
    <span className={classNames('brand', compact && 'brand-compact')}>
      <BrandMark size={compact ? 30 : 34} />
      <span className="brand-word">
        PrismCheck <span className="brand-ai">AI</span>
      </span>
    </span>
  );
}

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  icon,
  iconRight,
  loading = false,
  className = '',
  type = 'button',
  ...props
}) {
  return (
    <button
      type={type}
      className={classNames('btn', `btn-${variant}`, `btn-${size}`, className)}
      disabled={loading || props.disabled}
      {...props}
    >
      {loading ? <Spinner size={16} /> : icon ? <Icon name={icon} size={17} /> : null}
      <span>{children}</span>
      {iconRight ? <Icon name={iconRight} size={17} /> : null}
    </button>
  );
}

export function IconButton({ label, icon, className = '', ...props }) {
  return (
    <button
      type="button"
      className={classNames('icon-btn', className)}
      aria-label={label}
      title={label}
      {...props}
    >
      <Icon name={icon} size={18} />
    </button>
  );
}

export function Badge({ children, tone = 'neutral', dot = false, className = '' }) {
  return (
    <span className={classNames('badge', `badge-${tone}`, className)}>
      {dot ? <span className="badge-dot" /> : null}
      {children}
    </span>
  );
}

export function StatusBadge({ status, label }) {
  const meta = statusMeta(status, label);
  return (
    <Badge tone={meta.tone} dot>
      {label || meta.label}
    </Badge>
  );
}

export function SeverityBadge({ severity }) {
  return (
    <Badge tone={severity === 'hard' ? 'red' : 'amber'}>
      {severity === 'hard' ? 'Hard stop' : 'Soft note'}
    </Badge>
  );
}

export function Avatar({ name = '', size = 36, tone = 0, className = '' }) {
  return (
    <span
      className={classNames('avatar', `avatar-tone-${tone % 5}`, className)}
      style={{ width: size, height: size, fontSize: Math.round(size * 0.34) }}
      aria-hidden="true"
    >
      {initials(name)}
    </span>
  );
}

export function Spinner({ size = 18 }) {
  return <span className="spinner" style={{ width: size, height: size }} aria-hidden="true" />;
}

export function ProgressRing({ value = 0, size = 76, stroke = 7, label, caption }) {
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const clamped = Math.max(0, Math.min(100, value));
  const offset = circumference - (clamped / 100) * circumference;
  return (
    <div className="ring-wrap" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="ring" aria-hidden="true">
        <circle cx={size / 2} cy={size / 2} r={radius} strokeWidth={stroke} className="ring-track" />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={stroke}
          className="ring-value"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
        />
      </svg>
      <span className="ring-label">
        <strong>{label ?? `${Math.round(clamped)}%`}</strong>
        {caption ? <small>{caption}</small> : null}
      </span>
    </div>
  );
}

export function PageHeader({ eyebrow, title, description, actions, back, backLabel = 'Back' }) {
  return (
    <header className="page-header">
      <div className="page-header-main">
        {back ? (
          <button type="button" className="back-link" onClick={back}>
            <Icon name="arrowLeft" size={16} />
            {backLabel}
          </button>
        ) : null}
        {eyebrow ? <p className="eyebrow">{eyebrow}</p> : null}
        <h1 className="page-title">{title}</h1>
        {description ? <p className="page-description">{description}</p> : null}
      </div>
      {actions ? <div className="page-actions">{actions}</div> : null}
    </header>
  );
}

export function EmptyState({ icon = 'spark', title, body, action }) {
  return (
    <div className="empty-state">
      <span className="empty-icon">
        <Icon name={icon} size={22} />
      </span>
      <h3>{title}</h3>
      {body ? <p>{body}</p> : null}
      {action}
    </div>
  );
}

export function LoadingBlock({ label = 'Loading…' }) {
  return (
    <div className="loading-block" role="status">
      <Spinner size={20} />
      <span>{label}</span>
    </div>
  );
}

export function ErrorBlock({ message, onRetry, title = 'We could not load this' }) {
  return (
    <div className="error-block" role="alert">
      <span className="error-icon">
        <Icon name="alert" size={20} />
      </span>
      <div>
        <h3>{title}</h3>
        <p>{message}</p>
      </div>
      {onRetry ? (
        <Button variant="secondary" size="sm" icon="refresh" onClick={onRetry}>
          Try again
        </Button>
      ) : null}
    </div>
  );
}

export function Toast({ toast, onClose }) {
  useEffect(() => {
    if (!toast) return undefined;
    const timer = setTimeout(onClose, 4200);
    return () => clearTimeout(timer);
  }, [toast, onClose]);

  if (!toast) return null;
  return (
    <div className={classNames('toast', `toast-${toast.tone || 'success'}`)} role="status" aria-live="polite">
      <span className="toast-icon">
        <Icon name={toast.tone === 'error' ? 'alert' : toast.tone === 'info' ? 'info' : 'check'} size={17} />
      </span>
      <span>{toast.message}</span>
      <button type="button" className="toast-close" onClick={onClose} aria-label="Dismiss notification">
        <Icon name="close" size={15} />
      </button>
    </div>
  );
}

export function SectionHeading({ eyebrow, title, description, action }) {
  return (
    <div className="section-heading">
      <div>
        {eyebrow ? <p className="eyebrow">{eyebrow}</p> : null}
        <h2>{title}</h2>
        {description ? <p>{description}</p> : null}
      </div>
      {action}
    </div>
  );
}

export function Callout({ tone = 'purple', icon = 'info', title, children }) {
  return (
    <div className={classNames('callout', `callout-${tone}`)}>
      <span className="callout-icon">
        <Icon name={icon} size={18} />
      </span>
      <div>
        {title ? <strong>{title}</strong> : null}
        <div className="callout-body">{children}</div>
      </div>
    </div>
  );
}

export function CopyButton({ value, onCopy, label = 'Copy' }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      type="button"
      className="copy-btn"
      onClick={async () => {
        try {
          await navigator.clipboard.writeText(value);
          setCopied(true);
          onCopy?.(value);
          setTimeout(() => setCopied(false), 1600);
        } catch {
          onCopy?.('Copy failed — select the value manually.');
        }
      }}
    >
      <Icon name={copied ? 'check' : 'copy'} size={14} />
      {copied ? 'Copied' : label}
    </button>
  );
}
