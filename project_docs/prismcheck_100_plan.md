# PrismCheck — 100/100 Round 1 Plan

This is the full Round 1 submission plan for PrismCheck, built from a deep read of the actual Inkloom AI problem statement, the Round 1 PDF requirements, the Round 1 rubric, the evidence base, the competitive landscape, and the other Inkloom teams' likely directions. It is written so the team can lift exact paragraphs into the PDF and the form.

---

## How to read this document

Round 1 is judged on 100 points across five criteria:

- Understanding of the problem statement — 25
- The proposed solution — 25
- Technical plan — 20
- Originality of approach — 15
- Feasibility and scope — 15

To score near 100, PrismCheck must do three things at once:
1. Prove it understands the brief better than a generic "AI brand checker" team, with real evidence.
2. Show a concrete, walkable workflow that directly covers every required capability.
3. Make originality specific and defensible, not a slogan.

The hardest originality risk is real and recent: another Inkloom team already shipped a "Living Brand Intelligence" system with the explicit thesis that "the AI doesn't silently rewrite... the founder stays in control" and a "Current vs Proposed" approval flow. If PrismCheck's originality story is only "we keep humans in the loop and show a diff," it loses originality points to that team. So PrismCheck's originality must rest on mechanisms those teams do not have: **cite-or-silence**, **intent-lock rewriting**, and **guideline health that treats overrides as a signal about the kit, not the creator**. Those are the three legs the originality score stands on.

---

## 1. Understanding of the problem statement — target 25/25

### What the brief actually says

The problem is not "make a brand checker." It is this, line by line:

- Growing organizations publish through multiple employees, agencies, and AI tools.
- That makes consistent, trustworthy brand identity hard to maintain.
- Incorrect claims, outdated information, inconsistent language, and off-brand visuals can damage credibility before anyone notices.
- Build an intelligent brand-governance platform that reviews content before publication and checks it against approved guidelines, facts, and assets.
- Detect issues involving tone, terminology, messaging, visual consistency, accessibility, and unsupported promotional claims.
- Instead of simply rejecting content, explain each issue and suggest corrections that preserve the creator's original purpose.
- Include a review and approval workflow where creators, managers, and authorized reviewers can collaborate and track changes.
- Support different content formats and provide insights into repeated mistakes **and areas where the brand guidelines are unclear**.
- Balance automation with human control, protect confidential materials, and produce reliable, explainable results.

That last sentence is the spine of the whole brief. Every paragraph in PrismCheck's understanding section should trace back to one of those lines.

### The specific part PrismCheck solves

PrismCheck solves the **pre-publication governance gap**, not the creation gap. Many organizations already have brand materials, templates, and AI tools. What they lack is a last gate that reviews what was produced against a single approved source of truth, explains each finding with a citation, preserves creator intent, and routes repeated overrides back as evidence that a guideline may be unclear.

This is the right slice because the brief explicitly lists both "prevent brand inconsistency before content is published" and "areas where the brand guidelines are unclear" as outcomes. PrismCheck addresses both with one architecture: the Brand Kit is the only admissible evidence, and human behavior against that kit becomes a governance signal.

### Evidence that the problem is real

Use a tight, sourced evidence set. Do not pad with a hundred weak stats. The strongest package is:

**Scale.** 62% of brand managers say brand consistency has gotten harder to maintain over the last two years (Marq, 2026, citing brand manager survey data). The original Lucidpress/Marq State of Brand Consistency research found consistent brand presentation can increase revenue by 10–33%, and 68% of companies reported brand consistency contributed directly to revenue growth (Lucidpress/Marq, 2019). Sources: Marq blog on digital brand governance; Omnibound 2026 brand consistency statistics roundup, which compiles Lucidpress/Marq and other primary sources.

**The gap between having guidelines and using them.** 95% of companies have brand guidelines, but only 25–30% actively use them across the organization (Capital One Shopping Research, 2024, as compiled by Omnibound 2026). That is the central fact behind the brief: the problem is not the absence of a brand book. It is that the brand book is not the system of record at the moment of publication.

