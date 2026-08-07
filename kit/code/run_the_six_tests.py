#!/usr/bin/env python3
"""The six hypothesis tests, FROZEN before growth data exists.

Growth enters through ONE door: a CSV with columns
    domain, employees_now, growth_6m, growth_1y, growth_2y
passed as --growth. Until Friday that file doesn't exist, so this module runs
in --simulate mode against synthetic outcomes to prove the machinery and to
measure real power at the real n.

Pre-registered choices (plan §5), written down now so they cannot be chosen
after seeing results:
  primary treatment set = the 97 Sonnet-verified narrowers (55 / 155 = sensitivity)
  primary measure       = deduped incremental (new-clients-only) top1 share
  primary outcome       = growth_2y
  primary tier          = Tier A only (pivot 2022-2024) for any causal-flavoured wording
  everything else       = exploratory, labelled as such
Cut-offs below are PLACEHOLDERS until JC fixes them from real distributions.
Every result is re-run at neighbouring cut-offs; a finding that exists at only
one threshold is not a finding.
"""
import csv, json, os, sys, argparse, random
from collections import defaultdict
import stats_lib as S

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = '/Users/jeancarlohim/Documents/GitHub/study-outreach/outputs'

CUTOFFS = {'rise_pts': 0.15, 'flat_pts': 0.05, 'min_clients': 3,
           'hi_share': 0.50, 'lo_share': 0.33, 'min_clients_snapshot': 4}

def load_measures():
    with open(os.path.join(HERE, 'measures_v2.csv')) as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        for k, v in list(r.items()):
            if k in ('domain', 'window', 'cohort', 'demonstrated_combo', 'client_keys',
                     'pivot_year', 'truncated') or k.startswith('topbucket'):
                continue
            r[k] = float(v) if v not in ('', 'None', None) else None
    m = {}
    for r in rows:
        m[(r['domain'], r['window'])] = r
    return m

def parse_pct(v):
    """Growth arrives as strings: '+30%', '0%', '-12%', '', 'n/a'. The existing
    433 CSV uses exactly this format, so parse it rather than assuming floats."""
    if v is None:
        return None
    s = str(v).strip().replace('%', '').replace('+', '').replace(',', '.')
    if s in ('', 'None', 'n/a', 'NA', '-'):
        return None
    try:
        return float(s) / 100.0
    except ValueError:
        return None

def load_growth(path):
    g = {}
    if not path or not os.path.exists(path):
        return g
    with open(path) as fh:
        for r in csv.DictReader(fh):
            d = (r.get('domain') or r.get('real_site') or '').strip().lower()
            d = re.sub(r'^https?://(www\.)?', '', d).rstrip('/')
            if not d:
                continue
            rec = {}
            for k in ('growth_6m', 'growth_1y', 'growth_2y'):
                if k in r:
                    rec[k] = parse_pct(r[k])
            if 'employees_now' in r:
                try:
                    rec['employees_now'] = float(str(r['employees_now']).strip() or 'nan')
                except ValueError:
                    rec['employees_now'] = None
            g[d] = rec
    return g

def pairs_and_tiers():
    tg = json.load(open(f'{ROOT}/2026-08-02-historical-proof/_targets.json'))
    pairs = [((t.get('matched_to') or '').lower(), t['domain'].lower())
             for t in tg if t['cohort'] == 'control' and t.get('matched_to')]
    piv = {t['domain'].lower(): t.get('pivot_year') for t in tg}
    def tier(d):
        y = piv.get(d)
        if not y: return 'unknown'
        y = int(y)
        return 'A' if 2022 <= y <= 2024 else 'B' if y >= 2025 else 'C'
    return pairs, tier

def verified97():
    p = f'{ROOT}/2026-08-02-narrowers-confirmed.csv'
    if not os.path.exists(p): return set()
    with open(p) as fh:
        return {r['domain'].strip().lower() for r in csv.DictReader(fh)}

# --------------------------------------------------------------------- the tests
def h5_specificity(M, G, outcome='growth_2y'):
    """Do agencies whose cases are MORE CONCRETE grow more? Sliding scale.
    Needs no vocabulary — all four ingredients are raw extracted fields."""
    x, y = [], []
    for (dom, win), r in M.items():
        if win != 'after':            # one row per agency, the later window
            continue
        g = G.get(dom, {}).get(outcome)
        if g is None or r['avg_specificity'] is None or r['n_distinct_clients'] < CUTOFFS['min_clients']:
            continue
        x.append(r['avg_specificity']); y.append(g)
    rho, p, n = S.spearman(x, y)
    return {'test': 'Concrete proof: specificity vs growth', 'rho': rho, 'p': p, 'n': n}

