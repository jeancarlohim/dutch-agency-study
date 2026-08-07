# Locked decisions — do not re-open

Decided by JC, Jul 27–28, 2026. Claude Code: read before every run.
If new evidence contradicts one, REPORT it — do not act against it.

## Dates
- JC stops working Aug 7. Away Aug 10–21. Back Aug 24.

## The study
- ONE Dutch study: national, 433 agencies. Rotterdam is a later zoom-in
  from the same dataset, published after JC returns.
- 433 = 394 national + 39 net-new Rotterdam. Duplicates removed (6).
  Giants OUT: DEPT, iO, Merkle.
- Depth: the FULL schema for everyone (actual count is 31 columns, not 23 —
  triage run found only 2 fields map 1:1 between the national and Rotterdam
  sources; see outputs/2026-07-28-column-triage.md). Do not flatten.
- Column decision (made Jul 28, a day early): of the 21 columns missing on
  the 388 national rows, recompute 19 for FREE (LLM read of cached homepage
  text, all on Sonnet — see Model rule below). Skip `url` (doesn't apply to
  national). Do NOT run a full-coverage paid Apify pass for `founder`.
  JC's framing for the article: founder-posting alone doesn't separate
  winners from stuck — the point is sharper than "skip it": it shows that
  posting without strong positioning doesn't move the needle. That's a
  supporting beat for the thesis, not a scored dimension. Sample `founder`
  only for the ~40 Loom people if the color is wanted for those videos.
- Model rule: use Sonnet for all new scoring, never Haiku, for the whole
  project. Confirmed (searching prior session transcripts + the actual
  scripts) that national's existing cta_type/positioning_class ran on
  Haiku (CLAUDE-CODE-BRIEF.md), while Rotterdam's 21 deep fields were
  teardown'd in an interactive Claude Code session reusing the US/UK
  study's codebook — which prior sessions confirm was Sonnet-verified.
  So Sonnet for new work matches Rotterdam's rubric, not national's old
  Haiku pass. The existing Haiku-scored national cta_type/positioning_class
  fields stay as-is (not being redone) — noted as a known, accepted gap.
- The article MUST include growth proof (the thesis: agencies that sharpened
  their positioning are pulling more demand — shown with headcount growth,
  new client logos, reviews, hiring). Ranking-only is not worth publishing.
- Numbers rule: no topline percentages until all 433 are scored on the SAME
  rubric. Never cite agencies-raw.tsv revenue (fabricated).
- No metered API calls anywhere in this project, for anything — not just
  Apify. All LLM scoring runs through JC's Claude subscription (Claude Code
  sessions), never a separately billed Anthropic API key. Cost estimates in
  outputs/2026-07-28-column-triage.md (e.g. "~$2-3 on Sonnet") were priced
  as if metered API — they don't apply. Budget this in TIME, not dollars.

## Publishing
- Channel: LinkedIn newsletter. No site build.
- Daniela publishes the finished draft Monday Aug 10.
- NOTHING sends before the article is live. Publish first, then messages.

## The gate
- Nothing happens until the article is done. No filming before the article
  is final. Article final = Aug 4 (hard gate).

## Looms
- Loom = per-person video showing where they stand in the ranking.
- Cap ~25–30 total. Order: (1) the 7 connected S1/S2 first,
  (2) the worthwhile rest of the ~36 connected, (3) new accepters by ~Aug 5.
- Only filmable for people connected before JC leaves.

## Outreach tiers
- Top 40 ranked (top ~20%): congratulations message + article. No Loom.
- Below top 40: Loom candidates, within the cap.
- 20 connection requests/day, triggered by JC daily, started Jul 28.
  JC prefilters the Connect tab himself.

## People
- Daniela: shared VA. ~1 hour/day on JC's account. She executes only —
  research and writing are JC's. She gets instructions, not decisions.
- Kirian: a CLIENT (not staff). Daniela also sends for her account.
- Evan: client, workshop Sep 1. Before Aug 7: intake-chase message + handover
  note to Daniela (keep warm, escalate, no delivery).
