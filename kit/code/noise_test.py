#!/usr/bin/env python3
"""How much do the tagging misses actually move the answer?

Not a textbook rule of thumb — a simulation on the real portfolios. Each
client's tag is knocked to a different bucket with the measured miss rate, the
focus score is recomputed, and the damage is measured at two levels:

  * one agency  — how far its own focus score moves
  * one group   — how far the group's middle score moves

Because a focus score is an average over many clients, most misses cancel each
other out. The question is how many clients, and how many agencies, it takes
before they cancel out enough to stop mattering.
"""
import csv, json, os, random, statistics, sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rules import AXIS_KEY

ANA = '/Users/jeancarlohim/Documents/GitHub/study-outreach/outputs/2026-08-04-analysis'
csv.field_size_limit(10 ** 9)
random.seed(20260807)

AXIS, FIELD = 'what_they_sell', 'delivered_raw'        # the axis JC picked for the split
MISS = 0.15                                   # measured miss rate, rounded up
TRIALS = 400

m = json.load(open(f'{ANA}/mappings/{AXIS_KEY[AXIS]}.json'))
rows = list(csv.DictReader(open(f'{ANA}/cases_v2.csv')))

def spec(r):
    return ((r['named'] == 'Y') + (r['has_number'] == 'Y') +
            (r['depth'] == 'full-case-page') + bool((r['sector_raw'] or '').strip()))

# dedup exactly as measures.py does: one row per distinct client, richest wins
grp = defaultdict(dict)
for r in rows:
    k = r['client_key']
    if not k:
        continue
    g = grp[(r['domain'], r['window'])]
    if k not in g or spec(r) > spec(g[k]):
        g[k] = r

portfolios = {}
for key, g in grp.items():
    bs = [m.get((r[FIELD] or '').lower().strip(), 'unknown') for r in g.values()]
    bs = [b for b in bs if b and b != 'unknown']
    if bs:
        portfolios[key] = bs

MARGINAL = Counter(b for bs in portfolios.values() for b in bs)
POOL = list(MARGINAL.elements())

def top1(bs):
    c = Counter(bs)
    return c.most_common(1)[0][1] / len(bs)

def corrupt(bs):
    return [random.choice(POOL) if random.random() < MISS else b for b in bs]

print(f'axis: {AXIS}   miss rate simulated: {MISS:.0%}   portfolios: {len(portfolios)}\n')

# ---------------------------------------------------- level 1: one agency
print('ONE AGENCY — how far its own focus score moves')
print(f'{"clients shown":>14} {"agencies":>9} {"typical move":>13} {"moves >10 pts":>14}')
BANDS = [(3, 3), (4, 4), (5, 6), (7, 9), (10, 14), (15, 24), (25, 9999)]
agency_rows = []
for lo, hi in BANDS:
    sel = [bs for bs in portfolios.values() if lo <= len(bs) <= hi]
    if not sel:
        continue
    errs = []
    for bs in sel:
        t = top1(bs)
        for _ in range(max(1, TRIALS // max(len(sel), 1))):
            errs.append(abs(top1(corrupt(bs)) - t))
    med = statistics.median(errs)
    big = sum(1 for e in errs if e > 0.10) / len(errs)
    label = f'{lo}' if lo == hi else (f'{lo}+' if hi > 1000 else f'{lo}-{hi}')
    print(f'{label:>14} {len(sel):>9} {med*100:>11.0f} pts {big:>13.0%}')
    agency_rows.append((label, len(sel), med, big))

# ---------------------------------------------------- level 2: one group
print('\nONE GROUP — how far the group\'s middle focus score moves')
print(f'{"agencies in group":>18} {"typical move":>13} {"moves >3 pts":>13} {"worst in 100":>13}')
eligible = [bs for bs in portfolios.values() if len(bs) >= 4]
group_rows = []
for G in (10, 20, 30, 50, 75, 100, 150, 200):
    if G > len(eligible):
        continue
    shifts = []
    for _ in range(TRIALS):
        sample = random.sample(eligible, G)
        true = statistics.median(top1(bs) for bs in sample)
        seen = statistics.median(top1(corrupt(bs)) for bs in sample)
        shifts.append(abs(seen - true))
    shifts.sort()
    med = statistics.median(shifts)
    big = sum(1 for s in shifts if s > 0.03) / len(shifts)
    p99 = shifts[int(0.99 * (len(shifts) - 1))]
    print(f'{G:>18} {med*100:>11.0f} pts {big:>12.0%} {p99*100:>11.0f} pts')
    group_rows.append((G, med, big, p99))

json.dump({'axis': AXIS, 'miss_rate': MISS,
           'agency_level': agency_rows, 'group_level': group_rows},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '_noise_test.json'), 'w'), indent=1)

# ------------------------------------- level 3: the DIFFERENCE between two groups
# This is what actually gets reported. The flattening above hits both groups
# equally, so most of it cancels when you subtract one from the other.
print('\nTWO GROUPS COMPARED — how far the GAP between them moves')
print(f'{"agencies per group":>19} {"typical move":>13} {"moves >3 pts":>13} {"worst in 100":>13}')
diff_rows = []
for G in (10, 20, 30, 40, 50, 75, 100, 150):
    if 2 * G > len(eligible):
        continue
    shifts = []
    for _ in range(TRIALS):
        s = random.sample(eligible, 2 * G)
        a, b = s[:G], s[G:]
        true = (statistics.median(top1(x) for x in a) -
                statistics.median(top1(x) for x in b))
        seen = (statistics.median(top1(corrupt(x)) for x in a) -
                statistics.median(top1(corrupt(x)) for x in b))
        shifts.append(abs(seen - true))
    shifts.sort()
    med = statistics.median(shifts)
    big = sum(1 for x in shifts if x > 0.03) / len(shifts)
    p99 = shifts[int(0.99 * (len(shifts) - 1))]
    print(f'{G:>19} {med*100:>11.0f} pts {big:>12.0%} {p99*100:>11.0f} pts')
    diff_rows.append((G, med, big, p99))

json.dump({'axis': AXIS, 'miss_rate': MISS, 'agency_level': agency_rows,
           'group_level': group_rows, 'difference_level': diff_rows},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '_noise_test.json'), 'w'), indent=1)
