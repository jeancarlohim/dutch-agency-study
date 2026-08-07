#!/usr/bin/env python3
"""Run the six frozen tests with JC's fixed cut-offs (Aug 7).

The test functions in 2026-08-04-analysis/run_the_six_tests.py are NOT edited —
they are imported and called. The only things supplied from outside are the
things the pre-registration says JC supplies: the cut-offs and the growth file.

JC's cut-offs (approved Aug 7, from the real distributions, blind to growth):
  minimum clients            4   (3 and 5 as sensitivity)
  concentrated line          50%
  narrowing rise             15 points  (10 and 20 as sensitivity)
  primary outcome            growth_2y  (growth_1y reported alongside)
  narrow-right-now axis      what they sell (craft) — one focus type, not best-of-seven
Primary treatment set stays the 97 verified narrowers; Tier A for causal wording.
Growth is read in BOTH percent and people added (the like-for-like rule).
"""
import csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ANA = '/Users/jeancarlohim/Documents/GitHub/study-outreach/outputs/2026-08-04-analysis'
ROOT = '/Users/jeancarlohim/Documents/GitHub/study-outreach/outputs'
sys.path.insert(0, ANA)
import run_the_six_tests as T

JC = {'rise_pts': 0.15, 'flat_pts': 0.05, 'min_clients': 4,
      'hi_share': 0.50, 'lo_share': 0.33, 'min_clients_snapshot': 4}

def load_growth():
    G = {}
    with open(f'{ROOT}/2026-08-07-growth.csv') as fh:
        for r in csv.DictReader(fh):
            rec = {}
            for k in ('growth_6m', 'growth_1y', 'growth_2y',
                      'added_6m', 'added_1y', 'added_2y', 'employees_now'):
                v = (r.get(k) or '').strip()
                rec[k] = float(v) if v else None
            G[r['domain']] = rec
    return G

def run(label, cutoffs, M, G, pairs, tierfn, v97, outcome='growth_2y'):
    T.CUTOFFS.clear(); T.CUTOFFS.update(cutoffs)
    return {
        'label': label, 'cutoffs': dict(cutoffs), 'outcome': outcome,
        'concrete_proof': T.h5_specificity(M, G, outcome=outcome),
        'stacked_focus': T.h6_depth(M, G, outcome=outcome),
        'said_it_and_showed_it': {
            'industry_tierA_97': T.h1_overt(M, G, v97, tierfn, pairs, axis='industry', outcome=outcome),
            'craft_tierA_97': T.h1_overt(M, G, v97, tierfn, pairs, axis='craft', outcome=outcome),
            'industry_allTiers_97': T.h1_overt(M, G, v97, tierfn, pairs, axis='industry', outcome=outcome, tier_filter=None),
            'craft_allTiers_97': T.h1_overt(M, G, v97, tierfn, pairs, axis='craft', outcome=outcome, tier_filter=None),
            'craft_allTiers_all155': T.h1_overt(M, G, None, tierfn, pairs, axis='craft', outcome=outcome, tier_filter=None),
        },
        'showed_it_quietly': {
            'industry': T.h4_covert(M, G, tierfn, axis='industry', outcome=outcome),
            'craft': T.h4_covert(M, G, tierfn, axis='craft', outcome=outcome),
        },
        'narrow_right_now': {
            'craft_PRIMARY': T.h3_snapshot(M, G, axis='craft', outcome=outcome),
            'industry': T.h3_snapshot(M, G, axis='industry', outcome=outcome),
        },
    }

def main():
    M = T.load_measures()
    pairs, tierfn = T.pairs_and_tiers()
    v97 = T.verified97()
    G = load_growth()
    print(f'growth loaded for {len(G)} companies; '
          f'{sum(1 for g in G.values() if g["growth_2y"] is not None)} with 2y growth')

    out = {'born_narrow_old_instrument': T.h2_born_niche({})}

    out['PRIMARY'] = run('JC cut-offs, growth_2y (percent)', JC, M, G, pairs, tierfn, v97)
    out['outcome_growth_1y'] = run('growth_1y', JC, M, G, pairs, tierfn, v97, outcome='growth_1y')
    out['outcome_people_added_2y'] = run('people added, 2y', JC, M, G, pairs, tierfn, v97, outcome='added_2y')

    sens = {}
    for mc in (3, 5):
        c = dict(JC, min_clients=mc, min_clients_snapshot=max(4, mc))
        sens[f'min_clients_{mc}'] = run(f'min clients {mc}', c, M, G, pairs, tierfn, v97)
    for rp in (0.10, 0.20):
        c = dict(JC, rise_pts=rp)
        sens[f'rise_{int(rp*100)}pts'] = run(f'rise {int(rp*100)} pts', c, M, G, pairs, tierfn, v97)
    out['SENSITIVITY'] = sens

    json.dump(out, open(f'{HERE}/results_full.json', 'w'), indent=1, default=str)
    print('wrote results_full.json')

if __name__ == '__main__':
    main()
