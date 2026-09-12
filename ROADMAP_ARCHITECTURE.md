# Strategic Architecture & Implementation Roadmap: Vocabulary Size Estimation

> **Document Version:** 1.1.0  
> **Status:** Strategy Approved · Implementation Architecture Conditionally Approved (Pending P0 Technical Specifications)  
> **Target Audience:** Engineering Leads, PMs, Backend, Flutter Mobile/Web, Data & Psychometrics Teams (`itpro-vn`)  
> **Strategic Advisor Review:** Reviewed by GPT-6-Astra (Conditional Sign-off with P0 Action Items)

---

## ⚠️ Strategic Advisor Sign-off Status & Guardrails
* **Strategy & Core Principles:** **APPROVED** (Receptive construct definition, frequency-stratified baseline before CAT, LLM as drafting assistant only, telemetry-driven offline calibration).
* **Production Implementation Architecture:** **CONDITIONALLY APPROVED** (Requires resolution of 5 P0 Specifications below before locking scoring contracts or public scoring claims).
* **Public Beta with "Vocabulary Size" Claims:** **NOT APPROVED YET** (Requires empirical validation against an independent reference test with characterized measurement error).

---

## 1. Executive Summary & Problem Framing

Project **`vocabulary-research`** addresses the fundamental challenge of accurately, quickly, and reliably estimating an individual's English vocabulary size through an adaptive digital assessment.

While commercial benchmarks (such as Preply's Vocabulary Test) claim a "±10% margin of error", systematic audits show that these figures rely on uncalibrated heuristic assumptions (such as logarithmic midpoint estimation over static dictionary headwords) without published peer-reviewed validation. Conversely, traditional psychometric instruments (such as Paul Nation's Vocabulary Size Test - VST) utilize simplistic fixed-form scoring (`Total Correct × 100`) without guessing penalties, item exposure controls, or response-time quality gates.

**Core Mission:** Transition from theoretical research (Iterations 01–65) into an enterprise-grade, scientifically grounded, and user-centric software platform.

### Key Construct Definition (Non-Negotiable)
To prevent construct invalidity, the system does not make ambiguous marketing claims like *"You know N English words"*. The formal measurement construct is strictly defined as:
> **"Estimated Receptive Meaning Recognition across a standardized, stratified lexical frequency framework, evaluated under bounded assessment conditions."**

All score reporting must explicitly disclose:
1. **The Lexical Unit:** Standardized Lemma / Headword frame (excluding archaic/specialized tail noise).
2. **Evaluation Depth:** Receptive recognition (meaning selection), distinguished from productive or collocate mastery.
3. **Uncertainty Bounds:** Bayesian credible interval and Conditional Standard Error of Measurement (CSEM) rather than a single point estimate.

---

## 2. Phased Transition Roadmap

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Phase A: Formal Measurement Specification & Freeze (Current)             │
│ - Finalize Lexical Frame, item authoring schema, and Decision Register    │
│ - Implement Cold-Start Item Bank (1,200 curated items)                   │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ Phase B: Controlled Stratified Beta Engine (5–8 min assessment)          │
│ - Two-stage Stratified Sampling Core (Screening + Focused Bracket)       │
│ - Rapid-Guessing & Latency Quality Filters (No naive score penalties)    │
│ - Launch Web & Mobile Beta to collect clean empirical telemetry          │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ Phase C: Structured Data Collection & Empirical Pilot Calibration        │
│ - Retain random item exposure quotas & anchor items across forms         │
│ - Regularized 1PL (Rasch) / 2PL calibration via Marginal Maximum Likelihood│
│ - Validate against an independent, long-form reference ground truth      │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ Phase D: Full Adaptive Engine (Multistage / Constrained Shadow-CAT)      │
│ - Deploy Content-Constrained Adaptive Routing only after proven out-of-   │
│   sample accuracy gain over Stratified Baseline                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 3. System Architecture (5 Decoupled Modules)

The software architecture is decoupled into 5 independent subsystems to allow the underlying statistical and estimation engines to evolve without modifying frontend applications.

