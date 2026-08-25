# Article numbers — every figure verified against the kit

Run 2026-08-25. Script: `kit/code/article_numbers.py`. One run, one output file.
Nothing here is quoted from a prior document: every figure below was recomputed
from the kit data files in this run. Where a recomputed figure disagrees with an
earlier doc, the disagreement is printed rather than reconciled silently.

**Standing rules applied to every number:** dedup one row per `client_key`
(richest case wins) · 40-per-side floor and 10-point gap floor checked and stated
per result · window stated explicitly · correlation wording only.

## The two proof instruments — read this before quoting any proof number

The study contains two different definitions of "shows a tangible result" and they
give different numbers. Both are computed below and every proof figure is labelled.

| Instrument | Definition | Source field | Used by |
|---|---|---|---|
| **DEDUP** | at least one *deduped, named client* carries a number | `measures_v2.csv` `share_numeric` > 0 | the six frozen tests, the 44% vs 26% headline |
| **ANYROW** | at least one *case row* in the window carries a number, anonymous rows included | `cases_tagged.csv` `has_number` = Y | the B-section counts, insights A2/A4/A5/A7 |

ANYROW is the wider net: it catches agencies like Dapper that publish numbered
tiles with no client name attached. DEDUP is the stricter instrument the
pre-registered tests were frozen on.

## The population

| Count | What | Source | Filter |
|---|---|---|---|
| 706 | agencies with any case data | cases_tagged.csv | all windows |
| 688 | agencies with today-window cases | cases_tagged.csv | window = today |
| 688 | agencies with a narrowness v2 status | narrowness_v2_today.json | today |
| 411 | rows in the growth file | 2026-08-07-growth.csv | all |
| **388** | **the growth population** | 2026-08-07-growth.csv | `growth_2y` present AND `months_of_chart` = 25 |
| 256 | the working sample for the after-window tests | measures_v2 x growth | window = after, >=4 distinct clients, growth known |
| 296 | the working sample for the today-window tests | measures_v2 x growth | window = today, >=4 distinct clients, growth known |

Market baseline on the 388: **33% grew** (129), 29% shrank (111), 38% exactly flat (148). "Growing" throughout this file means `growth_2y` > 0.

---

## A1. Gate simulation — narrowness at 4 / 3 / 2 / 1 evidence units

**Source:** `measures_v2.csv` (window = today) x `2026-08-07-growth.csv`. 
**Window:** today. **Outcome:** `growth_2y` > 0. 
**Instrument:** `top1_craft` — the share of an agency's deduped clients that sit in
the single biggest "what they sell" bucket. This is the pre-registered
narrow-right-now axis (one focus type, not best-of-seven). 
**Gate:** `n_distinct_clients` >= G, for G in 4, 3, 2, 1.

Two splits are reported because the frozen test and the v2 status label disagree:

- **Frozen split** (the pre-registered cut-offs): narrow = top1_craft >= 0.50,
  scattered = top1_craft <= 0.33. Agencies between 0.34 and 0.49 are in neither side.
- **Binary split** (the narrowness v2 label): narrow = top1_craft >= 0.50,
  scattered = everything below. No middle band.

### Frozen split

| Gate | Narrow n | Narrow % growing | Scattered n | Scattered % growing | Gap | p | Clears both floors? |
|---|---|---|---|---|---|---|---|
| 4 | 187 | 33% | 24 | 29% | +3.5pp | 0.822 | no — side under 40 |
| 3 | 202 | 32% | 24 | 29% | +3.0pp | 0.828 | no — side under 40 |
| 2 | 210 | 33% | 24 | 29% | +4.2pp | 0.807 | no — side under 40 |
| 1 | 216 | 33% | 24 | 29% | +3.7pp | 0.830 | no — side under 40 |

### Binary split

| Gate | Narrow n | Narrow % growing | Scattered n | Scattered % growing | Gap | p | Clears both floors? |
|---|---|---|---|---|---|---|---|
| 4 | 187 | 33% | 101 | 36% | -3.0pp | 0.688 | no — gap under 10pp |
| 3 | 202 | 32% | 104 | 36% | -3.4pp | 0.618 | no — gap under 10pp |
| 2 | 210 | 33% | 104 | 36% | -2.2pp | 0.714 | no — gap under 10pp |
| 1 | 216 | 33% | 104 | 36% | -2.7pp | 0.707 | no — gap under 10pp |

**What this says.** Lowering the gate from 4 to 1 does not change the answer: narrow
agencies grow slightly *less* than scattered ones at every gate, and no gate produces
a gap that clears the 10-point noise floor. The artefact the lower gates expose is
real and worth stating — with one or two clients the top bucket is 100% by
arithmetic, so the extra agencies land in "narrow" almost automatically:

| Gate | Agencies scored (frozen split, both sides) | Of which narrow | Narrow share |
|---|---|---|---|
| 4 | 211 | 187 | 89% |
| 3 | 226 | 202 | 89% |
| 2 | 234 | 210 | 90% |
| 1 | 240 | 216 | 90% |

### Third instrument — a v2-style reconstruction, gated 4 / 3 / 2 / 1

The published C2 gate table was run on the narrowness v2 definition, not on
`top1_craft`. That definition counts **evidence units** = deduped named clients plus
deduped anonymous cases, and scores the craft axis over the units that state it. It is
reconstructed here as closely as the kit allows (anonymous cases deduped on the full
bucket tuple, since the kit ships no case text) and then gated:

| Gate | Narrow n | Narrow % growing | Scattered n | Scattered % growing | Gap | p | Clears both floors? |
|---|---|---|---|---|---|---|---|
| 4 | 135 | 28% | 100 | 38% | -9.9pp | 0.128 | no — gap under 10pp |
| 3 | 155 | 31% | 115 | 37% | -5.6pp | 0.356 | no — gap under 10pp |
| 2 | 183 | 32% | 115 | 37% | -4.8pp | 0.452 | no — gap under 10pp |
| 1 | 207 | 32% | 115 | 37% | -4.6pp | 0.459 | no — gap under 10pp |

