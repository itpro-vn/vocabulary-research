"""Offline, read-only LazzyBee vocabulary audit. Research reference, not production."""
import argparse
from collections import Counter
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import unicodedata

CONTENT_FIELDS = ('id', 'question', 'answers', 'meaning', 'l_en', 'l_vn', 'level', 'packages', 'pos')


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def normalize(text):
    return ' '.join(unicodedata.normalize('NFC', text).casefold().split())


@contextmanager
def readonly(path):
    path = Path(path).resolve(strict=True)
    if Path(str(path) + '-wal').exists() and Path(str(path) + '-wal').stat().st_size:
        raise ValueError('Use a consistent offline SQLite backup, not a live WAL database.')
    con = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)
    try:
        con.execute('PRAGMA query_only=ON')
        con.execute('PRAGMA trusted_schema=OFF')
        con.row_factory = sqlite3.Row
        yield con
    finally:
        con.close()


def read_vocabulary(path):
    before = digest(path)
    with readonly(path) as con:
        table = con.execute("SELECT type FROM sqlite_master WHERE name='vocabulary'").fetchone()
        if not table or table['type'] != 'table':
            raise ValueError('Expected a vocabulary TABLE, not a view.')
        columns = {r['name'] for r in con.execute('PRAGMA table_info(vocabulary)')}
        if not {'id', 'question'}.issubset(columns):
            raise ValueError('vocabulary must contain id and question columns.')
        selected = [c for c in CONTENT_FIELDS if c in columns]
        rows = [dict(r) for r in con.execute('SELECT ' + ','.join('"' + c + '"' for c in selected) + ' FROM vocabulary')]
    if before != digest(path):
        raise ValueError('Input changed during reading; provide an offline backup.')
    return rows, columns, before


def audit(path):
    rows, columns, sha = read_vocabulary(path)
    words = [normalize(r['question']) for r in rows if isinstance(r['question'], str) and normalize(r['question'])]
    invalid, missing = {}, {}
    for field in ('answers', 'meaning'):
        invalid[field] = 0
        missing[field] = 0
        for row in rows:
            raw = row.get(field)
            if raw is None or raw == '':
                missing[field] += 1
                continue
            try:
                if not isinstance(json.loads(raw), dict):
                    invalid[field] += 1
            except (ValueError, TypeError):
                invalid[field] += 1
    ids = [str(r['id']) for r in rows if r['id'] is not None]
    return {
        'schema_version': 'audit-v0.1', 'source_sha256': sha,
        'rows': len(rows), 'nonempty_headword_rows': len(words),
        'unique_normalized_headwords': len(set(words)),
        'duplicate_normalized_headword_rows': len(words) - len(set(words)),
        'blank_or_nontext_headwords': len(rows) - len(words),
        'duplicate_id_rows': len(ids) - len(set(ids)),
        'null_id_rows': len(rows) - len(ids),
        'invalid_json': invalid, 'missing_json': missing,
        'available_content_columns': sorted(set(CONTENT_FIELDS) & columns),
        'validated_vocabulary_size': False,
        'interpretation': 'Record/headword counts only; not lemma-POS/sense counts or psychometric validation.',
    }


