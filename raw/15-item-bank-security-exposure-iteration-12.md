# Iteration 12 — item-bank security, exposure and repeated-attempt contamination

## Scope and evidence status

This iteration isolates an operational risk not covered by earlier scoring/calibration work: a vocabulary test can become a memory test if the same items are repeatedly shown or harvested. The evidence below is from two ETS research-report landing pages, an ERIC-hosted simulation study, an archived ERIC paper, and the International Test Commission (ITC) test-security guideline. All cited URLs returned HTTP 200 during this iteration. The quantitative results from the CAT exposure study are simulation results; they are not production parameters for Preply or for this vocabulary test.

## 1. Exposure control must preserve measurement precision

Boztunc Ozturk and Dogan compare four exposure conditions—Randomesque, Sympson-Hetter, Fade-Away and no exposure control—under multiple item-selection methods and item-pool characteristics. The abstract reports no great differences in measurement-precision indicators when exposure-control methods are used. It also reports that Fade-Away generally produced better item-pool utilization and reduced skewness of pool use and test overlap. The paper's recommendations favor Fade-Away, particularly with a-stratification for medium/high-difficulty pools, but the authors explicitly frame the work as a simulation study.

**Algorithmic implication.** Exposure protection should be a constrained optimization objective, not an excuse to remove informative items indiscriminately. At every item-selection step, maximize expected information subject to:

- content and frequency/domain quotas;
- an item exposure cap, both global and conditional on ability band;
- a recent-user exclusion window;
- a form-overlap cap; and
- a minimum information/precision requirement.

The implementation must compare conditional SE, bias and coverage with and without the exposure constraint in a pilot. No universal exposure threshold should be copied from this study.

