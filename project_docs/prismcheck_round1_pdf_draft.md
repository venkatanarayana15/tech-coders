# PrismCheck AI — Round 1 Submission

Intelligent Pre-Publication Brand Governance Platform

---

## 1. Understanding of the Given Problem Statement

Growing organizations no longer fail to govern their brand because they lack brand materials. They fail because the brand book is not the system of record at the moment content is published.

The problem statement is about decentralization. Employees, agencies, and AI tools now produce content across many channels, and the volume and speed of that production outpace the organization's ability to check it. The result is not merely "a slightly off-brand post." It is incorrect claims, outdated information, inconsistent language, and off-brand visuals going out before anyone notices.

The brief identifies several concrete failure modes, and PrismCheck treats each as a first-class problem:

- Unsupported promotional claims and incorrect facts reach the audience because there is no last gate that verifies them against approved material.
- Outdated information and inconsistent language appear because the approved brand guidelines exist as documents or folders that creators do not reliably open at publication time.
- Off-brand visuals—colors, logo usage, contrast, alt text—slip through because visual checks are often manual, subjective, or delayed until after publishing.
- Accessibility issues such as poor contrast and missing alt text are frequently missed until they become complaints or legal exposure.
- Approval workflows alone are not enough. As content governance guidance documents, even reviewed and approved content can still expose a brand to risk when the checks do not cover everything.

That last point matters for PrismCheck's understanding of the problem. The brief is not asking for another approval button. It is asking for an intelligent pre-publication review that checks content against approved guidelines, facts, and assets, explains each issue, suggests corrections that preserve the creator's purpose, supports human review and workflow, provides insights into repeated mistakes and unclear guidelines, balances automation with human control, protects confidential materials, and produces reliable, explainable results.

The specific part PrismCheck solves is the pre-publication gap: the moment between "someone produced this" and "this goes out," where the organization has no citable, explainable check against a single approved source of truth.

---

## 2. The Users Affected by the Problem

Content creators and copywriters face creative anxiety, delayed approvals, and subjective, unexplained pushback. They often "guess the tone" and hope the manager does not catch the mistake after the deadline.

External agencies and freelancers must work across multiple clients' brand books, often with outdated brand assets and uncertainty about which document is current. They do not know which version of the palette, the disclaimer, or the approved claim language to use.

Brand and compliance managers face review fatigue. They spend disproportionate time catching the same low-level errors repeatedly, and they often see problems only after content has gone live.

The organizational setting is a mid-to-large organization—D2C, fintech, edtech, SaaS, or campus/departmental communications—with one central brand team and many distributed creators publishing 30 or more multi-channel assets per week. In that setting, the brand guidelines exist, but the problem is that they are not actively used at the point of publication.

---

## 3. Proposed Solution

PrismCheck AI is a pre-publication brand-governance platform that reviews text, images, and documents against an authoritative Brand Kit before anything is published.

Its value proposition is simple: it is the last gate before publish. It does not generate content. It reviews what was produced, explains every finding with a citation, suggests intent-preserving fixes, and never auto-overwrites the creator.

The central design choice is that the Brand Kit is the only admissible evidence. If a rule, fact, or asset exists in the kit, PrismCheck can flag against it and cite it. If the kit has no rule, PrismCheck stays silent instead of inventing an "off-brand" judgment. That choice is what makes the results explainable and reliable rather than a generic AI opinion.

The solution directly addresses the brief:

- Import or define brand guidelines, approved facts, terminology, and reusable assets through a structured Brand Kit.
- Review text, images, and documents before publication through parallel text, visual, and document pipelines.
- Detect tone, terminology, messaging, visual consistency, accessibility, and unsupported claims through four cited checks.
- Explain why each issue was flagged and identify the guideline, fact, or asset involved.
- Suggest corrections without automatically overriding human decisions.
- Support comments, approvals, revision history, and role-based review.
- Provide insights into repeated mistakes and areas where the brand guidelines are unclear.
- Protect confidential materials and disclose the use of AI or external services.

Each of these is mapped to a concrete behavior in Section 4 and a concrete feature in Section 5.

::page-break::

The originality spine is this: because every team has received the same brief, most submissions will claim “AI checks content against brand guidelines.” PrismCheck is different.

Other tools ask whether content feels off-brand. PrismCheck asks for the kit line. If the Brand Kit has no rule, PrismCheck stays silent instead of inventing an off-brand judgment. That is the first originality claim: show the kit line or stay silent.

