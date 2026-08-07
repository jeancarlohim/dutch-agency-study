# Test results — the six frozen tests, run on real growth

Aug 7, 2026. Cut-offs fixed by JC blind to growth (min 4 clients, 50%
concentrated, 15-point rise, 2-year growth primary, "narrow right now" on
what-they-sell only). Tests run exactly as frozen Aug 4. Growth = LinkedIn
monthly headcount, 388 usable companies. Full numbers:
`2026-08-07-mapping/results_full.json`.

## The verdict in one line

**Focus does not predict growth in this data — but publishing a case with a
tangible result does: 44% of those agencies grew vs 26% without, and it
survives every sensitivity check.**

## The six tests

| Test | Result | Numbers |
|---|---|---|
| Said it and showed it | **Cannot be run** | 0–4 pairs survive the filters (need ~30). Thin Wayback archives, not agency behaviour |
| Showed it quietly | Null | narrowed 36 vs flat 19, both median 0% growth, p=0.62 |
| Narrow right now | Null | concentrated 187 vs spread 24, both median 0%, p=0.37 |
| Born narrow | Null (unchanged) | 0% vs 0%, p=0.97 |
| Concrete proof (sliding scale) | Null | rho -0.06, p=0.36, n=256 |
| Stacked focus | Null | rho 0.01, p=0.85, n=256 |

Every null stays null at min clients 3/4/5, rise 10/15/20 points, growth as
percent and as people added, 1-year and 2-year.

## The one thing that replicated

July's signal, retested on the new instrument as registered (design doc §B5.3):
agencies showing **at least one case with a tangible result** vs none.

| Cut | With tangible result | Without | Gap | p |
|---|---|---|---|---|
| min 3 clients | 44% growing | 25% | +19pp | 0.0005 |
| min 4 (primary) | 44% growing | 26% | +19pp | 0.0015 |
| min 5 clients | 44% growing | 27% | +17pp | 0.0050 |
| 1-year growth | 32% growing | 19% | +13pp | 0.024 |

July found +12pp on the old instrument; this is +19pp on the better one.
It is a correlation on the after-window portfolios — reverse causality
(growing agencies have results to publish) is not ruled out. In the today
window the gap shrinks to +7pp and is not significant.

## Context for reading the nulls

- The market is flat: 33% of agencies grew, 29% shrank, 38% exactly flat.
  Median growth is 0% in every group — the medians tests compare are zeros.
- The pooled-language rule from the pre-registration was never triggered:
  nothing to pool. "Narrowing and growth travel together" is NOT supported.

## What this means, one sentence each

1. The thesis "agencies that narrowed are pulling more demand" did not
   survive contact with the growth data, on any of the five ways it was asked.
2. The publishable finding is the proof finding: showing measurable client
   results travels with growth; narrowing alone does not.
3. "Said it and showed it" died on archive coverage, not on the answer —
   report it as not testable, not as a null.

## Addendum — inside the categories (JC asked, Aug 7 evening)

Registered cuts (pre-registered Aug 4, so safe to quote):

| Cut | Result |
|---|---|
| Narrowing vs growth, small agencies (≤3 people) | null (rho +0.02, p=0.88) |
| … medium (4–11) | null (rho −0.01, p=0.95) |
| … large (12+) | null (rho +0.09, p=0.49) |
| Growth spread widens with focus (the double-edged bet) | no clean pattern (sd 0.26 / 0.37 / 0.44 / 0.32 across concentration bands) |

Exploratory (NOT registered — 5 groups, one will look good by luck):

| Concentrated on | n | Grew |
|---|---|---|
| Video, animatie & fotografie | 12 | 42% |
| Campagnes & creatieve concepten | 12 | 33% |
| Website & webdesign | 46 | 24% |
| Branding & huisstijl | 27 | 22% |
| Grafisch ontwerp, drukwerk & print | 11 | 18% |

Industry concentration: too thin to slice — fewer than 8 agencies per client
sector concentrate at 50%+.

The cleanest cut of the thing JC sells — sharpened their MESSAGE vs stayed
broad: 97 verified narrowers 36% grew, twins 33% (p=0.59). Null.

Nothing inside the categories rescues the narrowing thesis.

## Addendum 2 — the confound-controlled grid (JC, Aug 7 evening)

JC's concern: agencies with big accounts grow regardless of positioning, and
that could bury the effect. Checked.

Premise first: agencies showcasing big/corporate clients grew LESS, not more
(22% vs 34%, p=0.056, n=32 — thin, since client size is stated in only 4% of
cases; this is "who brags about corporates", not "who has them").

Eight declared cuts, all exploratory, counted honestly:

| # | Cut | Grew | p |
|---|---|---|---|
| 1 | Narrowed vs flat, big-client agencies excluded | 46% vs 27% | 0.064 |
| 2 | Concentrated now vs spread now, big excluded | 34% vs 33% | 0.46 |
| 3 | Message AND portfolio both narrowed vs neither | 38% vs 26% | 0.38 |
| 4 | Narrowed vs flat, only agencies WITH proof | 48% vs 47% | 0.54 |
| 5 | Narrowed vs flat, agencies without proof | 27% vs 15% | 0.52 |
| 6 | Proof + concentrated vs proof + spread | 34% vs 33% | 0.52 |
| 7 | Narrowed vs flat, ≤5-person agencies only | 19% vs 12% | 0.96 |
| 8 | Message narrowers (97) vs twins, big excluded | 36% vs 34% | 0.75 |

**0 of 8 significant.** Cut 1 is the closest thing to JC's story in the whole
sweep (46% vs 27% once big-client agencies are removed, p=0.064) — but it is
one cut of eight, unregistered, at n=28 vs 37. It is a lead for a FUTURE
study designed around it, not a finding this one can print.

Note the direction across cuts 1/3/5/7: narrowers edge flat agencies in four
low-power cuts. Consistent with a small real effect this study is too small
to prove — and equally consistent with nothing. The honest sentence for the
article: "if narrowing helps headcount growth, the effect is too small to see
in 2 years of data on ~400 agencies — unlike proof, which shows up loudly."

## Addendum 3 — the predictor sweep and JC's stuck-profile prediction

One declared sweep, 14 features vs 2-year growth (n up to 388). Hits:

| Signal | rho | p | Read |
|---|---|---|---|
| Median staff tenure | −0.38 | <0.0001 | mechanical — growth creates new hires, new hires create low tenure. Not usable as a driver |
| Agency size | +0.13 | 0.012 | bigger agencies grew a little more |
| Agency age | −0.11 | 0.031 | younger agencies grow more: young 40% grew vs old (15y+) 27% |

Null: publishing pace, message breadth (say-side), client churn, case
specificity, full case pages, foreign staff share, breadth-bragging.

JC's pre-written prediction (Aug 4, before growth data): "old + broad + no
proof = stuck". Tested: that profile grew 32% vs 34% for everyone else,
p=0.67 — null. Of its three ingredients only AGE separates on its own.

## The bottom line after every cut

Ran in total: 6 frozen tests, registered size/age subgroups, category slices,
an 8-cut confound grid, a 14-feature sweep, and JC's own registered
prediction. What growth tracks in this data, in order of strength:

1. having at least one case with a tangible result (+19pp, robust)
2. being young (+13pp, registered subgroup)
3. being bigger (small)

What growth does not track, anywhere, in any slice: narrowing the client
mix, narrowing the message, focus depth, or any positioning measure held.
Further slicing of THIS dataset is fishing; the positioning question needs a
different outcome (pricing, win rate, revenue per head) or a longer window.