```
                  ┌─────────────────────────────────────────┐
                  │      Client Apps (Flutter Web/Mobile)   │
                  └────────────────────┬────────────────────┘
                                       │ REST / gRPC
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 2. Test Delivery Engine (Session, Staging, Latency Capture, Shadow Constraints) │
└───────────────────────┬───────────────────────────────────┬──────────────────────┘
                        │                                   │
                        ▼                                   ▼
┌───────────────────────────────────────┐ ┌────────────────────────────────────────┐
│ 1. Lexical Frame & Item Registry      │ │ 3. Scoring Engine (Plug-and-Play)     │
│ - Frequency metadata (Zipf, BNC/COCA) │ │ - Baseline: Stratified Weighted Est.   │
│ - Versioned Item Bank & Distractors   │ │ - Advanced: Bayesian EAP / 2PL-IRT     │
│ - Content provenance & licensing      │ │ - Output: θ, Count, CSEM, Credible Int.│
└───────────────────────────────────────┘ └────────────────────────────────────────┘
                        │                                   │
                        ▼                                   ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 4. Telemetry, Audit & Response Store                                             │
│ - Raw item responses, item position, latency (ms), client telemetry               │
│ - Pure event sourcing: Scores can be recomputed retrospectively under new models │
└───────────────────────────────────────┬──────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 5. Offline Calibration & Quality Pipeline                                        │
│ - Item response modeling, Distractor functioning analysis, DIF detection         │
│ - Shadow-test item bank health, anchor verification, model registry & rollback    │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### Module Specifications:
1. **Lexical Frame & Item Registry:**
   - Defines word frequency strata (Bands 1k to 20k+ based on SUBTLEX, COCA, BNC).
   - Immutable item versioning: altering a distractor creates item `v1.1` to preserve calibration history.
2. **Test Delivery Engine:**
   - Controls progression: Stage 1 (Screening: ~25 items across all bands) -> Stage 2 (Focused: ~45 items around estimated boundary) -> Dynamic items (5–10 calibration research items).
   - Enforces time budgets (targeted at 5–7 minutes, max 8 minutes).
3. **Scoring Engine:**
   - Completely agnostic of delivery UI.
   - Computes score and uncertainty interval independently.
4. **Telemetry & Audit Store:**
   - Raw logs remain immutable. If model parameters are recalibrated, past telemetry can be re-scored for longitudinal validation.
5. **Offline Calibration Pipeline:**
   - Runs periodic MML / EM estimation, evaluates item discrimination parameters ($a$) and difficulties ($b$), identifies misfitting items.

---

## 4. Cold-Start Item Bank Strategy

| Component | Strategic Purpose | Hard Boundary / What NOT to do |
|---|---|---|
| **Corpus Frequency (Zipf/COCA)** | Stratified sampling blueprint, initial ability prior | Do NOT treat word frequency rank as empirical item difficulty. |
| **LLM-Assisted Generation** | Drafting sentence contexts, definitions, and plausible distractors | Do NOT publish without human review. Distractors must be checked for unintended grammatical or semantic cues. |
| **Open Psychometric Datasets** | Covariate calibration (familiarity, word length, part of speech) | Do NOT import external dataset statistics directly as calibrated IRT item parameters. |
| **Response Latency (Time)** | Quality gate: flagging rapid-guessing (<1.5s) and timeout | Do NOT apply rigid numerical score penalties based on elapsed seconds. |

---

## 5. Verification Gates & KPI Framework

To scientifically validate that our engine outperforms commercial heuristic tests (e.g., Preply) and traditional static VSTs, the following gates must be met:

### Gate 1: Safe Public Beta Release
- [ ] Item Bank contains >= 1,200 human-verified items across 14 frequency strata.
- [ ] Median completion time is verified between 5.0 and 7.5 minutes in internal dogfooding.
- [ ] Telemetry pipeline captures milliseconds, option selections, and client device properties without data loss.
- [ ] Score report presents vocabulary count + 95% Credible Interval; no unverified claims.

### Gate 2: Empirical Accuracy & Calibration Verification
- [ ] Independent validation study conducted against a calibrated long-form reference assessment (>= 140 items).
- [ ] Empirical 95% credible intervals demonstrate nominal coverage (actual hit rate between 92% and 97%).
- [ ] Mean Absolute Error (MAE) and root-mean-square error (RMSE) evaluated across low, mid, and high ability tiers.

### Gate 3: Superiority Claim Gate (vs. Preply / Baseline)
- [ ] Direct counterbalanced within-subject test against Preply on a representative L2 cohort.
- [ ] Statistically significant reduction in estimation variance (CSEM) under identical time constraints.
- [ ] Verified test-retest reliability ($r \ge 0.88$) on alternate forms.

---

## 6. Engineering Action Plan & Team Allocation

### Immediate Permitted Scope vs. Blocked Scope
* **Backend:** Permitted to build Item Registry, authoring workflows, and telemetry pipelines. *BLOCKED from locking final scoring APIs or adaptive routing logic until P0.1, P0.2, and P0.4 contracts are signed off.*
* **Frontend (Flutter Mobile/Web):** Permitted to build UI prototypes, accessibility flows, and timing/reconnect spikes. *BLOCKED from hardcoding final score labels or confidence interval visualizations.*
* **Data / Psychometrics:** Permitted to curate initial lexical frames and draft item bank. *BLOCKED from claiming calibrated IRT parameters until empirical pilot data is gathered.*
* **Product / PMs:** Permitted to design consent flows and study protocols. *BLOCKED from marketing "±X% accuracy" claims.*

---

## 7. Mandatory P0 Specifications Required for Final Implementation Sign-off

Before production implementation and public beta release, the team must produce and freeze the following formal specifications:

1. **`MEASUREMENT_SPEC.md` (P0.1):**
   - Precise definition of Lexical Universe size ($N$), lemma/headword boundary rules, and handling of polysemy (lemma vs. lemma-sense).
   - Mathematical specification of the primary estimand:
     $$\widehat{V} = \sum_{h=1}^H N_h \cdot \widehat{p}_h$$
     with an explicit operational definition of $\widehat{p}_h$ (recognition probability vs. raw percent correct).
2. **`SAMPLING_AND_ESTIMATION_SPEC.md` (P0.2):**
   - Design-based vs. model-based sampling weights and extrapolation rules for unobserved strata.
   - Simulation analysis demonstrating coverage and bias across varied proficiency profiles.
3. **`SCORING_SPEC_V0.md` (P0.3):**
   - Transparent guessing models and sensitivity checks; distinction between Credible Interval, Confidence Interval, and CSEM on count scale vs. latent $\theta$.
4. **`API_AND_STATE_MACHINE_SPEC.md` (P0.4):**
   - Session lifecycle state machine (`created` -> `in_progress` -> `completed` / `expired` / `invalidated`).
   - Monotonic clock latency capture contract with client device telemetry; idempotent event submission schemas.
5. **`ARTIFACT_LINEAGE_AND_GOVERNANCE.md` (P0.5):**
   - Immutable artifact lineage tracking ensuring 100% reproducible re-scoring of any historical session across versioned models and item bank snapshots.

