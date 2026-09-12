# Vocabulary Research — architecture and implementation roadmap

**Version:** 2.1.0
**Status:** harmonized implementation target; production and empirical claims not approved. Historical Advisor reviews apply only to their [archived revision](raw/specs-before-harmonization/ROADMAP_ARCHITECTURE.md), not automatically to this revision.

## 1. Current evidence

The owner confirms a full server dictionary export: 42,497 records in JSON/SQLite, separate from the earlier 3,885-record learning snapshot. Both remain private local artifacts. The full verifier reports matched records/IDs and zero mapped-field mismatches but **overall verification failure**; the exact failed gate remains unresolved. No source migration, reviewed full measurement frame or human calibration is completed. [Source evidence](docs/data/SERVER_DICTIONARY_STATUS.md).

Research files 01–75 are retained in [raw/](raw/README.md), including the newly reviewed files 66–75/iterations 63–72. The [incorporation matrix](docs/specs/RESEARCH_INCORPORATION.md) distinguishes accepted clarification, already-covered controls and deferred models. The vocabulary research cron and subagents remain paused.

## 2. Architecture decisions

- Use LazzyBee owner data first. Keep original export and flattened SQLite unchanged; create a separately versioned standardized private artifact later.
- Separate source row, reviewed lemma/POS-target-sense unit, supported sampling frame and approved item version. Do not use row count as vocabulary N.
- Default `baseline-design-v0.1` estimates `finite_frame_correct_response_total`, using disjoint screening plus probability-sampled remainder, not latent known-word count.
- Baseline remains diagnostic-only: public vocabulary claim false, theta/vocabulary_count/CEFR null. Empirical recognition claims require separate evidence/profile approval.
- Preserve single-key MCQ, explicit dont_know, no missing-as-wrong, no adaptive early stopping and no automatic guessing/isotonic/RT correction.
- Prefer explicit artifact/response/claim contracts and a verified baseline before calibrated CAT or other advanced models. Papers/vendor claims do not provide local calibration.

## 3. Modules and boundaries

1. **Private data onboarding:** source fidelity, standardized lookup, hashes/versions, exception inventory; no production DB replacement.
2. **Unit/content pipeline:** human sense/POS/key review, cue/distractor/accessibility checks, supported frame and form manifests.
3. **Sampling/session service:** frozen plans/probabilities, secure assignments, idempotent submission and consent-aware research slots.
4. **Scoring/claims:** deterministic response reduction/residual intervals, explicit no-score behavior, restricted diagnostic results and later separately validated models.
5. **Governance/validation:** dependency closure, privacy/erasure, exposure/integrity review, simulation/pilot/holdout and rollback.

Data and item IDs are not public enumeration APIs. Keys, raw source content, seeds and detector internals remain restricted. Public documentation contains schema, tests using synthetic values and approved aggregate evidence.

## 4. Six delivery phases

**P0 is a cross-cutting contract designation, not delivery Phase 0.** P0.1–P0.7 define what must be correct across every phase: measurement, sampling, scoring, API, governance, pilot evidence and privacy/accessibility. Writing those contracts does not complete the implementation phases below.

```text
P0 contracts govern every phase
Phase 1: trusted data → Phase 2: reviewed frame and items
→ Phase 3: pilot MVP → Phase 4: empirical validation
→ Phase 5: LazzyBee production → Phase 6: optional optimization
```

Owners below are proposed accountable roles, not claims that people have been assigned. Each phase needs a named owner, approved scope/budget, concrete backlog and evidence-linked acceptance decision before execution. No delivery dates, recruitment counts or performance guarantees are assumed without estimation and study design. A document complete is not a phase complete.

### Phase 1 — Trusted, usable dictionary data

**Purpose:** turn received source files into a reproducible, protected data foundation.

**Entry dependency:** owner-confirmed source files and the existing [SQLite standardization contract](docs/specs/SQLITE_DATA_STANDARDIZATION_SPEC.md); execution remains deferred until requested.

**Accountable owner:** Data Engineering Lead; Data Steward reviews provenance, rights and exceptions.

**Work:**

