#!/usr/bin/env python3
"""Synthetic-labelled evaluation harness for the PrismCheck engine.

The set is deliberately synthetic: it is built from the seven kit rules and the
approved fact bank so the harness is deterministic and repeatable. It is not a
claim about real-world accuracy; it is the reusable measurement rig that a
30-draft real-world labelled set can be dropped into later.

Run from the repository root:
    python backend/evaluate.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.engine import run_review
from app.kit_seed import KIT

# (caption, expected rule ids)
LABELLED_CASES = [
    ("Earn 2.5% cashback on everyday spend, capped at ₹12,000 a year.", set()),
    ("No annual fee in year one on the Northwind Signature card.", set()),
    ("Approval decisions are usually returned within 3 working days.", set()),
    ("Cashback is credited to the statement at the end of each billing cycle.", set()),
    ("Earn 5% cashback for life.", {"C-01"}),
    ("5% cashback on everything.", {"C-01"}),
    ("Best card in the market.", {"C-01", "T-14"}),
    ("No annual fee for life.", {"T-14", "C-01"}),
    ("100% guaranteed approval.", {"T-14"}),
    ("Risk-free rewards, guaranteed.", {"T-14"}),
    ("Instant approval on application.", {"T-14"}),
    ("Save 50% off everywhere, guaranteed.", {"T-14", "C-01"}),
    ("Act now and hurry.", {"T-02"}),
    ("Last chance to apply today.", {"T-02"}),
    ("This limited time offer ends soon.", {"T-02"}),
    ("Always best prices, never miss out.", {"T-02"}),
    ("Unbeatable offer, perfect for everyone.", {"T-02"}),
    ("Cheap top-ups for all users.", {"T-03"}),
    ("Sign up now and grab rewards.", {"T-03", "T-02"}),
    ("Act now and sign up.", {"T-02", "T-03"}),
    ("Earn 2.5% cashback, act now.", {"T-02"}),
    ("No annual fee in year one. Act now.", {"T-02"}),
    ("Earn 5% cashback guaranteed for life. Act now.", {"T-14", "C-01", "T-02"}),
    ("We never charge hidden fees, always transparent.", {"T-02"}),
    ("Apply for the card today and earn rewards.", set()),
    ("Earn unlimited cashback forever.", {"C-01"}),
    ("The cheapest card available.", {"C-01"}),
    ("Approval guaranteed in 3 working days.", {"T-14"}),
    ("Get 2.5% cashback and apply today.", set()),
    ("Welcome offer: no annual fee in year one.", set()),
]


def run() -> dict:
    tp = fp = fn = 0
    mismatches = []
    for caption, expected in LABELLED_CASES:
        result = run_review(KIT, caption, "", None, doc_text="")
        predicted = {f["rule_id"] for f in result["findings"]}
        tp += len(predicted & expected)
        fp += len(predicted - expected)
        fn += len(expected - predicted)
        if predicted != expected:
            mismatches.append((caption, sorted(expected), sorted(predicted)))

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    false_positive_rate = fp / (tp + fp) if tp + fp else 0.0

    print(f"cases: {len(LABELLED_CASES)}")
    print(f"true positives: {tp}  false positives: {fp}  false negatives: {fn}")
    print(f"precision: {precision:.3f}  recall: {recall:.3f}  F1: {f1:.3f}")
    print(f"false positive rate: {false_positive_rate:.3f}")
    if mismatches:
        print("mismatches:")
        for caption, expected_order, predicted_order in mismatches:
            print(f"  - {caption!r} expected={expected_order} predicted={predicted_order}")
    return {
        "cases": len(LABELLED_CASES),
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "false_positive_rate": round(false_positive_rate, 3),
    }


if __name__ == "__main__":
    run()
