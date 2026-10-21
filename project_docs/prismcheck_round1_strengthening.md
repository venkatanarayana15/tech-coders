# PrismCheck AI — How to Make This Win Round 1 (and Position for Rounds 2–3)

This read is a critique and upgrade of the PrismCheck concept against the Inkloom AI problem statement and the 11-section Round 1 PDF rubric. It is written so the team can lift exact paragraphs into the submission.

---

## 1. The core strategic shift (do not skip this)

The draft concept is already strong on the right thesis: **cite-or-silence, intent-lock, guideline health**. Keep that. The winning move is to sharpen three things that separate PrismCheck from every generic "AI content checker" team:

1. **Position against an existing category, not a vague problem.**
   Competitors exist: Marq (template + approval + DAM), Adobe GenStudio (brand compliance for performance marketing), Typeface (brand hub + AI generation with quality gates), CrawlQ (brand governance for AI content with BRAND Score). Several of these already claim "automated compliance checks before publication" and "brand consistency at scale."
   PrismCheck does **not** win by being another brand governance tool. It wins by occupying the **pre-publication audit layer that the generators and template tools do not own**: a cite-or-silence review gate that sits between content creation and publication, explains every finding with a specific approved source, and turns human overrides into guideline-quality evidence. That is a real gap. Marq locks templates; Adobe enforces brand compliance in campaign production; Typeface governs AI generation. None of them is marketed as the **explainable pre-flight courtroom** that reviews *any* uploaded draft—text, image, document—against a single source of truth and produces citations, not vibes.

2. **Make "explainability" concrete and verifiable, not a buzzword.**
   Judges will ask: "How do you prevent the LLM from inventing an 'off-brand' flag?" The answer in the draft is good—Pydantic schema forcing a `source_id`, drop findings with empty source, deterministic checks for banned terms and color. Strengthen it into a **named mechanism** with a clear failure mode: "The Citation Lock." Say explicitly that the system can **stay silent** when the kit has no rule, and that this silence is a *feature*, not a gap. Most tools over-flag; PrismCheck under-flags by design and routes the ambiguity to the Guideline Health signal. That is the originality story.

3. **Make the "guideline health" insight the differentiator, not an extra dashboard.**
   The brief explicitly asks for "insights into repeated mistakes or areas where the brand guidelines are unclear." Many teams will build "top violations." Fewer will build "rules that humans override so often the rule itself is probably wrong." PrismCheck's **Ambiguous Guideline Alert** is the answer to that line. Frame it as a governance insight that improves the brand kit itself over time, not just reports creator mistakes. That is the "self-optimizing brand book" angle.

---

## 2. Competitive reality check (cite these if asked)

Use these as evidence that the space is real and that PrismCheck has a defensible position.

- **The problem is real and quantified.**
  - Marq (2026): "62% of brand managers say brand consistency has gotten harder to maintain over the last two years."
  - Omnibound (2026): senior professionals at mid-sized and large businesses report poor brand consistency costs their companies more than **$6 million** in lost revenue/growth.
  - Shno.co / industry reporting: "Consistent branding can lead to up to a 23% revenue increase. 68% of companies say brand consistency added 10%–20% growth to their revenue."
  - Skyword / PR Newswire (2026): "When AI and brand messaging conflict, only 29% of consumers trust the brand."
  - Typeface (2026): enterprise teams report 5–7 revision rounds and 7–10 day approval cycles before governance; after governance, 2–3 rounds and 2–4 day cycles. They also report 40–60% faster approval cycles once governance is implemented.
  - CrawlQ (2026): brand governance for AI content is now driven by EU AI Act Article 50 transparency obligations and FTC scrutiny of AI content liability—defensibility is a procurement criterion.

  For Round 1, the strongest evidence mix is: one scale statistic (62% harder to maintain consistency), one cost statistic ($6M+ impact for poor consistency, or the 23% revenue lift from consistency), one AI-specific trust statistic (29% trust when AI conflicts with brand), and one workflow statistic (approval cycle compression). That gives you the problem's breadth, cost, urgency, and AI angle.

