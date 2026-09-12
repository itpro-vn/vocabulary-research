"""Research-only residual Horvitz-Thompson reference; NOT latent word knowledge.
Input is a trusted server-side frozen design, never a user-supplied score payload.
Requires SRS without replacement within each remaining stratum, quotas fixed before
focused responses, complete fixed binary potential outcomes, and no repeat units.
"""
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.stats import hypergeom


def sample_frame(frame, quotas, seed, excluded=None):
    """Reproducible SRSWOR research plan. Persist and freeze it BEFORE responses.
    Seed/quota choice must never be retried based on focused responses.
    """
    import random
    if not frame or set(frame) != set(quotas):
        raise ValueError('Explicit quota required for every stratum')
    excluded = {h: [] for h in frame} if excluded is None else excluded
    if set(excluded) != set(frame):
        raise ValueError('Explicit exclusions required for every stratum')
    ids = [x for group in frame.values() for x in group]
    if any(not isinstance(x, str) or not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError('Frame IDs must be globally unique nonempty strings')
    rng = random.Random(seed)
    result = {}
    for h in sorted(frame):
        if len(excluded[h]) != len(set(excluded[h])) or not set(excluded[h]).issubset(frame[h]):
            raise ValueError('Invalid excluded units')
        available = sorted(set(frame[h]) - set(excluded[h]))
        n = quotas[h]
        if type(n) is not int or not 0 <= n <= len(available):
            raise ValueError('Impossible quota')
        result[h] = rng.sample(available, n)
    return result


def score(document, alpha=0.05):
    if not isinstance(alpha, (int, float)) or not math.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError('alpha must be strictly between 0 and 1')
    frame = document['frame']
    screening = document['screening']
    focused = document['focused']
    responses = document['responses']
    if not frame or set(frame) != set(screening) or set(frame) != set(focused):
        raise ValueError('Every stratum must be represented in the frozen design')
    ids = [x for group in frame.values() for x in group]
    if any(not isinstance(x, str) or not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError('Frame IDs must be globally unique nonempty strings')
    if any(not isinstance(group, list) or not group for group in frame.values()):
        raise ValueError('Every frame stratum must be a nonempty list')
    presented = []
    for h, group in frame.items():
        s, f = screening[h], focused[h]
        if not isinstance(s, list) or not isinstance(f, list):
            raise ValueError('Selection must be lists of unit IDs')
        selected = s + f
        if len(set(selected)) != len(selected) or not set(selected).issubset(group):
            raise ValueError('Duplicate or out-of-frame selected unit')
        remaining = len(group) - len(s)
        if remaining and len(f) < min(2, remaining):
            raise ValueError('Insufficient focused coverage; census singleton remainders')
        presented.extend(selected)
    if not set(responses).issubset(presented):
        raise ValueError('Response for an unpresented unit')
    valid = {'correct', 'incorrect', 'dont_know', 'timeout', 'not_answered', 'technical_failure'}
    if any(not isinstance(v, str) or v not in valid for v in responses.values()):
        raise ValueError('Unrecognized response category')
    missing = [x for x in presented if responses.get(x) not in {'correct', 'incorrect', 'dont_know'}]
    base = {'scoring_version': 'baseline-design-v0.1',
            'estimand': 'finite_frame_correct_response_total',
            'unit': 'frozen_frame_assessment_unit', 'frame_size': len(ids),
            'public_vocabulary_claim_allowed': False}
    if missing:
        return dict(base, status='insufficient_evidence', estimate=None, interval=None,
                    reason_codes=['incomplete_design_responses'], missing_count=len(missing))
    value = lambda x: int(responses[x] == 'correct')
    estimate, lower, upper = 0.0, 0, 0
    detail = []
    for h, group in frame.items():
        A = sum(value(x) for x in screening[h])
        M = len(group) - len(screening[h])
        n = len(focused[h])
        k = sum(value(x) for x in focused[h])
        if M == 0:
            point, lo, hi = float(A), A, A
        else:
            point = A + M * k / n
            candidates = np.arange(k, M - n + k + 1, dtype=np.int64)
            threshold = alpha / len(frame) / 2
            accepted = candidates[(hypergeom.sf(k - 1, M, candidates, n) >= threshold) &
                                  (hypergeom.cdf(k, M, candidates, n) >= threshold)]
            if not len(accepted):
                raise ValueError('Numerical interval failure; do not emit a score')
            lo, hi = A + int(accepted[0]), A + int(accepted[-1])
        estimate += point
        lower += lo
        upper += hi
        detail.append({'stratum': h, 'N': len(group), 'screened': len(screening[h]),
                       'remaining': M, 'focused': n, 'estimate': point})
    return dict(base, status='scored', estimate=estimate,
                interval={'type': 'design_confidence', 'method': 'hypergeometric_inversion_bonferroni',
                          'level': 1 - alpha, 'bounds': [lower, upper],
                          'conditional_on': 'fixed potential outcomes, frozen screening, valid focused sampling'},
                strata=detail)


def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError('Usage: python baseline.py TRUSTED_DESIGN.json')
        result = score(json.loads(Path(sys.argv[1]).read_text()))
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({'status': 'scoring_unavailable', 'message': str(exc)}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