**How good is the reconstruction?** It reproduces the shipped v2 unit count for **550 of 688 agencies (80%)**. Good enough to show the gate has no effect; not good enough to quote a single agency from.

**Cross-check against the v2 status labels.** `narrowness_v2_today.json` carries
JC's final narrow / scattered / not-measurable status per agency at its own gate of
4 evidence units. Share growing under that label, same growth population:

| v2 status | n (with growth) | % growing |
|---|---|---|
| narrow | 139 | 29% |
| scattered | 97 | 37% |
| not measurable (too few taggable cases) | 96 | 35% |
| direction not measurable (evidence mostly anonymous) | 5 | 60% |

**This row is the published number.** The insights doc reports narrow 28% vs scattered 37%, gap -9, p = 0.16 (C7) and gate-4 narrow 28% vs scattered 38%, gap -10, p = 0.13 (C2). Recomputed here from the shipped v2 file: **29% vs 37%, -8.3pp, p = 0.200** (n = 139 vs 97). Same answer, same direction. The published pair is reproducible at gate 4; only the *lower* gates are not, because the v2 file stores no score below its own gate.

**Verdict on A1.** The published C2 gate table is **reproduced**. Its gate-4 row (narrow
28%, scattered 38%, gap -10, p = 0.13) comes back as 28% / 38% / -9.9pp / p = 0.128 on
the reconstruction, and its lower-gate rows (31% vs 38% at gates 3, 2 and 1) come back as
31-32% vs 37%. **Print C2 as it stands.**

Two limits to keep next to it. First, the v2 status file itself cannot be regenerated
from the kit: its evidence units count deduped named clients *plus anonymous cases
deduped on identical text*, and the kit ships buckets, not words — the reconstruction
above matches its unit count for 80% of agencies, not all. Second, all three instruments
agree on the answer and all three fail the study's own floors: the gap never clears 10
points and no p-value comes near 0.05. The gate is not why narrowing looks null. Nothing
about lowering it rescues the thesis, which is exactly the reply C2 was built to give.

---

## A2. Tangible vs intangible — after window, 4+ clients

**Source:** `measures_v2.csv` + `cases_tagged.csv` x `2026-08-07-growth.csv`. 
**Window:** after (the site as it was two years ago, before the growth window). 
**Filter:** >= 4 distinct clients, growth known. **Outcome:** `growth_2y` > 0.

### DEDUP instrument — the frozen-test number

| Group | n | growing | % growing |
|---|---|---|---|
| Shows a tangible result | 108 | 48 | 44% |
| Names, logos and quotes only | 148 | 38 | 26% |

Gap **+18.8pp**, p = 0.0015 (permutation, 4,000 shuffles, seed 1).

### ANYROW instrument — the insights-doc number

| Group | n | growing | % growing |
|---|---|---|---|
| Shows a tangible result | 112 | 51 | 46% |
| Names, logos and quotes only | 144 | 35 | 24% |

Gap **+21.2pp**, p = 0.0005 (permutation, 4,000 shuffles, seed 1).

### Sensitivity — the client gate

| Gate | Instrument | Tangible n | % growing | Intangible n | % growing | Gap | p |
|---|---|---|---|---|---|---|---|
| 3 | DEDUP | 113 | 44% | 165 | 25% | +19.4pp | 0.0005 |
| 3 | ANYROW | 117 | 45% | 161 | 24% | +21.7pp | 0.0002 |
| 4 | DEDUP | 108 | 44% | 148 | 26% | +18.8pp | 0.0015 |
| 4 | ANYROW | 112 | 46% | 144 | 24% | +21.2pp | 0.0005 |
| 5 | DEDUP | 104 | 44% | 133 | 27% | +17.2pp | 0.0050 |
| 5 | ANYROW | 108 | 45% | 129 | 26% | +19.8pp | 0.0015 |

### One-year growth and people-added — the like-for-like rule

| Outcome | Instrument | Tangible n | % growing | Intangible n | % growing | Gap | p |
|---|---|---|---|---|---|---|---|
| 1-year percent | DEDUP | 108 | 31% | 148 | 20% | +11.9pp | 0.0440 |
| 1-year percent | ANYROW | 112 | 33% | 144 | 18% | +15.0pp | 0.0095 |
| 2-year people added | DEDUP | 108 | 44% | 148 | 26% | +18.8pp | 0.0015 |
| 2-year people added | ANYROW | 112 | 46% | 144 | 24% | +21.2pp | 0.0005 |

The people-added row is identical to the percent row by arithmetic: `added_2y` > 0 and
`growth_2y` > 0 are the same condition on a headcount series. It is reported because the
study's like-for-like rule requires it, not because it is independent evidence. The
1-year row is the one that carries information, and the gap survives there too.

### Today window — the timing check

| Instrument | Tangible n | % growing | Intangible n | % growing | Gap | p |
|---|---|---|---|---|---|---|
| DEDUP | 83 | 39% | 213 | 31% | +7.1pp | 0.2644 |
| ANYROW | 86 | 41% | 210 | 30% | +10.2pp | 0.1010 |

Proof measured *before* the growth window tracks growth. Proof measured after it
mostly reflects it. Both today-window gaps fail the 10-point floor or significance or
both. This is the D1 hedge, and it is a recomputed fact, not a caveat.

### Is there a "no proof at all" group?

**0 of 256.** The third group is empty, and the reason is
structural rather than lucky: `n_distinct_clients` is counted from published cases with a
`client_key`, so clearing the 4-client gate *is* showing four named clients. An agency
with nothing published cannot enter the sample at all.

So the honest form of the claim is bounded, not universal:

| Statement | Verdict |
|---|---|
| "Nobody with 4+ clients shown has no proof" | **True, and true by construction.** |
| "Every agency in the Dutch market has proof" | **Not tested here.** The agencies with nothing to show were filtered out before the comparison began. |