The second is about what happens when people disagree with the system. If humans keep overriding a rule, PrismCheck treats that as a signal that the rule may be unclear, not only as creator error. In short: if humans keep overriding a rule, the kit is the bug.

---

## Evidence Package

The following evidence supports the problem understanding above. Sources are noted in parentheses.

- 62% of brand managers say brand consistency has gotten harder to maintain over the last two years (Marq, 2026).
- 95% of companies have brand guidelines, but only 25–30% actively use them across the organization (Capital One Shopping Research, 2024; compiled by Omnibound, 2026).
- Consistent brand presentation can increase revenue by 10–33%, and 68% of companies reported that brand consistency contributed directly to revenue growth (Lucidpress/Marq, State of Brand Consistency, 2019; compiled by Omnibound, 2026).
- 80% of people trust brands they use more than government, media, or NGOs, and 71% of global consumers say brand trust is a buy-or-boycott factor (Edelman, 2025 Brand Trust special report and 2024 Trust Barometer; compiled by Omnibound, 2026).
- 75% of content professionals say AI alone has increased their organization's content volume (Marq, 2026).
- When AI and brand messaging conflict, only 29% of consumers trust the brand (Skyword, reported via PR Newswire, 2026).
- Even reviewed-and-approved content can still expose a brand to risk, because approval alone is not governance (Aprimo, 2026).

If the team has any real interview, observation, or survey evidence, use it in place of the illustrative persona quotes. If not, label any persona quotes clearly as illustrative.

---

## Suggested Persona Quotes

Creator: "I guess the tone and hope the manager doesn't catch it after the deadline."

Manager: "I keep seeing the same mistakes on things that go live before I review them."

Agency or freelancer: "Every client sends a different brand PDF, and I never know which one is current."

---

## 4. Complete Product Workflow

One concrete walkthrough shows how the product is used.

A creator at a mid-size fintech drafts a LinkedIn carousel announcing a new credit-card offer. They upload the copy and the banner image.

Step 1 — Privacy shield. Before anything leaves the creator's machine, the client-side privacy layer masks emails, phone numbers, and internal tokens locally.

Step 2 — Four cited checks run in parallel.

- Claims and terminology: the claim "no annual fee for life" is not in the approved Fact Bank, and the banner uses a banned promotional phrase. The unsupported claim is flagged with a hard gate, the missing Fact Bank entry is cited, and two rewrites are offered that preserve the announcement intent without inventing a comparison. The banned phrase is flagged deterministically with the rule ID.
- Tone and intent: the system extracts the intent as "urgent promotional offer" and offers two rewrites that keep the urgency while removing the unsupported promise.
- Visual: the banner's dominant colors are checked in CIELAB space against the Brand Kit palette. One color is outside the approved range, so it is flagged as soft guidance with the kit color it drifted from.
- Accessibility: the text-over-image contrast fails WCAG, and the in-image text has no alt text. Both are flagged with the specific ratio and a suggested alt-text draft.

Step 3 — Explainable diff view. Each finding shows the issue, the guideline/fact/asset ID, the quoted source, the severity, and a suggested fix. The creator clicks Accept Fix on the claim rewrite and Keep Mine + Note on the color flag, because the marketing team has an approved exception for that campaign. The note is attached to the draft.

Step 4 — Approval state machine. The draft moves to Pending Review. The manager sees the claim fix, the color exception note, the accessibility suggestions, and any comments. The manager approves or requests changes. The revision history records what changed and why.

Step 5 — Insights. In the Insights tab, the brand manager later sees that the "no annual fee" claim type has been flagged multiple times this month, and that the color rule flagged in this carousel is one of the top overridden rules, now carrying an "Ambiguous Guideline" badge suggesting the Brand Kit be reviewed.

That workflow covers the full path from Brand Kit definition through creator submission, cited review, human decision, approval, and governance insight.

---

## 5. Main Features to Build

- Authoritative Brand Kit: structured ingestion of approved colors, terminology, facts, and tone parameters. This is the source of truth the rest of the system cites.
- Citation Lock cite-or-silence verification: every finding requires a source_id from the ingested Brand Kit. Findings without a valid source are dropped before the user sees them, so the system never invents rules.
- Intent-Lock rewriter: the system extracts the creator's communicative intent and offers two non-destructive rewrites that preserve it, because the brief asks for corrections that preserve the creator's original purpose.
- Palette and safe-zone inspector: CIELAB color-distance comparison against the kit palette and logo clear-space checks, running deterministically.
- WCAG accessibility engine: mathematical contrast ratios for text over images and suggested alt text for review.
- Collaborative audit queue: role-based permissions for Creator, Manager/Reviewer, and Admin, with threaded notes, approval states, and version diffing.
- Guideline Health insights: top recurring violations plus a view of most-overridden rules with an "Ambiguous Guideline" badge, so the brand team can improve unclear guidelines rather than only flagging creator mistakes.

