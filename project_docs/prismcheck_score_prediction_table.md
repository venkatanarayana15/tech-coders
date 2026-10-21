# PrismCheck — Round 1 Score Prediction Table

This is an honest, rubric-based prediction of how the **strengthened PrismCheck plan** scores in Round 1, where it is strong, where it is still exposed, and what would move each score up or down. It is a prediction, not a guarantee. Judges are human and the exact wording in the PDF matters more than the plan does.

---

## Score table — Round 1, 100 points total

| Criterion | Points | Where PrismCheck stands now | Predicted score | Stronger than most teams? | Still exposed at |
|---|---|---|---|---|---|
| Understanding of the problem statement | 25 | High. Maps to the brief line by line; evidence package is sourced; setting is specific; the "approval alone is not governance" thesis is credible. | **22–24** | Yes — most teams will be generic here. | If the PDF drifts into "AI content is a problem" without tying every point back to the brief's specific lines, especially "unclear guidelines" and "preserve creator purpose" and "disclose AI." |
| The proposed solution | 25 | High, if the walkthrough is in the PDF. The workflow is concrete and covers every required capability. | **22–24** | Yes — if it is narrated as one real scenario, not only a diagram. | If it becomes a feature list connected by arrows and the judge cannot picture a person using it. |
| Technical plan | 20 | High. Names the hardest part, gives the Citation Lock architecture, explains stack choices, and keeps the LLM path honest. | **17–19** | Yes — the deterministic-vs-LLM split and the source_id drop rule are real technical differentiation. | If claims overshoot what the team can defend in Q&A, especially around "logic entailment" or RAG reliability. |
| Originality of approach | 15 | Medium-high, and improving. The three mechanisms are real. But another Inkloom team already claimed "human in control / current vs proposed," so "human in control" alone is no longer a strong originality claim. | **12–14** | Yes — if originality rests on Citation Lock + Intent Lock + Guideline Health. | If originality rests mostly on "we keep humans in the loop and show a diff," it gets crowded out by the other team's claim. |
| Feasibility and scope | 15 | Medium-high. Scope is focused and the build order is believable. | **13–15** | Yes — focused scope is a real advantage if the PDF commits to it. | If the PDF name-drops too many integrations, formats, or AI bells and whistles, it starts to look unreal. |
| **Total** | **100** | | **~86–96** | | |

---

## Where PrismCheck is stronger than most teams

1. **The brief mapping is unusually complete.** The plan does not just "cover brand governance." It traces the solution back to the specific brief lines: cite the source involved, preserve creator purpose, support multiple formats, provide insights into unclear guidelines, balance automation with human control, protect confidential materials, disclose AI. That is what the 25-point understanding and 25-point solution buckets reward.

2. **The evidence package is sourced, not decorative.** Most hackathon plans quote one or two weak stats. PrismCheck now has a tight set: the 62% harder-to-maintain figure, the 95%-have-guidelines-but-25–30%-use-them gap, the Lucidpress/Marq revenue-consistency range and the 68% figure, the Edelman trust figures, the AI-content-volume figure, the Typeface before/after approval-cycle framing, the Aprimo "approved content can still fail" point, and the AI-trust figure. That is enough to make the problem feel real without padding.

3. **The hardest technical part is named and addressed, not buried.** Judges like plans that say, in plain language, what is hard and how the architecture survives it. The Citation Lock with a required source_id, a middleware drop rule, and deterministic banned-term/color/contrast checks is exactly that kind of answer.

4. **The originality has three legs, not one slogan.** Cite-or-silence, intent-lock rewriting, and guideline health are three different mechanisms that each answer a different line in the brief. That is more robust than a single "we add explainability" claim.

5. **The scope is defendable.** One kit, one submit flow, cited findings, 1-click fixes, approval states, one insights page, privacy disclosure, three formats. That reads as buildable. Buildable reads as higher feasibility than "we also integrate with everything."

---

## Where PrismCheck is still exposed

1. **Originality is the most crowded bucket.** Another Inkloom team has already used the "AI doesn't silently rewrite / founder stays in control / current vs proposed" frame in public. If PrismCheck leans on that frame as its originality story, it will look similar to at least one other entrant. The fix is already in the plan: originality must rest on the three mechanisms, not on human-control as a slogan.

2. **The score depends heavily on the walkthrough being in the PDF.** The solution section is strong on paper, but if the PDF only contains a diagram and a feature table, it loses the "judge can picture a real person using it" advantage. The walkthrough is the difference between a 22–24 and a weaker score here.

3. **Technical credibility is only as good as the team's ability to explain it.** The plan is credible, but Round 1/2 judges may ask a member to explain the Citation Lock, the Fact Bank, or the deterministic checks. If the team cannot explain the source_id drop rule and why banned terms are not LLM-only, the technical score drops regardless of what the plan says.

4. **Evidence is strong but still secondhand in places.** The plan attributes numbers correctly, but a judge who wants the underlying primary source may probe. The team should know, at minimum, that the consistency/revenue figures trace to Lucidpress/Marq State of Brand Consistency and the trust figures to Edelman, and that the AI-trust figure traces to Skyword as reported by PR Newswire.

5. **Feasibility is strong only if the team does not inflate the PDF.** The plan is buildable as written. It stops being buildable if the PDF starts promising video, live CMS plugins, Canva/Figma extensions, Instagram integration, or custom model training in Round 1. That is the easiest way to lose feasibility points after having earned them.

---

## What would push this from ~86–96 toward the top of the range

- Put the named carousel walkthrough in the solution section, in plain prose, not just a diagram.
- Make the three originality mechanisms appear together in one short, named treatment, with one sentence each.
- Keep the technical plan's claims defensible in Q&A: structured output, kit-injected context, source_id required, findings dropped if source_id is empty or unmatched, banned terms and color/contrast deterministic, LLM used for citation and rewrites under the same rule.
- Keep the evidence short and attributed, with the consistency, trust, AI-volume, approval-cycle, and approved-content-fails points all present.
- Keep the scope tight in writing. If something is future scope, say so explicitly.

---

## What would drop the score

- Making the solution abstract: "AI checks content against brand guidelines" with no walkthrough.
- Making originality a human-control slogan without the three mechanisms behind it.
- Over-claiming the technical story beyond what the team can explain.
- Inflating scope so the plan stops looking feasible.
- Dropping the responsible-design section or the AI-disclosure line, since the brief asks for both explicitly.

---

## Bottom line

Against this rubric, the strengthened PrismCheck plan is not a generic AI brand checker and it is not over-scoped. If the PDF executes the plan as written — especially the walkthrough, the three-mechanism originality treatment, and the honest technical explanation — it should land in the top band of Round 1, with the largest remaining risk being originality crowding from another team's similar human-control framing. The single highest-value move is to make originality concrete rather than slogan-based.