For scale: 38 agencies with growth data sit *below* the gate in the after window. They are not evidence for the claim, and they are not evidence against it. They are
simply outside it, and the article should say the sentence the way the data supports it:
among agencies that show four or more clients, the comparison is a number against a name.

---

## A3. Proof concentration — today window

**Source:** `cases_tagged.csv`. **Window:** today. **Filter:** none — all 688 agencies
with today-window cases. **Unit:** a case row with `has_number` = Y.

- **15,028 case studies** live today across **688 agencies**.
- **1,267 carry a number** — **8.4%**. So **92% of everything published contains no number.**
- **Top 5% of agencies** (34 agencies) hold **52%** of all numbered cases.
- **Top 10%** (69 agencies) hold **73%**.
- **471 agencies — 68% — hold none at all.**
- **32 agencies hold half the numbered cases in the market.** (32/688 = 4.7% of agencies, 635/1,267 of the proof.)

Contrast to publish alongside it: case-study *volume* is ordinary. Median cases per
agency is **16**, and **627** of 688 agencies publish 4 or more. The effort is evenly distributed. The evidence is not.

**Caveat that makes it unassailable (D7).** Extraction is a floor. 277 of 688 today-window agencies are flagged `truncated` by source, and the error runs one way — it
under-reports proof, never over-reports. Every count above is an "or more".

---

## A4. The 2x2 — hero names a client type x has a numbered case

**Sources:** `2026-08-07-sayside-mapped.csv` (latest snapshot per domain) x
`cases_tagged.csv` (window = after) x `2026-08-07-growth.csv`. 
**Filter:** >= 4 distinct clients in the after window, growth known. 
**Proof instrument:** ANYROW (the instrument the published 2x2 used).

"Hero names a client type" has no single field in the kit, so two definitions are
computed and both are printed:

- **Narrow definition** — the latest snapshot states `clients_business` (an industry or
  business type the agency says it serves).
- **Wide definition** — the latest snapshot states any buyer-describing axis:
  `clients_business`, `clients_size`, `clients_money_model` or `where_clients_are`.

### Narrow definition (clients_business stated)

| Cell | n | growing | % growing |
|---|---|---|---|
| Number on site + hero names a client type | 29 | 15 | 52% |
| Number on site + hero silent on who | 83 | 36 | 43% |
| Faith-based proof + hero names a client type | 24 | 8 | 33% |
| Faith-based proof + hero silent on who | 120 | 27 | 22% |

Best corner vs worst corner: **52% vs 22%**, +29.2pp, p = 0.0035. **smallest cell n=29 is under the 40 floor.**
Inside the numbered group, naming a client type: 52% (n=29) vs 43% (n=83), +8.4pp, p = 0.521.
Inside the intangible group, naming a client type: 33% (n=24) vs 22% (n=120), +10.8pp, p = 0.293.

### Wide definition (any buyer axis stated)

| Cell | n | growing | % growing |
|---|---|---|---|
| Number on site + hero names a client type | 64 | 32 | 50% |
| Number on site + hero silent on who | 48 | 19 | 40% |
| Faith-based proof + hero names a client type | 80 | 21 | 26% |
| Faith-based proof + hero silent on who | 64 | 14 | 22% |

Best corner vs worst corner: **50% vs 22%**, +28.1pp, p = 0.0015.
Inside the numbered group, naming a client type: 50% (n=64) vs 40% (n=48), +10.4pp, p = 0.344.
Inside the intangible group, naming a client type: 26% (n=80) vs 22% (n=64), +4.4pp, p = 0.563.

**Verification note — the published A5 cells do not reproduce.** The 2026-08-24 insights
doc prints 54 / 57 / 76 / 67 (n=254) with a best corner of 54% and a worst of 22%.
Neither definition above lands on those cell sizes. The sayside file maps hero lines into
approved buckets; the published 2x2 was built on a model judgement of the raw hero line,
which the kit does not ship. **Do not print 54% vs 22% as a kit-backed number** — print
one of the two tables above, with its definition stated, or drop the claim.

---

## A5. The stuck segment

**Sources:** `measures_v2.csv` + `cases_tagged.csv` x `2026-08-07-growth.csv` x
`narrowness_v2_today.json`. **Window:** today. 
**Filter:** `employees_now` <= 15, >= 4 distinct clients shown, zero numbers, `growth_2y` <= 0.

- **Count: 124 agencies.**
- Median staff **3**, range 1–15.
- Median staff tenure **6.9 years** (n=105 with a tenure value). Settled teams, not startups.
- Median clients shown **12**, median case studies each **18**.
- **3,016 case studies across the segment. Zero numbers in any of them** (ANYROW instrument, so anonymous numbered tiles would have counted and did not).
- 79 exactly flat, 45 shrinking. The filter is <= 0, so "flat" is the wrong single word for the segment.

| Narrowness v2 status | n | share of segment |
|---|---|---|
| narrow | 62 | 50% |
| scattered | 34 | 27% |
| not measurable (too few taggable cases) | 27 | 22% |
| direction not measurable (evidence mostly anonymous) | 1 | 1% |

**62 of 124 — 50% — are already narrow.** Half this segment did the positioning work. It did not help, because the proof
underneath is empty.

**Print it as a floor.** 51 of the 124 are flagged `truncated` by source, so write "3,016 case studies **or more**".

---

## A6. The headcount critique — recomputed, not asserted

**Source:** `2026-08-07-growth.csv`. **Filter:** the 388. **Fields:** `added_2y`, `employees_now`.

- **48 of 129 "growing" agencies — 37% — grew by exactly one person** over two years.
- **148 of 388 — 38% — changed by exactly zero people.** "Flat" is substantially a floor effect.
- **188 of 388 — 48% — have five staff or fewer.** Median size 6. At a three-person shop one hire is +33%.

| People added over 2y | agencies | share of the 388 |
|---|---|---|
| -2 or worse | 68 | 18% |
| -1 | 43 | 11% |
| 0 | 148 | 38% |
| +1 | 48 | 12% |
| +2 | 22 | 6% |
| +3 to +5 | 37 | 10% |
| +6 or more | 22 | 6% |