- Diagnose the exact overall-verifier failure; distinguish data defects from verifier defects and fix narrowly with regression evidence.
- Reconcile the complete JSON/SQLite export, all mapped fields, types, NULL/missing/empty values, date precision and packages semantics.
- Build a new versioned standardized SQLite, leaving original sources unchanged and private.
- Provide reproducible import/read/verification commands, manifest hashes, safe promotion and rollback.
- Compare the learning snapshot under explicit normalization and preserve its unmatched entry for review, without automatic source repair.

**Deliverables:** validated private standardized artifact, source/target manifests, verification report, exception queue and tested read adapter/runbook.

**Exit gate:** all mandatory source/fidelity/integrity/protection checks pass; no blocking mismatch; original hashes unchanged; a previous build can be restored safely. Matching record counters alone do not satisfy the gate.

**Failure/rework:** remain in Phase 1; resolve the source or verifier issue. Do not weaken a check or move to semantic enrichment to hide the failure.

**Specification coverage:** SQLite specification exists; builder/reader implementation and full accepted data run are not completed.

### Phase 2 — Reviewed lexical frame and question bank

**Purpose:** transform dictionary content into defensible measurement assets, not merely searchable rows.

**Entry dependency:** an accepted Phase 1 snapshot for the scope being reviewed. Review-tool design and synthetic prototypes may proceed earlier, but no accepted frame may depend on unaccepted data.

**Accountable owner:** Lexical/Content Lead; Psychometric Lead approves construct, frame and item policy.

**Work:**

- Define and adjudicate lemma, POS, target-sense, variant/MWU and exclusion policies with durable source links.
- Acquire/document permitted frequency evidence and define strata where supported; do not treat stored levels as calibrated difficulty.
- Author and independently review stems, options, a single approved key, language burden, distractors and answer cues.
- Provide authoring/review/adjudication tooling or a controlled equivalent workflow, quarantine and versioned changes.
- Freeze eligible units, supported frame, item versions and form mapping, including transparent exclusions.

**Deliverables:** reviewed unit/sense crosswalk, approved frame/item/form manifests, content rubric, adjudication records and exception inventory.

**Exit gate:** every unit in the declared baseline frame has an approved supported item; no unresolved key ambiguity or silent extrapolation beyond support. Compute N from that frame, not the 42,497 source-record count.

**Failure/rework:** revise/quarantine content or narrow and rename the supported frame. Source fidelity defects return to Phase 1; do not silently fix the source during item review.

**Specification coverage:** P0 Measurement/Governance/Pilot define constraints. A detailed content-production and reviewer-workbench implementation spec/backlog remains to be authored.

**Scope strategy:** start with a smaller fully supported frame if necessary; do not require authoring an item for every dictionary record before a pilot. Findings and score labels must disclose that narrower scope.

### Phase 3 — End-to-end MVP for controlled pilot use

**Purpose:** deliver a working assessment flow and trustworthy research collection, not a production vocabulary-accuracy claim.

**Entry dependency:** a Phase 2 reviewed pilot frame/form; approved core/research data-purpose and consent policy. Service/UI work with synthetic fixtures may run in parallel before real-data gates pass.

**Accountable owner:** Engineering Lead; Product/UX Lead owns the supported user journey and research operators accept collection behavior.

**Work:**

- Implement session APIs, secure presentation, frozen sampling, response reduction and baseline scoring.
- Build the test UI: instructions, accessible choices/dont_know, loading/error states, disconnect/resume and honest completion/no-score views.
- Implement idempotency/concurrency/replay, versioned plans, restricted result access and server-side answer authority.
- Add operator tools for approved content/form selection, incident review and consented research export.
- Exercise the complete flow on supported mobile/web delivery environments, with optional research separate from core outcomes.

**Deliverables:** working staging/pilot service and client, administration workflow, reproducible deployment, end-to-end tests and minimized research event pipeline.

**Exit gate:** a participant can complete or safely discontinue/recover a session; scoring/design and API contracts agree; security/accessibility/concurrency tests pass; actual data can be collected under the approved protocol.

**Failure/rework:** fix service/UI defects within Phase 3; content defects return to Phase 2 and generate new item versions. Do not treat missing responses or incomplete sessions as wrong answers to obtain a score.

**Specification coverage:** API/schema and scoring contracts exist, but a client UX, service deployment and operator-workflow implementation spec/backlog is still required.