**Trust is now the commercial mechanism.** Edelman's 2025 Brand Trust special report found 80% of people trust brands they use more than government, media, or NGOs; 71% of global consumers say trust in brands is a buy-or-boycott factor (Edelman, 2024 Trust Barometer, as compiled by Omnibound 2026). The point for PrismCheck is that inconsistent content does not just "look bad" — it attacks the trust that gates revenue.

**AI is now inside the content pipeline, and it makes the problem worse, not better.** 75% of content professionals say AI alone has increased their organization's content volume (Marq, 2026). Typeface's 2026 governance guidance reports that before governance, teams often run 5–7 revision rounds and 7–10 day approval cycles; after governance, 2–3 rounds and 2–4 day cycles, with 40–60% faster approvals. The brief explicitly names AI tools as a cause of the problem. PrismCheck should say so plainly: more content, faster, from more unvetted sources, against brand PDFs that nobody opens.

**The compliance argument.** Aprimo's 2026 content-governance piece documents that even reviewed-and-approved content can still expose a brand to risk — the Lord & Taylor influencer campaign is the cautionary case: content was reviewed and approved, yet the FTC still took action because the compliance check did not cover disclosure. Source: Aprimo, "10 Content Governance Gaps That Increase Brand Risk," 2026. The lesson for PrismCheck: approval alone is not governance. A citeable, explainable pre-publication check that covers claims, terminology, visuals, and accessibility is what the brief is asking for.

**AI-content defensibility is now a procurement and legal concern, not a nice-to-have.** Brand-governance-for-AI-content guidance in 2026 frames the issue around EU AI Act Article 50 transparency obligations and FTC scrutiny of AI content liability, and argues that defensibility is now a procurement criterion (CrawlQ, 2026). PrismCheck should not over-claim its own legal effect, but it can reasonably say that an explainable, citation-backed review trail is the kind of artifact regulated and scrutinized teams increasingly want before publication.

**One trust-specific statistic tied to AI conflict.** When AI and brand messaging conflict, only 29% of consumers trust the brand (Skyword, reported via PR Newswire, 2026). This is the cleanest single statistic for the "AI tools are now part of the problem" argument.

### How to present the evidence in the PDF

Put the evidence where judges expect it: in the problem understanding section, briefly, with sources in parentheses. Then reinforce it with three concrete examples of the kind of issue PrismCheck would catch:

1. **Unsupported claim.** A social ad claims a product "lasts 3x longer than the leading alternative," but the approved Fact Bank contains no such claim and no comparative spec. PrismCheck flags it as an unsupported promotional claim with a hard gate, cites the missing Fact Bank entry, and offers two rewrites that preserve the announcement intent without inventing a comparison.

2. **Banned promotional language.** A banner uses "100% guaranteed results" or "risk-free" in a regulated category. The terminology rule is deterministic; the flag is immediate, with the exact banned term and the rule ID.

3. **Accessibility failure.** A banner image has light text over a near-matched background that fails WCAG contrast, and the in-image text is missing alt text. The visual pipeline flags contrast mathematically and suggests alt text for review.

Then add one persona quote per role, clearly labeled as illustrative if you do not have a real interview:

- Creator: "I guess the tone and hope the manager doesn't catch it after the deadline."
- Manager: "I keep seeing the same mistakes on things that go live before I review them."
- Agency/freelancer: "Every client sends a different brand PDF, and I never know which one is current."

### The organizational setting

Make it specific. PrismCheck is aimed at mid-to-large organizations publishing many assets across channels with a small central brand team and many distributed creators. Good settings: D2C, fintech, edtech, SaaS, campus/departmental communications, franchise or dealer networks. A concrete example: one brand manager, 20–200 creators and agencies, 30+ multi-channel assets per week, brand guidelines exist as a PDF or folder that creators do not reliably open. That setting is exactly the one the brief describes.

---

## 2. The proposed solution — target 25/25

### Value proposition in one sentence

PrismCheck is the last gate before publish: it reviews text, images, and documents against the Brand Kit, explains every flag with a citation, suggests intent-preserving fixes, never auto-overwrites the creator, and turns repeated human overrides into evidence that a guideline may be unclear.

### The one sentence that sets PrismCheck apart

