#!/usr/bin/env python3
"""Build the ONE growth file the frozen tests read, and close two data gaps.

Three jobs, all mechanical:
  1. Give every twin the pivot year of the narrower it was matched to — the
     SAME assignment the case side already uses (_targets.json), so the two
     halves of the study line up by construction rather than by luck.
  2. Drop the companies whose scraped identity does not match their domain.
  3. Turn 455 raw employee files into domain,employees_now,growth_6m,
     growth_1y,growth_2y — the shape run_the_six_tests.py expects.

Growth comes from series_monthly (LinkedIn's own headcount chart, ~25 monthly
points). That chart counts leavers correctly. headcount_by_year is NOT used
for growth: it is rebuilt from current employees' start dates, so everyone who
left is invisible and every past year reads too small.
"""
import csv, glob, json, os
from collections import Counter

ROOT = '/Users/jeancarlohim/Documents/GitHub/study-outreach/outputs'
EMP = f'{ROOT}/2026-08-03-salesnav-pilot/employees'

targets = json.load(open(f'{ROOT}/2026-08-02-historical-proof/_targets.json'))
PIVOT = {t['domain'].lower(): t.get('pivot_year') for t in targets}
COHORT = {t['domain'].lower(): t['cohort'] for t in targets}
MATCH = {t['domain'].lower(): (t.get('matched_to') or '').lower() for t in targets}

def pct(new, old):
    if old is None or new is None or old <= 0:
        return None
    return round((new - old) / old, 4)

rows, dropped, thin = [], [], []
for p in sorted(glob.glob(f'{EMP}/*.json')):
    d = json.load(open(p))
    dom = (d.get('domain') or '').lower()

    # ---- 2. identity gate
    if d.get('domain_match') is False:
        dropped.append({'domain': dom, 'group': d.get('group', ''),
                        'reason': 'scraped company does not match the domain',
                        'scraped_name': (d.get('name') or '')[:80]})
        continue

    # ---- 1. pivot year: twins inherit their narrower's, same as the case side
    pv = d.get('pivot_year') or PIVOT.get(dom)
    pv_src = '' if not pv else ('own' if COHORT.get(dom) == 'narrower' else 'matched twin')

    # ---- 3. growth off the monthly chart
    s = [(m, int(v)) for m, v in (d.get('series_monthly') or []) if v is not None]
    s.sort()
    rec = {'domain': dom, 'group': d.get('group', ''),
           'pivot_year': pv or '', 'pivot_year_source': pv_src,
           'matched_to': MATCH.get(dom, ''),
           'revenue_band': d.get('revenue') or '',
           'median_tenure_years': d.get('median_tenure_years') or '',
           'months_of_chart': len(s)}
    if len(s) < 13:
        thin.append(dom)
        rec.update({'employees_now': '', 'growth_6m': '', 'growth_1y': '',
                    'growth_2y': '', 'added_6m': '', 'added_1y': '', 'added_2y': ''})
        rows.append(rec)
        continue

    now = s[-1][1]
    def back(n):
        return s[-1 - n][1] if len(s) > n else None
    for label, n in (('6m', 6), ('1y', 12), ('2y', 24)):
        old = back(n)
        rec[f'growth_{label}'] = '' if pct(now, old) is None else pct(now, old)
        rec[f'added_{label}'] = '' if old is None else now - old
    rec['employees_now'] = now
    rows.append(rec)

cols = ['domain', 'employees_now', 'growth_6m', 'growth_1y', 'growth_2y',
        'added_6m', 'added_1y', 'added_2y', 'group', 'pivot_year',
        'pivot_year_source', 'matched_to', 'revenue_band',
        'median_tenure_years', 'months_of_chart']
with open(f'{ROOT}/2026-08-07-growth.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader(); w.writerows(rows)

with open(f'{ROOT}/2026-08-07-growth-excluded.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=['domain', 'group', 'reason', 'scraped_name'])
    w.writeheader(); w.writerows(dropped)

usable = [r for r in rows if r['growth_2y'] != '']
g = Counter(r['group'] for r in rows)
gu = Counter(r['group'] for r in usable)
piv = Counter(r['pivot_year_source'] for r in rows if r['pivot_year_source'])
print(f'wrote 2026-08-07-growth.csv           {len(rows)} companies ({dict(g)})')
print(f'wrote 2026-08-07-growth-excluded.csv  {len(dropped)} dropped on identity')
print(f'pivot year present                    {sum(1 for r in rows if r["pivot_year"])} ({dict(piv)})')
print(f'usable 2-year growth                  {len(usable)} ({dict(gu)})')
print(f'chart too thin to use                 {len(thin)}')
