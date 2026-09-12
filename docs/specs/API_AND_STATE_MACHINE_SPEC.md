# P0.4 — API and assessment state machine

**Version:** 2.0.0
**Protocol namespace:** proposed `/v1`; no deployed implementation claimed. [Suite contract](README.md). The previous embedded OpenAPI/Bayesian result design is [superseded history](../../raw/specs-before-harmonization/API_AND_STATE_MACHINE_SPEC.md), not a second active schema.

## 1. Inputs and readiness

The newly supplied 42,497-record server dictionary is not an API-ready item bank. The earlier 3,885 learning snapshot is distinct, and the overall data-verifier failure remains unresolved. [Data status](../data/SERVER_DICTIONARY_STATUS.md) and [deferred SQLite standardization](SQLITE_DATA_STANDARDIZATION_SPEC.md) control source readiness. APIs cannot use raw dictionary explanations automatically as assessment items or treat stored levels as difficulty.

Normative wire models: [assessment_contract.schema.json](assessment_contract.schema.json), JSON Schema 2020-12. HTTP operations are also defined in [assessment.openapi.json](assessment.openapi.json), OpenAPI 3.1. Every request rejects unknown fields. Required business constraints below supplement structural schema checks. No backend service is implemented by this document.

## 2. Authentication, transport and method rules

TLS is mandatory. Each request uses a scoped authenticated subject/session credential; an anonymous diagnostic credential, if offered, must be isolated, unguessable, expiring and subject to the same object authorization. Never expose or log bearer credentials. Cross-subject reads/writes are forbidden even with a valid session ID. Rate limits apply per subject/session and broader abuse dimensions without using IP alone as identity.

All mutating operations require `Idempotency-Key`; existing-session mutations carry `expected_version` in the request body. IDs are opaque nonempty server-issued strings, not dictionary stable IDs or enumerable ordinals. Server plans, answer keys, salts/seeds, selected-risk inventories, item parameters and sensitive integrity evidence are never serialized to client.

Input timing is untrusted. Use server receipt/presentation times and optional monotonic client telemetry separately. Missing telemetry does not become low effort or invalidation by default. Every payload is size-limited under a registered operational policy; invalid JSON including nonfinite numeric tokens is rejected before schema processing.

## 3. Endpoint contract

| Operation | Method/path | Request / response | Semantics |
|---|---|---|---|
| Start | POST `/v1/assessments` | `CreateAssessment` → 201 `Session` | Require an approved ready form/frame/profile and server-validated consent policy; allocate immutable session config |
| Next presentation | POST `/v1/assessments/{session_id}/next` | `VersionRequest` → 200 `Presentation`, or 204 | Mutation because it reserves/exposes an item; retry must return the same assignment, never reroll |
| Submit | POST `/v1/assessments/{session_id}/responses` | `SubmitResponse` → 200 `Receipt` | Atomic answer acceptance and state advance; never returns correctness/key/score |
| Read status | GET `/v1/assessments/{session_id}` | 200 `Session` | No new selection or hidden exposure on GET |
| Read result | GET `/v1/assessments/{session_id}/result` | 200 `AssessmentResult`; 409 pending; 410 erased | Quantitative contract requires approved research/diagnostic scope; ordinary UI gets a separate safe completion view |
| Cancel | POST `/v1/assessments/{session_id}/cancel` | `VersionRequest` → 200 `Session` | Terminal cancellation; no forced partial score |

`CreateAssessment.profile_id` must equal `baseline-design-v0.1`. Server validates the requested form's ownership, release status, language/accommodation compatibility and frame support; a client cannot supply its own manifests or override N/weights.

`next` returns 204 only when no next eligible presentation remains; it must not imply scoring passed. Read status/result to distinguish completed, insufficient evidence, expired or failed. A pending presentation is returned unchanged for an authorized retry/resume without disclosing a new item. No client skip can substitute an easier item while retaining SRS weights.

## 4. Session and item lifecycle

Session state enum: `created`, `screening`, `focused`, `research`, `completed`, `incomplete`, `cancelled`, `expired`, `failed`.

- `created → screening`: ready configuration, frozen screening plan, first presentation.
- `screening → focused`: every required screening outcome committed; routing plan/quotas locked before first focused exposure.
- `focused → research`: all focused observations committed and separately consented research slots remain; optional research is outside the scored design.
- `focused/research → completed`: required core design completed; optional research finished or omitted by policy. Refusal/withdrawal of optional research cannot erase a valid core diagnostic or create missing core observations.
- Active states → `incomplete`: required design observations/support lost under the registered policy; result may be insufficient evidence, never shortened-design score.
- Active states → `cancelled`, `expired`, `failed`: user cancellation, server expiry or technical failure. No automatic reopening, resampling or partial numeric count.
- Terminal history is immutable. A corrected/re-scored result uses new result/version lineage; erasure changes access/replay availability according to Governance.

Presentation state: reserved → delivered → accepted, or terminal timeout/technical failure/revocation. Delivery acknowledgement and answer acceptance are distinct events. At most one outstanding core presentation per session; only the exact assigned presentation may receive an answer. The server cannot infer actual human visibility solely from HTTP delivery, so rendering telemetry is recorded separately.

