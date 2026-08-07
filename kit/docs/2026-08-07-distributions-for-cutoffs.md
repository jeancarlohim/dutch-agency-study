# The real distributions — for fixing the cut-offs

Aug 7, 2026. Every number below is computed from the approved category
lists. **No growth data was read to produce this file**, on purpose: the
cut-offs get fixed while still blind to who grew.

Plain words used throughout:

| Word | What it means |
|---|---|
| focus score | of the different clients an agency shows in one window, the share sitting in its single biggest category, for one focus type |
| strongest focus score | the highest of an agency's seven focus scores — its own best axis, whatever that axis is |
| stacked focus | how many of the seven focus types are concentrated at the same time (0–7) |
| window | before = ~1 year before the message change · after = ~2 years after · today = the live site, Aug 2026 |
| distinct clients | different clients shown in that window after deduplicating |

## 1. How many clients each agency actually shows

This is the gate everything else sits behind: a focus score computed on two
clients is noise. Counts are agency-windows.

| Window | Agency-windows | Median distinct clients | With ≥2 | ≥3 | ≥4 | ≥5 | ≥8 |
|---|---|---|---|---|---|---|---|
| before | 320 | 10 | 308 | 289 | 267 | 240 | 201 |
| after | 337 | 12 | 328 | 320 | 295 | 273 | 230 |
| today | 688 | 10 | 662 | 642 | 586 | 553 | 450 |

## 2. How often each focus type is stated at all

An agency can only be scored on a focus type if its case text says something
about it. "Unknown" here means the extracted words carried no usable value —
either the site said nothing, or it said something the approved list has no
home for. Unknowns are excluded from the focus score, never counted as spread.

| Focus type | Agency-windows with ≥1 client stating it | …with ≥3 | Median clients stating it (of those with ≥1) |
|---|---|---|---|
| what the client's business is | 889 | 580 | 4 |
| what they sell | 1226 | 1013 | 7 |
| the problem they fix | 614 | 324 | 3 |
| platform or channel | 797 | 472 | 3 |
| the client's money model | 436 | 161 | 2 |
| the client's size | 383 | 124 | 2 |
| where the clients are | 729 | 373 | 3 |

## 3. The focus scores themselves

Read as: a quarter of agencies score below the first number, half score below
the middle number, a quarter score above the last. Only agency-windows with at
least 3 clients stating that focus type are counted — anything thinner cannot
produce a meaningful share.

### before

| Focus type | Agencies scored | Low quarter | Middle | High quarter | Score is 100% |
|---|---|---|---|---|---|
| what the client's business is | 159 | 25% | 33% | 50% | 2 |
| what they sell | 240 | 38% | 50% | 67% | 20 |
| the problem they fix | 99 | 33% | 43% | 55% | 3 |
| platform or channel | 127 | 33% | 50% | 67% | 9 |
| the client's money model | 44 | 38% | 50% | 67% | 7 |
| the client's size | 40 | 50% | 67% | 75% | 10 |
| where the clients are | 112 | 38% | 57% | 67% | 13 |

**Strongest focus score, before** — 253 agencies have at least one scorable focus type. Low quarter 56% · middle 67% · high quarter 86%.

| Strongest focus score at least | Agencies |
|---|---|
| 33% | 250 |
| 40% | 231 |
| 50% | 219 |
| 60% | 179 |
| 75% | 101 |

### after

| Focus type | Agencies scored | Low quarter | Middle | High quarter | Score is 100% |
|---|---|---|---|---|---|
| what the client's business is | 192 | 23% | 33% | 40% | 1 |
| what they sell | 269 | 38% | 50% | 67% | 13 |
| the problem they fix | 144 | 33% | 42% | 57% | 2 |
| platform or channel | 168 | 33% | 50% | 60% | 11 |
| the client's money model | 80 | 40% | 57% | 67% | 6 |
| the client's size | 71 | 50% | 67% | 75% | 12 |
| where the clients are | 147 | 38% | 50% | 67% | 11 |

**Strongest focus score, after** — 286 agencies have at least one scorable focus type. Low quarter 57% · middle 67% · high quarter 82%.

| Strongest focus score at least | Agencies |
|---|---|
| 33% | 282 |
| 40% | 266 |
| 50% | 243 |
| 60% | 202 |
| 75% | 116 |

### today

| Focus type | Agencies scored | Low quarter | Middle | High quarter | Score is 100% |
|---|---|---|---|---|---|
| what the client's business is | 229 | 28% | 33% | 50% | 5 |
| what they sell | 504 | 36% | 50% | 67% | 31 |
| the problem they fix | 81 | 33% | 50% | 67% | 5 |
| platform or channel | 177 | 43% | 58% | 75% | 22 |
| the client's money model | 37 | 67% | 75% | 100% | 14 |
| the client's size | 13 | 54% | 67% | 75% | 2 |
| where the clients are | 114 | 50% | 67% | 75% | 17 |

**Strongest focus score, today** — 543 agencies have at least one scorable focus type. Low quarter 50% · middle 67% · high quarter 80%.

| Strongest focus score at least | Agencies |
|---|---|
| 33% | 522 |
| 40% | 459 |
| 50% | 425 |
| 60% | 337 |
| 75% | 198 |

## 4. Which focus type is each agency strongest on

Descriptive only — the pre-registration forbids splitting the tests by axis.

| Focus type | Agencies whose strongest focus type it is (today) |
|---|---|
| what the client's business is | 40 |
| what they sell | 304 |
| the problem they fix | 26 |
| platform or channel | 83 |
| the client's money model | 25 |
| the client's size | 8 |
| where the clients are | 57 |

## 5. Stacked focus — narrow on several things at once

