# Pre-registration — how the six questions get tested

Aug 4, 2026. Written and frozen **before** any growth data exists on disk.
That is the whole point: the test code cannot be tuned to the answer if the
answer has not arrived yet. This closes the forking-path risk that already
burned this project once (the retracted alignment thesis).

Nothing here is a result. Everything here is a decision about how a result
will be produced.

---

## 1. What is decided in advance

| Choice | Locked value |
|---|---|
| Primary treatment set | the **97** Sonnet-verified narrowers |
| Sensitivity sets | 55 (Sonnet+Opus) and 155 (raw) |
| Primary measure | deduped **new-clients-only** biggest-bucket share |
| Primary outcome | `growth_2y` |
| Primary tier | **Tier A only** (pivot 2022–2024) for any causal-flavoured wording |
| Everything else | exploratory, and labelled exploratory in the report |
| Model for any new scoring | Sonnet (locked decision, Jul 28) |

**Language rule, binding.** Pooled results say *"narrowing and growth travel
together."* The phrase *"narrowing came first"* is earned only by Tier A, and
only if it holds there.

## 2. The measures (computed before growth is joined)

Per agency × window, after deduplicating clients by `client_key`:

| Measure | Plain English |
|---|---|
| distinct clients | how many different clients shown in that window |
| **biggest-bucket share** | of distinct clients, the fraction in the single biggest category |
| spread score (HHI) | second way to measure the same thing — backup check only |
| **new-clients-only mix** | concentration of clients present at AFTER and absent at BEFORE |
| carried / dropped | which clients stayed, which vanished |
| avg specificity (0–4) | named + number + full case page + sector stated |
| per-axis concentration | biggest-bucket share on each of the 7 axes |
| **demonstrated depth (0–7)** | how many axes concentrate at the same time |
| demonstrated combo | which axes, e.g. "ecommerce + SEO" |

**Never compare raw case counts across windows.** After-windows hold ~50% more
archived pages for mechanical reasons. Shares and concentration only.

## 3. The six tests

No codes. Each test is named for what it asks. (The older plan documents call
these H1–H6; the mapping is in the last column so old notes still line up, but
nothing downstream uses the codes.)

| Test name | The question, in plain words | Population | Who counts as narrowed | Status today | old code |
|---|---|---|---|---|---|
| **Said it and showed it** | Agencies that changed their message AND their client mix — did they grow more than their matched twin who changed neither? | 97 verified narrowers + matched twins | message narrowed AND case mix rose ≥15 pts; twin flat | data complete, needs growth. Sample size unknown until real categories exist — see §6 | H1 |
| **Showed it quietly** | Agencies whose new clients got narrower while their message stayed broad — did they grow more? | 300 twins | new-clients-only share rose ≥15 pts | data complete, needs growth. Viable | H4 |
| **Narrow right now** | Agencies whose client mix is concentrated TODAY vs spread out today — who grew more? | 300 twins | share now ≥50% vs ≤33%, ≥4 clients | **blocked** — needs today-window scrape | H3 |
| **Born narrow** | Agencies that were always focused vs always broad — did the always-focused grow more? | original 340 only | existing `path` column | **already answered — null, see §6** | H2 |
| **Concrete proof** | Do agencies with more concrete case studies (named client, real number, full write-up, sector stated) grow more? | everyone with cases + growth | sliding scale 0–4 | data complete, needs growth. Well powered | H5 |
| **Stacked focus** | Do agencies that are narrow on several things at once (e.g. webshops + SEO + one sector) grow more than those narrow on one thing? | everyone with cases + growth | sliding scale 0–7 | data complete, needs growth. Well powered | H6 |

"Case mix narrowed" is measured on **all seven axes**, and the winning axis is
recorded — "became an ecommerce-SEO shop" and "went all-in on schools" are
different stories that industry-only tagging would merge or miss.

## 4. Cut-offs are placeholders until JC fixes them

The 15-point rise, the 50%/33% split, the minimum-client filters: all
placeholders. They get fixed **after** tagging, from the real distributions,
and **before** growth is joined. Every result is then re-run at neighbouring
cut-offs. **A finding that exists at only one exact threshold is not a
finding.**

## 5. What this design cannot do

Stated up front so it does not have to be discovered in the write-up.

