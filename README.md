# Vocabulary Research

This repository contains the research archive and implementation blueprint for a vocabulary-size assessment.

## Start here

- [Roadmap and architecture](ROADMAP_ARCHITECTURE.md)
- [Harmonized P0 suite](docs/specs/README.md) — all seven measurement/product specifications updated to revision 2.0.0
- [New research incorporation](docs/specs/RESEARCH_INCORPORATION.md) — decisions for files 66–75 / iterations 63–72
- [Current server-dictionary status](docs/data/SERVER_DICTIONARY_STATUS.md) — full export supplied; overall verifier gate still unresolved
- [SQLite data standardization specification](docs/specs/SQLITE_DATA_STANDARDIZATION_SPEC.md) — complete data contract and proposed SQL schema; migration deferred
- [Actual LazzyBee snapshot audit](docs/data/LAZZYBEE_SNAPSHOT_AUDIT.md)
- [Raw research archive, complete index, and history](raw/README.md)
- [Offline audit and validation tools](tools/lazzybee/README.md)

`raw/` contains archived research documents only; it is not a raw lexical-data directory.

## Evidence boundary

The earlier learning snapshot contains **3,885 source headwords**; its audit found **3,848 WordNet lexical candidates**, not reviewed semantic matches. The owner has now confirmed a separate full server dictionary export, with **42,497 records** in JSON and SQLite. A local full-verifier rerun reports matching IDs and zero mapped-field mismatches, but its overall verification status failed and remains an open gate. The [standardization specification](docs/specs/SQLITE_DATA_STANDARDIZATION_SPEC.md) records that distinction and defers migration. **Oxford origin remains unverified.** Dictionary files and record-level evidence stay in Git-ignored private local storage, not this public repository.

These facts do not constitute semantic review, calibrated item parameters, a representative item bank, or production sign-off. See the [current data status](docs/data/SERVER_DICTIONARY_STATUS.md) for the full-export boundary and the [learning snapshot audit](docs/data/LAZZYBEE_SNAPSHOT_AUDIT.md) for earlier snapshot-specific evidence.

## Offline checks

Specification/schema checks are separate from the existing numerical/data-tool tests. See [test scope and setup](tools/specs/README.md). With the listed dependencies installed:

```bash
python3 tools/specs/verify_contracts.py
python3 -m unittest discover -s tools/lazzybee/tests -v
```
