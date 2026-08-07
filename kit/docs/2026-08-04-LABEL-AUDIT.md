# Label audit — every term and number in play, zero conflations

Aug 4, 2026. JC asked for a review of ALL labels after two same-day slips:
(1) a stand-in-vocabulary number was reported as a finding, (2) "pairs" and
"agencies" were conflated. This file is the single reference. If a term is not
here, it should not be used.

Status legend: **REAL** = safe to quote · **PENDING** = exists after JC
approves category lists · **ARTIFACT** = retracted, never quote ·
**SYNTHETIC** = simulation output, describes the machinery only.

---

## 1. The groups of agencies (populations)

| Label | Exactly who | Count | Status |
|---|---|---|---|
| Original 340 | The first study. 433 collected, minus not-an-agency (72) and dead sites (21). Has growth + bookability data. | 340 | REAL |
| Expansion cohort | New agencies found via directories + the trade register. No growth data yet. | 1,830 | REAL |
| Messaging-narrowers (raw) | Expansion agencies whose homepage message went broad → focused, single check | 155 | REAL |
| Messaging-narrowers (verified) | Same, survived 3 independent adversarial checks. **The primary set.** | 97 | REAL |
| Messaging-narrowers (strict) | Same, a second model also agreed independently | 55 | REAL |
| Twins (a.k.a. controls) | Broad-message agencies matched to narrowers for comparison | 300 | REAL |
| The 455 | 155 narrowers + 300 twins = everyone in the historical crawl | 455 | REAL |
| Agencies with extracted cases | Everyone with ≥1 case in the new case table. Bigger than 455 because it also holds original-340 sites whose today-pages were extracted. | 495 | REAL |

**Never conflate:** 155/97/55 are the SAME agencies at three strictness levels,
not three groups. "The 455" ≠ "the 495".

## 2. The time windows

| Label | Meaning | Status |
|---|---|---|
| before | Archived pages from ~1 year before the agency's message change (twins: assigned the same years as their narrower) | REAL |
| after | Archived pages from ~2 years after it | REAL |
| today | The live website, scraped Aug 3–4 | REAL (extraction 29% done) |
| say-side | What the agency claims about ITSELF in archived homepages — its message, not its clients | REAL (extraction 21% done) |

**Never conflate:** case-side (what clients they show) vs say-side (what they
claim). Same files, different question.

## 3. The six tests — plain names only

| Plain name | The question | Old code (do not use) |
|---|---|---|
| Said it and showed it | Changed message AND client mix — grew more than their twin? | H1 |
| Showed it quietly | New clients got narrower, message stayed broad — grew more? | H4 |
| Narrow right now | Client mix concentrated today vs spread today — who grew? | H3 |
| Born narrow | Always focused vs always broad — who grew? | H2 |
| Concrete proof | More concrete case studies — more growth? | H5 |
| Stacked focus | Narrow on several things at once — more growth? | H6 |

The four "trajectories" from the plan doc (T1–T4) map to: T1 = stayed broad,
T2 = showed it quietly, T3 = said it and showed it, T4 = born narrow. The T
codes are retired with the H codes.

## 4. Pairs vs agencies — the conflation that happened

| Term | Definition | Why it differs |
|---|---|---|
| Pair | One narrower + one matched twin. | Most narrowers have TWO twins, so pair counts run ~2× agency counts. **Report agencies, use pairs only inside the statistics.** |

The real coverage chain (client counts only — no categories involved, will
not move on Friday):

| Step | Agencies |
|---|---|
| Changed their messaging | **155** |
| …in at least one matched pair | 140 |
| …with ≥3 named clients in all four windows (own + twin) | **55** |

The 155→55 drop is thin Wayback archives (either side of the pair), not
agency behaviour.

## 5. Case-level labels (extraction output — all verbatim, all REAL)

| Field | Holds |
|---|---|
| client / client_key | Name as printed / normalized dedup key |
| named | Client identified by name, Y/N |
| delivered_raw | What was delivered, agency's own words |
| problem_raw | What the client hired them for, own words |
| sector_raw | What the client's business is, own words |
| model / stage / geo / channel_evidence | Verbatim fragments, empty if the text says nothing |
| depth | 5 structural rungs: logo-only → quote-testimonial → summary-tile → detailed-tile → full-case-page |
| has_number + metric | The case states a TANGIBLE RESULT (canonical term, JC Aug 4): a measurable outcome like "+40% omzet". Y/N + the outcome verbatim. Client size ≠ tangible result. |
| year_hint / duration_hint | When the work happened / how long the relationship |
| source_page | Which page it sat on (provenance for dedup) |

## 6. The seven axes (ways an agency can be narrow)

craft (what they make) · job (problem they solve) · industry (client's sector)
· business model (b2b, webshop…) · client stage (small, scale-up…) · channel
(Google, Shopify…) · geography. An agency's niche is a COMBINATION of axes.
Claimed-axis values for the original 340: REAL, on disk since Jul 31.
Case-side axis values: **PENDING** — need the approved category lists.

## 7. Every number used this session, with status

### REAL — safe to quote
| Number | What it is |
|---|---|
| 20,875 | Case rows extracted so far (5,555 of 6,467 files done) |
| 95% / 9.5% | Cases with a usable dedup key / quoting a numeric result |
| 91% · 100% · 99% · 97% | Reliability gate: two independent reads agreeing on case-recall · named+has-number · metric · depth |
| 155 / 140 / 55 | The coverage chain in §4 |
| ~260 | Agencies contributing to the no-twin sliding-scale tests |
| 0% vs 0%, p=0.97 (35 vs 135) | **Born narrow: NULL.** Always-focused grew no more than always-broad (original 340) |
| 355/358, 1,087 pages | The today-window scrape |
| 81% | Sales Nav growth coverage on the original 340 (planning input) |

### PENDING — do not quote until category lists are approved
Any concentration/biggest-bucket share · any case-mix-narrowed count · niche
depth (0–7) and combos · say/do gap · surviving pair count for "Said it and
showed it" · all thresholds (the 15-point rise, 50%/33%).

### ARTIFACT — retracted, never quote
| Number | Why dead |
|---|---|
| "26% narrowed their case mix" (also stated as 20%, and "3 of 4 didn't") | Computed with hashed stand-in categories |
| "12 pairs survive → test is dead" (also 8, 20) | Same contamination; real count unknown |
| "31 narrowed vs 97 flat" (Showed it quietly group sizes) | Same |
| Any median top1 share (0.22 / 0.25 / 0.33…) | Same |
| "Stand-in numbers are a lower bound" | Wrong direction claim — retracted |

### SYNTHETIC — machinery checks only
Power curves in simulation-report.txt (fabricated outcomes with known effect).
The Concrete-proof power curve used a real driver (specificity); the
Stacked-focus curve used a placeholder driver — treat both as design info, not
findings.

## 8. Standing rules going forward

1. No acronyms or code names anywhere JC reads.
2. Report agencies; pairs live only inside the statistics.
3. No concentration number leaves the analysis until `_measures_meta.json`
   says `"reportable": true` (code now raises an error otherwise).
4. Dry-run outputs carry a retraction header at the top of the file.
5. Anything derived from a stand-in vocabulary is an artifact, full stop.