def h6_depth(M, G, outcome='growth_2y'):
    """Does concentrating on MORE AXES AT ONCE predict growth? Retests the Jul-31
    claimed-depth null with the demonstrated (case-based) instrument."""
    x, y = [], []
    for (dom, win), r in M.items():
        if win != 'after': continue
        g = G.get(dom, {}).get(outcome)
        if g is None or r['n_distinct_clients'] < CUTOFFS['min_clients']: continue
        x.append(r['demonstrated_depth']); y.append(g)
    rho, p, n = S.spearman(x, y)
    return {'test': 'Stacked focus: demonstrated niche depth vs growth', 'rho': rho, 'p': p, 'n': n}

def h1_overt(M, G, treatment, tierfn, pairs, axis='industry', outcome='growth_2y',
             tier_filter=('A',)):
    """T3 vs T1, matched pairs. Narrower whose case mix ALSO narrowed, vs its
    matched control that stayed flat. Paired, so pair-level confounders cancel."""
    tre, ctl = [], []
    used = []
    for narrower, control in pairs:
        if treatment and narrower not in treatment: continue
        if tier_filter and tierfn(narrower) not in tier_filter: continue
        nb, na = M.get((narrower, 'before')), M.get((narrower, 'after'))
        cb, ca = M.get((control, 'before')), M.get((control, 'after'))
        if not all([nb, na, cb, ca]): continue
        if min(nb['n_distinct_clients'], na['n_distinct_clients'],
               cb['n_distinct_clients'], ca['n_distinct_clients']) < CUTOFFS['min_clients']:
            continue
        nbs, nas = nb[f'top1_{axis}'], na[f'top1_{axis}']
        cbs, cas = cb[f'top1_{axis}'], ca[f'top1_{axis}']
        if None in (nbs, nas, cbs, cas): continue
        if (nas - nbs) < CUTOFFS['rise_pts']: continue          # narrower must have narrowed
        if abs(cas - cbs) > CUTOFFS['flat_pts']: continue       # control must be flat
        gn, gc = G.get(narrower, {}).get(outcome), G.get(control, {}).get(outcome)
        if gn is None or gc is None: continue
        tre.append(gn); ctl.append(gc); used.append((narrower, control))
    res = S.mannwhitney(tre, ctl)
    return {'test': f'Said it and showed it: narrower vs matched twin (axis={axis}, tier={tier_filter})',
            'result': res, 'n_pairs': len(used), 'pairs': used[:40]}

def h4_covert(M, G, tierfn, axis='industry', outcome='growth_2y'):
    """T2 vs T1 inside the CONTROLS. Uses the new-clients-only mix: portfolios
    pile up, so total mix barely moves even when all NEW work is one niche."""
    narrowed, flat = [], []
    for (dom, win), r in M.items():
        if win != 'after' or r['cohort'] != 'control': continue
        b = M.get((dom, 'before'))
        if not b: continue
        if min(b['n_distinct_clients'], r['n_distinct_clients']) < CUTOFFS['min_clients']: continue
        inc, base = r.get(f'inc_top1_{axis}'), b.get(f'top1_{axis}')
        if inc is None or base is None: continue
        g = G.get(dom, {}).get(outcome)
        if g is None: continue
        d = inc - base
        if d >= CUTOFFS['rise_pts']: narrowed.append(g)
        elif abs(d) <= CUTOFFS['flat_pts']: flat.append(g)
    return {'test': f'Showed it quietly: new-client mix narrowed vs flat (axis={axis})',
            'result': S.mannwhitney(narrowed, flat)}

def h3_snapshot(M, G, axis='industry', outcome='growth_2y'):
    """T2 as a snapshot: concentrated NOW vs broad NOW. Needs the TODAY window."""
    hi, lo = [], []
    for (dom, win), r in M.items():
        if win != 'today': continue
        if r['n_distinct_clients'] < CUTOFFS['min_clients_snapshot']: continue
        s = r.get(f'top1_{axis}')
        g = G.get(dom, {}).get(outcome)
        if s is None or g is None: continue
        if s >= CUTOFFS['hi_share']: hi.append(g)
        elif s <= CUTOFFS['lo_share']: lo.append(g)
    return {'test': f'Narrow right now: concentrated today vs spread today (axis={axis})',
            'result': S.mannwhitney(hi, lo)}

def h2_born_niche(G, outcome='growth_2y'):
    """T4 vs T1 on the ORIGINAL 340 only — that population has always-niche
    agencies AND pre-existing growth. Descriptive; underpowered by construction."""
    p = f'{ROOT}/2026-08-01-full-433-uncapped.csv'
    if not os.path.exists(p): return {'test': 'Born narrow', 'error': 'source csv missing'}
    niche, broad = [], []
    with open(p) as fh:
        for r in csv.DictReader(fh):
            if r.get('class') in ('not-an-agency', 'dead-or-blocked'): continue
            g = parse_pct(r.get(outcome))
            if g is None: continue
            if r.get('path') == 'always-niche': niche.append(g)
            elif r.get('path') == 'always-broad': broad.append(g)
    return {'test': 'Born narrow: always-focused vs always-broad (original 340, descriptive)',
            'result': S.mannwhitney(niche, broad)}

