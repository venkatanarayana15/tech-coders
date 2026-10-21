# PrismCheck — Round 1 Reassessment Against the Real Rubric

This read compares the current PrismCheck direction against the actual Inkloom AI Round 1 brief and the 100-point rubric, then gives a verdict: keep and strengthen, or switch to a different approach. It also names the exact risks that could cost points.

---

## The real rubric, translated into what PrismCheck must show

### 1. Understanding of the problem statement — 25 pts
The brief is explicit. What judges want to see:
- You know the problem is **decentralized content creation across employees, agencies, and AI tools**.
- You know the failure modes: incorrect claims, outdated info, inconsistent language, off-brand visuals.
- You know the required capabilities: review before publication, check against approved guidelines/facts/assets, detect tone/terminology/messaging/visual consistency/accessibility/unsupported claims, **explain each issue and suggest corrections that preserve the creator's original purpose**, review/approval workflow with collaboration and change tracking, support multiple formats, insights into repeated mistakes **and unclear guidelines**, balance automation with human control, protect confidential materials, produce reliable explainable results.
- You have evidence the problem is real.
- You know the organizational setting.

PrismCheck currently maps well to this. The risk is not missing the brief — it is **sounding like every other team that will say "AI checks content against brand guidelines."** At 25 points, the understanding section rewards teams that show they have internalized the specific lines in the brief, especially:
- "explain each issue and suggest corrections that preserve the creator's original purpose"
- "areas where the brand guidelines are unclear"
- "protect confidential materials and clearly disclose the use of AI or external services"

PrismCheck already owns these three. Keep them. Make them impossible to miss.

### 2. Proposed solution — 25 pts
Judges want:
- A solution that directly addresses the identified problem.
- A main workflow that is clear and specific enough that the judges can understand how someone would use the product.

This is where the current draft is strong on vision but could be weaker on **concrete use**. The workflow diagram is good. What it needs is a **named, walkable scenario** that a judge can follow step by step, not just a pipeline. The strongest Round 1 submissions will read like: "Here is exactly what the brand manager does, here is exactly what the creator does, here is what the creator sees when something is flagged, here is how the creator responds, here is what the manager sees in review." If your PDF makes the judge picture a real person doing a real task, you win this section. If it reads like a feature list connected by arrows, you lose compared with teams that do the same thing but narrate a scenario.

### 3. Technical plan — 20 pts
Judges want:
- Why you selected your stack.
- The most technically challenging part.
- How your planned architecture will address it.

PrismCheck's technical plan is one of its best parts. The "hardest part: stop the LLM from inventing issues, and here is the Citation Lock" story is exactly what this section wants. Two small risks:
- Do not over-claim. If you say "RAG claim verification using vector similarity and logic entailment," be ready to explain what entailment means here and what happens when it fails. Judges may ask. Keep the claim honest: vector similarity against the Fact Bank plus a deterministic banned-term pass, with the LLM restricted to citing kit items. That is believable and protectable.
- Do not bury the deterministic-vs-LLM split. The brief literally asks for "reliable, explainable results." The architecture that delivers that is: deterministic checks for banned terms and color/contrast, LLM restricted to citing kit items for tone/claim/intent, and a middleware gate that drops findings with no valid source_id. Say that plainly.

### 4. Originality of approach — 15 pts
Judges want:
- What makes your interpretation, solution, workflow, or approach different from other teams.

PrismCheck's strongest originality assets:
- Cite-or-silence: no flag without a cited kit line; silence when the kit is silent.
- Intent-lock: preserve creator purpose; two non-destructive fixes.
- Guideline Health: overrides diagnose unclear guidelines, not only creator error.
- Hard gates vs soft coaching: automation balanced with human control.

The risk here is not that the ideas are weak — it is that 15 points is a smaller pool, so the originality must be **sharp and memorable**, not broad. A team that says "we add explainability + workflow + insights" is adding generic capabilities. A team that says "we refuse to flag anything that cannot cite a kit line, and we treat human overrides as a signal about the kit, not the creator" is making a defensible originality claim. The second is PrismCheck. Make the PDF say the second.

### 5. Feasibility and scope — 15 pts
Judges want:
- Can your team realistically build this in the available time?
- A focused, achievable solution scores higher than an unnecessarily large idea.

