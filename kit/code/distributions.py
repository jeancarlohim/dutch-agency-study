#!/usr/bin/env python3
"""Turn measures_v2.csv into the plain-language distributions document.

NO GROWTH DATA IS READ HERE. That is the point: JC fixes the cut-offs from
these numbers while still blind to who grew.
"""
import csv, json, os, sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rules import AXES, AXIS_KEY

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = '/Users/jeancarlohim/Documents/GitHub/study-outreach/outputs'
ANA = f'{ROOT}/2026-08-04-analysis'
csv.field_size_limit(10 ** 9)

NAME = {'industry': "what the client's business is", 'craft': 'what they sell',
        'job': 'the problem they fix', 'channel': 'platform or channel',
        'model': "the client's money model", 'stage': "the client's size",
        'geo': 'where the clients are'}
KEYS = [AXIS_KEY[a] for a in AXES]
COHORT = {'narrower': 'changed their message', 'control': 'twin (message stayed broad)',
          'original340': 'original study, today only'}

rows = list(csv.DictReader(open(f'{ANA}/measures_v2.csv')))
for r in rows:
    for c in list(r):
        if c.startswith(('top1_', 'inc_top1_', 'hhi_')) or c == 'avg_specificity':
            r[c] = float(r[c]) if r[c] not in ('', 'None') else None
        elif c.startswith(('n_', 'inc_n_')) or c == 'demonstrated_depth':
            r[c] = int(r[c]) if r[c] not in ('', 'None') else 0

def pct(x):
    return '—' if x is None else f'{100*x:.0f}%'

def quart(vals):
    v = sorted(x for x in vals if x is not None)
    if not v:
        return None, None, None, 0
    def q(f):
        return v[min(len(v) - 1, int(f * (len(v) - 1) + 0.5))]
    return q(.25), q(.5), q(.75), len(v)

by_win = defaultdict(list)
for r in rows:
    by_win[r['window']].append(r)

L = []
w = L.append
w('# The real distributions — for fixing the cut-offs')
w('')
w('Aug 7, 2026. Every number below is computed from the approved category')
w('lists. **No growth data was read to produce this file**, on purpose: the')
w('cut-offs get fixed while still blind to who grew.')
w('')
w('Plain words used throughout:')
w('')
w('| Word | What it means |')
w('|---|---|')
w('| focus score | of the different clients an agency shows in one window, the share sitting in its single biggest category, for one focus type |')
w('| strongest focus score | the highest of an agency\'s seven focus scores — its own best axis, whatever that axis is |')
w('| stacked focus | how many of the seven focus types are concentrated at the same time (0–7) |')
w('| window | before = ~1 year before the message change · after = ~2 years after · today = the live site, Aug 2026 |')
w('| distinct clients | different clients shown in that window after deduplicating |')
w('')

# ------------------------------------------------------------------ section 1
w('## 1. How many clients each agency actually shows')
w('')
w('This is the gate everything else sits behind: a focus score computed on two')
w('clients is noise. Counts are agency-windows.')
w('')
w('| Window | Agency-windows | Median distinct clients | With ≥2 | ≥3 | ≥4 | ≥5 | ≥8 |')
w('|---|---|---|---|---|---|---|---|')
for win in ('before', 'after', 'today'):
    rs = by_win.get(win, [])
    if not rs:
        continue
    ns = [r['n_distinct_clients'] for r in rs]
    _q1, med, _q3, _n = quart(ns)
    cells = ' | '.join(f'{sum(1 for x in ns if x >= k)}' for k in (2, 3, 4, 5, 8))
    w(f'| {win} | {len(rs)} | {med} | {cells} |')
w('')

# ------------------------------------------------------------------ section 2
w('## 2. How often each focus type is stated at all')
w('')
w('An agency can only be scored on a focus type if its case text says something')
w('about it. "Unknown" here means the extracted words carried no usable value —')
w('either the site said nothing, or it said something the approved list has no')
w('home for. Unknowns are excluded from the focus score, never counted as spread.')
w('')
w('| Focus type | Agency-windows with ≥1 client stating it | …with ≥3 | Median clients stating it (of those with ≥1) |')
w('|---|---|---|---|')
for k in KEYS:
    rs = [r for r in rows]
    a = sum(1 for r in rs if r[f'n_stated_{k}'] >= 1)
    b = sum(1 for r in rs if r[f'n_stated_{k}'] >= 3)
    _q1, med, _q3, _n = quart([r[f'n_stated_{k}'] for r in rs if r[f'n_stated_{k}'] >= 1])
    w(f'| {NAME[k]} | {a} | {b} | {med} |')