- Deb: in Tanzania until Aug 21. Parked. Nothing to do.

## Parked until after Aug 24
- Coach study + coach outreach (JC may add IF time and Claude budget fit —
  not planned in, not counted on).
- Rotterdam zoom-in piece.
- Supabase read cutover (needs JC supervision — never flip while away).
- Multi-ICP tags feature (two-accounts model covers the need for now).
- Both email newsletters. The 25 recheckable rejected profiles.

## Class field — unified definition (JC, Jul 30, after run 04)
- Rotterdam's original 45 rows used `class: generalist` for 38 rows (plain broad shops, no
  niche claim) and `class: real-specialist` for 7. That token isn't in the locked 6-token
  codebook run 04 used for the 388 national rows. JC's call: fold `generalist` into
  `false-niche`. Definition, unified across both halves of the 433:
  - `real-specialist` = genuinely focused on ONE niche/vertical.
  - `false-niche` = everything broad/not-genuinely-niched — whether it fakes a niche landing
    page or is just an honest full-service generalist. One bucket, no sub-distinction.
  - `mislabeled` = a real specialist, but a different niche than the name/LinkedIn suggested.
  - `not-an-agency` = a product, SaaS tool, holding co, directory, or individual
    freelancer/artist — not a marketing/positioning agency at all.
  - `dead-or-blocked` = site down, blocked, parked, or had no extractable content.
  - Applied: `outputs/2026-07-30-scored-433-v2.csv` remaps Rotterdam's 38 `generalist` rows
    to `false-niche`. This is now the canonical scored file (v2, not the original
    2026-07-30-scored-433.csv).

## Exclude non-agencies and dead rows from the study (JC, Jul 30)
- The 72 national rows scored `class: not-an-agency` (SaaS products, holding cos, directories,
  solo freelancers/artists — not marketing/positioning agencies) are OUT of the study. They
  don't get ranked, don't get a Loom, don't get outreach.
- The 21 `class: dead-or-blocked` rows (site down, blocked, parked, or no content) are OUT
  too — same treatment. Decided Jul 30, after the scoring report.
- Study population after exclusions: 295 national + 45 Rotterdam = **340 rows**.
- Neither group is deleted from the raw CSV — kept as the audit trail for why 388 became 295.
  Physical filtering into a "ranking set" happens at the ranking step (Gate 1), not now.

## Ranking rule — decided (JC + Fable, Jul 30)
- Mechanism: points score (Option 2). Weights: proof 8 pts/case capped at 8 cases,
  focus 25 (class 15 + icp 10), message 20 (fivesec 8 + kpi 7 + enemy 5), assets 12
  (method 7 + engine 5), skin 3 (risk 2 + pricing 1). Max score 125.
- Deliberately weighted zero: from_industry, founder, type, the old Haiku columns.
- Proof cap 8 (not 5): an agency publishing 12 numbered cases shows more proof than
  one with 5; 8 still stops the 14-case outlier from running away. Verified effect:
  top-40 membership identical at cap 5/6/8/uncapped — only the order at the very top
  moves. Dapper (the Sales-Nav-verified grower) is #1.
- Congrats tier = top 40 UNIQUE COMPANIES (not rows). Two contacts at one company
  share one slot and inherit the company rank. Top 40 companies = 43 contact rows.
- Sensitivity-tested: zero-proof agencies cannot enter the top 40 under any tested
  weight variant; message-weights-halved churns 1 border row; mislabeled-to-zero
  churns 0. Membership is proof-driven; weights only reorder within the tier.
- Ranked table: outputs/2026-07-30-ranked-340-v2.csv (supersedes the same-day v1).
- Still subject to JC's Friday sanity check against agencies he knows (Gate 1).

## Working style (binding for Claude Code)
- Plain language. Short sentences. No jargon. Tables over prose.
- Plans before execution, always. Execution starts only when JC says go.
- Questions for JC are asked when the plan that needs them is on the table,
  not before.
