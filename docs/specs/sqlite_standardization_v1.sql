-- Proposed schema, not a migration executed on owner data.
-- Apply only to a NEW staging database after the specification gates pass.
-- Requires SQLite >= 3.37 with working JSON functions.
PRAGMA foreign_keys = ON;
PRAGMA user_version = 1;

CREATE TABLE source_manifest (
    snapshot_id TEXT PRIMARY KEY NOT NULL,
    json_sha256 TEXT NOT NULL CHECK(length(json_sha256) = 64 AND json_sha256 NOT GLOB '*[^0-9a-f]*'),
    sqlite_sha256 TEXT NOT NULL CHECK(length(sqlite_sha256) = 64 AND sqlite_sha256 NOT GLOB '*[^0-9a-f]*'),
    source_record_count INTEGER NOT NULL CHECK(source_record_count >= 0),
    mapping_version TEXT NOT NULL,
    normalization_version TEXT NOT NULL,
    unicode_version TEXT NOT NULL,
    builder_version TEXT NOT NULL,
    source_provenance TEXT NOT NULL CHECK(source_provenance IN ('owner_confirmed_server_export', 'other_declared_export')),
    received_at_utc TEXT NOT NULL,
    metadata_json TEXT NOT NULL CHECK(json_valid(metadata_json) AND json_type(metadata_json) = 'object')
) STRICT;

CREATE TABLE source_record (
    source_id TEXT PRIMARY KEY NOT NULL CHECK(length(source_id) > 0),
    snapshot_id TEXT NOT NULL REFERENCES source_manifest(snapshot_id),
    source_ordinal INTEGER NOT NULL CHECK(source_ordinal >= 0),
    record_json TEXT NOT NULL CHECK(json_valid(record_json) AND json_type(record_json) = 'object'),
    record_sha256 TEXT NOT NULL CHECK(length(record_sha256) = 64 AND record_sha256 NOT GLOB '*[^0-9a-f]*'),
    UNIQUE(snapshot_id, source_ordinal),
    CHECK(json_type(record_json, '$._id') IS 'text'),
    CHECK(json_extract(record_json, '$._id') = source_id COLLATE BINARY)
) STRICT;

CREATE TABLE dictionary_entry (
    _id TEXT PRIMARY KEY NOT NULL REFERENCES source_record(source_id),
    id INTEGER,
    question TEXT NOT NULL CHECK(length(question) > 0),
    answers_pronounce TEXT,
    answers_explain TEXT,
    answers_example TEXT,
    meaning_vn TEXT,
    related TEXT,
    queue INTEGER,
    level INTEGER,
    due INTEGER,
    rev_count INTEGER,
    user_note TEXT,
    last_ivl INTEGER,
    e_factor INTEGER,
    l_vn TEXT,
    l_en TEXT,
    l_en_lingoe_1 TEXT,
    l_vn_lingoe_1 TEXT,
    db_version INTEGER,
    updated_at TEXT,
    created_at TEXT,
    popularity INTEGER,
    new_level INTEGER,
    packages TEXT CHECK(packages IS NULL OR CASE WHEN json_valid(packages) THEN json_type(packages) = 'array' ELSE 0 END),
    en_order INTEGER,
    vn_order INTEGER,
    question_key TEXT NOT NULL CHECK(length(question_key) > 0),
    updated_at_utc TEXT,
    created_at_utc TEXT,
    updated_at_parse_status TEXT NOT NULL CHECK(updated_at_parse_status IN ('missing', 'null', 'parsed', 'unparsed')),
    created_at_parse_status TEXT NOT NULL CHECK(created_at_parse_status IN ('missing', 'null', 'parsed', 'unparsed')),
    CHECK((updated_at_parse_status = 'parsed') = (updated_at_utc IS NOT NULL)),
    CHECK((created_at_parse_status = 'parsed') = (created_at_utc IS NOT NULL))
) STRICT;

-- Normalization collisions remain separate records: never make this UNIQUE.
CREATE INDEX idx_entry_question_key ON dictionary_entry(question_key, _id);
CREATE INDEX idx_entry_question ON dictionary_entry(question);
CREATE INDEX idx_entry_legacy_id ON dictionary_entry(id);
CREATE INDEX idx_entry_level ON dictionary_entry(level);

CREATE TABLE data_issue (
    issue_id TEXT PRIMARY KEY NOT NULL,
    source_id TEXT REFERENCES source_record(source_id),
    rule_version TEXT NOT NULL,
    issue_code TEXT NOT NULL,
    severity TEXT NOT NULL CHECK(severity IN ('blocking', 'review', 'info')),
    detail_json TEXT NOT NULL CHECK(json_valid(detail_json) AND json_type(detail_json) = 'object')
) STRICT;
CREATE INDEX idx_issue_entry ON data_issue(source_id, severity);

CREATE VIEW v_dictionary_lookup AS
SELECT _id AS source_id, question AS headword, question_key,
       answers_pronounce AS pronunciation_raw,
       answers_explain AS explanation_raw,
       answers_example AS example_raw,
       meaning_vn AS meaning_vn_raw,
       l_en, l_vn, level AS legacy_level, new_level AS legacy_new_level
FROM dictionary_entry;