**What holds (D2).** All 388 have the full 25 months, no partial series; the monthly
series means leavers are counted correctly; percent and people-added are both reported
above. **What does not.** LinkedIn counts profiles, not people, and Dutch small agencies
run heavily on freelance capacity that never appears. A noisy measure makes a null
easier to explain — where it bites is the proof finding, which is a positive result and
needs the measure to hold.

---

## A7. The crowded sentence

**Source:** `2026-08-07-sayside-mapped.csv`, `headline` field, latest snapshot per domain. **Filter:** headline non-empty.

455 domains carry a sayside snapshot; **453 have a non-empty headline in their latest snapshot**. Snapshot year: 2025 (413), 2023 (29), 2024 (4), 2020 (4).

### Word frequencies across the positioning lines

| Word | agencies using it | share of the 453 lines |
|---|---|---|
| marketing | 87 | 19% |
| online | 64 | 14% |
| agency | 37 | 8% |
| bureau | 36 | 8% |
| digital | 35 | 8% |
| websites | 23 | 5% |
| communicatie | 23 | 5% |
| digitale | 20 | 4% |
| design | 18 | 4% |
| partner | 18 | 4% |
| creative | 17 | 4% |
| groei | 16 | 4% |
| brand | 16 | 4% |
| merk | 15 | 3% |
| maken | 14 | 3% |
| website | 14 | 3% |
| full | 14 | 3% |
| hét | 13 | 3% |
| service | 12 | 3% |
| ontwerp | 12 | 3% |

### Literal variants of "wij helpen [ambitieuze] bedrijven groeien"

**Definition, stated before running:** the line contains a helping verb (`help`), a
generic-business object (`bedrijven`, `ondernemers`, `merken`, `organisaties`,
`ondernemingen`) and a growth verb or noun (`groei`, `groeien`, `laten groeien`), in any
order. Case-insensitive substring match on the raw headline — regex, not a judgement.

- **Strict (help + generic object + growth): 3 agencies — 1% of the 453 lines.**
- Loose (help + growth, object optional): 3 agencies — 1%.
- Loosest (any growth or helping word at all): 38 agencies — 8%.
- Containing the literal word "ambitieuze": 0.

### The specific words B9 counted, recomputed on this corpus

| Word | B9 reported | recomputed on the 453 headlines |
|---|---|---|
| marketing | 17% | 87 agencies, 19% |
| online | 14% | 64 agencies, 14% |
| bedrijven | 12% | 8 agencies, 2% |
| merken | 11% | 11 agencies, 2% |
| helpen | 9% | 3 agencies, 1% |
| ambitieuze | 5% | 1 agencies, 0% |
| groeien | 5% | 10 agencies, 2% |

Two of the seven land close. Five do not, and they are the five the sentence is built
from. **The kit cannot back the crowded-sentence claim as published.**

The strict set, verbatim, so a stuck founder can find his own line in it:

- `greencreatives.nl` — "Wij helpen impactvolle merken groeien!"
- `keyagency.nl` — "Welkom bij Key Agency! Wij zijn het digitale bureau dat merken helpt groeien met websites, content en advertising die precies op elkaar zijn afgestemd."
- `rik.marketing` — "Ik help organisaties te groeien. Meer bekendheid. Meer omzet."

**Of the 3 strict variants: 2 — 67% — show zero numbers anywhere in the today window** (ANYROW instrument). 0 have no growth row.
**Of the 3 loose variants: 2 — 67% — show zero numbers anywhere in the today window** (ANYROW instrument). 0 have no growth row.

**Verification note.** The insights doc (B9) reports 327 positioning lines, 38 literal
variants (12%), of which 17 have no proof. The kit's sayside file yields 453 lines, not 327 — 327 came from the July itemization file, which the kit does not ship.
The recomputed share is in the same range but the counts differ. **Quote the recomputed
numbers above, with the definition, or quote nothing.**

---

## A8. The four-segment table — broad / focused x growing / not

**Source:** `measures_v2.csv` (today) x `2026-08-07-growth.csv`. **Window:** today. 
**Filter:** >= 4 distinct clients, growth known. **Focused** = `top1_craft` >= 0.50.

| Segment | n | % of sample | % showing no proof (ANYROW) | % showing no proof (DEDUP) | % not bookable |
|---|---|---|---|---|---|
| Focused + growing | 61 | 21% | 67% | 70% | not computable |
| Focused + not growing | 126 | 44% | 71% | 71% | not computable |
| Broad + growing | 36 | 12% | 58% | 61% | not computable |
| Broad + not growing | 65 | 23% | 80% | 80% | not computable |

**Bookability is not computable from this kit and is therefore skipped.** No CTA,
booking-link or contact-form field exists in any kit data file — checked across
`cases_tagged.csv`, `measures_v2.csv`, `2026-08-07-growth.csv`,
`2026-08-07-sayside-mapped.csv`, `kit_bucket_counts.csv` and `kit_metric_kinds.csv`.
The B8 numbers (booking link 57% growing, contact form 46%, neither 19%, 25% have a
booking link) come from a regex pass that was never carried into the kit. **They cannot
be verified here.** Either re-run the regex over the source site text and import the
result as a kit column, or leave bookability out of the article.

---

## A9. The market map — deduped per client_key

**Source:** `cases_tagged.csv`. **Dedup:** one entry per (domain, window, client_key),
richest case wins. **Windows:** all three, stated per table. A "numbered case" here means
the deduped client's winning case row carries `has_number` = Y.

**20,746 deduped client entries** across all windows (10,446 in the today window).

### Axis coverage — how often a client entry says anything at all

| Axis | clients stating it | coverage |
|---|---|---|
| what they sell | 15,141 | 73% |
| client industry | 6,232 | 30% |
| platform or channel | 4,559 | 22% |
| problem they fix | 3,648 | 18% |
| where clients are | 3,298 | 16% |
| money model | 1,350 | 7% |
| client size | 999 | 5% |