def build_index(xml_path, output):
    """Read trusted WN-LMF XML/XML.GZ; do not process arbitrary untrusted XML."""
    import gzip
    import xml.etree.ElementTree as ET
    source_sha = digest(xml_path)
    Path(output).touch(exist_ok=False)
    con = sqlite3.connect(output)
    metadata = {'source_sha256': source_sha, 'index_schema': 'wn-candidates-v0.1'}
    try:
        con.execute('CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
        con.execute('CREATE TABLE candidates (lemma TEXT, normalized TEXT, pos TEXT, lexical_entry_id TEXT, sense_id TEXT, synset_id TEXT)')
        count = 0
        opener = gzip.open if str(xml_path).endswith('.gz') else open
        with opener(xml_path, 'rb') as stream:
            for event, element in ET.iterparse(stream, events=('start', 'end')):
                tag = element.tag.rsplit('}', 1)[-1]
                if event == 'start' and tag == 'Lexicon':
                    if 'lexicon_id' in metadata:
                        raise ValueError('This index supports exactly one Lexicon per release.')
                    metadata.update(lexicon_id=element.get('id'), version=element.get('version'), license=element.get('license'))
                if event == 'end' and tag == 'LexicalEntry':
                    lemma = next((x for x in element if x.tag.rsplit('}', 1)[-1] == 'Lemma'), None)
                    if lemma is not None:
                        text = lemma.get('writtenForm', '')
                        pos = lemma.get('partOfSpeech', '')
                        for sense in element:
                            if sense.tag.rsplit('}', 1)[-1] == 'Sense':
                                con.execute('INSERT INTO candidates VALUES (?,?,?,?,?,?)', (text, normalize(text), pos, element.get('id'), sense.get('id'), sense.get('synset')))
                                count += 1
                    element.clear()
                elif event == 'end' and tag == 'Synset':
                    element.clear()
        if not count or not metadata.get('lexicon_id'):
            raise ValueError('No usable WordNet sense links found.')
        if digest(xml_path) != source_sha:
            raise ValueError('WordNet source changed while indexing.')
        con.execute('CREATE INDEX lemma_idx ON candidates(lemma)')
        con.execute('CREATE INDEX normalized_idx ON candidates(normalized)')
        metadata['sense_links'] = count
        metadata['complete'] = True
        con.executemany('INSERT INTO metadata VALUES (?,?)', [(k, json.dumps(v)) for k, v in metadata.items()])
        con.commit()
    finally:
        con.close()
    return metadata


def map_candidates(db_path, index_path, output):
    import os
    rows, _, source_sha = read_vocabulary(db_path)
    counts = Counter()
    pos_alias = {'n': 'n', 'noun': 'n', 'v': 'v', 'verb': 'v', 'a': 'a', 's': 'a', 'adj': 'a', 'adjective': 'a', 'r': 'r', 'adv': 'r', 'adverb': 'r'}
    with readonly(index_path) as index:
        metadata = {r['key']: json.loads(r['value']) for r in index.execute('SELECT key,value FROM metadata')}
        if metadata.get('index_schema') != 'wn-candidates-v0.1' or not metadata.get('complete'):
            raise ValueError('Incomplete or unsupported WordNet index.')
        fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            for ordinal, row in enumerate(rows):
                word = row['question']
                candidates = []
                method = 'blank_or_nontext'
                raw_pos = row.get('pos')
                canonical_pos = pos_alias.get(str(raw_pos).strip().casefold()) if raw_pos else None
                if isinstance(word, str) and normalize(word):
                    candidates = [dict(r) for r in index.execute('SELECT lemma,pos,lexical_entry_id,sense_id,synset_id FROM candidates WHERE lemma=? ORDER BY sense_id', (word,))]
                    method = 'exact_headword'
                    if not candidates:
                        candidates = [dict(r) for r in index.execute('SELECT lemma,pos,lexical_entry_id,sense_id,synset_id FROM candidates WHERE normalized=? ORDER BY sense_id', (normalize(word),))]
                        method = 'normalized_headword' if candidates else 'unmatched'
                    if canonical_pos:
                        candidates = [c for c in candidates if pos_alias.get(c['pos']) == canonical_pos]
                        method = method + '_pos' if candidates else 'pos_conflict_or_unmatched'
                counts[method] += 1
                if candidates:
                    counts['rows_with_candidates'] += 1
                record = {
                    'source_key': source_sha + ':' + str(ordinal), 'source_id': row['id'],
                    'headword': word, 'source_pos': raw_pos,
                    'pos_status': 'recognized' if canonical_pos else ('unknown_review' if raw_pos else 'missing'),
                    'match_method': method, 'candidates': candidates,
                    'selected_synset_id': None, 'requires_sense_review': True,
                }
                stream.write(json.dumps(record, ensure_ascii=False) + '\n')
    return {'rows': len(rows), 'rows_with_candidates': counts.pop('rows_with_candidates', 0),
            'by_match_method': dict(counts), 'source_sha256': source_sha,
            'wordnet': metadata, 'index_sha256': digest(index_path),
            'output_sha256': digest(output), 'automatic_sense_matches': 0,
            'interpretation': 'Row-level lexical candidate coverage only; no confirmed sense mapping.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    cmd = subs.add_parser('audit')
    cmd.add_argument('--db', required=True, type=Path)
    cmd = subs.add_parser('index')
    cmd.add_argument('--xml', required=True, type=Path)
    cmd.add_argument('--out', required=True, type=Path)
    cmd = subs.add_parser('map')
    cmd.add_argument('--db', required=True, type=Path)
    cmd.add_argument('--index', required=True, type=Path)
    cmd.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'audit':
            result = audit(args.db)
        elif args.command == 'index':
            result = build_index(args.xml, args.out)
        else:
            result = map_candidates(args.db, args.index, args.out)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, sqlite3.Error) as exc:
        print(json.dumps({'status': 'error', 'message': str(exc)}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