1. **It cannot prove causation.** Growth is counted backwards from Aug 2026.
   Only Tier A aligns the growth window with the pivot, and even there the
   sequence is reconstructed, not observed.
2. **It is underpowered for the growth-magnitude test.** The benchmark is ~220
   agencies for 80% power; the realistic matched-pair count is far below that.
   Section 6 gives the measured numbers.
3. **The treatment label is noisy.** Independent strong models disagree on
   35–43% of broad-to-niche calls. That noise floor is intrinsic to the
   judgment, not a weak-model artifact.
4. **Controls were filtered less harshly than narrowers** (1 pass vs 3 lenses +
   Opus). Any narrower-vs-control gap inherits that asymmetry until a control
   audit is run.
5. **Reverse causality is live.** Growth buys nicer portfolios. The
   new-clients-only measure and Tier A timing are partial guards, not proof.
6. **Survivorship, twice.** Dead agencies fell out at triage; portfolios show
   winners. Every claim is about the *published portfolio* — "what they show" —
   never "who they serve."

## 6. The honest expected n

### 6a. What is real now (does NOT depend on any category list)

These counts come from client counts and dedup keys only. No vocabulary is
involved, so they will not move when the real categories land.

| Coverage step | Agencies |
|---|---|
| Classified as having changed their messaging | **155** |
| …appearing in at least one matched pair | 140 |
| …with ≥3 named clients in **all four** windows (own + twin, before + after) | **55** |

The drop from 155 to 55 is Wayback archiving, not agency behaviour: a pair dies
if *either* side has a thin archive. Tests that need no twin keep far more
agencies — roughly **260** contribute to the sliding-scale tests.

Growth then has to exist on both sides of a pair. At the original 340's Sales
Nav coverage (81%), ~0.81² ≈ 66% of pairs survive.

### 6b. What is NOT known yet

**Any number involving concentration, biggest-bucket share, case-mix
narrowing, or niche depth does not exist yet.** Those require the approved
category lists. A dry run using a hashed stand-in vocabulary was performed on
Aug 4 purely to prove the code paths execute; its outputs are mechanical
artifacts and must never be quoted, including:

- how many agencies "actually narrowed their case mix"
- the surviving matched-pair count
- whether the matched-pair test is viable at all

The stand-in produced ~470 industry buckets against a real list of 17. Plan
§3b predicts exactly what that does — with buckets that fine, no agency ever
has two clients in the same bucket, so everything looks scattered by
construction. That is a property of the stand-in, not of the agencies.

**Rule for this file:** no concentration number enters this document until
`mappings/` is populated with JC-approved lists and `_measures_meta.json`
reports `"reportable": true`.

### 6c. Already answered, and safe to quote

**Born narrow: null.** Always-focused vs always-broad on the original 340 —
median growth 0% vs 0%, p=0.97, n=35 vs 135. Uses the existing `path` and
`growth_2y` columns; no categories, no placeholder, nothing pending.

## 7. What lands Friday, in order

1. Finish extraction (912 files: today-window + say-side)
2. Frequency tables per axis — free
3. Derive the six vocabularies → **GATE: JC approves each list**
4. Apply mappings, compute measures, show real distributions
5. **GATE: JC fixes cut-offs from those distributions** — still blind to growth
6. Join growth, run the frozen tests, report however they land

Steps 1–4 change no code in `2026-08-04-analysis/`. The tests are already
written. Friday is: drop in the approved mappings, drop in the growth CSV,
run.

## 8. The files

| File | What |
|---|---|
| `2026-08-04-analysis/build_case_table.py` | merges every extraction batch → `cases_v2.csv` |
| `2026-08-04-analysis/measures.py` | the §2 measures; category mapping is a pluggable layer |
| `2026-08-04-analysis/run_the_six_tests.py` | the six tests + the power simulation |
| `2026-08-04-analysis/stats_lib.py` | rank/permutation stats, stdlib only |
| `2026-08-04-analysis/mappings/<axis>.json` | **empty until JC approves** — drop-in on Friday |
| `2026-08-04-analysis/simulation-report.txt` | measured power at the real n |

Growth enters through exactly one door: a CSV with
`domain, employees_now, growth_6m, growth_1y, growth_2y`, passed as
`--growth`. No other file in the analysis reads an outcome variable.