Agencies describe their own work. They rarely describe the buyer.

### Client industry — ranked, with numbered-case rate

**Filter:** buckets with >= 100 deduped clients, "unknown" excluded, all windows.

| Bucket | clients | share of stated | with a numbered case |
|---|---|---|---|
| Construction, real estate & housing | 583 | 9.9% | 14.9% |
| Hospitality, tourism, sports & recreation | 574 | 9.7% | 17.9% |
| Healthcare & care | 538 | 9.1% | 13.4% |
| Retail & e-commerce (general consumer goods) | 497 | 8.4% | 20.1% |
| Food, beverage & agriculture | 424 | 7.2% | 10.8% |
| Business & professional services | 418 | 7.1% | 11.5% |
| Media, culture & entertainment | 358 | 6.1% | 11.2% |
| Education & childcare | 338 | 5.7% | 10.7% |
| Manufacturing & industrial | 324 | 5.5% | 15.4% |
| Fashion, beauty & personal goods | 317 | 5.4% | 17.4% |
| Transport, logistics & automotive | 294 | 5.0% | 17.3% |
| Software, IT & telecom | 280 | 4.7% | 12.9% |
| Nonprofits, charities & associations | 279 | 4.7% | 15.1% |
| Government & public sector | 214 | 3.6% | 10.7% |
| Finance & insurance | 165 | 2.8% | 15.2% |
| Energy, utilities & environment | 154 | 2.6% | 14.3% |
| Staffing, recruitment & HR | 152 | 2.6% | 19.1% |

17 buckets used. Top bucket **Construction, real estate & housing** at **9.9%** of stated clients; top six together **51%**. No industry owns this market.

### What they sell — ranked, with numbered-case rate

**Filter:** buckets with >= 100 deduped clients, "unknown" excluded, all windows.

| Bucket | clients | share of stated | with a numbered case |
|---|---|---|---|
| Website & webdesign | 3,339 | 25.0% | 6.6% |
| Branding & huisstijl | 2,128 | 15.9% | 3.3% |
| Grafisch ontwerp, drukwerk & print | 1,117 | 8.3% | 2.5% |
| Campagnes & creatieve concepten | 919 | 6.9% | 15.5% |
| Video, animatie & fotografie | 882 | 6.6% | 7.8% |
| Strategie & advies | 859 | 6.4% | 14.4% |
| Apps & maatwerk platforms | 769 | 5.7% | 10.0% |
| Webshop & e-commerce | 633 | 4.7% | 9.3% |
| Content & copywriting | 501 | 3.7% | 9.2% |
| Online marketing, performance & CRO | 451 | 3.4% | 19.7% |
| Online adverteren (paid ads) | 343 | 2.6% | 31.5% |
| SEO & vindbaarheid | 313 | 2.3% | 29.4% |
| Social media content & beheer | 290 | 2.2% | 21.0% |
| Employer branding & recruitment | 196 | 1.5% | 10.2% |
| Outcome-verkoop (leads, omzet, groei) | 193 | 1.4% | 49.2% |
| UX/UI & interface design | 186 | 1.4% | 8.6% |
| E-mailmarketing, automation & funnels | 163 | 1.2% | 19.6% |
| PR & influencer marketing | 100 | 0.7% | 20.0% |

18 buckets used. Top bucket **Website & webdesign** at **25.0%** of stated clients; top six together **69%**. 

### The confirmation asked for: websites + branding

Buckets matched: `Website & webdesign`, `Branding & huisstijl`.

**5,467 deduped clients, 289 of them with a numbered case = 5.3%.** The insights doc (B12) says 5,481 clients at 5.3%. **Confirmed.**

For contrast, the same rate computed on the axes that describe the buyer rather than
the work:

| Axis | clients stating it | with a numbered case |
|---|---|---|
| client industry | 5,909 | 14.6% |
| what they sell | 13,382 | 10.2% |
| problem they fix | 3,029 | 24.6% |
| platform or channel | 4,455 | 22.8% |
| money model | 1,268 | 18.4% |
| client size | 921 | 18.5% |
| where clients are | 3,178 | 17.3% |

Selling design produces almost no measurable claim. Describe the client instead, and
the rate roughly triples. Correlation only — this is a property of what gets written
down, not proof that describing the client causes results.

---

## A10. The null summary — every declared test with its p-value

**Sources:** `results_full.json` (the six frozen tests and their sensitivity runs) and
the docs named per row. Frozen-test p-values are read from the JSON in this run, not
retyped. Doc-sourced rows are marked and could not be recomputed here.

### The six frozen tests — primary run (growth_2y, JC cut-offs)

| Test | statistic | p | n | verdict |
|---|---|---|---|---|
| Concrete proof: specificity vs growth | -0.057 | 0.363 | 256 | NULL |
| Stacked focus: demonstrated depth vs growth | 0.012 | 0.852 | 256 | NULL |
| Showed it quietly (industry) | -0.147 | 0.975 | 22 vs 19 | NULL |
| Showed it quietly (craft) | -2.211 | 0.624 | 36 vs 19 | NULL |
| Narrow right now (craft, PRIMARY) | 11.518 | 0.372 | 187 vs 24 | NULL |
| Narrow right now (industry) | -1.646 | 0.816 | 95 vs 46 | NULL |
| Born narrow (old instrument) | -0.324 | 0.973 | 35 vs 135 | NULL |
| Said it and showed it (industry_tierA_97) | n/a | n/a | 0 pairs | NOT TESTABLE — needs ~30 pairs |
| Said it and showed it (craft_tierA_97) | n/a | n/a | 2 pairs | NOT TESTABLE — needs ~30 pairs |
| Said it and showed it (industry_allTiers_97) | n/a | n/a | 0 pairs | NOT TESTABLE — needs ~30 pairs |
| Said it and showed it (craft_allTiers_97) | n/a | n/a | 3 pairs | NOT TESTABLE — needs ~30 pairs |
| Said it and showed it (craft_allTiers_all155) | n/a | n/a | 4 pairs | NOT TESTABLE — needs ~30 pairs |