- **Competitors and why PrismCheck is different**
  - **Marq**: templates + approvals + asset management. Strong when creation happens inside its system. Weaker as an *audit* layer for content that already exists as a draft from somewhere else. PrismCheck's upload-and-review gate is the adjacent gap.
  - **Adobe GenStudio (Performance Marketing)**: brand compliance inside campaign production for ads/emails. Competes on the production side; PrismCheck competes on the *review-with-citations* side for drafts that may come from anywhere.
  - **Typeface**: brand hub + AI generation with quality gates. Governs generation. PrismCheck governs *what was produced*, including by external agencies, employees, and tools you do not control.
  - **CrawlQ**: brand governance for AI content, BRAND Score, knowledge graph grounding, audit trails. Closest philosophically. Difference: CrawlQ is framed around scoring AI output across 5 dimensions and grounding in a knowledge graph. PrismCheck is framed around **cite-or-silence pre-publication review with intent-lock and guideline health**, and it is format-spanning (text + image + document), not only AI-generation scoring.

  The cleanest one-liner for the judges: "Generator and template tools manage creation. PrismCheck manages the last gate before publish, and it does it with citations, not scores."

---

## 3. Strengthen the thesis line

Current draft thesis is strong. Make it even tighter and more contestable:

> "Growing organizations do not fail because they lack brand PDFs. They fail because employees, agencies, and AI tools publish before anyone checks claims, tone, visuals, and accessibility against a single approved source of truth. PrismCheck is the last gate before publish: it reviews content against the Brand Kit, explains every flag with a citation, suggests intent-preserving fixes, never auto-overwrites the creator, and turns repeated overrides into evidence that the guideline itself is unclear."

That sentence maps to every required capability. Other teams will say "AI reviews content." You say "the Brand Kit is the only admissible evidence."

Even sharper originality line for the PDF:

> "Other tools ask, 'Does this feel off-brand?' PrismCheck asks, 'Show the kit line or stay silent — and if humans keep overriding a rule, the kit is the bug.'"

---

## 4. The three winning angles, sharpened

### A. Cite-or-Silence Verification Engine (explainability + originality)
- Every finding shows: issue, guideline/fact/asset ID, quoted source, severity, suggested fix.
- If the kit has no rule, PrismCheck stays silent. No hallucinated "off-brand" flags.
- This is the direct answer to "identify the guideline or approved source involved" and "reliable, explainable results."
- Name it as the **Citation Lock**: structured output schema, source_id required, finding dropped if source_id is empty or does not match an ingested kit item. Banned-term and color checks run deterministically, not by LLM.

### B. Intent-Lock Rewriting (preserve creator purpose)
- Extract the creator's communicative intent first (urgency, excitement, announcement, warning, etc.).
- Provide two non-destructive alternative rewrites that fix tone/claims without stripping the creator's voice.
- If the creator is announcing a Diwali sale in red, the system does not force brand-blue; it routes to "Keep Mine + Note."
- This is the answer to "suggest corrections that preserve the creator's original purpose."

### C. Bi-Directional Telemetry / Guideline Health (the hidden scoring item)
- Two insights views:
  - Most flagged rules (creator errors)
  - Most overridden rules with a badge: "Rule may be unclear — review the Brand Kit."
- This is exactly "areas where the brand guidelines are unclear." Most teams will miss it.
- Frame it as **self-optimizing brand governance**: the system helps the brand team improve the kit, not just punish creators.

---

## 5. What judges in this contest will probably reward

Based on the brief, the rubric is likely something close to:

- Problem understanding and evidence (≈15–20)
- Relevance to the brief and coverage of required capabilities (≈20–25)
- Originality of approach (≈10–15)
- Feasibility and technical plan (≈10–15)
- Responsible design: privacy, security, human oversight, AI disclosure (≈10–15)
- Workflow, roles, collaboration, insights (≈10–15)
- Clarity of the plan and expected impact (≈5–10)

To win, PrismCheck must be **obviously complete against the brief** and **obviously different from generic AI checkers**.

The biggest risk to the submission is not feasibility—it is **genericness**. If the PDF reads like "AI reviews content against brand guidelines," PrismCheck loses to teams that add one sharper mechanism. The three mechanisms above—Citation Lock, Intent Lock, Guideline Health—are the sharpness. Emphasize them as *named, designed* features, not as loose capabilities.

---

## 6. Strengthened evidence plan for Round 1

Do not rely on one generic stat. Use a small, coherent evidence set:

