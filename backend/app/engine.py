"""The review engine.

Deterministic checks run first and never depend on a model. A model, when one is
configured, may add claim findings, but every finding still has to pass Citation
Lock before it can be stored or displayed.
"""

from __future__ import annotations

import re
import time
import uuid
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

from .citation import enforce_citations
from .llm import model_identity, propose_model_findings

WORD_RE = re.compile(r"[a-z0-9]+(?:\.[0-9]+)?%?")
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is",
    "it", "of", "on", "or", "that", "the", "to", "was", "we", "with", "your",
    "you", "our", "this", "plus", "per", "over", "into", "than", "then",
}

CLAIM_PATTERNS = [
    re.compile(r"\b(?:no|zero)\s+[a-z]+\s+(?:fee|fees|cost|charge|charges)\b[^.!?;]*", re.I),
    re.compile(
        r"\b\d{1,3}(?:\.\d+)?%\s*(?:cashback|reward|rewards|interest|off|discount|savings?)\b[^.!?;]*",
        re.I,
    ),
    re.compile(r"\b(?:for life|lifetime|unlimited|best|cheapest|#1)\b[^.!?;]*", re.I),
]

URGENCY = [
    ("act now", "Apply when you are ready."),
    ("hurry", "Take your time."),
    ("last chance", "This offer is available for a set period."),
    ("don't miss", "You may want to consider this offer."),
    ("limited time", "This offer is available for a set period."),
    ("ends soon", "The offer end date is stated in the terms."),
]

ABSOLUTE_SOFT = ["always", "never", "everyone", "nobody", "unbeatable", "perfect"]

INTENTS = {
    "promotional announcement": ["offer", "launch", "cashback", "reward", "apply", "card"],
    "reassurance": ["safe", "secure", "protected", "support", "help"],
    "warning": ["alert", "warning", "avoid", "important", "notice"],
    "celebration": ["congratulations", "celebrate", "welcome", "anniversary"],
}


def _finding(**kwargs: Any) -> dict[str, Any]:
    base = {
        "id": f"fnd-{uuid.uuid4().hex[:10]}",
        "check": "claims",
        "rule_id": "C-01",
        "severity": "soft",
        "title": "",
        "detail": "",
        "quote": "",
        "field": "caption",
        "source_id": None,
        "fixes": [],
        "measured": None,
    }
    base.update(kwargs)
    return base


def _tokens(text: str) -> list[str]:
    out: list[str] = []
    for token in WORD_RE.findall(text.lower()):
        if token in STOPWORDS:
            continue
        if len(token) > 3 and token.endswith("s"):
            token = token[:-1]
        out.append(token)
    return out


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


_AADHAAR_RE = re.compile(r"\b\d{4}[ -]\d{4}[ -]\d{4}\b|\b\d{12}\b")
_EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
_PHONE_RE = re.compile(
    r"(?<![\w])\+?(?:\d{1,3}[-. ]?)?(?:\(\d{2,5}\)[-. ]?)?\d{4,5}[-. ]?\d{3,5}(?![\w])"
)


def mask_pii(text: str) -> str:
    """Replace obvious personal identifiers before text is stored or reviewed."""
    if not text:
        return text
    masked = _AADHAAR_RE.sub("[ID]", text)
    masked = _EMAIL_RE.sub("[email]", masked)
    masked = _PHONE_RE.sub("[phone]", masked)
    return masked


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [p.strip() for p in parts if p.strip()]


def _truncate(text: str, limit: int = 78) -> str:
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _linear(channel: int) -> float:
    c = channel / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(value: str) -> float:
    r, g, b = (_linear(c) for c in _hex_to_rgb(value))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a: str, b: str) -> float:
    la, lb = relative_luminance(a), relative_luminance(b)
    light, dark = max(la, lb), min(la, lb)
    return (light + 0.05) / (dark + 0.05)


def _lab(value: str) -> tuple[float, float, float]:
    r, g, b = (_linear(c) for c in _hex_to_rgb(value))
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e(a: str, b: str) -> float:
    la, aa, ba = _lab(a)
    lb, ab, bb = _lab(b)
    return float(np.sqrt((la - lb) ** 2 + (aa - ab) ** 2 + (ba - bb) ** 2))