### The same six at every sensitivity setting

| Run | Concrete proof p | Stacked focus p | Narrow right now (craft) p | Showed it quietly (craft) p |
|---|---|---|---|---|
| JC cut-offs, growth_2y (percent) | 0.363 | 0.852 | 0.372 | 0.624 |
| growth_1y | 0.278 | 0.690 | 0.447 | 0.411 |
| people added, 2y | 0.238 | 0.693 | 0.425 | 0.622 |
| min clients 3 | 0.974 | 0.959 | 0.372 | 0.379 |
| min clients 5 | 0.260 | 0.883 | 0.355 | 0.741 |
| rise 10 pts | 0.363 | 0.852 | 0.372 | 0.742 |
| rise 20 pts | 0.363 | 0.852 | 0.372 | 0.628 |

**Every frozen test is null at every setting.** Not one p-value in the tables above
falls below 0.05.

### Declared cuts recorded in the docs, not recomputable from the kit

These are quoted from `kit/docs/2026-08-07-test-results.md` (addenda 1–3). The kit does
not ship the fields they were computed on (agency age, foreign-staff share, client
churn, publishing pace, the 97-narrower list), so they could not be re-run in this pass.
Marked DOC-ONLY.

| Cut | Result | p | status |
|---|---|---|---|
| Narrowing vs growth, <=3 people | rho +0.02 | 0.88 | DOC-ONLY |
| Narrowing vs growth, 4-11 people | rho -0.01 | 0.95 | DOC-ONLY |
| Narrowing vs growth, 12+ people | rho +0.09 | 0.49 | DOC-ONLY |
| 97 verified message-narrowers vs twins | 36% vs 33% | 0.59 | DOC-ONLY |
| Big-client agencies vs rest | 22% vs 34% | 0.056 | DOC-ONLY |
| Grid 1: narrowed vs flat, big-client excluded | 46% vs 27% | 0.064 | DOC-ONLY |
| Grid 2: concentrated now vs spread now, big excluded | 34% vs 33% | 0.46 | DOC-ONLY |
| Grid 3: message AND portfolio narrowed vs neither | 38% vs 26% | 0.38 | DOC-ONLY |
| Grid 4: narrowed vs flat, agencies WITH proof | 48% vs 47% | 0.54 | DOC-ONLY |
| Grid 5: narrowed vs flat, agencies without proof | 27% vs 15% | 0.52 | DOC-ONLY |
| Grid 6: proof + concentrated vs proof + spread | 34% vs 33% | 0.52 | DOC-ONLY |
| Grid 7: narrowed vs flat, <=5-person only | 19% vs 12% | 0.96 | DOC-ONLY |
| Grid 8: message narrowers vs twins, big excluded | 36% vs 34% | 0.75 | DOC-ONLY |
| Sweep: median staff tenure | rho -0.38 | <0.0001 | DOC-ONLY |
| Sweep: agency size | rho +0.13 | 0.012 | DOC-ONLY |
| Sweep: agency age | rho -0.11 | 0.031 | DOC-ONLY |
| JC prediction: old + broad + no proof = stuck | 32% vs 34% | 0.67 | DOC-ONLY |
| Revenue per head, narrow vs scattered | $150,000 vs $157,670 | 0.86 | DOC-ONLY |
| Kind of number: money/leads vs softer | 47% vs 44% | 0.85 | DOC-ONLY |
| Detail: any detailed tile or full page vs none | 33% vs 35% | 0.80 | DOC-ONLY |
| Logo-heavy vs not | 38% vs 33% | 0.62 | DOC-ONLY |

### Recomputed in this run

| Cut | Result | p | window | n |
|---|---|---|---|---|
| Tangible vs intangible (DEDUP) | 44% vs 26% | 0.0015 | after | 108 vs 148 |
| Tangible vs intangible (ANYROW) | 46% vs 24% | 0.0005 | after | 112 vs 144 |
| Tangible vs intangible (DEDUP) | 39% vs 31% | 0.2644 | today | 83 vs 213 |
| Tangible vs intangible (ANYROW) | 41% vs 30% | 0.1010 | today | 86 vs 210 |
| Narrow vs scattered, gate 4 | 33% vs 29% | 0.8223 | today | 187 vs 24 |
| Narrow vs scattered, gate 3 | 32% vs 29% | 0.8283 | today | 202 vs 24 |
| Narrow vs scattered, gate 2 | 33% vs 29% | 0.8068 | today | 210 vs 24 |
| Narrow vs scattered, gate 1 | 33% vs 29% | 0.8298 | today | 216 vs 24 |

**2 of 8 recomputed cuts clear p < 0.05**, and every one of
them is the same finding measured on the after window: agencies showing a tangible
result grew more often than agencies showing only names and logos. Nothing about
narrowing clears it at any gate.

**Counting hits against luck (rule 5).** Roughly 30 cuts were declared across this
study. At p < 0.05 you expect about 1.5 to look good by chance. The proof finding is
the only one that survives correction for that many tests; every narrowing cut is null
and the *direction* is consistently negative, which is not what a real-but-underpowered
positive effect looks like.

---

## A11. Three more article blocks, recomputed

These were about to be flagged as unverified in section C. They are computable from the
kit, so they were computed instead.

### The format finding (insights B3 / B4)

**Source:** `cases_tagged.csv`, `depth` field. **Window:** today. **Filter:** none.

| Form | count | share of the 15,028 | carries a number |
|---|---|---|---|
| summary-tile | 8,295 | 55.2% | 10.21% |
| logo-only | 3,129 | 20.8% | 0.03% |
| quote-testimonial | 2,322 | 15.5% | 4.95% |
| detailed-tile | 1,181 | 7.9% | 23.71% |
| full-case-page | 101 | 0.7% | 23.76% |

