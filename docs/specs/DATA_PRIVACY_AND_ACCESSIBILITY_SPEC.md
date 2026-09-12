# P0.7 — Data privacy, ethics, security and accessibility

**Version:** 2.0.0
**Status:** release-blocking normative target; legal/operational approvals remain required. [Suite contract](README.md).

## 1. Source and personal-data boundaries

The owner-confirmed 42,497-record full server JSON/SQLite export is distinct from the 3,885 learning snapshot. The overall full-verifier failure remains open despite matched counters. Follow [current evidence](../data/SERVER_DICTIONARY_STATUS.md) and [deferred SQLite standardization](SQLITE_DATA_STANDARDIZATION_SPEC.md). Content possession does not automatically establish Oxford provenance, redistribution rights or participant research consent.

Separate:

1. Restricted lexical content, source IDs, definitions/audio/HTML and licensing/provenance.
2. Assessment item bank, keys, routing seeds and calibration parameters.
3. Personal responses, telemetry, subject estimates and linked demographic/consent records.
4. Safe aggregate/public documentation, after disclosure review.

Legacy `user_note`, scheduling and progress columns must not be published or interpreted as permission to use personal learning histories. Their reported NULL state in one export is not a permanent privacy guarantee. Participant withdrawal concerns in-scope personal data, not unrelated dictionary entries; lexical rights remain independently governed.

## 2. Threat model and minimized collection

Assess account/session takeover, cross-subject access, item/key scraping, prompt/HTML/URL injection, repeated-attempt memorization, sensitive logging, analyst re-identification, unauthorized joining/export, cache/backup leaks and research-purpose creep. Define data owner, steward, incident responder and reviewer responsibilities before launch.

Collect only fields required for session integrity, approved measurement and separately consented research. Server events may include pseudonymous session/presentation IDs, role/status, response/receipt timing and version references. Optional device/accessibility/demographic variables need documented purpose, minimum granularity and retention. No biometric/audio recording, precise location, contact details or free text by default.

Hashing/pseudonyms do not make responses anonymous. Store identity linkage separately with stricter authorization; analysts cannot join identity vaults by default. Use separate keys/scopes, access auditing and secure rotation without losing the ability to erase all still-linkable records.

## 3. Consent, purpose and withdrawal

Core service processing and optional research are separately explained and governed. Server-side consent records include subject reference, purpose, version, choice/time, permitted uses and withdrawal state. The client cannot set a trusted consent flag. Explain what is collected, why, retention, access/deletion, optionality and contact/escalation channels. Applicable legal basis and minor/guardian requirements must be reviewed for the actual jurisdiction/population; do not infer compliance from this technical spec.

Refusing optional research must not prevent the core service where not necessary, silently reduce score quality or be treated as dont_know. Default research items occur after core completion. Withdrawal blocks queued/new research ingestion and future use within the defined scope; consent-service failure fails research ingestion closed without requiring an unapproved core-service consent assumption.

Research participants can discontinue; the baseline then withholds incomplete core estimates rather than treating absence as incorrect. No coercive countdown or dark pattern to induce consent or an answer.

## 4. Storage, retention and erasure

Raw source/record mappings remain in Git-ignored private local storage; directories 700 and files 600 on the current host. In deployed storage use equivalent least privilege, encrypted transport/storage, key management and tested recovery. Public repository content is limited to schema, synthetic fixtures and approved aggregate evidence. No automatic upload of private data to external LLMs or services.

Before collecting people data, register finite retention and deletion timelines for identity links, responses, telemetry, research exports, queues, caches, backups, model snapshots and reports. Missing policy blocks collection; no indefinite default. Audit access grants and restrict download/export scope.

Valid erasure traverses dependency lineage. Remove or crypto-shred in-scope individual/linkable records and derived snapshots; evaluate aggregate model/parameter/report retention separately for legal basis, membership/inference risk, small groups and practical recall. A frozen artifact is not exempt from erasure. Preserve only a minimal non-identifying deletion attestation; mark historical replay unavailable when required, not a copy of the erased record in a tombstone or backup.

Do not promise universal model unlearning or guaranteed recall of previously public material. Document residual limits and approved rebuild/retention decisions transparently. A subject withdrawal does not force deletion of unrelated lexical source rows.

## 5. Calibration-data governance and optional privacy methods

Link consented dataset/version to source response events, inclusion/exclusion rules, purpose/access/retention, model fit, parameters and dependent results. A revised source dataset cannot silently reuse an incompatible fit. Withdrawal tests must identify dependent outputs and legal/risk dispositions.

Differential privacy, federated learning or other techniques are not default production controls by name alone. A DP claim requires an explicit privacy unit/adjacency, mechanism, clipping/sensitivity, epsilon/delta accounting and composition, access/threat model and evaluated utility/coverage/subgroup effects. Noise addition or hashing alone is not DP. No universal budget is imported; unsupported privacy-statistical releases remain research-only.