This is the section where PrismCheck is **most at risk if it drifts**. The current direction is already scoped reasonably well. The danger is scope creep in the PDF: if you name too many formats, too many integrations, or too many AI features, you signal that you do not understand feasibility. Round 1 is a plan, but the plan is judged on whether it is buildable. The safest PrismCheck scope for Round 1:
- One Brand Kit, one submit flow, cited findings, 1-click fixes, approval states, one insights page, privacy disclosure.
- Formats: text/caption + image (social/ad) + PDF/DOCX one-pager. That covers "text, images, documents" without pretending to do video or live CMS.
- No Instagram API, no Slack, no Canva/Figma in Round 1. Those belong in future scope only.

If your team is small or inexperienced, shrink further: text-only first, image pipeline as a clearly-marked next step, document pipeline as a clearly-marked next step. A smaller, believable scope beats a larger, shaky one at 15 points.

---

## Verdict: strengthen, do not switch

The current PrismCheck direction is strong enough to win if it is executed well. I would **not** switch to a different idea, for three reasons:

1. It already covers every required capability from the brief, in a way that is more specific than a generic "AI brand checker."
2. It has three genuinely distinctive mechanisms that are not standard in the category.
3. Switching ideas at this point would cost you the understanding-of-the-problem depth you have already built, and Round 1's biggest bucket is understanding.

The right move is not a new idea. It is a **tighter, more judge-facing version** of this one — trimmed of anything that sounds like scope creep, narrated around one concrete walkthrough, and making the three originality mechanisms impossible to miss.

---

## What a stronger PrismCheck Round 1 looks like, concretely

### Make the workflow a named walkthrough, not just a diagram

Give the PDF one concrete scenario and walk it. Example:

> A creator at a mid-size fintech drafts a LinkedIn carousel announcing a new credit-card offer. They upload the copy and the banner image. Before anything is sent to the manager, PrismCheck runs locally: emails and internal tokens are masked. The text pipeline checks the claim "no annual fee for life" against the Fact Bank; the Fact Bank does not contain that claim, so it is flagged as an unsupported claim with a hard gate. The tone pipeline extracts the intent as "urgent promotional offer" and offers two rewrites that keep urgency while removing the unsupported promise. The image pipeline checks the banner colors against the Brand Kit palette and flags one color that is outside the approved Delta-E range, and checks alt text against WCAG. The creator clicks "Keep Mine + Note" on the color flag because the marketing team has an approved exception, and accepts the rewrite on the claim. The draft moves to Pending Review. The manager sees the claim fix, the color exception note, the alt-text suggestion, and approves. In the Insights tab, the manager later sees that the "no annual fee" claim type has been flagged three times this month, and that the color rule flagged in this carousel is one of the top five overridden rules, flagged with "Rule may be unclear — review the Brand Kit."

That paragraph does more for the solution score than a feature table does, because it shows the judge exactly how a person uses the product and exactly how the originality mechanisms behave in a real case.

### Make the three originality mechanisms legible in one place

Do not bury them across sections. Give them one short, named treatment, ideally in the solution section, with one sentence each:

- **Citation Lock:** PrismCheck flags an issue only when it can cite a specific guideline, fact, or asset from the Brand Kit. If the kit has no rule, the system stays silent rather than inventing an "off-brand" judgment.
- **Intent Lock:** before suggesting a rewrite, PrismCheck extracts the creator's intent and offers two fixes that preserve it, because the brief asks for corrections that preserve the creator's original purpose.
- **Guideline Health:** when a rule is overridden repeatedly, PrismCheck flags it to the brand team as a possible unclear guideline, because the brief asks for insights into areas where the brand guidelines are unclear.

That is the originality section in miniature. Judges should be able to repeat it after one read.

### Make the evidence concrete and short

Round 1 asks for evidence that the problem is real. The strongest evidence package is small and coherent:
- One scale statistic on brand consistency getting harder.
- One cost statistic.
- One AI-specific stat about trust or liability.
- One workflow statistic about approval cycles.
- Three concrete issue examples of the kind PrismCheck would catch.
- One persona quote per role, clearly labeled.

Keep it short. Judges read many submissions. A tight evidence block beats a long one.

### Make responsible design explicit, not implied

The brief asks for "protect confidential materials and clearly disclose the use of AI or external services." Put that in its own short subsection:
- Client-side PII masking before any API call.
- Brand Kit facts marked Confidential stay in-org.
- A UI disclosure line: what uses AI, what runs locally, whether content is stored as training data.
- Hard gates for claims/facts/banned phrases; soft coaching for tone/color/accessibility; AI never publishes; AI never silently rewrites.

