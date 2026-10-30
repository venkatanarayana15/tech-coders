"""Unit tests for the PrismCheck review engine.

Run from the repository root:
    python -m pytest backend/tests -q
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.engine import check_banned, check_claims, check_tone, mask_pii
from app.kit_seed import KIT
from app.services import _replace_first_case


def test_no_overlapping_claim_findings():
    text = "Earn 5% cashback guaranteed for life. Act now."
    claims = [f for f in check_claims(text, text, "", KIT) if f["rule_id"] == "C-01"]
    assert len(claims) == 1
    assert "5% cashback for life" in claims[0]["quote"]


def test_approved_fact_is_not_flagged():
    text = "Earn 2.5% cashback on everyday spend, capped at ₹12,000 a year."
    findings = check_claims(text, text, "", KIT)
    assert findings == []


def test_mask_pii_replaces_identifiers():
    masked = mask_pii("Call +91 98765 43210 or rahul@example.com Aadhaar 1234 5678 9012.")
    assert "[phone]" in masked
    assert "+[phone]" not in masked
    assert "[email]" in masked
    assert "[ID]" in masked


def test_banned_promise_is_hard_stop():
    text = "100% guaranteed approval today."
    findings = check_banned(text, text, "", KIT)
    assert findings
    assert findings[0]["rule_id"] == "T-14"
    assert findings[0]["severity"] == "hard"


def test_urgent_tone_is_soft_note():
    findings = check_tone("Act now and hurry.", "Act now and hurry.", "", KIT)
    assert any(f["rule_id"] == "T-02" and f["severity"] == "soft" for f in findings)


def test_replace_first_case_preserves_capitalisation():
    text = "Earn 5% cashback for life."
    updated, applied = _replace_first_case(text, "5% cashback for life", "2.5% cashback")
    assert applied is True
    assert updated == "Earn 2.5% cashback."


def test_replace_first_case_missing_quote_reports_not_applied():
    text = "Earn 2.5% cashback."
    updated, applied = _replace_first_case(text, "5% cashback for life", "2.5% cashback")
    assert applied is False
    assert updated == text