Other teams will say "AI reviews content against brand guidelines." PrismCheck says: "Show the kit line or stay silent — and if humans keep overriding a rule, the kit is the bug."

That sentence is the originality spine. Put it in the solution section, and repeat a shorter version in the originality section.

### Why this directly addresses the problem

Map each required capability to a PrismCheck behavior:

- Import or define brand guidelines, approved facts, terminology, and reusable assets → the Brand Kit builder.
- Review text, images, documents, or other supported formats → the upload-and-review flow with text, image, and document pipelines.
- Detect tone, terminology, messaging, visual consistency, accessibility, and unsupported claims → four cited checks: Claims/Terminology, Tone+Intent, Visual vs Kit, Accessibility.
- Explain why an issue was flagged and identify the guideline or approved source → the Citation Lock and the explainable diff view.
- Suggest corrections without overriding human decisions → Intent Lock rewrites with Accept Fix or Keep Mine + Note.
- Comments, approvals, revision history, role-based workflow → Draft → Pending → Approved/Changes Requested with comments, history, and roles.
- Insights into repeated mistakes and unclear guidelines → Top recurring violations plus Guideline Health with ambiguous-rule badges.
- Balance automation with human control → hard gates for claims/facts/banned phrases, soft coaching for tone/color/accessibility.
- Protect confidential materials, disclose AI → client-side PII masking, Confidential facts stay in-org, and a UI disclosure line.

This mapping is what makes the solution score high: judges can see that PrismCheck is not only on the brief, but organized around it.

### The end-to-end workflow as a named walkthrough

Do not rely on a diagram alone. Give the PDF one concrete, named scenario and walk it. Example:

A creator at a mid-size fintech drafts a LinkedIn carousel announcing a new credit-card offer. They upload the copy and the banner image.

Step 1 — Privacy shield. Before anything leaves the creator's machine, the client-side privacy layer masks emails, phone numbers, and internal tokens such as [INTERNAL PRICE] locally.

Step 2 — Four cited checks run in parallel.

- Claims and terminology: "no annual fee for life" is not in the Fact Bank, and the banner uses a banned phrase. The unsupported claim gets a hard gate with the missing Fact Bank entry cited. The banned phrase is flagged deterministically with the rule ID.
- Tone and intent: the system extracts the intent as "urgent promotional offer" and offers two rewrites that keep the urgency while removing the unsupported promise.
- Visual: the banner's dominant colors are checked in CIELAB space against the Brand Kit palette; one color is outside the approved Delta-E range, so it is flagged as soft guidance with the kit color it drifted from.
- Accessibility: the text-over-image contrast fails WCAG, and the in-image text has no alt text; both are flagged with the specific ratio and a suggested alt-text draft.

Step 3 — Explainable diff view. Each finding shows issue, guideline/fact/asset ID, the quoted source, severity, and a suggested fix. The creator clicks Accept Fix on the claim rewrite and Keep Mine + Note on the color flag, because the marketing team has an approved exception for that campaign. The note is attached to the draft.

Step 4 — Approval state machine. The draft moves to Pending Review. The manager sees the claim fix, the color exception note, the accessibility suggestions, and any comments. The manager approves or requests changes. The revision history records what changed and why.

Step 5 — Insights. In the Insights tab, the brand manager later sees that the "no annual fee" claim type has been flagged multiple times this month, and that the color rule flagged in this carousel is one of the top overridden rules, now carrying an "Ambiguous Guideline" badge suggesting the Brand Kit be reviewed.

That walkthrough is what makes the solution section score. Judges can picture a person doing a real task, and they can see every required capability in action.

### The Brand Kit as the sole source of truth

The Brand Kit has four parts and stays focused:

- Colors: approved palettes with hex values, usage rules, and any safe-zone/clear-space rules for logos.
- Terminology: preferred terms, banned terms, and channel-specific wording rules.
- Approved facts: product specs, pricing, offers, disclaimers, and approved claims that can be cited.
- Tone: brand voice parameters and the intent categories the system uses for rewrites.

This is deliberately not a 50-page PDF parser. It is a structured, citable source of truth. That focus is what makes the Citation Lock possible.

---

## 3. Technical plan — target 20/20

### The stack and why