**Claim limit:** the baseline remains diagnostic-only. Staging completion and software tests do not authorize a public “words you know” estimate.

### Phase 4 — Human validation and claim approval

**Purpose:** establish what the instrument measures, for whom, over which frame and with what limitations.

**Entry dependency:** a controlled Phase 3 collection system, reviewed items and an approved registered study plan. Cognitive findings may iterate with Phases 2–3; independent validation follows frozen study/holdout rules.

**Accountable owner:** Psychometric/Research Lead; Product Owner accepts only supported interpretations, with Privacy/Accessibility review.

**Work:**

- Run cognitive and operational studies to distinguish meaning recognition from cues, familiarity, guessing and language burden.
- Collect independent validation data against an appropriate criterion whose own error and construct limitations are characterized.
- Measure bias/error, interval coverage/width, missingness, floor/ceiling effects, form equivalence and test–retest/practice effects.
- Evaluate supported population/subgroup, device and accommodation conditions with sufficient evidence and uncertainty reporting.
- If needed, calibrate a separately declared recognition model and evaluate parameter/model uncertainty; never relabel the response-total baseline as latent knowledge.
- Approve or reject each claim/use/population combination and its reporting language, not an unrestricted claim of global validity.

**Deliverables:** registered protocol, protected response dataset manifest, analysis code/environment, independent validation/form/fairness reports and evidence-linked claim decisions.

**Exit gate:** preregistered practical acceptance criteria pass for the proposed use and population. A recognition/vocabulary claim needs its own approved evidence/profile; otherwise retain or narrow diagnostic-only use. Correlation, vendor margins and synthetic tests alone cannot pass this gate.

**Failure/rework:** revise items/frame in Phase 2, delivery in Phase 3 or the statistical interpretation/study; collect new independent evidence as required. Preserve prior versions and do not tune against the final holdout while still calling it independent.

**Specification coverage:** P0 Pilot is the protocol foundation. Study-specific recruitment, budgets, practical margins, analysis plan and execution artifacts must still be specified and approved before collection.

### Phase 5 — LazzyBee integration and production operation

**Purpose:** turn an accepted instrument/use case into a maintainable LazzyBee product rather than a standalone demo.

**Entry dependency:** Phase 3 technical maturity plus Phase 4 authorization for the exact public use/claim. A restricted diagnostic launch must be explicitly approved as such; no presumed recognition/CEFR permission.

**Accountable owner:** Product/Engineering Lead; SRE/Security Lead owns operational readiness, with Data/Psychometric owners for content and validity changes.

**Work:**

- Integrate account/session identity, navigation and appropriate result/history presentation into LazzyBee without replacing its production dictionary implicitly.
- Implement supported languages/devices and UX that explains scope, uncertainty and no-score outcomes. History/growth claims require demonstrated form comparability.
- Establish CI/CD, staging/production separation, secret management, access roles and controlled release/feature flags.
- Define and test monitoring, service objectives under a declared workload, backup/restore, incident response, rollback and support escalation.
- Operate item exposure controls, bank/version releases, parameter/content drift monitoring and authorized data erasure.
- Release gradually with operational and validity stop conditions; prevent mixed-version sessions and unsupported score interpretations.

**Deliverables:** integrated LazzyBee release, operational/security/support runbooks, deployment/rollback pipeline, monitoring and data-retention/incident evidence.

**Exit gate:** end-to-end production-readiness review passes, recovery/rollback/deletion are exercised, named operators are assigned and only Phase 4-authorized claims are visible. Uptime does not substitute for validity.

**Failure/rework:** disable/roll back the affected feature or artifact; route software/UX issues to Phase 3 and content/validity issues to Phases 2/4. Do not serve misleading cached scores to conceal an incident.

**Specification coverage:** this product/operations phase was insufficiently detailed in the earlier A–F roadmap. LazzyBee integration, production/SRE and support/release implementation specs remain to be authored; P0 security/privacy/governance remain binding.

### Phase 6 — Optional optimization and expansion

**Purpose:** improve validated user value only when evidence justifies the additional complexity.

**Entry dependency:** an accepted baseline and stable versioned comparison environment, plus approved experiment scope/data use. Research prototypes may run earlier when separately authorized, but cannot bypass promotion gates.