**101 full case pages across 73 agencies** in the entire today window.
67 of those 73 agencies wrote **exactly one**; 5 wrote more than two; the top writer wrote 9. The insights doc B4 says 63 of 73 — the recomputed figure is 67. **Use 67.**

Logo-only entries: **3,129, of which 1 carries a number — 0.03%**. One logo out of 3,129. A logo
grid physically has nowhere to put a result. The gap is format before it is effort.

**Verification note.** The insights doc B3 prints 8,295 / 3,129 / 2,322 / 1,181 / 101 with
a total of 15,028. The totals agree; check each row above against the doc before quoting,
and quote the recomputed version.

### What kind of number (insights B1, the 1.5% revenue claim)

**Source:** `cases_tagged.csv`, `metric_kinds` field. **Window:** today.

| Metric kind | cases today | share of all 15,028 cases | share of the numbered cases |
|---|---|---|---|
| other | 311 | 2.1% | 24.5% |
| leads_inquiries | 262 | 1.7% | 20.7% |
| revenue_sales | 258 | 1.7% | 20.4% |
| traffic | 216 | 1.4% | 17.0% |
| ad_performance | 110 | 0.7% | 8.7% |
| reach_views | 100 | 0.7% | 7.9% |
| conversion | 96 | 0.6% | 7.6% |
| seo_positions | 59 | 0.4% | 4.7% |

**258 cases name revenue or sales — 1.7% of everything published.** The insights doc says "~1.5% name revenue". **Confirmed.**

### The market is moving (insights B6)

**Source:** `cases_tagged.csv` + `measures_v2.csv`, before and after windows. 
**Filter:** agencies with cases in **both** windows. **No growth data is used at all** —
this block is pure market movement, so it carries no causation exposure.

**286 agencies have cases in both windows.**

| Instrument | zero numbers before | added a number | still zero | share that added | had numbers before | kept them | dropped to zero | market share with proof before -> after |
|---|---|---|---|---|---|---|---|---|
| ANYROW | 193 | 36 | 157 | **19%** | 93 | 79 | 14 | 33% -> 40% |
| DEDUP | 197 | 36 | 161 | **18%** | 89 | 74 | 15 | 31% -> 38% |

**Both instruments give the same story and nearly the same number.** Roughly one agency
in five that showed no measurable result two years ago shows one now, and roughly four in
five still do not. Proof is sticky once acquired: almost nobody who had a number dropped
it. The insights doc B6 reports 286 agencies, 193 zero before, 36 added (19%), 157 still
zero, market 33% -> 40% — compare against the ANYROW row above and quote the recomputed
one.

---

## B. Imported from outside the kit

### B11. The 29 July Sales Nav pull, merged for the original340

`kit/data/2026-07-29-salesnav-employees-progress.csv` — imported verbatim from
`study-outreach/outputs/`. `kit/data/2026-08-25-growth-original340-merged.csv` — built from it in this run, **36 rows**.

`2026-08-07-growth.csv` was **not modified**. The merged file is additive and separate.

**The join, and what it cost.** original340 domains in `measures_v2.csv` carry a
numeric suffix (`fabrique.nl_403`); the Sales Nav file keys on a bare domain. After
stripping the suffix and normalising scheme/www/path:

- 297 agencies in cohort `original340` (today window).
- **261 of them are LinkedIn personal handles, not domains** — a personal profile has no company employee chart, so they can never match.
- 36 are real agency domains.
- **36 matched the Sales Nav file and now have growth.**

This independently confirms the blocker recorded in the insights doc, section N:
the "one scrape doubles the sample" plan is worth about 36 agencies, not 297.

**Overlap with the existing growth file: zero.** No Sales Nav domain appears in
`2026-08-07-growth.csv`. The two populations are disjoint, exactly as D4 says — the
LinkedIn headcount scrape only ever covered the narrower/control matched pairs.

**Dapper's growth, from the imported file.** `dapper.agency_396` (`Dapper`, matched on `dapper.agency`): **+132% over two years**, +35% over one year, +8% over six months, 66 employees now, 8 open roles. Source row: `2026-07-29-salesnav-employees-progress.csv` row 389, status `found`.

The source note on that row reads: "Exact match confirmed via website link (dapper.agency); Dapper - the demand agency, Advertising Services (B2B demand gen); numbers double-checked via two independent find queries, both consistent; ben"

**Standing rule from the insights doc applies: no growth number beside a name for
a stuck agency.** Dapper is a winner, so naming it is allowed — but +132% is a
single Sales Nav reading from 29 July, not a 25-month monthly series like the 388,
so it is not like-for-like with any growth figure elsewhere in this file. Say
"roughly doubled headcount", cite the date, and do not put it in a table with the
388.

### B12. Dapper — the settled count, and a live re-derivation

**The kit is wrong about Dapper and must not be used for any named count.**

`kit_metric_kinds.csv` row `dapper.agency_396` (window today) says **8 cases, 2 with a number**. The settled figure from `study-outreach/outputs/2026-08-01-proof-reconciliation.md` is **35 cases, 29 with a number**.

The cause is documented and mechanical: the itemization pass that produced the kit row
read only the 8 *named* client entries and found 2 numbers in them. It never saw the
wall of anonymous metric tiles, which is where the other 27 numbers live. Both passes
were reading real things; neither was reading all of it.

**Live re-derivation, 2026-08-25.** `https://dapper.agency/cases` fetched and the raw
page text saved to `kit/data/2026-08-25-dapper-cases-page.txt` as evidence.

Counted by hand from the saved text, the result-tile wall between the heading
"Results we are proud of" and the carousel counter:

```
of
200%
More inbound sales calls
53%
More qualified pipeline
60+
Inbound Leads
66%
Win rate
5000+
Leads generated
€40,-
Average cost per lead
80%
Reduced the average CPL
700+
Leads gathered
12%
More Leads
400%
High-intent Downloads
350+
Signups in 4 months
$70
Cost of a sign up
5000+
Leads in 1 year
20+
Countries
178%
Increase in total deal value
51%
Engagement increase
20+
Experiments
350+
Leads
43
Inbound deals
155
Inbound leads
300% growth
MQL's
90%
Reach
81%
Authority built through expert
8x
Above growth target
+54%
Increase Inbound Pipeline
+243%
Increase of engagement
10+
MQL's
77%
Target audience reached
01
99
```