# ------------------------------------------------------------------- simulation
def synth_growth(M, effect=0.0, driver='avg_specificity', noise=0.35, seed=0,
                 coverage=0.81):
    """Fabricate an outcome with a KNOWN effect size, to measure power.
    coverage mimics Sales Nav's 81% hit rate on the original 340."""
    rnd = random.Random(seed)
    vals = [r[driver] for (d, w), r in M.items() if w == 'after' and r.get(driver) is not None]
    if not vals: return {}
    lo, hi = min(vals), max(vals)
    rng = (hi - lo) or 1.0
    G = {}
    for (dom, win), r in M.items():
        if win != 'after': continue
        if rnd.random() > coverage: continue          # missing-at-random coverage
        z = ((r.get(driver) or lo) - lo) / rng
        G[dom] = {'growth_2y': effect * z + rnd.gauss(0, noise)}
    return G

def power_curve(M, testfn, effects, iters=120, **kw):
    out = []
    for eff in effects:
        hits = 0; ns = []
        for s in range(iters):
            G = synth_growth(M, effect=eff, seed=s, **kw)
            r = testfn(M, G)
            p = r.get('p') if 'p' in r else (r.get('result') or {}).get('p')
            n = r.get('n') if 'n' in r else (r.get('result') or {}).get('n_a')
            if n: ns.append(n)
            if p is not None and p < 0.05: hits += 1
        out.append({'effect': eff, 'power': round(hits / iters, 2),
                    'median_n': S.median(ns)})
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--growth', default=None, help='CSV with domain,growth_2y,...')
    ap.add_argument('--simulate', action='store_true')
    a = ap.parse_args()

    M = load_measures()
    pairs, tierfn = pairs_and_tiers()
    v97 = verified97()

    if a.simulate:
        print('=== SIMULATION (synthetic outcomes; no real growth data) ===\n')
        print('Concrete proof — power curve — effect = growth difference across the full')
        print('specificity range, in growth-rate units (noise sd 0.35, coverage 81%)')
        for row in power_curve(M, h5_specificity, [0.0, 0.10, 0.20, 0.30, 0.50]):
            print(f"   effect {row['effect']:.2f} -> power {row['power']:.0%}  (median n={row['median_n']})")
        print('\nStacked focus — power curve')
        for row in power_curve(M, h6_depth, [0.0, 0.10, 0.20, 0.30, 0.50],
                               driver='demonstrated_depth'):
            print(f"   effect {row['effect']:.2f} -> power {row['power']:.0%}  (median n={row['median_n']})")
        print('\nSaid it and showed it — pair yield at the real data (how many pairs survive every filter):')
        G = synth_growth(M, effect=0.0, seed=0, coverage=1.0)
        for ax in ('industry', 'craft', 'job'):
            for tf in [('A',), ('A', 'B'), None]:
                r = h1_overt(M, G, v97 or None, tierfn, pairs, axis=ax, tier_filter=tf)
                print(f"   axis={ax:9s} tier={str(tf):12s} -> {r['n_pairs']} pairs")
        print('\nShowed it quietly — group sizes (controls, synthetic full coverage):')
        for ax in ('industry', 'craft', 'job'):
            r = h4_covert(M, G, tierfn, axis=ax)
            res = r['result']
            print(f"   axis={ax:9s} -> narrowed n={res['n_a'] if res else 0}, flat n={res['n_b'] if res else 0}")
        print('\nBorn narrow (real data, no simulation needed):')
        print('  ', json.dumps(h2_born_niche({}), default=str)[:300])
        return

    G = load_growth(a.growth)
    if not G:
        print('No growth file. Run with --simulate, or pass --growth <csv>.'); return
    out = {
        'concrete_proof': h5_specificity(M, G),
        'stacked_focus': h6_depth(M, G),
        'born_narrow': h2_born_niche(G),
        'said_it_and_showed_it__industry': h1_overt(M, G, v97 or None, tierfn, pairs, axis='industry'),
        'said_it_and_showed_it__craft': h1_overt(M, G, v97 or None, tierfn, pairs, axis='craft'),
        'showed_it_quietly__industry': h4_covert(M, G, tierfn, axis='industry'),
        'narrow_right_now__industry': h3_snapshot(M, G, axis='industry'),
    }
    print(json.dumps(out, indent=1, default=str))
    json.dump(out, open(os.path.join(HERE, 'results.json'), 'w'), indent=1, default=str)

if __name__ == '__main__':
    main()