Frontend: React with Vite, Tailwind CSS, Lucide icons, and TanStack Table for the side-by-side inspection canvas and the insights tables. If the team prefers, Next.js App Router is fine; the important thing is a fast, responsive review canvas and clean tables for findings and insights. State management should be simple: React state plus a small store for the draft, findings, and approval state.

Backend: FastAPI on Python 3.12. FastAPI is chosen because the review pipelines are naturally async and parallel — text and image checks can run as separate tasks — and because Python is the right language for the image and NLP tooling. Pydantic is the backbone of the explainability story: every finding is a validated model with a required source_id.

Database: PostgreSQL, ideally via Supabase or a self-hosted instance. Postgres stores the Brand Kit, drafts, findings, approval state, comments, and revision history. It is chosen because the product needs structured audit data and role-based access, not just blob storage.

AI and NLP: Google Gemini, with structured JSON output enforced. The LLM is used for claim verification against the Fact Bank, tone and intent analysis, and intent-preserving rewrites. It is not used as a free-form critic. The Fact Bank uses a private vector store such as ChromaDB for semantic similarity during claim checks. The LLM is injected with kit context and restricted via a Pydantic schema that requires a source_id on every finding.

Deterministic vision: Pillow and OpenCV for color extraction, CIELAB color-distance computation, and WCAG contrast calculation. These run locally with no API cost and are fully deterministic. That is important: the most visual, most safety-relevant checks should not depend on an LLM's opinion.

OCR and alt text: Gemini Vision or EasyOCR for in-image text extraction and alt-text suggestion. Use this where text inside an image must be read; keep it optional and bounded.

Auth: simple role-based JWT with three roles: Creator, Manager/Reviewer, Admin. That is enough for "role-based review workflows" in Round 1 and Round 2. Do not add Legal/Agency seats in Round 1.

File store: local disk or an S3-compatible store for uploaded drafts and generated artifacts.

### The data flow

1. Admin/Brand Manager defines or imports the Brand Kit.
2. Creator or agent submits a draft — text with an image, or a document.
3. The client-side privacy layer masks PII locally before upload.
4. The backend fans out to parallel pipelines:
   - Text pipeline: banned-term/deterministic terminology check; Fact Bank claim check; intent extraction and rewrite generation.
   - Image pipeline: dominant color extraction and CIELAB/Delta-E comparison against the kit palette; WCAG contrast on any text-over-image; in-image text OCR; alt-text suggestion.
   - Document pipeline: extract text from PDF/DOCX and run the text pipeline; flag embedded images separately.
5. The backend assembles findings and validates each one through the Citation Lock.
6. The frontend renders the explainable diff view with Accept Fix and Keep Mine + Note.
7. The approval state machine moves the draft through Draft → Pending Review → Approved / Changes Requested.
8. Insights are computed from the findings and override history.

### The hardest technical part and how PrismCheck addresses it

The hardest part is not image processing or auth. It is **stopping the LLM from inventing issues and inventing sources.** A generic LLM told to "check this for brand compliance" will confidently flag things that are not in the kit, and will invent rule text. That is exactly the opposite of "reliable, explainable results."

PrismCheck addresses it with a named mechanism: the **Citation Lock**.

- The Brand Kit is injected as the only admissible context for findings. The LLM does not get a free-form brand voice prompt and then opine. It gets the kit items it is allowed to cite.
- Every finding is a Pydantic model that requires a non-empty source_id matching a real kit item — a guideline_id, fact_id, or asset_id.
- A backend middleware step drops any finding whose source_id is empty or does not match an ingested kit item. The user never sees it.
- Banned terminology and color/contrast checks run on deterministic algorithms, not the LLM. Banned terms use a Trie or regex pass so claims are not LLM-only. Color and contrast use Pillow/OpenCV and the WCAG luminosity formula.
- For claim verification, the Fact Bank is a private vector store; the system retrieves candidate facts and asks the LLM to cite which fact supports or contradicts the claim, with the rule that it may only cite a retrieved fact. If it cannot, it stays silent on that claim rather than inventing one.
- The output is structured JSON, not prose, so the frontend can render the cited diff deterministically.