def _clusters(path: Path, count: int = 8) -> list[dict[str, Any]]:
    image = Image.open(path).convert("RGB")
    image.thumbnail((220, 220))
    quantised = image.quantize(colors=count, method=Image.Quantize.MEDIANCUT).convert("RGB")
    colours = quantised.getcolors(maxcolors=image.width * image.height) or []
    total = sum(n for n, _ in colours) or 1
    out = []
    for n, rgb in colours:
        out.append(
            {
                "hex": "#{:02X}{:02X}{:02X}".format(*rgb),
                "share": round(n / total, 4),
            }
        )
    out.sort(key=lambda item: item["share"], reverse=True)
    return out


def _nearest_palette(hex_value: str, palette: list[dict[str, Any]]) -> tuple[dict[str, Any], float]:
    scored = [(colour, delta_e(hex_value, colour["hex"])) for colour in palette]
    scored.sort(key=lambda pair: pair[1])
    return scored[0]


def _best_fact(text: str, facts: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, float]:
    wanted = set(_tokens(text))
    best: dict[str, Any] | None = None
    best_score = 0.0
    for fact in facts:
        overlap = wanted & set(_tokens(fact["text"]))
        score = len(overlap) / max(1, len(wanted))
        if score > best_score:
            best, best_score = fact, score
    return best, round(best_score, 3)


def _is_supported(span: str, facts: list[dict[str, Any]]) -> tuple[bool, dict[str, Any] | None, float]:
    wanted = set(_tokens(span))
    best: dict[str, Any] | None = None
    best_score = 0.0
    for fact in facts:
        fact_tokens = set(_tokens(fact["text"]))
        if wanted and wanted <= fact_tokens:
            return True, fact, 1.0
        score = len(wanted & fact_tokens) / max(1, len(wanted))
        if score > best_score:
            best, best_score = fact, score
    return False, best, round(best_score, 3)


def _field_for(quote: str, caption: str, doc_text: str) -> str:
    if quote and _normalise(quote) in _normalise(caption):
        return "caption"
    if quote and _normalise(quote) in _normalise(doc_text):
        return "document"
    return "caption"


def classify_intent(text: str) -> str:
    lowered = text.lower()
    scores = {
        intent: sum(1 for word in words if word in lowered)
        for intent, words in INTENTS.items()
    }
    best = max(scores, key=scores.get)
    return best if scores[best] else "informational"


