"""Finite-population mathematical tests, not human vocabulary validation."""
from fractions import Fraction
import itertools
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import baseline


class BaselineTests(unittest.TestCase):
    def test_sampling_is_reproducible_disjoint_and_preserves_quotas(self):
        self.assertTrue(hasattr(baseline, 'sample_frame'), 'Reproducible sampler is not implemented')
        frame = {'h': ['a', 'b', 'c', 'd', 'e']}
        screen = baseline.sample_frame(frame, {'h': 1}, seed=7)
        focused = baseline.sample_frame(frame, {'h': 2}, seed=11, excluded=screen)
        self.assertEqual(screen, baseline.sample_frame(frame, {'h': 1}, seed=7))
        self.assertEqual(len(focused['h']), 2)
        self.assertFalse(set(screen['h']) & set(focused['h']))
        with self.assertRaises(ValueError):
            baseline.sample_frame(frame, {'h': 5}, seed=11, excluded=screen)
        with self.assertRaises(ValueError):
            baseline.sample_frame(frame, {}, seed=11)

    def design(self):
        return {'frame': {'h': ['a', 'b', 'c', 'd']}, 'screening': {'h': ['a']},
                'focused': {'h': ['b', 'c']},
                'responses': {'a': 'correct', 'b': 'correct', 'c': 'incorrect'}}

    def test_timeout_withholds_count(self):
        d = self.design()
        d['responses']['b'] = 'timeout'
        result = baseline.score(d)
        self.assertEqual(result['status'], 'insufficient_evidence')
        self.assertIsNone(result['estimate'])
        self.assertIsNone(result['interval'])

    def test_absent_response_withholds_count(self):
        d = self.design()
        del d['responses']['b']
        self.assertEqual(baseline.score(d)['status'], 'insufficient_evidence')

    def test_duplicate_selection_rejected(self):
        d = self.design()
        d['focused']['h'] = ['a', 'b']
        with self.assertRaises(ValueError):
            baseline.score(d)

    def test_zero_inclusion_remainder_rejected(self):
        d = self.design()
        d['focused']['h'] = []
        with self.assertRaises(ValueError):
            baseline.score(d)

    def test_extra_unpresented_response_rejected(self):
        d = self.design()
        d['responses']['d'] = 'correct'
        with self.assertRaises(ValueError):
            baseline.score(d)

    def test_census_has_zero_sampling_uncertainty(self):
        d = self.design()
        d['focused']['h'].append('d')
        d['responses']['d'] = 'correct'
        result = baseline.score(d)
        self.assertEqual(result['estimate'], 3)
        self.assertEqual(result['interval']['bounds'], [3, 3])

    def test_all_wrong_sample_does_not_imply_zero_upper_bound(self):
        d = self.design()
        d['responses'] = {x: 'incorrect' for x in ['a', 'b', 'c']}
        result = baseline.score(d)
        self.assertEqual(result['estimate'], 0)
        self.assertGreater(result['interval']['bounds'][1], 0)

    def test_exhaustive_adaptive_quota_estimator_and_interval(self):
        frame = {'h': [str(i) for i in range(6)]}
        truth = [1, 1, 1, 0, 0, 0]
        expectation = Fraction(0)
        coverage = Fraction(0)
        probability = Fraction(0)
        for first in range(6):
            remainder = [i for i in range(6) if i != first]
            n = 2 if truth[first] else 3
            samples = list(itertools.combinations(remainder, n))
            p = Fraction(1, 6 * len(samples))
            for sample in samples:
                d = {'frame': frame, 'screening': {'h': [str(first)]},
                     'focused': {'h': [str(i) for i in sample]},
                     'responses': {str(i): 'correct' if truth[i] else 'incorrect' for i in (first, *sample)}}
                result = baseline.score(d)
                expectation += p * Fraction(str(result['estimate']))
                lo, hi = result['interval']['bounds']
                coverage += p * int(lo <= sum(truth) <= hi)
                probability += p
        self.assertEqual(probability, 1)
        self.assertAlmostEqual(float(expectation), sum(truth), places=12)
        self.assertGreaterEqual(coverage, Fraction(95, 100))


if __name__ == '__main__':
    unittest.main()