Source: [ERIC PDF — Investigating Item Exposure Control Methods in Computerized Adaptive Testing](https://files.eric.ed.gov/fulltext/EJ1057460.pdf)

## 2. Item exposure and test overlap are different security measurements

The archived ERIC paper defines item exposure rate as the relative frequency with which an item is presented across all CAT administrations. It defines between-test overlap as the proportion of items in one fixed-length test that also appear in another, and average between-test overlap as the mean over all pairwise comparisons. The paper explains that monitoring both indices gives item-level and test-level views of exposure; controlling the item rate alone does not exactly control test overlap.

**Algorithmic implication.** The event log should store, for every administration:

```text
session_id, anonymized_user_id, form_id, item_id, ability_band,
frequency_band, domain, position, item_bank_version, timestamp
```

From this log calculate:

```text
item_exposure(i) = administrations containing i / all administrations
pair_overlap(A,B) = |items(A) intersect items(B)| / test_length
mean_overlap = mean(pair_overlap(A,B)) over sampled session pairs
```

For a public low-stakes test, the system can sample session pairs rather than perform every pairwise comparison, but it must preserve a reproducible sampling rule. A high mean overlap or a cluster of repeated items should trigger bank rotation or a security review even when the global exposure rate looks acceptable.

Source: [ERIC archive text — Exploring the Relationship between Item Exposure and Test Overlap](https://archive.org/download/ERIC_ED435643/ERIC_ED435643_djvu.txt)

## 3. Continuous online delivery changes the retest threat model

The ETS 1993 report states that paper-and-pencil programs commonly regulate security through form reuse and policies controlling how often a candidate may retake a test. It explains that continual CAT delivery, with a large and expensive item pool, requires new strategies. It discusses randomized selection, Sympson-Hetter and extensions intended for modern adaptive testing. The ETS 1995 report presents conditional exposure control based on the ability level of an individual test taker and explores its properties in five simulated studies.

**Algorithmic implication.** A retest policy cannot treat every administration as an independent fresh observation. The production service should distinguish:

1. **practice mode:** no claim of an independent estimate; show feedback and permit larger overlap;
2. **measurement mode:** issue a new form, enforce recent-item exclusion and maintain anchor policy;
3. **research/official mode:** authenticate the user where appropriate, protect anchors, record bank version and invalidate or review scores after a known breach.

In an adaptive vocabulary test, conditional exposure matters because the same highly informative items may be repeatedly selected for users in the same ability region. A practical first implementation is randomesque selection among near-max-information eligible items, with a fallback to the best eligible item only when the information loss stays under a pilot-calibrated tolerance. This is a design recommendation, not a verified Preply implementation.

Sources: [ETS RR-93-02](https://www.ets.org/research/policy_research_reports/publications/report/1993/hxkn.html) and [ETS RR-95-24](https://www.ets.org/research/policy_research_reports/publications/report/1995/hxsf.html)

## 4. Harvesting and score invalidation are part of validity, not only cybersecurity

The ITC guideline identifies digital capture of displayed questions, electronic recording of a test session, memorization of test content (called “harvesting”), and later recall as test-theft threats. It notes that online/computerized delivery increases such threats and recommends multiple layers rather than a single control. Its breach-action guidance includes possible score cancellation or invalidation, retesting, and replacement of item pools or test forms, depending on the incident.

**Algorithmic implication.** If a vocabulary item list is publicly posted or a breach is detected, the estimate may be contaminated upward through recognition/memorization. The service should not silently retain the same item difficulty calibration. It should:

- tag affected item IDs and exposure intervals;
- quarantine scores from affected forms/cohorts when the breach is material;
- publish a bank-version change and re-equating plan;
- offer a clean retest form; and
- retain the original score with a security-status flag rather than deleting audit history.

These controls are most important if the number is used for placement, research comparison or certification. For a casual self-assessment, a transparent “practice/possibly exposed” label may be sufficient, but the score should not be represented as an independent measurement.

Source: [ITC, The Security of Tests, Examinations, and Other Assessments](https://www.intestcom.org/files/guideline_test_security.pdf)

## 5. Comparison with the published Preply methodology

The fetched Preply methodology describes a dictionary/headword universe of more than 45,000 entries, logarithmic sampling, a first phase of about 40 words, a narrower second phase and currently 120 words in that second phase. It explains a midpoint estimator and vendor-provided approximately ±10% margin of error. The extracted methodology page does not describe exposure caps, item-overlap monitoring, item-bank versioning, retest invalidation or a breach-response procedure.

This is a **disclosure gap only**: absence from that page does not establish that the live Preply service lacks those controls. The direct Preply endpoint was previously blocked in this environment, while the methodology proxy was HTTP 200. Therefore no claim is made about the current production item bank or actual repeat-session behavior.

Source: [Preply, The Nitty-Gritty Details](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works)

## Proposed production rules

```text
for each requested item:
    eligible = items matching content/frequency/domain constraints
    remove items shown to this user in the recent exclusion window
    remove items above global exposure cap
    reduce/remove items above ability-band exposure cap
    remove items in a breached or quarantined bank version

    candidates = near_max_information(eligible)
    item = random_choice(candidates)  # randomesque anti-overlap step
    if no eligible candidate:
        use the least-exposed candidate satisfying minimum information
        and raise a bank-capacity/precision diagnostic

after administration:
    persist item/form/bank/version/ability-band events
    update exposure and overlap monitoring
    if security status is compromised:
        mark score as non-independent or invalidate per policy
```

Recommended validation gates are: (a) conditional SE and bias against an unconstrained oracle simulation; (b) item exposure distribution and maximum exposure; (c) mean and upper-tail form overlap; (d) score change after a deliberately repeated-item simulation; and (e) clean-form retest after excluding exposed items. The required item-bank size and caps remain open until response-level pilot data exist.

## Open gaps

- No item IDs, exposure counts, routing logs or repeated-session response data from Preply were available.
- No vocabulary-specific exposure cap or overlap threshold could be verified from the cited literature.
- The cited CAT exposure results are simulated and must not be turned into an unvalidated production cutoff.
- The effect of memorization on a headword midpoint estimate needs a controlled experiment with clean, partially exposed and heavily exposed forms.
- Chưa tìm được nguồn xác thực cho production implementation hiện tại của Preply regarding retest controls, exposure monitoring or breach handling.