A deliberately deferred feature is any creative-suite or publishing integration. Those belong in future scope. Round 1 and Round 2 focus on the review gate itself.

---

## 6. Technology Stack and Technical Plan

Frontend: React with Vite, Tailwind CSS, Lucide icons, and TanStack Table for the side-by-side inspection canvas and the insights tables. The frontend is chosen for a fast, responsive review canvas and clean tables for findings and audit data.

Backend: FastAPI on Python 3.12. FastAPI is chosen because the review pipelines are naturally async and parallel—text and image checks can run as separate tasks—and because Python is the right language for the image and NLP tooling. Pydantic is central to the explainability story: every finding is a validated model with a required source_id.

Database and persistence: PostgreSQL, ideally through Supabase or a self-hosted instance. Postgres stores the Brand Kit, drafts, findings, approval state, comments, and revision history. It is chosen because the product needs structured audit data and role-based access, not just blob storage.

AI and NLP engine: Google Gemini, with structured JSON output enforced via Pydantic schemas. The LLM is used for claim verification against the Fact Bank, tone and intent analysis, and intent-preserving rewrites. It is not used as a free-form critic. The Fact Bank uses a private vector store such as ChromaDB for semantic similarity during claim checks. The LLM is injected with kit context and restricted so that it may only cite kit items.

Deterministic vision engine: Pillow and OpenCV for color extraction, CIELAB color-distance computation, and WCAG contrast calculation. These run locally with no API cost and are fully deterministic. The most visual and most safety-relevant checks should not depend on an LLM's opinion.

OCR and alt text: Gemini Vision or EasyOCR for in-image text extraction and alt-text suggestion, used where text inside an image must be read.

Auth: simple role-based JWT with Creator, Manager/Reviewer, and Admin roles. That is enough for the role-based review workflow required in Round 1 and Round 2.

File store: local disk or an S3-compatible store for uploaded drafts and generated artifacts.

Data sources: the Brand Kit is the primary source. The Fact Bank is a private, in-organization vector store of approved facts and claims that can be cited. External AI services are used only where disclosed and only under the citation and privacy constraints described below.

Integrations: in Round 1 and Round 2, PrismCheck is a standalone review gate. It does not integrate with social platforms, messaging tools, or creative suites in this stage. The only external services used are disclosed AI services for text analysis and alt-text suggestions, and a local or S3-compatible file store. Creative-suite integrations, social publishing webhooks, and video support are explicitly deferred to future scope.

The hardest technical part is stopping the LLM from inventing issues and inventing sources. A generic LLM told to "check this for brand compliance" will confidently flag things that are not in the kit and invent rule text. That is the opposite of reliable, explainable results.

PrismCheck addresses this with the Citation Lock:

- The Brand Kit is injected as the only admissible context for findings.
- Every finding is a Pydantic model requiring a non-empty source_id that matches a real kit item—a guideline_id, fact_id, or asset_id.
- A backend middleware step drops any finding whose source_id is empty or does not match an ingested kit item. The user never sees it.
- Banned terminology and color/contrast checks run on deterministic algorithms, not the LLM. Banned terms use a Trie or regex pass so claims are not LLM-only. Color and contrast use Pillow/OpenCV and the WCAG luminosity formula.
- For claim verification, the Fact Bank retrieves candidate facts and the LLM is asked to cite which fact supports or contradicts the claim, with the rule that it may only cite a retrieved fact. If it cannot, it stays silent on that claim rather than inventing one.

This is how PrismCheck produces reliable, explainable results: deterministic checks where safety and precision matter most, and a restricted LLM that may only cite what is in the kit.

---

## 7. Responsibilities of Team Members

- Team lead and full-stack architect: backend architecture, PostgreSQL schemas, approval state machine, and API contracts.
- AI and NLP engineer: Gemini structured output, ChromaDB Fact Bank integration, intent-lock rewrite tuning, and the citation contract.
- Computer vision and accessibility engineer: OpenCV/Pillow pipelines, CIELAB color clustering, WCAG contrast engine, and in-image text and alt-text work.
- Frontend and UX lead: review canvas, one-click diff replacement components, Brand Kit configuration builder, and governance analytics dashboards.