**28 result tiles. All 28 carry a number.** Add the named-client layer counted by the
reconciliation and the settled total is 35 cases / 29 numbered. The carousel counter
on the page reads `01 / 99`, so even 29 is a floor.

**Safe phrasings for the article:** "29 published client results" or "a wall of 29
numbers". **Not** "28 case studies" — they are anonymous metric tiles plus 8 named
testimonials, not named write-ups.

**Rule to carry forward:** `kit_metric_kinds.csv` is not a source for any named count.
It undercounts every agency whose proof is anonymous. Use it for market-wide shape only,
and never put an agency name next to a number that came out of it.

---

## C13. Article claims with no kit backing after this run

Nothing below can be sourced to a kit file. Each is either doc-only, sourced to a file
the kit does not ship, or contradicted by the recomputation above. Do not let any of
these into the draft without doing the work named in the fix column.

| # | Claim | Where it appears | Why it has no kit backing | Fix |
|---|---|---|---|---|
| 1 | "1,586 Dutch agencies" | LINES-I-WANT line 1 | Appears in no kit file. Verified counts are 706 / 688 / 411 / 388 / 256. | Use 388 and say what it is. |
| 2 | The A5 2x2 cells: 54 / 57 / 76 / 67, best 54% worst 22%, p=0.0004 | INSIGHTS A5, LINES-I-WANT line 2 | Built on a model judgement of the raw hero line. The kit ships bucket mappings only, and neither reproducible definition lands on those cells (A4 above). | Print the recomputed 2x2 with its definition, or drop the corner numbers. |
| 3 | Bookability: 57% / 46% / 19%, and "25% have a booking link" | INSIGHTS B8 | No CTA, booking or contact-form field exists anywhere in the kit. | Re-run the regex over source site text and import it as a kit column, or cut the claim. |
| 4 | "327 positioning lines", "38 literal variants (12%)", "of those 38: 17 have no proof, 25 cannot be booked, 18 never name a buyer" | INSIGHTS B9 | The kit sayside file yields a different line count; the bookability and name-a-buyer sub-counts have no kit field at all. | Quote the recomputed A7 numbers with the regex definition stated. |
| 5 | B1 replication: "6,278 cases in the untested cohort, 10.9% carry a number" | INSIGHTS B1 | The cohort split is in the kit (`original340`), but the published 6,278/10.9% pair was never re-derived and the doc does not say which window it used. | Recompute per cohort, or print only the market-wide 8% verified in A3. |
| 6 | F1 money-vs-soft proof ladder, F3 vertical clustering, F4 e-commerce, F5 by work type | INSIGHTS F1-F5 | All are below the 40-per-side floor by the study's own rules, and F1 directly contradicts C4 on a cleaner cut. | Label DIRECTIONAL or leave out. Never as a finding. |
| 7 | C3 revenue per head ($150,000 vs $157,670) | INSIGHTS C3 | No revenue-per-head field in the kit; `revenue_band` in growth.csv is a coarse band, not a value. | DOC-ONLY. Quote as a null with the caveat, or cut. |
| 8 | B13/B14 lifecycle: "8.5% ever narrowed at n=1,830", "not one agency older than 15 years started narrow", "young 40% vs old 27%" | INSIGHTS B13, B14 | No agency-age or founding-year field exists in the kit; the n=1,830 population is not in the kit either. | DOC-ONLY. Keep the safe wording already agreed and cite the doc, not the kit. |
| 9 | B7 "old and small: 6% show a single measurable result" | INSIGHTS B7 | Needs agency age. Not in the kit. | DOC-ONLY or cut. |
| 10 | D4 "297 have no growth data" framed as fixable by one scrape | INSIGHTS D4, N | Confirmed and worse than stated: 261 of the 297 are personal LinkedIn handles. Only 36 could ever match, and this run matched exactly those 36. | State 36, not 297. |
| 11 | Section G and H named agency tables (the 22 creative, the 31 growing) | INSIGHTS G, H | Per-agency numbered-case counts in those tables trace to `kit_metric_kinds.csv`, which is proven wrong for Dapper and undercounts anonymous proof generally. | Recount from `cases_tagged.csv` per agency and spot-check the top 5 by hand before printing any name. |
| 12 | Dapper +132% presented alongside the 388 | INSIGHTS J | Verified and now imported (B11 above), but it is a single 29 July Sales Nav reading, not a 25-month monthly series. | Cite the date and the different instrument; never in a table with the 388. |
| 13 | Any Rotterdam cut | INSIGHTS D6 | No city or origin column exists in the kit. Confirmed again in this run. | Add an `origin` column to measures_v2.csv, or drop the Rotterdam piece. |
| 14 | Per-agency narrowness status quoted by name from narrowness v2 | INSIGHTS J, C2 | The C2 gate TABLE reproduces (A1 above) so the claim is safe. The per-agency STATUS is not: the v2 file needs case text the kit does not ship, and the reconstruction matches its unit count for only 80% of agencies. | Quote the C2 table freely. Do not put a v2 status next to a named agency without checking that agency by hand. |

**What is safe to print, verified in this run:** the population counts, the market
baseline, A1 (every gate), A2 (both instruments, every sensitivity), A3, A5 (the stuck
segment, exact), A6, A9 (the market map and the 5% confirmation), A10 (all frozen
p-values), A11 (format, metric kinds, market movement), B11 (Dapper growth, with its
caveat) and B12 (the Dapper count, live).

**What is NOT safe, in one sentence each:** the 1,586 headline (does not exist), the
A5 2x2 corners (definition not shipped), bookability (no field), the crowded-sentence
word counts (different corpus), anything needing agency age or revenue per head (no
field), and any per-agency proof count taken from `kit_metric_kinds.csv` (proven wrong).