That is a believable and defendable architecture for "reliable, explainable results." Say it plainly in the technical plan, because the rubric asks for exactly that.

### Why this stack, briefly

- React/Vite gives a fast review canvas and clean tables without over-engineering.
- FastAPI gives async parallel pipelines and a clean contract for the frontend.
- Postgres gives the audit, role, and version history the brief asks for.
- Gemini gives structured output and enough context for tone and intent work.
- ChromaDB gives a private, in-org Fact Bank for claim checks.
- Pillow/OpenCV give deterministic, zero-API-cost color and contrast checks, which makes the visual story reliable and cheap.
- JWT gives role-based review without building a full identity platform for Round 1.

### What PrismCheck does not build, and why

It does not build a CMS, a creative suite, or a publishing integration in Round 1. It does not promise Instagram, Slack, Canva, or Figma integration in Round 1. It does not do video. It does not train a custom model. Those are future scope. The point of Round 1 is to prove the plan is buildable and on-brief; the point of Round 2 is to prove the workflow runs end to end.

---

## 4. Originality of approach — target 15/15

### The originality thesis

PrismCheck's originality is not "AI + workflow + insights." That is what most teams will submit. PrismCheck's originality is a **cite-or-silence brand courtroom** with three designed mechanisms: the Citation Lock, the Intent Lock, and Guideline Health.

### The three mechanisms

**1. The Citation Lock — cite-or-silence.**

Every finding PrismCheck shows is tied to a specific guideline, fact, or asset in the Brand Kit. If the kit has no rule, PrismCheck stays silent instead of hallucinating an "off-brand" judgment. This is a feature, not a gap. It directly answers the brief's demand to "identify the guideline or approved source involved" and to produce "reliable, explainable results." It also prevents the most common LLM failure mode in this category: inventing rules that sound plausible but are not in the kit.

Be exact in the PDF: findings are Pydantic models with a required source_id; the middleware drops findings without a valid source; banned-term and color/contrast checks are deterministic and not LLM-sourced; claim verification may only cite a retrieved Fact Bank entry.

**2. The Intent Lock — preserve the creator's purpose.**

The brief says "suggest corrections that preserve the creator's original purpose." PrismCheck does that by extracting the creator's intent first and offering two non-destructive rewrites that keep it. If the creator is announcing a Diwali sale in red, the system does not force brand-blue; it routes the color flag to Keep Mine + Note. If the creator is making an urgent promotional announcement, the rewrites keep urgency while fixing the unsupported claim.

This is the best answer in the category to the "preserve original purpose" line, because it makes intent explicit rather than assuming the "best" rewrite is the one that most closely matches brand voice.

**3. Guideline Health — overrides diagnose the kit, not only the creator.**

Most tools treat a human override as creator non-compliance. PrismCheck treats repeated overrides as evidence that a guideline may be unclear. The Insights tab has two views: most flagged rules, and most overridden rules with an "Ambiguous Guideline" badge. That directly answers the brief's demand for "insights into repeated mistakes or areas where the brand guidelines are unclear." It also turns the Brand Kit from a static artifact into something the organization can improve from real behavior.

This is the insight many teams will miss. Make it visible.

### What makes this different from other teams

Most teams in this event will likely do one of three things:

- A generic AI brand checker that flags "off-brand" content with prose explanations.
- A generation-plus-governance tool aimed at content made inside their own system.
- A "living brand" tool aimed at founders and strategy evolution, with a Current vs Proposed approval flow and a "founder stays in control" story.

PrismCheck is different from all three in a way the judges can verify:

- From the generic checker: PrismCheck refuses to flag anything it cannot cite, and it makes the citation visible to the user.
- From the generation-oriented tool: PrismCheck governs what was produced, including by external agencies, employees, and tools you do not control. It is a review gate, not only a generation assist.
- From the "living brand" tool: PrismCheck is about pre-publication governance of concrete assets against an approved kit, with citeable findings and guideline health, not about evolving brand strategy from a founder's conversation.

The safest originality line for the PDF is therefore:

> Most teams will build "AI says this is off-brand." PrismCheck builds "show the kit line or stay silent — and if humans keep overriding a rule, the kit is the bug."

