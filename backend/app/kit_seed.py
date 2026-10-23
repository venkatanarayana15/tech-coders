from __future__ import annotations

"""The seeded Brand Kit: the only source PrismCheck may cite."""

KIT = {
    "id": "kit-northwind",
    "name": "Northwind Signature — Brand Kit",
    "client": "Northwind Bank",
    "version": "4.2",
    "updated": "2026-10-18",
    "owner": "Brand & Content Governance",
    "audience": "Retail banking customers in India, aged 21 and over.",
    "palette": [
        {"id": "C-01", "name": "Deep Indigo", "hex": "#1B2A6B", "role": "primary"},
        {"id": "C-02", "name": "Mist", "hex": "#EEF1FB", "role": "neutral"},
        {"id": "C-03", "name": "Signal Coral", "hex": "#E4572E", "role": "accent"},
        {"id": "C-04", "name": "Ink", "hex": "#101322", "role": "text"},
        {"id": "C-05", "name": "Sand", "hex": "#F4EDE3", "role": "neutral"},
    ],
    "tolerance": {"delta_e": 12, "min_contrast": 4.5},
    "tone": {
        "name": "Calm confidence",
        "summary": "Plain-spoken, specific and never pushy. State what is true, not what sounds biggest.",
        "avoid": ["absolute guarantees", "urgency", "superlatives"],
    },
    "rules": [
        {
            "id": "C-01",
            "label": "Claims policy",
            "check": "claims",
            "severity": "hard",
            "text": "Every performance, price or approval claim must match an approved fact in the fact bank.",
        },
        {
            "id": "T-14",
            "label": "No absolute guarantees",
            "check": "claims",
            "severity": "hard",
            "text": "Guarantees and 100% promises are not permitted in any channel or format.",
        },
        {
            "id": "T-02",
            "label": "Considered tone",
            "check": "tone",
            "severity": "soft",
            "text": "Write with calm confidence. Avoid urgency, pressure and superlatives.",
        },
        {
            "id": "T-03",
            "label": "Preferred vocabulary",
            "check": "tone",
            "severity": "soft",
            "text": "Use the approved plain-language alternatives recorded in this kit.",
        },
        {
            "id": "V-05",
            "label": "Approved palette",
            "check": "visual",
            "severity": "soft",
            "text": "Only palette colours within a CIELAB distance of 12 may be used in brand artwork.",
        },
        {
            "id": "A-03",
            "label": "Accessible artwork",
            "check": "accessibility",
            "severity": "hard",
            "text": "Body text needs 4.5:1 contrast. Every image needs descriptive alternative text.",
        },
        {
            "id": "L-01",
            "label": "Logo clear space",
            "check": "visual",
            "severity": "soft",
            "text": "Keep clear space equal to the height of the N on all sides of the mark.",
        },
    ],
    "facts": [
        {
            "id": "F-01",
            "category": "offer",
            "text": "No annual fee in year one on the Northwind Signature card.",
        },
        {
            "id": "F-02",
            "category": "rewards",
            "text": "Earn 2.5% cashback on everyday spend, capped at ₹12,000 a year.",
        },
        {
            "id": "F-03",
            "category": "approval",
            "text": "Approval decisions are usually returned within 3 working days.",
        },
        {
            "id": "F-04",
            "category": "eligibility",
            "text": "The Signature card is available to residents of India aged 21 and over.",
        },
        {
            "id": "F-05",
            "category": "rewards",
            "text": "Cashback is credited to the statement at the end of each billing cycle.",
        },
    ],
    "banned": [
        {"id": "B-01", "term": "guaranteed", "rule_id": "T-14"},
        {"id": "B-02", "term": "100%", "rule_id": "T-14"},
        {"id": "B-03", "term": "no annual fee for life", "rule_id": "T-14"},
        {"id": "B-04", "term": "risk-free", "rule_id": "T-14"},
        {"id": "B-05", "term": "instant approval", "rule_id": "T-14"},
        {"id": "B-06", "term": "best in the market", "rule_id": "T-14"},
    ],
    "preferred": [
        {"id": "P-01", "from": "cheap", "to": "low-cost", "rule_id": "T-03"},
        {"id": "P-02", "from": "grab", "to": "get", "rule_id": "T-03"},
        {"id": "P-03", "from": "users", "to": "cardholders", "rule_id": "T-03"},
        {"id": "P-04", "from": "sign up", "to": "apply", "rule_id": "T-03"},
    ],
}