w('')

# ------------------------------------------------------------------ section 3
w('## 3. The focus scores themselves')
w('')
w('Read as: a quarter of agencies score below the first number, half score below')
w('the middle number, a quarter score above the last. Only agency-windows with at')
w('least 3 clients stating that focus type are counted — anything thinner cannot')
w('produce a meaningful share.')
w('')
for win in ('before', 'after', 'today'):
    rs = by_win.get(win, [])
    if not rs:
        continue
    w(f'### {win}')
    w('')
    w('| Focus type | Agencies scored | Low quarter | Middle | High quarter | Score is 100% |')
    w('|---|---|---|---|---|---|')
    for k in KEYS:
        vals = [r[f'top1_{k}'] for r in rs if r[f'n_stated_{k}'] >= 3]
        q1, med, q3, n = quart(vals)
        full = sum(1 for v in vals if v is not None and v >= 0.999)
        w(f'| {NAME[k]} | {n} | {pct(q1)} | {pct(med)} | {pct(q3)} | {full} |')
    w('')
    strongest = []
    for r in rs:
        cand = [r[f'top1_{k}'] for k in KEYS if r[f'n_stated_{k}'] >= 3 and r[f'top1_{k}'] is not None]
        if cand:
            strongest.append(max(cand))
    q1, med, q3, n = quart(strongest)
    w(f'**Strongest focus score, {win}** — {n} agencies have at least one scorable '
      f'focus type. Low quarter {pct(q1)} · middle {pct(med)} · high quarter {pct(q3)}.')
    w('')
    w('| Strongest focus score at least | Agencies |')
    w('|---|---|')
    for t in (0.33, 0.40, 0.50, 0.60, 0.75):
        w(f'| {t:.0%} | {sum(1 for v in strongest if v >= t)} |')
    w('')

# ------------------------------------------------------------------ section 4
w('## 4. Which focus type is each agency strongest on')
w('')
w('Descriptive only — the pre-registration forbids splitting the tests by axis.')
w('')
w('| Focus type | Agencies whose strongest focus type it is (today) |')
w('|---|---|')
cnt = Counter()
for r in by_win.get('today', []):
    cand = [(r[f'top1_{k}'], k) for k in KEYS
            if r[f'n_stated_{k}'] >= 3 and r[f'top1_{k}'] is not None]
    if cand:
        cnt[max(cand)[1]] += 1
for k in KEYS:
    w(f'| {NAME[k]} | {cnt[k]} |')
w('')

# ------------------------------------------------------------------ section 5
w('## 5. Stacked focus — narrow on several things at once')
w('')
w('Counted with the placeholder rule still in the code: a focus type counts as')
w('concentrated when at least 3 clients state it AND the focus score is 50% or')
w('more. Both halves of that rule are cut-offs JC has to fix (decision 2 below).')
w('')
w('| Stacked focus | before | after | today |')
w('|---|---|---|---|')
for d in range(0, 8):
    cells = ' | '.join(str(sum(1 for r in by_win.get(win, []) if r['demonstrated_depth'] == d))
                       for win in ('before', 'after', 'today'))
    w(f'| {d} | {cells} |')
w('')

# ------------------------------------------------------------------ section 6
pairs = {}
for r in rows:
    if r['window'] in ('before', 'after'):
        pairs.setdefault(r['domain'], {})[r['window']] = r

def strongest(r):
    cand = [r[f'top1_{k}'] for k in KEYS
            if r[f'n_stated_{k}'] >= 3 and r[f'top1_{k}'] is not None]
    return max(cand) if cand else None

changes = defaultdict(list)        # symmetric: strongest after - strongest before
anchored = defaultdict(list)       # anchored on the before-window winner (biased)
inc_scores = defaultdict(list)
for dom, d in pairs.items():
    if 'before' not in d or 'after' not in d:
        continue
    b, a = d['before'], d['after']
    sb, sa = strongest(b), strongest(a)
    if sb is not None and sa is not None:
        changes[b['cohort']].append(sa - sb)
    cand = [(b[f'top1_{k}'], k) for k in KEYS
            if b[f'n_stated_{k}'] >= 3 and b[f'top1_{k}'] is not None]
    if not cand:
        continue
    k = max(cand)[1]
    if a[f'n_stated_{k}'] < 3 or a[f'top1_{k}'] is None:
        continue
    anchored[b['cohort']].append(a[f'top1_{k}'] - b[f'top1_{k}'])