**Accountable owner:** Product/Psychometric Lead; Engineering/Data/SRE implement and operate approved experiments.

**Work:**

- Evaluate CAT or other selection/stopping profiles to reduce burden without weakening error/coverage/support/fairness guarantees.
- Expand lexical scope, populations, languages or response formats through new reviewed frames and validation, not automatic parameter transfer.
- Evaluate longitudinal progress, learning recommendations and external criterion links under their distinct claim requirements.
- Monitor maintainability, exposure, compute/storage cost and operational complexity as well as measurement performance.

**Deliverables:** preregistered comparative experiment, versioned candidate profile, holdout evidence, compatibility/migration plan and explicit promote/reject decision.

**Exit gate:** demonstrate worthwhile benefit over the accepted baseline under the same declared time/item budget and relevant accuracy, coverage, fairness, security and operational constraints. A feature failing this comparison stays research-only or is rejected.

**Failure/rework:** retain the baseline; revise or stop the experiment. Expansion that changes content/construct/population re-enters Phases 2–4 and production readiness as appropriate.

**Specification coverage:** advanced-model/CAT, expansion and learning-impact specs are conditional future work, not prerequisites for a useful first production release.

**Optionality:** Phase 6 is not mandatory. A reliable baseline may remain the best product choice.

### Delivery controls and current position

- Dependencies describe acceptance order, not a ban on safe parallel design. No real-data release bypasses an upstream gate; only one writer may mutate an approved data artifact at a time.
- At phase entry, convert work into bounded tasks with owner, input/output paths, allowed mutations, test IDs, budget and review checkpoints. Record status as planned/in progress/blocked/accepted with evidence, not a guessed completion percentage.
- The existing A/B work packages map to Phase 1; C maps to Phase 2; D maps to Phase 3; E maps to Phase 4; F maps to optional Phase 6. **Phase 5 explicitly adds LazzyBee production integration and operations.**
- **Current position:** P0 contracts and the SQLite specification exist; source files and reference tools exist; Phase 1's overall verification gate remains open. No delivery phase is asserted complete by this roadmap revision.
- The first execution task, when resumed by the owner, is Phase 1 verifier diagnosis and acceptance—not new algorithm research. Cron/subagents remain paused, and this roadmap edit does not authorize recruitment, migration or deployment.
- Do not implement a profile or raise public claim strength merely to use additional research. Source count, bank size, strata and recruitment N are separate quantities. Historical 20,000-frame/1,200-item/ten-band plans are not mandatory current constants.

## 5. Active specification suite

- [Measurement](docs/specs/MEASUREMENT_SPEC.md)
- [Sampling and estimation](docs/specs/SAMPLING_AND_ESTIMATION_SPEC.md)
- [Scoring V0](docs/specs/SCORING_SPEC_V0.md)
- [API and state machine](docs/specs/API_AND_STATE_MACHINE_SPEC.md) + [machine schema](docs/specs/assessment_contract.schema.json)
- [Artifact lineage and governance](docs/specs/ARTIFACT_LINEAGE_AND_GOVERNANCE.md)
- [Pilot and calibration](docs/specs/PILOT_CALIBRATION_PROTOCOL.md)
- [Privacy/accessibility](docs/specs/DATA_PRIVACY_AND_ACCESSIBILITY_SPEC.md)
- Data companion: [SQLite standardization](docs/specs/SQLITE_DATA_STANDARDIZATION_SPEC.md) + [proposed DDL](docs/specs/sqlite_standardization_v1.sql)

[Suite README](docs/specs/README.md) defines ownership/precedence. The seven P0 documents are updated together at revision 2.0.0. Historical detail is retained under raw/specs-before-harmonization, not simultaneously authoritative.

## 6. Status and approval boundary

Completed artifacts: research archive, older snapshot audit/reference tools, data-copy evidence, research decision review, SQLite specification/DDL and harmonized P0 documents. Existing offline tests and new schema checks are engineering evidence only.

Not completed: resolved overall data audit, standardized owner-data build, reviewed full-frame bank, API service, human pilot/calibration, independent production snapshot comparison or public recognition/CEFR validation. Source data and application code remain unchanged in this documentation revision. Implementation and background research stay deferred until separately requested.