Expiry and hard operational timeouts are not psychometric stopping rules. Recovery may resume the same plan/presentation only if its registered timing/delivery assumptions remain valid; otherwise close incomplete. Never renew a task into a fresh draw under the old plan ID.

## 5. Response submission

`SubmitResponse` includes expected version, presentation ID, opaque answer and optional allowlisted timing. `answer` is exactly one of:

```json
{"kind":"choice","option_id":"opaque-option-id"}
```

```json
{"kind":"dont_know"}
```

`dont_know` must not carry an option ID. A selected option must belong to the exact locked presentation. Client correctness, ability, weight and answer-key fields are forbidden. The server derives `correct`/`incorrect`; preserves dont_know separately; missing/timeout/technical states are server observation categories, not forged choice outcomes. See [Scoring](SCORING_SPEC_V0.md).

No revising an accepted answer in place. A policy-approved correction/incident creates an audit event and a new governed interpretation, not a mutable response row. A duplicate submission with the same key/body returns its original receipt even if session version subsequently advanced.

## 6. Idempotency, concurrency and storage

Idempotency scope is principal + session/create scope + operation + key. Store a hash of the normalized request and the response receipt atomically with the state change. Check an existing idempotency record **before** optimistic-version rejection so a valid retry after commit succeeds. Same key/different body returns 409 `idempotency_conflict`.

For new requests, compare-and-swap `expected_version`, validate outstanding assignment and append event/update state/reserve next-stage plan in one transaction. Unique constraints enforce one accepted response per presentation and one semantic operation per key. Competing devices cannot both advance the same version. Return 409 `stale_version` or `presentation_conflict` without leaking other items; client fetches authorized status and resumes.

Response receipt, assignment and result creation use transactionally durable outbox/worker semantics when separated. At-least-once worker delivery is safe through unique operation IDs. No new selection or grading must occur merely because a transport retry changed timing. Idempotency retention must cover the registered retry/session horizon; do not expire keys while corresponding retries are promised safe.

## 7. Result and errors

The shared `AssessmentResult` schema fixes response-total profile/estimand and `count_unit=lemma_pos`. Baseline result statuses are `scored`, `insufficient_evidence`, `invalidated`. Numeric estimate/interval exist only for scored. Latent `theta`, `vocabulary_count`, `cefr` stay null; public vocabulary claim remains false. User-facing labels must not contradict this schema.

HTTP errors have `code`, safe `message`, and opaque `request_id`, never stack traces or raw records:

- 400 malformed JSON/request syntax.
- 401 missing/invalid credential; 403 insufficient scope or object authorization.
- 404 unknown authorized resource; use a consistent no-enumeration policy for cross-subject access.
- 409 stale version, idempotency/presentation conflict, terminal session or result pending.
- 410 authorized data deletion/expired retained resource, without sensitive details.
- 422 schema/business validation, unsupported profile, option not in presentation or unready form.
- 429 rate limit with safe retry guidance; no score implications.
- 503 service/engine failure; no fabricated zero score or misleading psychometric status.

A public completion projection is deliberately not `AssessmentResult`: it contains only state, allowed next action and safe limitation message. It must not expose a quantitative research estimate without approved scope. Do not return score changes after each response; they can leak keys and encourage gaming.

## 8. Security, observability and accessibility

Store keys and raw content server-side/restricted; deliver only the assigned reviewed item. Sanitize approved content at rendering, use a strict content-security policy and constrained assets, and prohibit arbitrary HTML/URL fetching from dictionary fields. Bind presentation IDs to session, principal, item version and server policy. Never accept external unit IDs as a way to enumerate the item bank.

Audit auth failures, stale-version conflicts, retries, missingness, stage transitions and scoring failures using minimized IDs/reasons. Keep integrity detector internals private. Provide keyboard/screen-reader compatible controls, explicit dont_know, resilient focus and network error recovery. Accessibility options and permitted timing differ by registered form; no device/latency suspicion alone invalidates an attempt. [Privacy/accessibility](DATA_PRIVACY_AND_ACCESSIBILITY_SPEC.md) owns detailed gates.

## 9. Acceptance

- API01: exact request/result schemas accept dont_know and insufficient evidence; reject extra client grading fields and numeric no-score outputs.
- API02: same-key replay returns same receipt; conflicting-body replay fails; retries after version advance remain safe.
- API03: concurrent submissions/next calls cannot double-grade, double-expose or alter the frozen route.
- API04: unpresented option/unit, cross-user access, terminal mutation and unready form fail safely.
- API05: disconnect/resume preserves presentation and plan; expiry/technical failure does not become incorrect.
- API06: schema validation and business checks enforce profile/unit/result consistency and null latent fields.
- API07: no key/seed/parameter/pool/PII leak in payloads, logs, exceptions or unauthorized result projections.
- API08: optional research consent/withdrawal leaves core sampling semantics intact; deletion produces authorized access/replay behavior.

Schema tests validate structure only. Load, transactional, security, accessibility and true end-to-end service tests remain required before deployment.
