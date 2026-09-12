"""Aggregate-only content profiler. HTML clues are not reviewed POS/CEFR labels."""
from collections import Counter
from html import unescape
import json
from pathlib import Path
import re
import sqlite3
import sys

from vocabtool import read_vocabulary, readonly

POS_LABELS = {
    'danh từ': 'n', 'danh từ số nhiều': 'n', 'danh từ, số nhiều': 'n',
    'danh từ, (thường) số nhiều': 'n',
    'ngoại động từ': 'v', 'nội động từ': 'v', 'động từ': 'v',
    'tính từ': 'a', 'phó từ': 'r', 'trạng từ': 'r',
    'giới từ': 'adp', 'liên từ': 'conj', 'đại từ': 'pron',
    'thán từ': 'intj', 'số từ': 'num', 'trợ động từ': 'aux',
}


def visible(raw):
    if not isinstance(raw, str):
        return ''
    # Text-presence heuristic only; NOT an HTML sanitizer for browser rendering.
    return ' '.join(unescape(re.sub(r'<[^>]*>', ' ', raw)).split())


def object_or_empty(raw):
    try:
        value = json.loads(raw)
        return value if isinstance(value, dict) else {}
    except (ValueError, TypeError):
        return {}


def profile(path):
    rows, columns, sha = read_vocabulary(path)
    answer_fields = {k: Counter() for k in ('explain', 'example', 'pronounce')}
    vietnamese = Counter()
    pos_counts, pos_row_sizes = Counter(), Counter()
    cefr_counts = Counter()
    cefr_any = 0
    target_mentions = Counter({'explain': 0, 'example': 0})
    for row in rows:
        answers = object_or_empty(row.get('answers'))
        target = visible(row.get('question')).casefold()
        if target:
            pattern = re.compile(r'(?<!\w)' + re.escape(target) + r'(?!\w)')
            for field in target_mentions:
                target_mentions[field] += bool(pattern.search(visible(answers.get(field)).casefold()))
        for key, count in answer_fields.items():
            count['present'] += key in answers
            count['string_values'] += isinstance(answers.get(key), str)
            count['nonempty_visible_text'] += bool(visible(answers.get(key)))
        meaning = object_or_empty(row.get('meaning'))
        vietnamese['vn_key_present'] += 'vn' in meaning
        vietnamese['nonempty_visible_text'] += bool(visible(meaning.get('vn')))
        vn = row.get('l_vn') or ''
        labels = re.findall(r'<span\b[^>]*class=[\"\x27]tl[\"\x27][^>]*>(.*?)</span>', vn, flags=re.I | re.S)
        labels += re.findall(r'<strong\b[^>]*>(.*?)</strong>', vn, flags=re.I | re.S)
        hints = {POS_LABELS[label] for raw in labels if (label := visible(raw).casefold()) in POS_LABELS}
        pos_counts.update(hints)
        pos_row_sizes['none' if not hints else 'single' if len(hints) == 1 else 'multiple'] += 1
        classes = re.findall(r'class=[\"\x27]([^\"\x27]+)', row.get('l_en') or '')
        hints = {level for level in ('A1', 'A2', 'B1', 'B2', 'C1', 'C2')
                 if any('epp-xref' in cls.split() and level in cls.split() for cls in classes)}
        cefr_counts.update(hints)
        cefr_any += bool(hints)
    with readonly(path) as con:
        schema = [dict(r) for r in con.execute('PRAGMA table_info(vocabulary)')]
        integrity = [r[0] for r in con.execute('PRAGMA quick_check')]
        tables = {}
        for name in ('system', 'vocabulary', 'packageinfo', 'packagestatus'):
            exists = con.execute('SELECT 1 FROM sqlite_master WHERE type=? AND name=?', ('table', name)).fetchone()
            if exists:
                tables[name] = con.execute('SELECT COUNT(*) FROM "' + name + '"').fetchone()[0]
    return {
        'profile_schema': 'lazzybee-content-profile-v0.1', 'source_sha256': sha,
        'bytes': Path(path).stat().st_size, 'rows': len(rows), 'sqlite_quick_check': integrity,
        'table_row_counts': tables, 'vocabulary_columns': schema,
        'level_counts': dict(sorted(Counter(str(r.get('level')) for r in rows).items())),
        'target_mentions': dict(target_mentions),
        'target_mention_method': 'casefolded exact headword with Unicode word boundaries after HTML text stripping; not full cue detection',
        'answer_fields': {k: dict(v) for k, v in answer_fields.items()},
        'meaning': dict(vietnamese),
        'dictionary_fields': {field: {'nonempty_raw': sum(bool(r.get(field)) for r in rows),
                                       'nonempty_visible_text': sum(bool(visible(r.get(field))) for r in rows)}
                              for field in ('l_en', 'l_vn')},
        'pos_hints': {'source': 'whitelisted l_vn span.tl/strong labels; dictionary-wide clues',
                      'rows_with_single_hint': pos_row_sizes['single'],
                      'rows_with_multiple_hints': pos_row_sizes['multiple'],
                      'rows_without_hint': pos_row_sizes['none'], 'per_pos_rows': dict(sorted(pos_counts.items())),
                      'reviewed_target_pos': False},
        'cefr_hints': {'source': 'l_en epp-xref class labels', 'rows_with_any_hint': cefr_any,
                       'per_label_rows': dict(sorted(cefr_counts.items())), 'validated_person_or_item_level': False},
        'notes': ['Nonempty fields do not establish correctness or ownership.',
                  'POS/CEFR row counts can overlap; dictionary hints may describe other senses or phrases.',
                  'No source headwords, definitions, user notes, progress values or system values exported.'],
    }


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('Usage: python profile_snapshot.py PRIVATE_OFFLINE.db')
        print(json.dumps(profile(Path(sys.argv[1])), ensure_ascii=False, indent=2))
    except (ValueError, OSError, sqlite3.Error) as exc:
        print(json.dumps({'status': 'error', 'message': str(exc)}), file=sys.stderr)
        raise SystemExit(2)