1. **Scale**: 62% of brand managers say brand consistency has gotten harder to maintain over the last two years (Marq, 2026).
2. **Cost**: poor brand consistency costs mid-to-large businesses more than $6 million in lost revenue/growth (Omnibound, 2026); consistent branding can lift revenue up to 23%, and 68% of companies attribute 10%–20% revenue growth to brand consistency (industry reporting, 2026).
3. **AI urgency**: when AI and brand messaging conflict, only 29% of consumers trust the brand (Skyword/PR Newswire, 2026); EU AI Act Article 50 and FTC scrutiny make defensible AI content a procurement criterion (CrawlQ, 2026).
4. **Workflow pain**: before governance, 5–7 revision rounds and 7–10 day approval cycles; after governance, 2–3 rounds and 2–4 day cycles, with 40–60% faster approvals (Typeface, 2026).
5. **Persona quotes** (write 1 each, attributed to a role, not a real person unless you have one):
   - Creator: "I guess the tone and hope the manager doesn't catch it after deadline."
   - Manager: "I keep seeing the same mistakes on things that go live before I review them."
   - Agency: "Every client sends a different PDF, and I never know which one is current."

If you can get one real interview or survey response, do it. If not, the above stats plus the persona quotes are a credible evidence base for Round 1.

Also include 3 concrete public-style examples:
- A social ad that claims a product spec not in the approved fact bank.
- A banner using a banned promotional phrase (e.g., "100% guaranteed").
- A banner with low-contrast text that fails WCAG contrast.

---

## 7. Strengthened product architecture

### Brand Kit as the sole source of truth
- Four parts, kept tight: colors, terminology, approved facts, tone.
- Not a 50-page PDF parser. Structured ingestion.
- Facts marked Confidential stay in-org.

### Review pipelines
- Text pipeline: lexicon/banned terms (deterministic Trie), RAG claim verification against the Fact Bank (vector similarity + logic entailment), intent-lock tone rewrite.
- Visual pipeline: CIELAB Delta-E color distance, WCAG contrast ratio engine, OCR in-image text check, logo safe-zone check.
- Document pipeline (Round 2/3): extract text from PDF/DOCX and run the text pipeline; flag embedded images separately.

### Explainable diff view
- Cited guideline IDs and matched sources.
- Two intent-preserving suggested fixes.
- Two buttons: "Accept 1-Click Fix" and "Keep Mine + Add Context."

### Approval state machine
- Draft → Pending Review → Approved / Changes Requested.
- Comments, revision history, role-based queue.

### Insights
- Top recurring violations.
- Guideline Ambiguity Index: high-override rules flagged for brand kit review.

---

## 8. Strengthened responsible-design story

This is where many teams lose points. PrismCheck should be explicit:

- **Privacy shield**: client-side regex masks emails, phones, internal tokens before any API call. Brand Kit facts marked Confidential never leave the org.
- **AI disclosure**: UI states plainly what uses AI and what does not. Example: "Text analysis uses Gemini. Image colors run locally. No content is stored as training data."
- **Human control**: hard gates block publication for unsupported claims, contradicted facts, banned legal phrases; soft gates flag tone, color, accessibility for human review. AI never publishes. AI never silently rewrites.
- **Explainability**: every flag cites a source. If no source exists, the system stays silent and surfaces ambiguity to Guideline Health.

---

## 9. Strengthened feasibility story

- Frontend: React + Vite (or Next.js if the team prefers), Tailwind, Lucide, TanStack Table for the diff canvas.
- Backend: FastAPI.
- DB: PostgreSQL (Supabase or self-hosted).
- Text/claims/tone: Gemini with forced citation. ChromaDB for the private Fact Bank vector store.
- Image colors/contrast: Pillow/OpenCV local, deterministic, zero API cost.
- OCR/alt-text: Gemini Vision or EasyOCR.
- Auth: simple role JWT.
- File store: local or S3-compatible.
- Hardest technical part: stopping the LLM from inventing issues. Fix: structured JSON output, kit injected as the only context, drop any finding with empty source_id, plus deterministic regex/Trie pass for banned terms so claims are not LLM-only.

Feasibility is a win if the team commits to a tight scope:

- Round 2 ship: one Brand Kit, one submit flow, cited findings, 1-click fixes, approval states, one insights page, privacy disclosure.
- Formats: caption/text + image (social/ad) + PDF/DOCX one-pager. That covers text, images, documents without video.
- Do not promise Instagram API, Slack, Canva, or CMS plugins in Round 1.

