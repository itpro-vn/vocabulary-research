# Vocabulary Research

This repository contains the research archive and implementation blueprint for a vocabulary-size assessment.

## Start here

- [Roadmap and architecture](ROADMAP_ARCHITECTURE.md)
- [P0 specifications](docs/specs/) — seven design and implementation specifications
- [Actual LazzyBee snapshot audit](docs/data/LAZZYBEE_SNAPSHOT_AUDIT.md)
- [Raw research archive, complete index, and history](raw/README.md)
- [Offline audit and validation tools](tools/lazzybee/README.md)

`raw/` contains archived research documents only; it is not a raw lexical-data directory.

## Evidence boundary

The supplied snapshot contains **3,885 source headwords**. The audit found **3,848 lexical candidates** in pinned Open English WordNet, but those candidates are **not reviewed semantic matches**. The approximately **44,000-item master scope** is unverified, and the **Oxford origin** is unverified. The public repository excludes the database, the full word inventory, and record-level mappings.

These facts do not constitute semantic review, calibrated item parameters, a representative item bank, or production sign-off. See the [snapshot audit](docs/data/LAZZYBEE_SNAPSHOT_AUDIT.md) for the evidence and limitations.

## Offline checks

Run the tools' test suite from the repository root:

```bash
python3 -m unittest discover -s tools/lazzybee/tests -v
```
