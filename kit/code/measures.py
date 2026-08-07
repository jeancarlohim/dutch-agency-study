#!/usr/bin/env python3
"""Per agency x window measures (plan §4). FROZEN before growth data exists.

The category mapping is a PLUGGABLE layer, on purpose:
  mappings/<axis>.json  =  {"raw value seen in text": "category", ...}
If a mapping file is absent, that axis falls back to PLACEHOLDER clustering so
the mechanics can be dry-run today. Placeholder results are marked as such and
must never be reported. On Friday, drop the JC-approved mappings into
mappings/ and re-run — nothing else changes.

Nothing in this file looks at growth. That is what makes it pre-registration.
"""
import csv, json, os, re, sys
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
AXES = ['industry', 'craft', 'job', 'channel', 'model', 'stage', 'geo']

# which verbatim field feeds which axis
SOURCE_FIELD = {
    'industry': 'sector_raw', 'craft': 'delivered_raw', 'job': 'problem_raw',
    'channel': 'channel_evidence', 'model': 'model_evidence',
    'stage': 'stage_evidence', 'geo': 'geo_evidence',
}

# ---------------------------------------------------------------- mapping layer
def load_mappings():
    out, real = {}, {}
    for ax in AXES:
        p = os.path.join(HERE, 'mappings', f'{ax}.json')
        if os.path.exists(p):
            out[ax] = {k.lower().strip(): v for k, v in json.load(open(p)).items()}
            real[ax] = True
        else:
            out[ax] = None
            real[ax] = False
    return out, real

STOP = set('''de het een en of van voor met in op bij aan naar door onze ons we wij
onder over is zijn was werd worden om te dat die deze dit er als ook nog al meer
the a an and or for with of to in on at by our we is are was were that this it
new nieuwe klant client case project'''.split())

def tokens(s):
    return [t for t in re.findall(r"[a-zà-ÿ][a-zà-ÿ0-9\-']{2,}", (s or '').lower())
            if t not in STOP]

def placeholder_bucket(raw):
    """DRY-RUN ONLY. Crude head-token cluster so shares can be computed today.
    Not a vocabulary. Never report numbers derived from this."""
    t = tokens(raw)
    return t[0] if t else ''

def bucket(raw, axis, maps):
    raw = (raw or '').strip()
    if not raw:
        return ''
    m = maps.get(axis)
    if m is None:
        if os.environ.get('ALLOW_PLACEHOLDER') != '1':
            raise RuntimeError(
                f"No approved category list for axis '{axis}'. Any concentration, "
                f"case-mix or niche-depth number computed without one is a "
                f"mechanical artifact, NOT a result (see 2026-08-04-PRE-REGISTRATION "
                f"§6b). Drop the JC-approved mappings/{axis}.json in place, or set "
                f"ALLOW_PLACEHOLDER=1 for a mechanics-only dry run whose output "
                f"must never be quoted.")
        return placeholder_bucket(raw)
    key = raw.lower().strip()
    if key in m:
        return m[key]
    for t in tokens(raw):                      # token-level fallback for the tail
        if t in m:
            return m[t]
    return 'unknown'

# ------------------------------------------------------------------- specificity
def specificity(case):
    """H5: how concrete is this case, 0-4. All four ingredients are RAW fields —
    no categories needed, so H5 is computable without any vocabulary."""
    s = 0
    if case['named'] == 'Y': s += 1
    if case['has_number'] == 'Y': s += 1
    if case['depth'] == 'full-case-page': s += 1
    if (case['sector_raw'] or '').strip(): s += 1
    return s

# ----------------------------------------------------------------------- shares
def top1_share(buckets):
    """THE 'how narrow' number: of distinct clients, what fraction sit in the
    single biggest category. Ignores blanks — an agency whose text never states
    a sector is not thereby 'concentrated'."""
    vals = [b for b in buckets if b and b != 'unknown']
    if not vals:
        return None, None, 0
    c = Counter(vals)
    top, n = c.most_common(1)[0]
    return n / len(vals), top, len(vals)

def hhi(buckets):
    vals = [b for b in buckets if b and b != 'unknown']
    if not vals:
        return None
    c = Counter(vals); n = len(vals)
    return sum((v / n) ** 2 for v in c.values())

# --------------------------------------------------------------------- assembly
def load_cases(path=None):
    path = path or os.path.join(HERE, 'cases_v2.csv')
    with open(path) as fh:
        return list(csv.DictReader(fh))