Adjust the number of members to the actual team, but keep the roles honest and inspectable. Round 2 judges may ask any member to explain their contribution.

---

## 8. Development Plan Across All Three Rounds

Round 1 — The Plan:

- Finalize the Brand Kit schema and the Pydantic finding model with the required source_id.
- Finalize the approval state machine and the role model.
- Describe the privacy layer and the deterministic checks.
- Describe the LLM citation contract and the middleware drop rule.
- Assemble the evidence package and the walkthrough.

Round 2 — The Build:

- Stand up FastAPI and the React review canvas.
- Implement the deterministic checks first: banned terms, color/contrast, and logo safe zone. These are the backbone and they work without the LLM.
- Implement the LLM path under the Citation Lock: structured output, kit-injected context, source_id required, middleware drop.
- Implement the Fact Bank vector store for claim checks.
- Implement the approval workflow and revision history.
- Add the insights page and the privacy and AI-disclosure UI.

Round 3 — Polish and Telemetry:

- Harden Guideline Health and the ambiguous-rule badges.
- Improve rewrite quality and intent detection.
- Add revision-history depth and audit-trail clarity.
- Performance-tune the review flow for routine assets.

This plan is intentionally focused. It does not promise video, live CMS plugins, or creative-suite integrations in Round 1. It proves the core gate first, then composes the workflow and insights around it.

---

## 9. Expected Impact

- Faster review for routine collateral. Governance guidance reports that before governance, teams often run 5–7 revision rounds and 7–10 day approval cycles, and after governance, 2–3 rounds and 2–4 day cycles, with 40–60% faster approvals. PrismCheck is designed to move routine social and marketing copy toward that faster, more predictable cadence by catching the same issues before they reach the manager.
- Fewer unsupported claims and banned phrases reaching publication through hard-gate enforcement. This is the direct answer to the brief's concern about incorrect claims and unsupported promotional content.
- A brand kit that improves over time. Guideline Health turns repeated overrides into evidence that a guideline may be unclear, so the organization improves the kit itself instead of treating every override as creator error.

These are grounded expectations, not promises of a specific percentage. The impact story is that PrismCheck prevents brand inconsistency before publication, uses approved source material, and makes the findings understandable to humans.

---

## 10. Future Scope of the Product After the Event

- Creative-suite integrations such as Figma and Canva browser extensions for in-flow linting.
- Video and audio support, including logo tracking, frame-aware checks, and transcript analysis.
- Verified one-click publishing webhooks to social and CMS tools.
- Broader compliance integrations for regulated industries.

All of these are future scope. They are not part of the Round 1 or Round 2 commitment.

---

## Responsible-Design Considerations

This section is included because the Round 1 submission asks for responsible-design considerations, including privacy, security, and human oversight.

- Privacy: the client-side privacy layer masks emails, phone numbers, and internal tokens locally before any content leaves the creator's machine. Brand Kit facts marked Confidential stay in the organization and are not used as free-floating LLM context outside the citation contract.
- Security: role-based access with Creator, Manager/Reviewer, and Admin roles; drafts, findings, and revision history are stored in Postgres with role-appropriate access; uploaded files are stored in a controlled store, not scattered in logs.
- Human oversight: hard gates block publication for unsupported claims, contradicted facts, and banned legal phrases until an authorized manager approves; soft coaching flags tone, color, and accessibility for human decision. AI never publishes. AI never silently rewrites. The creator always chooses Accept Fix or Keep Mine + Note.
- AI disclosure: the UI states plainly what uses AI and what does not. A representative disclosure line is: "Text analysis and alt-text suggestions use Gemini. Image color and contrast checks run locally. No content is stored as training data. Brand Kit facts marked Confidential stay in this organization."
- Explainability: every flag cites a source. If no source exists, the system stays silent, and the ambiguity appears in Guideline Health.

---

## 11. Complete Team and Participant Details

Team Name: [Insert Exact Team Name]

Member 1: [Full Legal Name] — [Email] — [Role]

Member 2: Venkata Narayana G V — venkatnarayana727@gmail.com — Team Leader, Developer

Member 3: [Full Legal Name] — [Email] — [Role]

Member 4: [Full Legal Name] — [Email] — [Role]

Enter the team name exactly as it should appear on certificates. Enter each member's full legal name and email exactly. Check all spellings before submitting, because certificate names will not be changed later.
