"""Aggregate profiling test; fixture content is synthetic."""
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ProfileTests(unittest.TestCase):
    def test_profiles_json_and_html_hints_without_exporting_text(self):
        with tempfile.TemporaryDirectory() as temp:
            db = Path(temp) / 'synthetic.db'
            with sqlite3.connect(db) as con:
                con.execute('CREATE TABLE vocabulary (id INTEGER, question TEXT, answers TEXT, meaning TEXT, l_en TEXT, l_vn TEXT, level INTEGER)')
                con.executemany('INSERT INTO vocabulary VALUES (?,?,?,?,?,?,?)', [
                    (1, 'SYNTHETIC-PRIVATE-HEADWORD', '{"explain":"<p>SYNTHETIC-PRIVATE-HEADWORD explanation</p>","example":"Example","pronounce":"X"}', '{"vn":"Translation"}', '<span class="epp-xref B1">B1</span>', '<span class="tl">danh từ</span>', 1),
                    (2, 'SECOND-SYNTHETIC-HEADWORD', 'invalid', '{}', '', '', 2),
                ])
            p = subprocess.run([sys.executable, str(ROOT / 'profile_snapshot.py'), str(db)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            report = json.loads(p.stdout)
            self.assertEqual(report['rows'], 2)
            self.assertEqual(report.get('target_mentions', {}).get('explain'), 1)
            self.assertEqual(report['answer_fields']['explain']['nonempty_visible_text'], 1)
            self.assertEqual(report['pos_hints']['rows_with_single_hint'], 1)
            self.assertEqual(report['pos_hints']['rows_without_hint'], 1)
            self.assertEqual(report['cefr_hints']['rows_with_any_hint'], 1)
            self.assertEqual(report['cefr_hints']['per_label_rows']['B1'], 1)
            self.assertNotIn('SYNTHETIC-PRIVATE-HEADWORD', p.stdout)
            self.assertFalse(report['pos_hints']['reviewed_target_pos'])


if __name__ == '__main__':
    unittest.main()