def build(cases, maps, depth_threshold=0.50):
    """Per (domain, window): dedup by client_key, then compute every §4 measure."""
    grp = defaultdict(list)
    for c in cases:
        grp[(c['domain'], c['window'])].append(c)

    out = {}
    for (dom, win), rows in grp.items():
        # ---- dedup: one row per distinct client, richest case wins
        best = {}
        anon = []
        for r in rows:
            k = r['client_key']
            if not k:
                anon.append(r); continue
            if k not in best or specificity(r) > specificity(best[k]):
                best[k] = r
        clients = list(best.values())

        rec = {
            'domain': dom, 'window': win, 'cohort': rows[0]['cohort'],
            'pivot_year': rows[0]['pivot_year'],
            'n_case_rows': len(rows),
            'n_distinct_clients': len(clients),
            'n_anonymous_rows': len(anon),
            'client_keys': sorted(best.keys()),
            'avg_specificity': (round(sum(specificity(r) for r in clients) / len(clients), 3)
                                if clients else None),
            'share_numeric': (round(sum(1 for r in clients if r['has_number'] == 'Y') / len(clients), 3)
                              if clients else None),
            'share_full_page': (round(sum(1 for r in clients if r['depth'] == 'full-case-page') / len(clients), 3)
                                if clients else None),
            'truncated': any(r['truncated_by_source'] in ('True', 'true', True) for r in rows),
        }

        depth_axes = []
        for ax in AXES:
            fld = SOURCE_FIELD[ax]
            bs = [bucket(r.get(fld), ax, maps) for r in clients]
            share, top, n = top1_share(bs)
            rec[f'top1_{ax}'] = round(share, 3) if share is not None else None
            rec[f'topbucket_{ax}'] = top
            rec[f'n_stated_{ax}'] = n
            rec[f'hhi_{ax}'] = round(hhi(bs), 3) if hhi(bs) is not None else None
            # an axis counts toward depth only if enough clients state it AND it concentrates
            if share is not None and n >= 3 and share >= depth_threshold:
                depth_axes.append(ax)

        rec['demonstrated_depth'] = len(depth_axes)
        rec['demonstrated_combo'] = '+'.join(depth_axes)
        out[(dom, win)] = rec
    return out

def add_incremental(measures, maps, depth_threshold=0.50):
    """new-clients-only mix: the concentration of clients present at AFTER and
    absent at BEFORE. Plan §4 calls this the main 'did they narrow' number —
    portfolios pile up, so total mix barely moves even when all NEW work is
    one niche."""
    cases = load_cases()
    idx = defaultdict(dict)
    for c in cases:
        if c['client_key']:
            idx[(c['domain'], c['window'])].setdefault(c['client_key'], c)

    for (dom, win), rec in measures.items():
        if win != 'after':
            continue
        before = set(measures.get((dom, 'before'), {}).get('client_keys', []))
        after_rows = idx.get((dom, 'after'), {})
        fresh = [r for k, r in after_rows.items() if k not in before]
        rec['n_new_clients'] = len(fresh)
        rec['n_carried'] = len([k for k in after_rows if k in before])
        rec['n_dropped'] = len(before - set(after_rows.keys()))
        for ax in AXES:
            bs = [bucket(r.get(SOURCE_FIELD[ax]), ax, maps) for r in fresh]
            share, top, n = top1_share(bs)
            rec[f'inc_top1_{ax}'] = round(share, 3) if share is not None else None
            rec[f'inc_n_stated_{ax}'] = n
    return measures

def main():
    maps, real = load_mappings()
    placeholder = [a for a in AXES if not real[a]]
    cases = load_cases()
    m = build(cases, maps)
    m = add_incremental(m, maps)

    rows = list(m.values())
    for r in rows:
        r['client_keys'] = ';'.join(r['client_keys'][:200])
    cols = sorted({k for r in rows for k in r})
    cols = ['domain', 'window', 'cohort'] + [c for c in cols if c not in ('domain', 'window', 'cohort')]
    with open(os.path.join(HERE, 'measures_v2.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)

    meta = {'agency_windows': len(rows),
            'axes_using_REAL_mapping': [a for a in AXES if real[a]],
            'axes_using_PLACEHOLDER': placeholder,
            'reportable': not placeholder}
    json.dump(meta, open(os.path.join(HERE, '_measures_meta.json'), 'w'), indent=1)
    print(json.dumps(meta, indent=1))
    if placeholder:
        print('\n*** PLACEHOLDER MAPPINGS IN USE — mechanics only, do NOT report ***')
    print(f'wrote measures_v2.csv ({len(rows)} agency-windows)')

if __name__ == '__main__':
    main()
