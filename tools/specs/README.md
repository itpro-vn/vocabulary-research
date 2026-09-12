# Specification contract checks

These checks use only public schema/documents and synthetic request/result fixtures. They do not read the private dictionary, implement the assessment API or validate human vocabulary measurement.

From the repository root, in a suitable virtual environment:

```bash
python3 -m pip install -r tools/specs/requirements.txt
python3 tools/specs/verify_contracts.py
python3 -m unittest discover -s tools/lazzybee/tests -v
```

Checks cover JSON Schema meta-validation; positive/negative baseline result and dont_know fixtures; local OpenAPI/schema references and six operation shapes; shared profile/data/version tokens across seven specs; preservation hashes for prior specs/roadmap; the complete 75-file research inventory; and active local Markdown link target existence.

The eight byte-preserved historical specs/roadmap under `raw/specs-before-harmonization/` are excluded from link resolution because their relative links belong to the original file locations. Their byte hashes are checked instead. Link fragments/external URLs, full OpenAPI meta-schema conformance, runtime business invariants, numerical interval coverage, API authorization/concurrency and pilot validity require additional tests; a PASS here does not certify them.

See the [active suite](../../docs/specs/README.md) and [research incorporation matrix](../../docs/specs/RESEARCH_INCORPORATION.md).