Counted with the placeholder rule still in the code: a focus type counts as
concentrated when at least 3 clients state it AND the focus score is 50% or
more. Both halves of that rule are cut-offs JC has to fix (decision 2 below).

| Stacked focus | before | after | today |
|---|---|---|---|
| 0 | 101 | 94 | 263 |
| 1 | 96 | 83 | 252 |
| 2 | 72 | 89 | 116 |
| 3 | 32 | 38 | 46 |
| 4 | 16 | 24 | 10 |
| 5 | 3 | 8 | 1 |
| 6 | 0 | 1 | 0 |
| 7 | 0 | 0 | 0 |

## 6. Did the client mix narrow — the change from before to after

One row per agency that has BOTH a before and an after window, and at least
3 clients stating some focus type in each. Positive = the mix got NARROWER.

The number compared is the agency's strongest focus score in each window —
its best axis before, against its best axis after. That is the fair
comparison: an agency that switched which axis it is narrow on still counts.

- **changed their message** (68 agencies): the middle agency moved +0 points; low quarter -9, high quarter +11.
- **twin (message stayed broad)** (146 agencies): the middle agency moved +0 points; low quarter -10, high quarter +9.

| Group | Agencies measurable both windows | Got narrower by ≥5 pts | ≥10 | ≥15 | ≥20 | Got broader by ≥15 |
|---|---|---|---|---|---|---|
| changed their message | 68 | 27 | 18 | 16 | 12 | 15 |
| twin (message stayed broad) | 146 | 51 | 32 | 26 | 17 | 29 |

### The same question asked a second way — and why it reads worse

The table below anchors on whichever focus type was strongest BEFORE, then
watches that same one after. It looks much more negative, and that is a
measurement artifact, not agency behaviour: picking the highest of seven
noisy scores in the before window guarantees some of them were high by luck,
and luck does not repeat. **Do not read this table as "agencies got broader."**
It is here only so the effect is on the record.

| Group | Agencies | Got narrower by ≥5 pts | ≥10 | ≥15 | ≥20 | Got broader by ≥15 |
|---|---|---|---|---|---|---|
| changed their message | 62 | 13 | 7 | 7 | 6 | 20 |
| twin (message stayed broad) | 133 | 26 | 13 | 7 | 5 | 41 |

_(the original before-anchored figures)_

### New clients only

The same question asked of the clients that appear AFTER and were absent
BEFORE. Portfolios pile up, so an agency can go all-in on one niche and barely
move its total mix — this is where that shows.

| Group | Agencies with ≥3 new clients stating a focus type | Middle strongest score on the new clients | New-client score ≥50% | ≥60% | ≥75% |
|---|---|---|---|---|---|
| changed their message | 67 | 67% | 57 | 48 | 27 |
| twin (message stayed broad) | 128 | 67% | 102 | 90 | 48 |

## 7. Unknown rates — how much text the approved lists could not place

| Focus type | Cases stating it | Landed in a real bucket | Unknown |
|---|---|---|---|
| what the client's business is | 8727 | 8264 (95%) | 463 (5%) |
| what they sell | 23863 | 20719 (87%) | 3144 (13%) |
| the problem they fix | 5096 | 4153 (81%) | 943 (19%) |
| platform or channel | 6799 | 6603 (97%) | 196 (3%) |
| the client's money model | 1876 | 1756 (94%) | 120 (6%) |
| the client's size | 1335 | 1231 (92%) | 104 (8%) |
| where the clients are | 4525 | 4350 (96%) | 175 (4%) |

## 8. The decisions JC has to make

### Decision 1 — minimum clients before an agency gets a focus score

| Minimum distinct clients | Agencies kept, before+after both | Agencies kept, today |
|---|---|---|
| ≥2 | 272 | 662 |
| ≥3 | 251 | 642 |
| ≥4 | 227 | 586 |
| ≥5 | 201 | 553 |
| ≥8 | 169 | 450 |

### Decision 2 — what counts as "concentrated" for stacked focus

Today window, agencies with at least one scorable focus type:

| Line for "concentrated" | Median stacked focus | Agencies stacked on ≥2 | ≥3 |
|---|---|---|---|
| 40% | 1 | 219 | 86 |
| 50% | 1 | 173 | 57 |
| 60% | 0 | 102 | 18 |
| 75% | 0 | 36 | 6 |

### Decision 3 — how big a rise counts as "the client mix narrowed"

Numbers are in section 6. The placeholder was 15 points.

### Decision 4 — the "narrow right now" split

Today window. Placeholder was concentrated ≥50% vs spread ≤33%, minimum 4 clients.

**Read the first row and you will see the problem.** Taking the highest of
seven scores makes almost every agency look concentrated, so the "spread"
side of the split starves. That is arithmetic, not the Dutch market: with
seven chances to be narrow at something, hardly anyone is broad at everything.

| Concentrated line / spread line | Concentrated agencies | Spread agencies |
|---|---|---|
| ≥50% vs ≤33% | 411 | 21 |
| ≥60% vs ≤40% | 323 | 84 |
| ≥75% vs ≤50% | 194 | 166 |

The same split on ONE focus type — what they sell, the best-covered one —
gives two usable sides. This is the version worth considering:

| Concentrated line / spread line | Concentrated agencies | Spread agencies |
|---|---|---|
| ≥50% vs ≤33% | 288 | 59 |
| ≥60% vs ≤40% | 189 | 153 |
| ≥75% vs ≤50% | 104 | 254 |

### Decision 5 — which focus types are allowed to carry a test

Section 2 and section 7 give the two halves of this: how often a focus type is
stated at all, and how much of what is stated the approved list could place.
The two thin ones were already agreed descriptive-only when the lists were
locked (the client's money model, the client's size).