for r in by_win.get('after', []):
    cand = [r.get(f'inc_top1_{k}') for k in KEYS
            if r.get(f'inc_n_stated_{k}', 0) >= 3 and r.get(f'inc_top1_{k}') is not None]
    if cand:
        inc_scores[r['cohort']].append(max(cand))

w('## 6. Did the client mix narrow — the change from before to after')
w('')
w('One row per agency that has BOTH a before and an after window, and at least')
w('3 clients stating some focus type in each. Positive = the mix got NARROWER.')
w('')
w('The number compared is the agency\'s strongest focus score in each window —')
w('its best axis before, against its best axis after. That is the fair')
w('comparison: an agency that switched which axis it is narrow on still counts.')
w('')
for coh in ('narrower', 'control'):
    v = changes.get(coh, [])
    if not v:
        continue
    q1, med, q3, n = quart(v)
    w(f'- **{COHORT[coh]}** ({n} agencies): the middle agency moved '
      f'{med*100:+.0f} points; low quarter {q1*100:+.0f}, high quarter {q3*100:+.0f}.')
w('')
w('| Group | Agencies measurable both windows | Got narrower by ≥5 pts | ≥10 | ≥15 | ≥20 | Got broader by ≥15 |')
w('|---|---|---|---|---|---|---|')
for coh in ('narrower', 'control'):
    v = changes.get(coh, [])
    if not v:
        continue
    cells = ' | '.join(str(sum(1 for x in v if x >= t)) for t in (.05, .10, .15, .20))
    w(f'| {COHORT[coh]} | {len(v)} | {cells} | {sum(1 for x in v if x <= -.15)} |')
w('')
w('### The same question asked a second way — and why it reads worse')
w('')
w('The table below anchors on whichever focus type was strongest BEFORE, then')
w('watches that same one after. It looks much more negative, and that is a')
w('measurement artifact, not agency behaviour: picking the highest of seven')
w('noisy scores in the before window guarantees some of them were high by luck,')
w('and luck does not repeat. **Do not read this table as "agencies got broader."**')
w('It is here only so the effect is on the record.')
w('')
w('| Group | Agencies | Got narrower by ≥5 pts | ≥10 | ≥15 | ≥20 | Got broader by ≥15 |')
w('|---|---|---|---|---|---|---|')
for coh in ('narrower', 'control'):
    v = anchored.get(coh, [])
    if not v:
        continue
    cells = ' | '.join(str(sum(1 for x in v if x >= t)) for t in (.05, .10, .15, .20))
    w(f'| {COHORT[coh]} | {len(v)} | {cells} | {sum(1 for x in v if x <= -.15)} |')
w('')
w('_(the original before-anchored figures)_')
w('')
w('### New clients only')
w('')
w('The same question asked of the clients that appear AFTER and were absent')
w('BEFORE. Portfolios pile up, so an agency can go all-in on one niche and barely')
w('move its total mix — this is where that shows.')
w('')
w('| Group | Agencies with ≥3 new clients stating a focus type | Middle strongest score on the new clients | New-client score ≥50% | ≥60% | ≥75% |')
w('|---|---|---|---|---|---|')
for coh in ('narrower', 'control'):
    v = inc_scores.get(coh, [])
    if not v:
        continue
    _q1, med, _q3, n = quart(v)
    cells = ' | '.join(str(sum(1 for x in v if x >= t)) for t in (.50, .60, .75))
    w(f'| {COHORT[coh]} | {n} | {pct(med)} | {cells} |')
w('')

# ------------------------------------------------------------------ section 7
cov = json.load(open(f'{HERE}/_merge_summary.json'))
w('## 7. Unknown rates — how much text the approved lists could not place')
w('')
w('| Focus type | Cases stating it | Landed in a real bucket | Unknown |')
w('|---|---|---|---|')
for ax in AXES:
    c = cov[ax]
    w(f'| {NAME[AXIS_KEY[ax]]} | {c["mass"]} | {c["real"]} ({c["real"]/c["mass"]:.0%}) '
      f'| {c["unknown"]} ({c["unknown"]/c["mass"]:.0%}) |')
