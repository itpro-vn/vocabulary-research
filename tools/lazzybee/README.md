# Offline LazzyBee research tools

These are executable **research references**, not a production assessment service. They support the real snapshot audit in [../../docs/data/LAZZYBEE_SNAPSHOT_AUDIT.md](../../docs/data/LAZZYBEE_SNAPSHOT_AUDIT.md). No source dictionary or user data is bundled.

## Commands

`vocabtool.py` and `profile_snapshot.py` use only the Python standard library. Numerical baseline tests require the versions in `requirements.txt`; Python 3.11 was used for verification.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r tools/lazzybee/requirements.txt
.venv/bin/python -m unittest discover -s tools/lazzybee/tests -v

.venv/bin/python tools/lazzybee/vocabtool.py audit --db /private/english_optimized.db
.venv/bin/python tools/lazzybee/profile_snapshot.py /private/english_optimized.db
.venv/bin/python tools/lazzybee/vocabtool.py index --xml /private/english-wordnet-2025.xml.gz --out /private/wordnet.sqlite
.venv/bin/python tools/lazzybee/vocabtool.py map --db /private/english_optimized.db --index /private/wordnet.sqlite --out /private/candidates.jsonl
```

Official pinned input: https://github.com/globalwordnet/english-wordnet/releases/download/2025-edition/english-wordnet-2025.xml.gz

Expected resource SHA-256: `9ca6d1dcb75f822fdd66617f7d9da48142ace38dd544d6ad5e2feca1674ad3fe`.

## Interpretation and safety

- Read consistent offline SQLite backups, not production/live WAL databases. Content columns are allowlisted; no system values or learning-progress values are exported.
- Audit and profile output is aggregate-only. Record-level candidate JSONL is **private** and created with mode 0600. Do not commit it. Existing output files are not overwritten.
- A failed process may leave partial output. Consume a mapping only after exit code 0, a completed summary, matching output hash and matching record count.
- Exact and normalized matching generate candidates, not reviewed senses. One candidate still requires review; no matches never means an invalid word. Optional explicit POS filtering does not infer POS from dictionary HTML.
- The profiler's POS/CEFR extraction and exact target-mention check are limited heuristics. They do not prove the target sense, difficulty, semantic quality, absence of all answer cues, or content ownership.
- HTML text stripping is for profiling only, **not** a web sanitizer. Do not render imported raw HTML in an assessment frontend without a separately reviewed sanitizer.
- Index only trusted WN-LMF XML/XML.GZ resources. The tool is not an arbitrary-upload XML security boundary.
- Source IDs require a reviewed cross-version identity policy. Snapshot hash plus row ordinal is not a durable business identity.

## Baseline

`baseline.py` exposes `sample_frame(frame, quotas, seed, excluded=None)` and `score(document, alpha=0.05)`. Run `python3 tools/lazzybee/baseline.py TRUSTED_DESIGN.json` for a complete design payload; synthetic examples are in the tests.

The server must own correct/incorrect labels, persist frozen selections/quotas/seeds before focused responses, and enforce session authorization and release lineage. The CLI does not provide that server, choose optimized quotas, or verify that a submitted design genuinely came from the sampler.

Residual HT estimates a **finite-frame correct-response total** under SRSWOR and complete fixed potential outcomes. It does not directly estimate latent word knowledge. `dont_know` is non-correct for this estimand; timeout, technical failure or absent response withholds the result. Zero sampled variance is not proof of zero measurement error. Intervals are conservative design confidence intervals, not Bayesian credible intervals. Public vocabulary claims are disabled in all outputs.

The reference assumes coverage of the assessed frame by valid item units. It does not implement estimation across a separately probability-sampled item-bank stage. Restrict a pilot's estimand to its reviewed frame until that wider design is established and validated.

## Evidence separation

- Unit/CLI tests: synthetic fixtures only.
- Snapshot audit JSON: actual aggregate measurements from the owner-supplied database.
- WordNet: actual pinned official resource.
- Human calibration/validation: **not performed**.

Database contents, full vocabulary, per-record review decisions and live answer keys remain outside this repository. Source dictionary rights and WordNet attribution requirements must be handled separately.
