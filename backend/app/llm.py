"""Optional model adapters.

The product is fully functional without a cloud key: deterministic checks and
retrieval handle the review. When Gemini or a local Ollama model is configured,
the adapter may add claim findings, and those findings still pass Citation Lock.

Provider order in ``auto`` mode: Gemini (if a key is present), then Ollama (if a
model is installed and the daemon answers), then the local engine.
"""

from __future__ import annotations

import json
import time
import uuid
from typing import Any

import httpx

from .config import settings

_IDENTITY_CACHE: dict[str, Any] = {"at": 0.0, "value": None}
_IDENTITY_TTL = 20.0


def _ollama_models() -> list[str]:
    try:
        response = httpx.get(f"{settings.ollama_host}/api/tags", timeout=1.2)
        response.raise_for_status()
        return [item["name"] for item in response.json().get("models", [])]
    except Exception:
        return []


def model_identity(force: bool = False) -> dict[str, str]:
    now = time.time()
    if not force and _IDENTITY_CACHE["value"] and now - _IDENTITY_CACHE["at"] < _IDENTITY_TTL:
        return dict(_IDENTITY_CACHE["value"])

    mode = settings.model_mode
    identity: dict[str, str]

    if mode in {"auto", "gemini"} and settings.gemini_api_key:
        identity = {"engine": "gemini", "model": settings.gemini_model, "status": "ready"}
    elif mode in {"auto", "ollama"}:
        models = _ollama_models()
        chosen = settings.ollama_model or (models[0] if models else "")
        if chosen and (not models or chosen in models or settings.ollama_model):
            identity = {
                "engine": "ollama",
                "model": chosen,
                "status": "ready" if models else "unavailable",
            }
        else:
            identity = {
                "engine": "local",
                "model": "PrismCheck Review Engine v1",
                "status": "ready",
            }
    elif mode == "gemini" and not settings.gemini_api_key:
        identity = {
            "engine": "local",
            "model": "PrismCheck Review Engine v1",
            "status": "fallback",
        }
    else:
        identity = {
            "engine": "local",
            "model": "PrismCheck Review Engine v1",
            "status": "ready",
        }

    _IDENTITY_CACHE.update({"at": now, "value": identity})
    return dict(identity)


def _prompt(kit: dict[str, Any], text: str) -> tuple[str, dict[str, Any]]:
    rules = [
        {"id": rule["id"], "label": rule["label"], "text": rule["text"]}
        for rule in kit.get("rules", [])
        if rule.get("check") in {"claims", "tone"}
    ]
    facts = [{"id": fact["id"], "text": fact["text"]} for fact in kit.get("facts", [])]
    allowed = [item["id"] for item in rules] + [item["id"] for item in facts]

    instruction = (
        "You review a marketing draft against an approved brand kit. "
        "Return ONLY claim findings that the draft makes and that the approved facts do not support. "
        "Never invent a fact or a rule. Use only an allowed source_id. "
        "Each quote must be an exact substring of the draft. "
        "Give at most two fixes per finding; fixes must be grounded in an approved fact. "
        "Return JSON only, matching the schema.\n\n"
        f"Allowed source_id values: {', '.join(allowed)}\n\n"
        f"Approved rules:\n{json.dumps(rules, ensure_ascii=False)}\n\n"
        f"Approved facts:\n{json.dumps(facts, ensure_ascii=False)}\n\n"
        f"Draft:\n{text[:4000]}"
    )

    schema = {
        "type": "object",
        "properties": {
            "claims": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "quote": {"type": "string"},
                        "source_id": {"type": "string"},
                        "explanation": {"type": "string"},
                        "fixes": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "label": {"type": "string"},
                                    "text": {"type": "string"},
                                },
                                "required": ["label", "text"],
                            },
                        },
                    },
                    "required": ["quote", "source_id", "explanation", "fixes"],
                },
            }
        },
        "required": ["claims"],
    }
    return instruction, schema


def _call_gemini(prompt: str, schema: dict[str, Any]) -> str:
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{settings.gemini_model}:generateContent"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "application/json",
            "responseSchema": schema,
        },
    }
    with httpx.Client(timeout=12.0) as client:
        response = client.post(
            url,
            params={"key": settings.gemini_api_key},
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


def _call_ollama(prompt: str, model: str) -> str:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.1, "num_predict": 700},
    }
    with httpx.Client(timeout=25.0) as client:
        response = client.post(f"{settings.ollama_host}/api/chat", json=payload)
        response.raise_for_status()
        return response.json()["message"]["content"]


def propose_model_findings(
    kit: dict[str, Any], text: str, caption: str, doc_text: str
) -> tuple[list[dict[str, Any]], str | None]:
    identity = model_identity()
    if identity.get("status") != "ready" or identity.get("engine") == "local":
        return [], None

    prompt, schema = _prompt(kit, text)
    raw: str | None = None
    error: str | None = None
    for attempt in range(2):
        try:
            if identity["engine"] == "gemini":
                raw = _call_gemini(prompt, schema)
            else:
                raw = _call_ollama(prompt, identity["model"])
            break
        except Exception as exc:  # noqa: BLE001 - surfaced as a status, never a crash
            error = type(exc).__name__
            time.sleep(0.4 if attempt == 0 else 0)

    if not raw:
        return [], error or "model_unavailable"

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return [], "invalid_json"

    lowered = text.lower()
    out: list[dict[str, Any]] = []
    for item in data.get("claims", [])[:4]:
        quote = str(item.get("quote", "")).strip()
        source_id = str(item.get("source_id", "")).strip()
        if not quote or not source_id or quote.lower() not in lowered:
            continue
        fixes = []
        for fix in item.get("fixes", [])[:2]:
            fix_text = str(fix.get("text", "")).strip()
            if fix_text:
                fixes.append(
                    {
                        "label": str(fix.get("label", "Suggested fix"))[:60],
                        "text": fix_text[:240],
                        "kind": "text",
                    }
                )
        if not fixes:
            continue
        out.append(
            {
                "id": f"fnd-{uuid.uuid4().hex[:10]}",
                "check": "claims",
                "rule_id": "C-01",
                "severity": "hard",
                "title": f"Unsupported claim: “{quote[:54]}”",
                "detail": str(item.get("explanation", "The approved facts do not support this claim."))[:400],
                "quote": quote,
                "field": "caption" if quote.lower() in caption.lower() else "document",
                "source_id": source_id,
                "fixes": fixes,
                "measured": None,
                "proposed_by": identity["engine"],
            }
        )
    return out, error