def check_claims(text: str, caption: str, doc_text: str, kit: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    facts = kit.get("facts", [])
    banned = kit.get("banned", [])
    seen_spans: list[str] = []
    for sentence in _sentences(text):
        banned_ranges: list[tuple[int, int]] = []
        for entry in banned:
            for match in re.finditer(re.escape(entry["term"]), sentence, re.I):
                banned_ranges.append((match.start(), match.end()))
        if banned_ranges:
            chars = list(sentence)
            for left, right in banned_ranges:
                chars[left:right] = " " * (right - left)
            searchable = "".join(chars)
        else:
            searchable = sentence
        for pattern in CLAIM_PATTERNS:
            for match in pattern.finditer(searchable):
                raw_span = match.group(0)
                span = re.sub(r"\s+", " ", raw_span).strip(" ,;:")
                span = re.sub(r"[\s,;:]*(?:with|and|plus|but|for|on|at|from|to|by|of)\s*$", "", span, flags=re.I)
                span = span.strip(" ,;:")
                if len(span) < 4:
                    continue
                supported, closest, overlap = _is_supported(span, facts)
                if supported:
                    continue
                fix_text = closest["text"] if closest else span
                if closest:
                    prefix = searchable[: match.start()].rstrip(" ,;:")
                    first_word = fix_text.split(maxsplit=1)[0]
                    if prefix.lower().endswith(first_word.lower()) and len(fix_text.split(maxsplit=1)) > 1:
                        fix_text = fix_text.split(maxsplit=1)[1]
                    tail = searchable[match.end():].lstrip()
                    if "," in raw_span or tail.startswith(","):
                        fix_text = fix_text.rstrip(".")
                fixes = [
                    {
                        "label": "Use the approved fact",
                        "text": fix_text,
                        "kind": "text",
                    }
                ]
                if closest:
                    fixes.append(
                        {
                            "label": "Ground it explicitly",
                            "text": f"Per our approved facts: {fix_text[0].lower() + fix_text[1:]}",
                            "kind": "text",
                        }
                    )
                else:
                    fixes.append(
                        {
                            "label": "Remove the claim",
                            "text": "",
                            "kind": "text",
                        }
                    )
                norm_span = _normalise(span)
                if any(norm_span in kept for kept in seen_spans):
                    continue
                seen_spans.append(norm_span)

                findings.append(
                    _finding(
                        check="claims",
                        rule_id="C-01",
                        severity="hard",
                        title=f"Unsupported claim: “{_truncate(span, 54)}”",
                        detail=(
                            f"“{span}” does not match any approved fact in the fact bank. "
                            + (
                                f"The closest approved fact is {closest['id']} — “{closest['text']}”."
                                if closest
                                else "No approved fact is close enough to support it."
                            )
                        ),
                        quote=span,
                        field=_field_for(span, caption, doc_text),
                        source_id="C-01",
                        fixes=fixes,
                        measured={"closest_fact": closest["id"] if closest else None, "overlap": overlap},
                    )
                )
    return findings


def _clause_for(sentence: str, term: str) -> str:
    for part in re.split(r",\s*", sentence):
        if term.lower() in part.lower():
            return part.strip(" ,;.")
    return sentence.strip(" ,;.")


def _grounded_phrase(fact_text: str, clause: str) -> str:
    phrase = fact_text.rstrip(".").strip()
    connector = ""
    match = re.match(r"^(with|and|plus|but)\s+", clause, re.I)
    if match:
        connector = match.group(1).lower()
    if clause[:1].islower() or connector:
        phrase = phrase[:1].lower() + phrase[1:]
    return f"{connector} {phrase}".strip()


def check_banned(text: str, caption: str, doc_text: str, kit: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    facts = kit.get("facts", [])
    for sentence in _sentences(text):
        hits = [entry for entry in kit.get("banned", []) if entry["term"].lower() in sentence.lower()]
        if not hits:
            continue
        rule_id = hits[0].get("rule_id", "T-14")
        clause = _clause_for(sentence, hits[0]["term"])
        if not clause:
            clause = hits[0]["term"]
        fact, _ = _best_fact(clause, facts)
        fixes = []
        if fact:
            grounded = _grounded_phrase(fact["text"], clause)
            fixes = [
                {
                    "label": "Replace with the approved fact",
                    "text": grounded,
                    "kind": "text",
                },
                {
                    "label": "Soften the promise",
                    "text": "Here is what we can confirm: " + grounded[:1].lower() + grounded[1:],
                    "kind": "text",
                },
            ]
        else:
            softened = clause
            for hit in hits:
                softened = re.sub(re.escape(hit["term"]), "", softened, flags=re.I)
            softened = re.sub(r"\s+", " ", softened).strip(" ,;.")
            fixes = [
                {
                    "label": "Remove the banned promise",
                    "text": softened,
                    "kind": "text",
                },
                {
                    "label": "Remove this clause",
                    "text": "",
                    "kind": "text",
                },
            ]
        terms = ", ".join(f"“{hit['term']}”" for hit in hits)
        findings.append(
            _finding(
                check="claims",
                rule_id=rule_id,
                severity="hard",
                title=f"Banned promise: “{_truncate(clause, 58)}”",
                detail=(
                    f"This clause contains {terms}. Rule {rule_id} prohibits absolute "
                    "guarantees in any channel or format."
                ),
                quote=clause,
                field=_field_for(clause, caption, doc_text),
                source_id=rule_id,
                fixes=fixes,
                measured={"terms": [hit["term"] for hit in hits]},
            )
        )
    return findings


def check_tone(text: str, caption: str, doc_text: str, kit: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    lowered = text.lower()

    for term, alternative in URGENCY:
        if term not in lowered:
            continue
        quote = term
        findings.append(
            _finding(
                check="tone",
                rule_id="T-02",
                severity="soft",
                title=f"Urgent phrasing: “{term}”",
                detail=(
                    f"“{term}” adds pressure that the Northwind tone rule T-02 asks writers to avoid. "
                    "Keep the invitation, drop the urgency."
                ),
                quote=quote,
                field=_field_for(quote, caption, doc_text),
                source_id="T-02",
                fixes=[
                    {"label": "Remove the pressure", "text": alternative, "kind": "text"},
                    {"label": "Calm rewrite", "text": "Apply when it suits you.", "kind": "text"},
                ],
            )
        )

    for term in ABSOLUTE_SOFT:
        if re.search(rf"\b{re.escape(term)}\b", lowered):
            findings.append(
                _finding(
                    check="tone",
                    rule_id="T-02",
                    severity="soft",
                    title=f"Absolute wording: “{term}”",
                    detail=(
                        f"“{term}” reads as an absolute. Tone rule T-02 asks for calm, "
                        "specific statements over absolutes."
                    ),
                    quote=term,
                    field=_field_for(term, caption, doc_text),
                    source_id="T-02",
                    fixes=[
                        {"label": "Make it specific", "text": "in most cases", "kind": "text"},
                        {"label": "Keep it factual", "text": "according to the approved terms", "kind": "text"},
                    ],
                )
            )

    for entry in kit.get("preferred", []):
        if re.search(rf"\b{re.escape(entry['from'])}\b", lowered):
            findings.append(
                _finding(
                    check="tone",
                    rule_id=entry.get("rule_id", "T-03"),
                    severity="soft",
                    title=f"Preferred wording: use “{entry['to']}”",
                    detail=(
                        f"The kit prefers “{entry['to']}” over “{entry['from']}”. "
                        "Preferred vocabulary keeps the same meaning in plainer language."
                    ),
                    quote=entry["from"],
                    field=_field_for(entry["from"], caption, doc_text),
                    source_id=entry.get("rule_id", "T-03"),
                    fixes=[
                        {"label": "Use the preferred word", "text": entry["to"], "kind": "text"},
                        {"label": "Keep the meaning", "text": entry["to"], "kind": "text"},
                    ],
                )
            )
    return findings


def check_image(path: Path, caption: str, alt_text: str, kit: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if not path.exists():
        return findings

    palette = kit.get("palette", [])
    tolerance = kit.get("tolerance", {}).get("delta_e", 12)
    raw_clusters = _clusters(path)
    clusters = [c for c in raw_clusters if c["share"] >= 0.04]

    worst: tuple[dict[str, Any], dict[str, Any], float] | None = None
    for cluster in clusters[:4]:
        nearest, distance = _nearest_palette(cluster["hex"], palette)
        if distance > tolerance and (worst is None or distance > worst[2]):
            worst = (cluster, nearest, distance)

    if worst:
        cluster, nearest, distance = worst
        primary = next((c for c in palette if c["role"] == "primary"), nearest)
        accent = next((c for c in palette if c["role"] == "accent"), nearest)
        findings.append(
            _finding(
                check="visual",
                rule_id="V-05",
                severity="soft",
                title=f"Off-palette colour {cluster['hex']}",
                detail=(
                    f"This colour covers {cluster['share'] * 100:.0f}% of the image and sits "
                    f"ΔE {distance:.1f} from the nearest approved colour ({nearest['name']} {nearest['hex']}). "
                    f"Rule V-05 allows ΔE {tolerance}."
                ),
                quote=cluster["hex"],
                field="image",
                source_id="V-05",
                fixes=[
                    {
                        "label": f"Use {nearest['name']}",
                        "text": f"Replace {cluster['hex']} with {nearest['hex']} ({nearest['name']}).",
                        "kind": "guidance",
                    },
                    {
                        "label": "Use the brand pair",
                        "text": f"Use {primary['hex']} for the field and {accent['hex']} for one accent only.",
                        "kind": "guidance",
                    },
                ],
                measured={
                    "hex": cluster["hex"],
                    "share": cluster["share"],
                    "nearest_id": nearest["id"],
                    "nearest_hex": nearest["hex"],
                    "nearest_name": nearest["name"],
                    "delta_e": round(distance, 1),
                    "tolerance": tolerance,
                },
            )
        )

    if len(raw_clusters) >= 2:
        background = raw_clusters[0]
        candidates = [c for c in raw_clusters[1:] if c["share"] >= 0.008]
        if candidates:
            foreground = max(candidates, key=lambda c: contrast_ratio(c["hex"], background["hex"]))
            ratio = contrast_ratio(foreground["hex"], background["hex"])
            threshold = kit.get("tolerance", {}).get("min_contrast", 4.5)
            if ratio < threshold:
                ink = next((c for c in palette if c["role"] == "text"), {"hex": "#101322", "name": "Ink"})
                mist = next((c for c in palette if c["name"] == "Mist"), {"hex": "#EEF1FB", "name": "Mist"})
                ink_ratio = contrast_ratio(ink["hex"], background["hex"])
                pair_ratio = contrast_ratio(ink["hex"], mist["hex"])
                findings.append(
                    _finding(
                        check="accessibility",
                        rule_id="A-03",
                        severity="hard",
                        title=f"Low text contrast: {ratio:.1f}:1",
                        detail=(
                            f"The dominant text and background pair ({foreground['hex']} on "
                            f"{background['hex']}) measures {ratio:.1f}:1. WCAG 2.2 SC 1.4.3 and "
                            f"rule A-03 require {threshold}:1 for body text."
                        ),
                        quote=f"{foreground['hex']} on {background['hex']}",
                        field="image",
                        source_id="A-03",
                        fixes=[
                            {
                                "label": f"Set text to {ink['name']}",
                                "text": (
                                    f"Set the text to {ink['hex']} — {ink_ratio:.1f}:1 on "
                                    f"{background['hex']}."
                                    if ink_ratio >= threshold
                                    else f"Switch to {ink['hex']} on {mist['hex']} — {pair_ratio:.1f}:1."
                                ),
                                "kind": "guidance",
                            },
                            {
                                "label": "Use the approved pair",
                                "text": (
                                    f"Use {ink['hex']} text on {mist['hex']} — {pair_ratio:.1f}:1, "
                                    "the kit's accessible pair."
                                ),
                                "kind": "guidance",
                            },
                        ],
                        measured={
                            "ratio": round(ratio, 2),
                            "foreground": foreground["hex"],
                            "background": background["hex"],
                            "threshold": threshold,
                            "standard": "WCAG 2.2 SC 1.4.3",
                        },
                    )
                )

    if not alt_text.strip():
        rewards = next((f for f in kit.get("facts", []) if f["category"] == "rewards"), None)
        suggested = f"Northwind Signature banner: {caption.strip().rstrip('.')[:110]}."
        if rewards:
            suggested = f"Northwind Signature card artwork. {rewards['text']}"
        findings.append(
            _finding(
                check="accessibility",
                rule_id="A-03",
                severity="hard",
                title="Image has no alternative text",
                detail=(
                    "This image has no alt text. Rule A-03 requires descriptive alternative "
                    "text so the message survives for screen-reader users."
                ),
                quote="(image has no alt text)",
                field="alt_text",
                source_id="A-03",
                fixes=[
                    {"label": "Use the suggested description", "text": suggested, "kind": "text"},
                    {
                        "label": "Describe the offer",
                        "text": "Northwind Signature card announcement with the approved cashback offer.",
                        "kind": "text",
                    },
                ],
            )
        )
    return findings


def _dedupe(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, Any]] = []
    for finding in findings:
        key = (finding.get("rule_id", ""), _normalise(finding.get("quote", ""))[:90])
        if key in seen:
            continue
        seen.add(key)
        out.append(finding)
    return out


def run_review(
    kit: dict[str, Any],
    caption: str,
    alt_text: str = "",
    image_path: Path | None = None,
    doc_text: str = "",
    use_model: bool = True,
) -> dict[str, Any]:
    started = time.perf_counter()
    text = "\n".join(part for part in [caption, doc_text] if part.strip())
    findings: list[dict[str, Any]] = []

    findings += check_banned(text, caption, doc_text, kit)
    findings += check_claims(text, caption, doc_text, kit)
    findings += check_tone(text, caption, doc_text, kit)

    checks_run = ["claims", "tone"]
    if image_path is not None:
        findings += check_image(image_path, caption, alt_text, kit)
        checks_run += ["visual", "accessibility"]

    identity = (
        model_identity()
        if use_model
        else {"engine": "local", "model": "PrismCheck Review Engine v1", "status": "ready"}
    )
    model_error: str | None = None
    if use_model and identity.get("status") == "ready" and identity.get("engine") != "local":
        proposals, model_error = propose_model_findings(kit, text, caption, doc_text)
        for proposal in proposals:
            proposal.setdefault("rule_id", "C-01")
            proposal.setdefault("check", "claims")
            proposal.setdefault("severity", "hard")
            proposal.setdefault("field", _field_for(proposal.get("quote", ""), caption, doc_text))
            findings.append(proposal)

    findings = _dedupe(findings)
    kept, lock = enforce_citations(findings, kit)

    checks_run = sorted(set(checks_run))
    return {
        "findings": kept,
        "meta": {
            "engine": identity.get("engine", "local"),
            "model": identity.get("model", "PrismCheck Review Engine v1"),
            "model_status": "error" if model_error else identity.get("status", "ready"),
            "model_error": model_error,
            "intent": classify_intent(text),
            "checks_run": checks_run,
            "rules_checked": len(kit.get("rules", [])) + len(kit.get("facts", [])),
            "citation_lock": lock,
            "duration_ms": int((time.perf_counter() - started) * 1000),
        },
    }