That line is specific enough to be judged and different enough to score.

### A caution on the "human in control" originality claim

"Human in control" and "we don't silently rewrite" are now common claims in this event, because another Inkloom team has already used them publicly. If PrismCheck's originality rests only on that, it will not stand out. The originality must rest on the three mechanisms above. Keep the human-control story as a responsible-design strength, not as the originality claim.

---

## 5. Feasibility and scope — target 15/15

### The buildable Round 1 plan

Round 1 is a plan, but feasibility is judged. The plan must be buildable by Round 2 and finishable by Round 3.

The buildable scope is:

- One Brand Kit with colors, terminology, approved facts, and tone.
- One submit flow: upload text plus image, or upload a document.
- Client-side PII masking.
- Four cited checks: claims/terminology, tone+intent, visual vs kit, accessibility.
- An explainable diff view with Accept Fix and Keep Mine + Note.
- An approval state machine: Draft → Pending Review → Approved / Changes Requested, with comments and revision history.
- Roles: Creator, Manager/Reviewer, Admin.
- One insights page: top recurring violations and Guideline Health with ambiguous-rule badges.
- A privacy and AI-disclosure statement in the UI.

### Formats, bounded

Cover text, image, and document without pretending to do everything. The Round 2 build covers:

- Text/caption review.
- Image review for social/ad-style banners: color, contrast, in-image text, alt text, logo safe zone where applicable.
- PDF/DOCX one-pager review: extract text, run the text pipeline, and flag embedded images.

That covers "text, images, documents" from the brief without reaching for video, live CMS plugins, or creative-suite integrations.

### What is explicitly deferred

Defer these to future scope only:

- Instagram/social platform APIs.
- Slack or other messaging integrations.
- Canva/Figma browser extensions.
- Video and audio review.
- Multi-brand agency OS.
- Custom model training.

Deferring them is a feasibility strength, not a weakness, because it shows the team understands scope.

### The build sequence

Round 1 — the plan:

- Finalize the Brand Kit schema and the Pydantic finding model with the required source_id.
- Finalize the approval state machine and role model.
- Describe the privacy layer and the deterministic checks.
- Describe the LLM citation contract and the middleware drop rule.
- Write the evidence package and the walkthrough.

Round 2 — the build:

- Stand up FastAPI and the React review canvas.
- Implement the deterministic checks first: banned terms, color/contrast, logo safe zone. These are the backbone and they work without the LLM.
- Implement the LLM path with the Citation Lock: structured output, kit-injected context, source_id required, middleware drop.
- Implement the Fact Bank vector store for claim checks.
- Implement the approval workflow and revision history.
- Implement the insights page.
- Add the privacy and AI-disclosure UI.

Round 3 — polish and telemetry:

- Harden Guideline Health and the ambiguous-rule badges.
- Improve rewrite quality and intent detection.
- Add revision-history depth and audit trail.
- Performance tuning: aim for a fast enough review that the walkthrough feels immediate for routine assets; do not claim a specific sub-second number unless you can measure it.

### The feasibility story

The feasibility story is: build the deterministic backbone first, then add the LLM path under the Citation Lock, then compose the workflow and insights around them. The hardest piece is the Citation Lock, and it is also the piece that makes the product explainable, so it gets built early. If the Citation Lock works, the rest is mostly wiring and UI. That is a believable build order for a small team.

---

## 6. Responsible-design considerations — woven through, with one 명시적 section

The brief asks for "responsible-design considerations, including privacy, security and human oversight." PrismCheck should have one short section that states them plainly:

- Privacy: client-side regex masks emails, phone numbers, and internal tokens before any content leaves the creator's machine. Brand Kit facts marked Confidential stay in-org and are not used as a free-floating LLM context outside the citation contract.
- Security: role-based access with Creator, Manager/Reviewer, and Admin; drafts, findings, and revision history are stored in Postgres with role-appropriate access; uploaded files are stored in a controlled store, not scattered in logs.
- Human oversight: hard gates block publication for unsupported claims, contradicted facts, and banned legal phrases until an authorized manager approves; soft coaching flags tone, color, and accessibility for human decision. AI never publishes. AI never silently rewrites. The creator always chooses Accept Fix or Keep Mine + Note.
- AI disclosure: the UI states plainly what uses AI and what does not. A good disclosure line is: "Text analysis and alt-text suggestions use Gemini. Image color and contrast checks run locally. No content is stored as training data. Brand Kit facts marked Confidential stay in this organization."
- Explainability: every flag cites a source. If no source exists, the system stays silent and the ambiguity shows up in Guideline Health.

