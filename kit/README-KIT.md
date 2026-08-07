# The analysis kit — everything needed to answer a new question

Aug 7, 2026. Slim by design: the final agreed taggings and the per-agency
numbers, without the raw scrape text. Any question answerable in this study is
answerable from these files.

## To ask a new question, start here

**data/cases_tagged.csv** — one row per case, with the FINAL agreed buckets
already applied (definition v2, all seven approved lists, the mapping run of
Aug 7). Columns:

| Column | Holds |
|---|---|
| domain, cohort, window | which agency, which group (narrower / control / original340), before / after / today |
| client_key | dedup key; empty = anonymous case |
| named, depth, has_number | Y/N named client · structural depth · states a tangible result |
| metric_kinds | kind(s) of tangible result: revenue_sales; leads_inquiries; traffic; conversion; seo_positions; ad_performance; reach_views; other |
| bucket_industry … bucket_geo | the approved bucket per focus type; empty = the case says nothing on that axis; "unknown" = says something the lists cannot place |

Dedup rule when counting clients: one per client_key, richest case wins.
Anonymous cases: dedup on identical text, can make an agency narrow but never
scattered (JC's definition v2).

## The other data files

| File | What |
|---|---|
| measures_v2.csv | per agency × window: focus scores, distinct clients, specificity — the frozen engine's output |
| 2026-08-07-growth.csv | growth per agency (LinkedIn monthly chart): percent AND people added, 6m/1y/2y + pivot years |
| 2026-08-07-growth-excluded.csv | the 44 dropped on identity mismatch |
| 2026-08-07-sayside-mapped.csv | what each agency claimed about itself per snapshot year, same buckets |
| narrowness_v2_today.json | JC's final narrow/scattered/not-measurable status per agency |
| kit_bucket_counts.csv | per agency × window × axis: distinct clients per bucket (named and anonymous separated) |
| kit_metric_kinds.csv | per agency × window: counts per kind of tangible result |
| results_full.json | the six frozen tests + sensitivity runs, full output |

## The rules that bind any new number

1. Minimum 4 distinct clients before an agency gets a focus score.
2. Comparisons need ≥40 agencies per side; a gap under 10 points is not a
   finding (measured tagging-noise floor).
3. Growth medians are 0% almost everywhere — compare share-growing, and
   check percent AND people added.
4. Correlation wording only. Nothing here proves causation.
5. Exploratory cuts: declare them before running, count hits against luck
   (~1 in 20 at p<0.05).

## docs/ — what was already answered (read before recomputing)

test-results (+ 3 addendums) · mapping-coverage (accuracy + noise floor) ·
proof-age-size-grid · distributions-for-cutoffs · the July docs (thesis test,
alignment finding, lifecycle, article angle) · label audit · pre-registration ·
decisions · the full RUNLOG.

## code/ — the exact scripts behind every number

stats_lib (permutation tests) · measures.py (frozen engine) ·
run_the_six_tests.py (frozen tests) · run_tests.py (JC's cut-offs) ·
rules.py (the keyword mapper) · build_growth.py · distributions.py ·
noise_test.py (the 40-per-side floor).