### Make the technical plan honest about the hard part

Say plainly:
- Hardest part: preventing the LLM from inventing issues.
- Architecture answer: structured output schema requiring a source_id from the ingested kit; findings with empty or non-matching source_id are dropped; banned terms and color/contrast run deterministically; the LLM is restricted to citing kit items and generating intent-preserving rewrites.
- Why the stack: React/Vite or Next.js for the inspection canvas; FastAPI for the backend; Postgres for audit/role/version data; Gemini for structured text work; ChromaDB for the private Fact Bank; Pillow/OpenCV for deterministic color and contrast; optional Gemini Vision or EasyOCR for in-image text and alt text; role JWT for auth; local or S3-compatible file store.

That answers "why this stack" and "what is hard and how we address it."

### Make feasibility believable

State the Round 1 scope in one paragraph and defend it:
- We are building one Brand Kit, one submit flow, cited findings, 1-click fixes, approval states, one insights page, and a privacy disclosure.
- We are covering text, image, and document formats through a single review flow, not attempting video or live CMS integrations.
- The hardest piece, the Citation Lock, is built first because it is the backbone of explainability; if it works, the rest composes around it.
- Round 2 adds the full approval workflow and user testing; Round 3 adds Guideline Health depth and polish.

If your team is smaller or less experienced, say so honestly and shrink the scope rather than over-promise.

---

## The two ways this idea could lose

### Risk A: It reads as a generic AI brand checker
If the PDF says "AI reviews content against brand guidelines and suggests fixes," you blend in. If it says "PrismCheck refuses to flag anything that cannot cite a kit line; if humans keep overriding a rule, the kit is the problem," you stand out. The difference is the sentence you lead with.

### Risk B: It sounds too big to build
If the PDF names many formats, many integrations, video, and two-AI debate, you look unrealistic at the feasibility criterion. If the PDF names a focused scope, builds the hardest piece first, and marks the rest as Round 2/3, you look buildable. Feasibility is a smaller bucket than understanding or solution, but it is an easy place to lose points you cannot get back elsewhere.

---

## One alternative angle worth considering, only if your team is weaker on AI engineering

If your team is not confident building the Citation Lock and Fact Bank RAG reliably in the event window, there is a different, still-defensible PrismCheck shape:

**PrismCheck as a deterministic-first governance gate with AI only for the parts that need it.**

In that version:
- Banned terms: deterministic Trie/regex, no LLM.
- Color and contrast: deterministic Pillow/OpenCV, no LLM.
- Logo safe zone: deterministic geometry check, no LLM.
- Fact/claim verification: a simpler exact-match-plus-semantic-similarity check against the Fact Bank, with the LLM used only to propose a citation and a rewrite, and still gated on a source_id.
- Tone and intent: LLM, but only for suggesting rewrites, and only with intent extraction first.

Why consider this: it reduces the part of the system that is most likely to fail under judge scrutiny, and it makes the "reliable, explainable results" claim easier to defend, because the most safety-critical checks are deterministic. The trade-off is that it is slightly less ambitious on the AI side. For Round 1, that trade-off can be worth it if your team's strength is more full-stack/product than AI engineering. If your team is strong on AI, keep the fuller version.

---

## What I would not change

- Do not drop the cite-or-silence idea. It is the spine of the originality claim and the best answer to "reliable, explainable results."
- Do not drop intent-lock. It is the best answer to "preserve the creator's original purpose."
- Do not drop Guideline Health. It is the best answer to "areas where the brand guidelines are unclear," and it is a line in the brief that many teams will miss.
- Do not drop the hard-gate/soft-coach split. It is the best answer to "balance automation with human control."
- Do not drop the privacy/AI-disclosure section. It is explicitly in the brief.

---

## Decision helper

If your team can honestly build the fuller PrismCheck with the Citation Lock, Fact Bank RAG, intent-lock rewrites, image color/contrast, document extraction, approval workflow, and Guideline Health — and can explain the hard part without waving — keep the current direction and make it judge-facing as above.

If your team is stronger on product/full-stack than on AI engineering, or the event window is short, switch to the deterministic-first version: keep cite-or-silence and intent-lock as the story, but make the claim-verification and image checks deliberately deterministic where possible and reserve the LLM for rewrites and citation suggestion. Still original. Still complete against the brief. Easier to defend.

Either way, do not invent a new product. The win here is execution sharpness on a already-good idea.
