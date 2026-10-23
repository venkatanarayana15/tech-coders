from __future__ import annotations

"""Citation Lock: a finding is only displayable if its source resolves to a kit item."""

from typing import Any


def resolve_source(kit: dict[str, Any], source_id: str | None) -> dict[str, Any] | None:
    if not source_id:
        return None

    for rule in kit.get("rules", []):
        if rule["id"] == source_id:
            return {
                "type": "rule",
                "id": rule["id"],
                "label": rule["label"],
                "quote": rule["text"],
            }

    for fact in kit.get("facts", []):
        if fact["id"] == source_id:
            return {
                "type": "fact",
                "id": fact["id"],
                "label": f"Approved fact · {fact['category']}",
                "quote": fact["text"],
            }

    for colour in kit.get("palette", []):
        if colour["id"] == source_id:
            return {
                "type": "asset",
                "id": colour["id"],
                "label": f"Palette · {colour['name']}",
                "quote": f"{colour['hex']} · {colour['role']}",
            }

    for entry in kit.get("banned", []):
        if entry["id"] == source_id:
            return resolve_source(kit, entry.get("rule_id"))

    for entry in kit.get("preferred", []):
        if entry["id"] == source_id:
            return resolve_source(kit, entry.get("rule_id"))

    return None


def enforce_citations(
    findings: list[dict[str, Any]], kit: dict[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    kept: list[dict[str, Any]] = []
    dropped: list[dict[str, str]] = []

    for finding in findings:
        source = resolve_source(kit, finding.get("source_id"))
        if source is None:
            dropped.append(
                {
                    "rule_id": str(finding.get("rule_id") or "unknown"),
                    "reason": "source_id did not resolve to a kit item",
                }
            )
            continue
        finding = dict(finding)
        finding["source"] = source
        kept.append(finding)

    received = len(findings)
    coverage = 100.0 if kept or received == 0 else 0.0
    return kept, {
        "received": received,
        "kept": len(kept),
        "dropped": len(dropped),
        "coverage": coverage,
        "dropped_detail": dropped,
    }
