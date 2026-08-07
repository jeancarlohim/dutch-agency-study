#!/usr/bin/env python3
"""Minimal stats, stdlib only (no scipy on this machine).

Permutation / rank tests only — no normality assumptions, which matters because
headcount growth in this dataset is heavily zero-inflated and right-skewed.
"""
import random, math
from collections import Counter

def _ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r

def _tdist_sf(t, df):
    """Two-sided survival function for Student t, via the regularized incomplete
    beta. Stdlib only. Accurate enough for p-value reporting at df>10."""
    x = df / (df + t * t)
    return _betainc(df / 2.0, 0.5, x)

def _betainc(a, b, x):
    """Regularized incomplete beta I_x(a,b) by continued fraction (NR 6.4)."""
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return front * _betacf(a, b, x) / a
    return 1.0 - math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                          + b * math.log(1 - x) + a * math.log(x)) * _betacf(b, a, 1 - x) / b

def _betacf(a, b, x, itmax=200, eps=3e-12):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < 1e-30: d = 1e-30
    d = 1.0 / d; h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30: d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30: c = 1e-30
        d = 1.0 / d; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30: d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30: c = 1e-30
        d = 1.0 / d; de = d * c; h *= de
        if abs(de - 1.0) < eps: break
    return h

def spearman(x, y, exact=False):
    """Rank correlation. p via t-approximation (fast, used in simulation loops)
    or permutation when exact=True (used for the single real reported result)."""
    pairs = [(a, b) for a, b in zip(x, y) if a is not None and b is not None]
    if len(pairs) < 5:
        return None, None, len(pairs)
    a = [p[0] for p in pairs]; b = [p[1] for p in pairs]
    ra, rb = _ranks(a), _ranks(b)
    n = len(ra)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    da = math.sqrt(sum((v - ma) ** 2 for v in ra))
    db = math.sqrt(sum((v - mb) ** 2 for v in rb))
    if da == 0 or db == 0:
        return None, None, n
    rho = num / (da * db)
    if exact:
        return rho, perm_p_corr(ra, rb, rho), n
    if n < 8 or abs(rho) >= 1.0:
        return rho, None, n
    t = rho * math.sqrt((n - 2) / max(1 - rho * rho, 1e-15))
    return rho, _tdist_sf(t, n - 2), n

def perm_p_corr(ra, rb, obs, iters=4000, seed=1):
    rnd = random.Random(seed)
    n = len(ra); ma = sum(ra) / n; mb = sum(rb) / n
    da = math.sqrt(sum((v - ma) ** 2 for v in ra))
    db = math.sqrt(sum((v - mb) ** 2 for v in rb))
    shuf = list(rb); hits = 0
    for _ in range(iters):
        rnd.shuffle(shuf)
        num = sum((ra[i] - ma) * (shuf[i] - mb) for i in range(n))
        if abs(num / (da * db)) >= abs(obs) - 1e-12:
            hits += 1
    return (hits + 1) / (iters + 1)

def mannwhitney(a, b, iters=4000, seed=1):
    """Two-group rank test by permutation. Returns (median_a, median_b, p, na, nb)."""
    a = [v for v in a if v is not None]; b = [v for v in b if v is not None]
    if len(a) < 3 or len(b) < 3:
        return None
    allv = a + b
    r = _ranks(allv)
    obs = sum(r[:len(a)]) / len(a) - sum(r[len(a):]) / len(b)
    rnd = random.Random(seed); pool = list(r); hits = 0
    for _ in range(iters):
        rnd.shuffle(pool)
        d = sum(pool[:len(a)]) / len(a) - sum(pool[len(a):]) / len(b)
        if abs(d) >= abs(obs) - 1e-12:
            hits += 1
    return {'median_a': median(a), 'median_b': median(b), 'mean_rank_diff': round(obs, 3),
            'p': (hits + 1) / (iters + 1), 'n_a': len(a), 'n_b': len(b)}

def median(xs):
    xs = sorted(v for v in xs if v is not None)
    if not xs: return None
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2

def prop_test(succ_a, n_a, succ_b, n_b, iters=4000, seed=1):
    """Difference in 'share growing', permutation. Returns dict."""
    if n_a < 3 or n_b < 3:
        return None
    obs = succ_a / n_a - succ_b / n_b
    pool = [1] * (succ_a + succ_b) + [0] * (n_a - succ_a + n_b - succ_b)
    rnd = random.Random(seed); hits = 0
    for _ in range(iters):
        rnd.shuffle(pool)
        d = sum(pool[:n_a]) / n_a - sum(pool[n_a:]) / n_b
        if abs(d) >= abs(obs) - 1e-12:
            hits += 1
    return {'share_a': round(succ_a / n_a, 3), 'share_b': round(succ_b / n_b, 3),
            'diff_pp': round(obs * 100, 1), 'p': (hits + 1) / (iters + 1),
            'n_a': n_a, 'n_b': n_b}