Privacy-induced parameter error can change calibration and result uncertainty. Keep it separate from the simple baseline's design interval rather than quietly describing non-private accuracy as private accuracy.

## 6. Item security, exposure and response integrity

Keep keys, parameters, full pools, source inventories, salts/seeds and detector internals restricted. Deliver only the assigned reviewed item, bind IDs to subject/session/version and enforce per-object authorization. Parameterize SQL. Do not fetch/evaluate URLs or markup from dictionary imports. Sanitize HTML under an approved renderer/allowlist, constrain asset origins and content security policy, and never use raw content as an instruction to an agent.

Rate limit scraping/repeated attempts using justified multi-signal policies without treating shared IP or assistive technology as proof of abuse. Exposure controls must be consistent with the frozen sampling design; silent rejection/replacement cannot retain invalid SRS weights. Research on exposure or person-fit does not approve new scoring corrections.

Anomaly flags are non-punitive evidence. Statistical misfit, response speed or similarity alone cannot label cheating, subtract a count or automatically invalidate. Use versioned detector validation, false-positive/operating characteristics where applicable, independent review and appeal/reversal. Confirmed technical compromise has its own policy/evidence path. Public responses expose only safe reasons; detailed thresholds or individual evidence remain restricted.

## 7. Accessibility and delivery neutrality

Target WCAG 2.1 AA with documented verification; meeting a named standard cannot be claimed from a checklist alone. Test semantic structure, keyboard navigation, visible focus, screen-reader option labels/grouping, status announcements, contrast, zoom/reflow, touch targets and absence of color-only cues. Escape/sanitize rendered content without changing assessment meaning silently; content-affecting fixes create new item versions.

Provide an explicit accessible dont_know control distinct from skip/network error. Announce submission/connection state, prevent accidental double submit and preserve focus after recovery. Loading time is not thinking time. A missing client visibility/latency event is not a behavioral verdict. Do not require raw audio/voice for a reading recognition construct.

Register accommodations and timing policy per form. Extended time, screen readers, alternative input or device constraints must be studied for comparability rather than assumed invariant or penalized. Session expiry is an operational rule, not adaptive psychometric stopping. Resume only when original plan/timing assumptions remain valid; otherwise no-score with clear guidance. Avoid blanket disabling accessibility tools as anti-cheating controls.

## 8. Fairness and claims

Review cultural/domain/L1/translation burden, sensitive content, stereotype and accessibility risks. Collect subgroup information only when needed and protected. Assess effect sizes, support, uncertainty and DIF/invariance under the [pilot protocol](PILOT_CALIBRATION_PROTOCOL.md); nonsignificance in a tiny subgroup is not proof of fairness.

Default `baseline-design-v0.1` uses `finite_frame_correct_response_total`, reviewed `lemma_pos` units and `diagnostic_only` claims. Public vocabulary claim is false; theta, vocabulary count and CEFR are null. No demographic score adjustment or misleading level label is introduced by privacy/fairness processing. Separate unsupported population/placement/CEFR claims from valid limited diagnostics.

## 9. Incident response and access controls

Test role separation: service/presentation worker, scoring worker, content reviewer, psychometric analyst, steward and identity administrator have only required artifacts. Audit privileged actions and export; approval for a public report does not grant raw-data export. Secrets stay out of logs/prompts/repo; rotate affected credentials/keys under incident procedure.

On leakage, key compromise or major validity incident, pause affected releases/new sessions, preserve minimized forensic evidence under lawful scope, assess notification obligations and impact, revoke exposed artifacts and create versioned correction/rollback decisions. Coordinate recovery with Governance. Do not restart the paused vocabulary cron or stopped subagents as an incident side effect.

## 10. Acceptance

- PRIV01: unauthorized subject/analyst/role access and unknown sensitive payload fields are rejected; logs do not contain raw values/credentials.
- PRIV02: server-validated research consent, withdrawal-in-queue and consent-service failure behave as specified without corrupting core sampling.
- PRIV03: erasure traverses exports/caches/backups/derived artifacts under documented timelines; no retained personal tombstone; unrelated lexical content remains intact.
- PRIV04: raw dictionary and record-level artifacts stay private/ignored; safe aggregate release is separately reviewed.
- PRIV05: source HTML/URL/SQL injection fixtures cannot execute or exfiltrate; keys, seeds and detector evidence do not leak.
- PRIV06: real keyboard/screen-reader/mobile/zoom/network-recovery tests pass for the supported delivery configurations.
- PRIV07: accommodations and subgroup limitations are documented and empirically evaluated; no unvalidated demographic/latency penalty.
- PRIV08: DP claims without accounting/utility evidence fail; baseline interval is not mislabelled as total/private-model uncertainty.
- PRIV09: incident and rollback drills preserve valid state/erasure limits; public claims remain within Measurement authorization.

[Governance](ARTIFACT_LINEAGE_AND_GOVERNANCE.md) owns release decisions. This document specifies controls; it does not certify legal compliance or accessibility without execution evidence.
