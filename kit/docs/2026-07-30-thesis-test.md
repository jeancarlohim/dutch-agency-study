# Does positioning predict growth? — the test, and the answer

Run Jul 30, after JC asked whether the "market is shrinking" line was claimable.
It wasn't, and testing it properly turned up something more important.

**Headline: the article's current thesis is NOT supported by this data.**
Better to know today than on Aug 3 with the draft half-written.

## What was tested

Sample: 268 agencies with all three of — positioning score, 2-year headcount
change (Sales Nav), current headcount. The thesis under test: *"agencies that
sharpened their positioning are pulling more demand."*

## Result 1 — no relationship

Correlation between positioning score and 2-year growth: **-0.014**.
That is zero. Not weak-positive. Zero.

| Score quartile | n | % growing | % shrinking | median growth |
|---|---|---|---|---|
| Q1 (worst positioned) | 67 | 42% | 25% | 0% |
| Q2 | 67 | 55% | 21% | +6% |
| Q3 | 67 | 45% | 28% | 0% |
| Q4 (best positioned) | 67 | 55% | 28% | +14% |

Best-positioned quartile does grow a bit more often than the worst (55% vs 42%)
and has a higher median (+14% vs 0%) — but the middle is non-monotonic and the
best-positioned quartile also shrinks MORE often than the worst. No clean trend.

## Result 2 — it isn't hidden by company size

Score barely tracks size (correlation +0.11), so size isn't masking an effect.
Splitting each size band into better- and worse-positioned halves:

| Size | n | worse-positioned % growing | better-positioned % growing | gap |
|---|---|---|---|---|
| 1-4 | 75 | 32% | 39% | +7pp |
| 5-9 | 81 | 40% | 41% | +1pp |
| 10-19 | 61 | 67% | 61% | **-5pp** |
| 20+ | 50 | 56% | 76% | +20pp |

Direction flips by band. That is noise, not a finding.

## Result 3 — one component does carry signal: PROOF

Testing each ingredient separately against "% growing":

| Ingredient | has it | lacks it | gap |
|---|---|---|---|
| **proof (1+ numeric case study)** | **59%** (n=63) | **46%** (n=205) | **+12pp** |
| sells the client's KPI | 53% | 48% | +5pp |
| named method | 46% | 50% | -4pp |
| clear hero (5-sec) | 45% | 51% | -6pp |
| genuinely niched | 44% | 51% | **-7pp** |
| deep content engine | 41% | 50% | -9pp |

Proof is the only ingredient pointing the right way. Being *niched* points the
WRONG way (-7pp). So does having a clear hero. This is the opposite of the
current thesis, which leads on niching.

## Result 4 — the pivot data (tiny n, but causally ordered)

Only Rotterdam has positioning-change dating, so this is the one place we can
ask "did they sharpen, THEN grow?" rather than correlating today's site with
past growth.

| Pivot history | n | growing |
|---|---|---|
| broad-to-niche | 6 | 4 (Dapper +132%, STUDIO 10am +100%, Pionect +23%, Wild Digital +16%) |
| always-broad | 27 | 17 |
| always-niche | 2 | 2 |

63% of pivoters grew vs 63% of always-broad. **n=6. Proves nothing.** Dapper is
a great story but one agency is an anecdote, not evidence.

## Why the test may be unfair to the thesis — and what would fix it

Three real limitations, in order of how much they matter:

1. **The clock is backwards.** We measured TODAY'S website against the LAST two
   years of growth. If an agency sharpened its positioning eight months ago, its
   2-year growth number mostly predates the change. This is a design flaw, not a
   result — and it's the most likely reason the correlation is zero.
   **Fix:** date the positioning change (Wayback), then measure growth AFTER it.
   That data exists for 45 Rotterdam rows and zero of the 295 national rows.
   It is exactly the Aug 1-2 scheduled work.
2. **Headcount is a poor proxy for demand.** An agency can grow revenue while
   staying lean, especially now. LinkedIn headcount also just counts people who
   list the employer — noisy, laggy, self-reported.
3. **Survivor bias.** Agencies that already died aren't in the list, so the true
   downside is under-counted.

## What JC can honestly say right now

- "Half of these agencies grew over two years, a quarter shrank." (Solid.)
- "Agencies publishing numeric proof grew more often than those that don't —
  59% vs 46%." (Solid, and it's the study's strongest real finding.)
- "Only 24% of agencies show a single case study with a real number." (Solid,
  and this is the actual gap in the market.)

## What JC must NOT say

- "Sharper positioning drives growth." **Not supported. Correlation is zero.**
- "Niching drives growth." Points the wrong way in this data (-7pp).
- Any causal claim from the 6 pivoters. n=6.

## Three ways forward (JC's call)

1. **Narrow the thesis to proof.** "Proof, not polish, separates the growing
   from the stuck." Fully supported today, no extra data needed. The niching
   story becomes context, not the claim.
2. **Fix the clock, then re-test.** Wayback-date the positioning change for the
   top ~40, measure growth after that date. If the thesis is real, this is where
   it shows up. Costs the Aug 1-2 window; may still come back negative.
3. **Publish the null.** "Everyone says niching drives growth. I scored 340
   Dutch agencies and it doesn't — but proof does." Contrarian, honest, and
   harder to argue with than the original claim.

Recommendation: **1 or 3, and both survive if the Aug 1-2 work adds nothing.**
Option 2 is worth attempting only because the data is already scheduled — but
do not build the article on the assumption it will rescue the original thesis.