This section matters because the brief names it explicitly, and because it is where many teams will be thin.

---

## 7. The 11-section PDF, with the strongest framing for each

Use these as the actual PDF sections. The numbered list matches the required 11.

**1. Your understanding of the given problem statement**

Growing organizations publish through many employees, agencies, and AI tools, so the brand book is no longer the system of record at the moment of publication. The failure is not the absence of guidelines; it is that incorrect claims, outdated information, inconsistent language, and off-brand visuals can go out before anyone notices. PrismCheck solves the pre-publication governance gap: a last gate that reviews content against a single approved Brand Kit, explains each finding with a citation, preserves creator intent, and turns repeated human overrides into evidence that a guideline may be unclear.

Then include the evidence package from Section 1 above: the 62% harder-to-maintain statistic, the 95%-have-guidelines-but-25–30%-use-them gap, the Lucidpress/Marq revenue-consistency range and the 68% figure, the Edelman trust figures, the AI content-volume statistic, the Typeface before/after approval-cycle framing, the Aprimo "approved content can still fail" point, and the AI-trust statistic. Cite sources in parentheses.

**2. The users affected by the problem**

- Content creators and copywriters: creative anxiety, delayed approvals, subjective unexplained pushback.
- External agencies and freelancers: multiple clients, outdated assets, uncertainty about which brand PDF is current.
- Brand and compliance managers: review fatigue, catching the same low-level errors repeatedly, and content going live before review.

Setting: mid-to-large organizations in D2C, fintech, edtech, SaaS, or campus/departmental communications, with one central brand team and many distributed creators publishing 30+ assets per week.

**3. Your proposed solution**

Use the value-proposition sentence and the "show the kit line or stay silent" originality line. Then describe the Brand Kit as the sole source of truth and the four cited checks. Keep it concrete.

**4. The complete product workflow**

Use the named fintech-carousel walkthrough from Section 2 above. A diagram is fine as a supplement, but the walkthrough is what makes judges understand the product.

**5. The main features you intend to build**

Use a short table:

- Authoritative Brand Kit: colors, terminology, approved facts, tone.
- Citation Lock cite-or-silence verification: findings require a source_id from the kit; findings without one are dropped.
- Intent-Lock rewriter: intent extraction plus two intent-preserving rewrites.
- Palette and safe-zone inspector: CIELAB color distance and logo clear-space checks.
- WCAG accessibility engine: contrast ratios and alt-text suggestion.
- Collaborative audit queue: role-based review, comments, approval states, revision history.
- Guideline Health insights: top recurring violations and ambiguous-rule badges.

**6. The technology stack you plan to use**

Use the stack and reasoning from Section 3. State the hardest part and the Citation Lock architecture plainly.

**7. The responsibilities of each team member**

Assign four roles that match what you will actually build:

- Team lead / full-stack architect: backend architecture, Postgres schemas, approval state machine, API contracts.
- AI/NLP engineer: Gemini structured output, ChromaDB Fact Bank, intent-lock rewrite tuning, citation contract.
- Computer vision/accessibility engineer: OpenCV/Pillow pipelines, CIELAB clustering, WCAG contrast, in-image text and alt text.
- Frontend/UX lead: review canvas, diff replacement components, Brand Kit builder, insights dashboard.

Adjust the number of members to your actual team, but keep the roles honest and inspectable. Round 2 judges may ask any member to explain their contribution.

**8. Your development plan across all three rounds**

Use the Round 1/2/3 sequence from Section 5. Keep it realistic.

**9. The expected impact of your solution**

Keep it grounded:

- Faster review for routine collateral: the before/after approval-cycle framing from Typeface's governance guidance is the basis for claiming meaningful cycle compression for routine social and marketing copy.
- Fewer unsupported claims and banned phrases reaching publication through hard-gate enforcement.
- A brand kit that improves over time through Guideline Health, instead of remaining a static PDF that creators do not open.