w('')

# ------------------------------------------------------------------ section 8
w('## 8. The decisions JC has to make')
w('')
minc = {}
for t in (2, 3, 4, 5, 8):
    keep = 0
    for dom, d in pairs.items():
        if 'before' in d and 'after' in d and \
           d['before']['n_distinct_clients'] >= t and d['after']['n_distinct_clients'] >= t:
            keep += 1
    minc[t] = keep
today_keep = {t: sum(1 for r in by_win.get('today', []) if r['n_distinct_clients'] >= t)
              for t in (2, 3, 4, 5, 8)}

w('### Decision 1 — minimum clients before an agency gets a focus score')
w('')
w('| Minimum distinct clients | Agencies kept, before+after both | Agencies kept, today |')
w('|---|---|---|')
for t in (2, 3, 4, 5, 8):
    w(f'| ≥{t} | {minc[t]} | {today_keep[t]} |')
w('')
w('### Decision 2 — what counts as "concentrated" for stacked focus')
w('')
w('Today window, agencies with at least one scorable focus type:')
w('')
w('| Line for "concentrated" | Median stacked focus | Agencies stacked on ≥2 | ≥3 |')
w('|---|---|---|---|')
for line in (0.40, 0.50, 0.60, 0.75):
    depths = []
    for r in by_win.get('today', []):
        d = sum(1 for k in KEYS if r[f'n_stated_{k}'] >= 3
                and r[f'top1_{k}'] is not None and r[f'top1_{k}'] >= line)
        depths.append(d)
    _q1, med, _q3, _n = quart(depths)
    w(f'| {line:.0%} | {med} | {sum(1 for d in depths if d >= 2)} | '
      f'{sum(1 for d in depths if d >= 3)} |')
w('')
w('### Decision 3 — how big a rise counts as "the client mix narrowed"')
w('')
w('Numbers are in section 6. The placeholder was 15 points.')
w('')
w('### Decision 4 — the "narrow right now" split')
w('')
w('Today window. Placeholder was concentrated ≥50% vs spread ≤33%, minimum 4 clients.')
w('')
w('**Read the first row and you will see the problem.** Taking the highest of')
w('seven scores makes almost every agency look concentrated, so the "spread"')
w('side of the split starves. That is arithmetic, not the Dutch market: with')
w('seven chances to be narrow at something, hardly anyone is broad at everything.')
w('')
w('| Concentrated line / spread line | Concentrated agencies | Spread agencies |')
w('|---|---|---|')
for hi, lo in ((0.50, 0.33), (0.60, 0.40), (0.75, 0.50)):
    c = s = 0
    for r in by_win.get('today', []):
        cand = [r[f'top1_{k}'] for k in KEYS
                if r[f'n_stated_{k}'] >= 3 and r[f'top1_{k}'] is not None]
        if not cand or r['n_distinct_clients'] < 4:
            continue
        m = max(cand)
        c += m >= hi
        s += m <= lo
    w(f'| ≥{hi:.0%} vs ≤{lo:.0%} | {c} | {s} |')
w('')
w('The same split on ONE focus type — what they sell, the best-covered one —')
w('gives two usable sides. This is the version worth considering:')
w('')
w('| Concentrated line / spread line | Concentrated agencies | Spread agencies |')
w('|---|---|---|')
for hi, lo in ((0.50, 0.33), (0.60, 0.40), (0.75, 0.50)):
    c = s = 0
    for r in by_win.get('today', []):
        v = r['top1_craft']
        if v is None or r['n_stated_craft'] < 3 or r['n_distinct_clients'] < 4:
            continue
        c += v >= hi
        s += v <= lo
    w(f'| ≥{hi:.0%} vs ≤{lo:.0%} | {c} | {s} |')
w('')
w('### Decision 5 — which focus types are allowed to carry a test')
w('')
w('Section 2 and section 7 give the two halves of this: how often a focus type is')
w('stated at all, and how much of what is stated the approved list could place.')
w('The two thin ones were already agreed descriptive-only when the lists were')
w('locked (the client\'s money model, the client\'s size).')
w('')

open(f'{ROOT}/2026-08-07-distributions-for-cutoffs.md', 'w').write('\n'.join(L) + '\n')
print(f'wrote 2026-08-07-distributions-for-cutoffs.md ({len(L)} lines)')
