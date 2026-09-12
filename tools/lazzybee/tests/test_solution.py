"""Synthetic fixtures only. No LazzyBee vocabulary or user records included."""
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class OfflineSolutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.db = self.work / 'synthetic.db'
        with sqlite3.connect(self.db) as con:
            con.execute('CREATE TABLE vocabulary (id INTEGER, question TEXT, answers TEXT, meaning TEXT, l_en TEXT, l_vn TEXT, level INTEGER, user_note TEXT)')
            con.executemany('INSERT INTO vocabulary VALUES (?,?,?,?,?,?,?,?)', [
                (1, 'bank', '{"explain":"A financial institution"}', '{"vn":"ngan hang"}', '', '', 1, 'PRIVATE-NOTE'),
                (2, ' Bank ', '{}', '{}', '', '', 1, 'PRIVATE-NOTE'),
                (3, 'run', 'not-json', '{}', '', '', 2, 'PRIVATE-NOTE'),
                (4, '', '{}', '{}', '', '', 2, 'PRIVATE-NOTE'),
            ])

    def cli(self, *args):
        return subprocess.run([sys.executable, str(ROOT / 'vocabtool.py'), *map(str, args)], capture_output=True, text=True)

    def test_missing_database_does_not_create_file(self):
        missing = self.work / 'missing.db'
        result = self.cli('audit', '--db', missing)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(missing.exists())

    def test_wrong_schema_is_rejected(self):
        wrong = self.work / 'wrong.db'
        with sqlite3.connect(wrong) as con:
            con.execute('CREATE TABLE other (id INTEGER)')
        result = self.cli('audit', '--db', wrong)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('vocabulary TABLE', result.stderr)

    def test_view_is_not_executed_as_vocabulary(self):
        wrong = self.work / 'view.db'
        with sqlite3.connect(wrong) as con:
            con.execute('CREATE VIEW vocabulary AS SELECT 1 AS id, "bank" AS question')
        result = self.cli('audit', '--db', wrong)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('not a view', result.stderr)

    def test_index_output_never_overwrites_existing_file(self):
        xml = self.work / 'input.xml'
        xml.write_text('<LexicalResource/>')
        output = self.work / 'existing.sqlite'
        output.write_bytes(b'DO-NOT-OVERWRITE')
        result = self.cli('index', '--xml', xml, '--out', output)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output.read_bytes(), b'DO-NOT-OVERWRITE')

    def test_audit_counts_without_modifying_or_exporting_personal_data(self):
        before = hashlib.sha256(self.db.read_bytes()).hexdigest()
        result = self.cli('audit', '--db', self.db)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['rows'], 4)
        self.assertEqual(report['nonempty_headword_rows'], 3)
        self.assertEqual(report['unique_normalized_headwords'], 2)
        self.assertEqual(report['duplicate_normalized_headword_rows'], 1)
        self.assertEqual(report['invalid_json']['answers'], 1)
        self.assertNotIn('PRIVATE-NOTE', result.stdout)
        self.assertEqual(before, hashlib.sha256(self.db.read_bytes()).hexdigest())
        self.assertFalse(report['validated_vocabulary_size'])

    def test_wordnet_candidates_never_claim_automatic_sense_match(self):
        xml = self.work / 'synthetic-wordnet.xml'
        xml.write_text('''<LexicalResource><Lexicon id="synthetic" version="test" license="test-only">
          <LexicalEntry id="bank-n"><Lemma writtenForm="bank" partOfSpeech="n"/>
            <Sense id="bank-finance" synset="finance-n"/><Sense id="bank-river" synset="river-n"/>
          </LexicalEntry>
          <LexicalEntry id="run-v"><Lemma writtenForm="run" partOfSpeech="v"/>
            <Sense id="run-motion" synset="motion-v"/>
          </LexicalEntry>
        </Lexicon></LexicalResource>''')
        index = self.work / 'index.sqlite'
        result = self.cli('index', '--xml', xml, '--out', index)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['sense_links'], 3)
        out = self.work / 'private-mapping.jsonl'
        result = self.cli('map', '--db', self.db, '--index', index, '--out', out)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['rows'], 4)
        self.assertEqual(report['rows_with_candidates'], 3)
        self.assertEqual(report.get('output_sha256'), hashlib.sha256(out.read_bytes()).hexdigest())
        self.assertEqual(report['index_sha256'], hashlib.sha256(index.read_bytes()).hexdigest())
        mapped = [json.loads(line) for line in out.read_text().splitlines()]
        self.assertEqual(len(mapped[0]['candidates']), 2)
        self.assertEqual(mapped[1]['match_method'], 'normalized_headword')
        self.assertTrue(mapped[2]['requires_sense_review'])
        self.assertIsNone(mapped[2]['selected_synset_id'])
        self.assertEqual(mapped[3]['match_method'], 'blank_or_nontext')
        self.assertNotIn('PRIVATE-NOTE', out.read_text())

    def test_baseline_cli_returns_design_score_not_latent_vocabulary(self):
        document = {
            'frame': {'easy': ['a', 'b', 'c', 'd'], 'hard': ['e', 'f', 'g', 'h']},
            'screening': {'easy': ['a'], 'hard': ['e']},
            'focused': {'easy': ['b', 'c'], 'hard': ['f', 'g']},
            'responses': {'a': 'correct', 'b': 'correct', 'c': 'incorrect', 'e': 'incorrect', 'f': 'dont_know', 'g': 'correct'}
        }
        payload = self.work / 'synthetic-score.json'
        payload.write_text(json.dumps(document))
        result = subprocess.run([sys.executable, str(ROOT / 'baseline.py'), str(payload)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['status'], 'scored')
        self.assertEqual(report['estimate'], 4.0)
        self.assertEqual(report['frame_size'], 8)
        self.assertEqual(report['interval']['bounds'], [3, 5])
        self.assertEqual(report['estimand'], 'finite_frame_correct_response_total')
        self.assertFalse(report['public_vocabulary_claim_allowed'])


if __name__ == '__main__':
    unittest.main()