Do not over-claim a specific percentage unless you can tie it to a source or a measured demo. The Typeface 40–60% faster-approval framing is the safest anchor for "faster review," attributed as the basis for the expectation, not as a PrismCheck guarantee.

**10. The future scope of the product after the event**

- Creative-suite integrations such as Figma and Canva browser extensions for in-flow linting.
- Video and audio support: logo tracking, frame-aware checks, transcript analysis.
- Verified one-click publishing webhooks to social and CMS tools.
- Broader compliance integrations for regulated industries.

Label all of this future scope, not Round 1 scope.

**11. Complete team and participant details**

Enter the team name exactly as you want it to appear on certificates. Enter each member's full legal name and email exactly. Double-check spelling. The organizers will not fix this later.

---

## 8. The evidence package, finalized

Use this exact set in the PDF and keep it short.

Scale and revenue:
- 62% of brand managers say brand consistency has gotten harder to maintain over the last two years (Marq, 2026).
- Consistent brand presentation can increase revenue by 10–33%; 68% of companies reported brand consistency contributed directly to revenue growth (Lucidpress/Marq, State of Brand Consistency, 2019; compiled by Omnibound, 2026).

Guidelines exist but do not govern:
- 95% of companies have brand guidelines, but only 25–30% actively use them across the organization (Capital One Shopping Research, 2024; compiled by Omnibound, 2026).

Trust:
- 80% of people trust brands they use more than government, media, or NGOs; 71% of global consumers say brand trust is a buy-or-boycott factor (Edelman, 2025 Brand Trust special report and 2024 Trust Barometer; compiled by Omnibound, 2026).

AI in the pipeline:
- 75% of content professionals say AI alone has increased their organization's content volume (Marq, 2026).
- When AI and brand messaging conflict, only 29% of consumers trust the brand (Skyword, reported via PR Newswire, 2026).

Workflow:
- Before governance, teams often run 5–7 revision rounds and 7–10 day approval cycles; after governance, 2–3 rounds and 2–4 day cycles, with 40–60% faster approvals (Typeface, 2026 governance guidance).

Compliance:
- Even reviewed-and-approved content can still expose a brand to risk; the Lord & Taylor influencer campaign was reviewed and approved, yet the FTC still acted because disclosure was missed (Aprimo, 2026).

Defensibility:
- Brand governance for AI content is increasingly framed around EU AI Act Article 50 transparency obligations and FTC scrutiny of AI content liability, with defensibility as a procurement criterion (CrawlQ, 2026).

Use these as supporting evidence, not as the whole story. The story is the brief itself, plus the fact that the brand book is not the system of record at publication time.

---

## 9. What a 100/100 submission looks like, in one paragraph

A 100/100 PrismCheck Round 1 PDF is one that lets a judge do four things in under five minutes: see that you understood the brief line by line; see a concrete walkthrough of a real person using the product; see a technical plan that names the hardest part and explains how you prevent the LLM from inventing issues; and see an originality story that is sharper than "we keep humans in control." If the PDF does those four things, with sourced evidence and a believable scope, it is positioned for the top of the Round 1 rubric.

---

## 10. The one thing that would weaken this plan

The one thing that would weaken this plan is scope creep in the PDF. If the plan starts naming many integrations, many formats, video, multiple AI agents, or custom training, it stops looking feasible and starts looking like a wish list. The strongest PrismCheck plan is the focused one: one kit, one submit flow, cited findings, intent-preserving fixes, approval states, one insights page, privacy disclosure, three formats, no video, no CMS plugins, no creative-suite integrations in Round 1.

---

## 11. Immediate next step

Before writing the PDF, confirm the team's real shape and strength: how many members, and whether the team is stronger on AI engineering or on product/full-stack. If the team is strong on AI, keep the fuller Gemini-plus-Citation-Lock plan as written. If the team is stronger on product/full-stack, bias the technical plan toward deterministic checks first and reserve the LLM for citation and rewrite suggestion under the same source_id gate. Either way, the originality story stays the same.