---

## 10. Strengthened impact claims

Keep them grounded and tied to the evidence:

- ~85% reduction in review turnaround for routine social collateral and marketing copy (from days to under 30 seconds for routine checks; use the Typeface before/after framing as the basis).
- Elimination of compliance violations for unverified specifications, false pricing, and legally risky claims via hard-gate enforcement.
- Self-optimizing guidelines: converts static brand books into dynamic assets by diagnosing ambiguous guidelines through real-world creator behavior.

---

## 11. What to cut (kills feasibility and credibility)

- Multi-brand agency OS.
- Video/audio in Round 1.
- Live CMS plugins, Figma/Canva extensions in Round 1 (keep as future scope only).
- Two-AI debate or custom ML training.
- Over-broad promises about integrations.

---

## 12. One-paragraph version you can paste into the PDF's "Proposed Solution"

"PrismCheck AI is a pre-publication brand-governance engine that reviews text, images, and documents against an authoritative Brand Kit before anything is published. Unlike generators and template tools that manage creation, PrismCheck manages the last gate before publish. It uses a cite-or-silence verification engine: every finding is tied to a specific guideline, fact, or asset in the Brand Kit, and if the kit has no rule, the system stays silent rather than hallucinating an 'off-brand' flag. It preserves creator intent through intent-lock rewriting, which offers two non-destructive fixes that keep the creator's purpose. It balances automation with human control through hard gates for unsupported claims, contradicted facts, and banned legal phrases, and soft coaching for tone, color, and accessibility. It protects confidential materials with client-side PII masking and never stores content as training data, and it discloses AI usage in the UI. Over time, it turns repeated human overrides into Guideline Health insights that help the brand team improve unclear guidelines, not just flag creator mistakes."

---

## 13. Round 1 PDF map (11 sections, with the strongest framing)

1. **Understanding of the problem** — use the decentralized-content thesis + AI tools as a cause + manual bottleneck + cost/trade statistics above.
2. **Users affected** — creators, agencies/freelancers, brand/compliance managers; setting: mid-to-large D2C/fintech/edtech/SaaS publishing 30+ assets/week.
3. **Proposed solution** — the one-paragraph version above.
4. **End-to-end workflow** — the diagram in the draft is good; keep it and make sure each stage maps to a brief requirement.
5. **Main features** — use the feature table in the draft; keep Cite-or-Silence, Intent-Lock, Palette/Safe-Zone, WCAG engine, Collaborative Audit Queue, Guideline Health Index.
6. **Technology stack and technical plan** — keep the stack; make the "hardest technical part" paragraph explicit about stopping LLM invention.
7. **Responsibilities of team members** — keep the four roles; ensure they match the certificate.
8. **Development plan across all three rounds** — keep the three-round plan; commit to a tight Round 2/3 scope.
9. **Expected impact** — use the grounded impact claims.
10. **Future scope** — keep integrations, video, publishing webhooks as post-event only.
11. **Team and participant details** — ensure names/emails match certificate requirements exactly.

---

## 14. The single most important thing to add

Add a short section or paragraph that says, in plain language:

> "Most brand-governance tools ask whether content feels off-brand. PrismCheck asks for the kit line. If no kit line exists, PrismCheck says nothing and flags the ambiguity to the brand team. That is the difference between a checker that over-flags and a governance system that improves the brand book itself."

That is the sentence that positions PrismCheck against both generic AI checkers and the existing brand-governance vendors. Put it in the problem understanding, the solution, and the originality discussion.

---

## 15. Final checklist before submission

- Every required capability from the brief is covered in the PDF.
- At least 3 real/public examples of the kind of issue PrismCheck would catch.
- At least 1 persona quote per role.
- At least 3 quantitative evidence points with sources.
- The three named mechanisms—Citation Lock, Intent Lock, Guideline Health—are explained, not just listed.
- Privacy, security, human oversight, and AI disclosure are explicit.
- The scope is tight enough to be believable for Round 2/3.
- Team names and emails match certificate requirements exactly.

If you want, I can turn this into the full Round 1 PDF copy, section by section, with the exact paragraphs above folded in and the placeholders left for team names.
