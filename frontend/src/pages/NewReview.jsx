import { useEffect, useRef, useState } from 'react';
import { api, classNames } from '../lib.js';
import { Button, Callout, Icon, PageHeader } from '../ui.jsx';

function Dropzone({ id, accept, label, hint, icon, file, onFile, onClear, compact = false }) {
  const inputRef = useRef(null);
  const [dragging, setDragging] = useState(false);

  function choose(event) {
    const picked = event.target.files?.[0];
    if (picked) onFile(picked);
    event.target.value = '';
  }

  function drop(event) {
    event.preventDefault();
    setDragging(false);
    const picked = event.dataTransfer.files?.[0];
    if (picked) onFile(picked);
  }

  return (
    <div
      className={classNames(
        'dropzone',
        compact && 'dropzone-compact',
        dragging && 'is-dragging',
        file && 'has-file',
      )}
      onDragOver={(event) => {
        event.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={drop}
    >
      <input
        ref={inputRef}
        id={id}
        type="file"
        accept={accept}
        onChange={choose}
        className="visually-hidden"
      />
      {file ? (
        <div className="file-selected">
          <span className="file-icon">
            <Icon name={icon} size={20} />
          </span>
          <div>
            <strong>{file.name}</strong>
            <span>{Math.max(1, Math.round(file.size / 1024))} KB · ready to upload</span>
          </div>
          <button
            type="button"
            className="file-clear"
            onClick={onClear}
            aria-label={`Remove ${file.name}`}
          >
            <Icon name="close" size={16} />
          </button>
        </div>
      ) : (
        <button type="button" className="dropzone-button" onClick={() => inputRef.current?.click()}>
          <span className="drop-icon">
            <Icon name={icon} size={21} />
          </span>
          <span>
            <strong>{label}</strong>
            <span className="drop-hint">{hint}</span>
          </span>
          <span className="drop-action">
            <Icon name="upload" size={16} />
          </span>
        </button>
      )}
    </div>
  );
}

export default function NewReview({ user, navigate, notify }) {
  const [title, setTitle] = useState('');
  const [caption, setCaption] = useState('');
  const [altText, setAltText] = useState('');
  const [image, setImage] = useState(null);
  const [document, setDocument] = useState(null);
  const [preview, setPreview] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!image) {
      setPreview('');
      return undefined;
    }
    const url = URL.createObjectURL(image);
    setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [image]);

  async function submit(event) {
    event.preventDefault();
    setError('');
    if (!title.trim()) {
      setError('Give the draft a title.');
      return;
    }
    if (!caption.trim() && !document && !image) {
      setError('Add a caption, artwork, or a document so there is something to review.');
      return;
    }
    const form = new FormData();
    form.append('title', title.trim());
    form.append('caption', caption.trim());
    form.append('alt_text', altText.trim());
    form.append('kit_id', 'kit-northwind');
    if (image) form.append('image', image);
    if (document) form.append('document', document);

    setBusy(true);
    try {
      const data = await api.createDraft(form);
      notify('Draft reviewed. Every finding is cited.');
      navigate(`/drafts/${data.draft.id}`);
    } catch (err) {
      setError(err.message);
      setBusy(false);
    }
  }

  return (
    <div className="page new-review">
      <PageHeader
        back={() => navigate('/')}
        backLabel="Workspace"
        eyebrow="New review"
        title="Put a draft through the kit."
        description="Caption, artwork, and documents are checked against the same seven rules. Every finding comes back with a source and a fix."
      />

      <form className="review-form" onSubmit={submit}>
        <div className="form-main">
          <section className="panel form-panel">
            <div className="panel-head">
              <div>
                <p className="eyebrow">01 · The copy</p>
                <h2>What are we reviewing?</h2>
              </div>
            </div>

            <label className="field">
              <span className="field-label">
                Draft title <span className="required">required</span>
              </span>
              <input
                type="text"
                value={title}
                onChange={(event) => setTitle(event.target.value)}
                placeholder="e.g. Signature card launch"
                maxLength={120}
                autoFocus
              />
            </label>

            <label className="field">
              <span className="field-label">
                Caption <span className="optional">or attach a document below</span>
              </span>
              <textarea
                rows={5}
                value={caption}
                onChange={(event) => setCaption(event.target.value)}
                placeholder="Paste the customer-facing caption exactly as it will run…"
              />
              <span className="field-hint">{caption.length} characters · checked live on submit</span>
            </label>

            <label className="field">
              <span className="field-label">
                Alt text <span className="optional">for the artwork</span>
              </span>
              <input
                type="text"
                value={altText}
                onChange={(event) => setAltText(event.target.value)}
                placeholder="Describe the image for someone who cannot see it"
              />
              <span className="field-hint">
                Rule A-03 requires descriptive alt text. Missing text is a hard finding.
              </span>
            </label>
          </section>

          <section className="panel form-panel">
            <div className="panel-head">
              <div>
                <p className="eyebrow">02 · Context</p>
                <h2>Artwork &amp; documents</h2>
              </div>
            </div>

            <div className="upload-grid">
              <div>
                <span className="field-label">Artwork</span>
                {preview ? (
                  <div className="image-preview">
                    <img src={preview} alt="Selected artwork preview" />
                    <div className="image-preview-bar">
                      <span>{image?.name}</span>
                      <button type="button" onClick={() => setImage(null)}>
                        Replace
                      </button>
                    </div>
                  </div>
                ) : (
                  <Dropzone
                    id="artwork"
                    accept="image/png,image/jpeg,image/webp"
                    label="Drop artwork here"
                    hint="PNG, JPG or WebP · up to 8 MB"
                    icon="image"
                    file={image}
                    onFile={setImage}
                    onClear={() => setImage(null)}
                  />
                )}
                <span className="field-hint">Palette and contrast are sampled from the pixels.</span>
              </div>

              <div>
                <span className="field-label">Document</span>
                <Dropzone
                  id="document"
                  accept=".pdf,.docx"
                  label="Attach a PDF or DOCX"
                  hint="Optional · text is extracted and reviewed"
                  icon="doc"
                  file={document}
                  onFile={setDocument}
                  onClear={() => setDocument(null)}
                  compact
                />
                <span className="field-hint">Useful for long-form copy, terms, or a brief.</span>
              </div>
            </div>
          </section>

          {error ? (
            <div className="form-error form-error-box" role="alert">
              <Icon name="alert" size={17} />
              {error}
            </div>
          ) : null}

          <div className="form-submit">
            <div>
              <strong>Ready when you are.</strong>
              <p>The review is deterministic, cited, and usually takes under a second.</p>
            </div>
            <Button type="submit" icon="spark" loading={busy}>
              Run review
            </Button>
          </div>
        </div>

        <aside className="form-rail">
          <section className="panel rail-card">
            <p className="eyebrow">What gets checked</p>
            <ul className="check-list">
              <li>
                <span className="check-list-icon purple">
                  <Icon name="alert" size={16} />
                </span>
                <div>
                  <strong>Claims &amp; promises</strong>
                  <p>Every number, fee, and guarantee against the approved fact bank.</p>
                </div>
              </li>
              <li>
                <span className="check-list-icon amber">
                  <Icon name="message" size={16} />
                </span>
                <div>
                  <strong>Tone &amp; vocabulary</strong>
                  <p>Urgency, absolutes, and preferred words in one pass.</p>
                </div>
              </li>
              <li>
                <span className="check-list-icon teal">
                  <Icon name="palette" size={16} />
                </span>
                <div>
                  <strong>Palette &amp; contrast</strong>
                  <p>CIELAB distance from the kit plus WCAG contrast on artwork.</p>
                </div>
              </li>
              <li>
                <span className="check-list-icon red">
                  <Icon name="eye" size={16} />
                </span>
                <div>
                  <strong>Accessibility</strong>
                  <p>Alt text and text contrast, checked before anything ships.</p>
                </div>
              </li>
            </ul>
          </section>

          <Callout tone="purple" icon="shield" title="The Citation Lock">
            Model output only reaches the screen if its <code>source_id</code> resolves to a rule,
            fact, or palette entry. Uncited findings are dropped and counted.
          </Callout>

          <section className="panel rail-card quiet-card">
            <span className="quiet-icon">
              <Icon name="clock" size={17} />
            </span>
            <h3>Runs in the workspace</h3>
            <p>
              No copy leaves the demo unless a model provider is configured. The local engine is
              the default.
            </p>
          </section>
        </aside>
      </form>
    </div>
  );
}
