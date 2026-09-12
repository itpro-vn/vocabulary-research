# ARTIFACT_LINEAGE_AND_GOVERNANCE.md

> **Concrete source artifact:** [Aggregate snapshot evidence](../data/snapshot-audit.json) now records the actual SQLite checksum, pinned WordNet resource/index hashes, mapping-output hash and tool hashes. The database and row-level mapping/review queue remain private. Audit ordinals are snapshot-local, not durable lexical identities; frame/bank/calibration release artifacts remain pending.

> **Project:** `vocabulary-research`  
> **Repository:** `itpro-vn/vocabulary-research`  
> **Specification version:** `1.0.0`  
> **Priority:** P0.5 — Release-blocking  
> **Status:** Proposed normative specification  
> **Scope:** Artifact governance, immutable versioning, reproducible re-scoring, re-estimation và audit lineage

Tài liệu này quy định kiến trúc đích và các điều kiện nghiệm thu bắt buộc; không khẳng định các thành phần mô tả dưới đây đã tồn tại trong repository.

---

## 1. Mục tiêu và phạm vi

Hệ thống MUST có khả năng lấy một kết quả đánh giá trong quá khứ và:

1. **Chấm lại bằng đúng mô hình lịch sử**, tạo ra cùng kết quả chuẩn hóa, không sai khác số học hoặc quyết định.
2. **Chấm lại bằng mô hình mới**, tạo một kết quả mới có lineage đầy đủ, không ghi đè kết quả lịch sử.
3. **Giải thích nguồn gốc kết quả**, bao gồm item đã hiển thị, phản hồi được ghi nhận, tham số calibration, thuật toán chấm điểm, routing policy và môi trường thực thi.

Nguồn sự thật của phản hồi là **immutable event log**. Bảng tổng hợp kết quả, cache và dashboard không phải nguồn sự thật.

### 1.1. Thuật ngữ chuẩn tắc

- **MUST / MUST NOT:** Bắt buộc / nghiêm cấm.
- **SHOULD / SHOULD NOT:** Khuyến nghị mạnh; ngoại lệ phải có quyết định được ghi nhận.
- **MAY:** Tùy chọn.

### 1.2. Cam kết tái lập

“100% deterministic re-scoring” nghĩa là:

```text
Same verified input events
+ Same immutable dependency closure
+ Same deterministic execution profile
→ Same canonical scoring result bytes
→ Same SHA-256 result hash
```

Không sử dụng tiêu chí “sai khác trong epsilon” để thay thế cam kết này.

Các trường vận hành như thời điểm chạy lại, worker ID và request ID MUST nằm ngoài đối tượng kết quả được so sánh.

Cam kết áp dụng trong thời hạn lưu giữ đã công bố, với điều kiện dữ liệu và khóa giải mã vẫn được lưu hợp lệ. Hệ thống MUST NOT tuyên bố còn khả năng tái lập sau khi dữ liệu bắt buộc đã bị xóa theo chính sách pháp lý.

---

## 2. Phân biệt các hoạt động

| Hoạt động | Đầu vào | Mục đích | Có thay đổi kết quả lịch sử? |
|---|---|---|---|
| Historical re-scoring | Event log và artifact lịch sử | Tái tạo chính xác kết quả ban đầu | Không |
| Response re-estimation | Phản hồi lịch sử và mô hình mục tiêu | Ước lượng lại năng lực hoặc điểm | Không; tạo kết quả mới |
| Calibration re-estimation | Dataset calibration được đóng băng | Ước lượng lại tham số item | Không; tạo calibration snapshot mới |
| Routing replay | Lịch sử đã quan sát và routing policy lịch sử | Kiểm chứng quyết định chọn câu | Không |
| Counterfactual simulation | Mô hình/routing khác và giả định mô phỏng | Nghiên cứu tình huống giả định | Không được gọi là kết quả quan sát thực tế |

Một routing policy mới có thể chọn các item mà người dùng chưa từng trả lời. Vì vậy MUST NOT gọi việc chạy policy mới trên phiên cũ là “tái lập phiên thực tế”.

---

## 3. Các bất biến kiến trúc

### 3.1. Bất biến bắt buộc

1. Artifact đã đăng ký không được sửa nội dung.
2. Một cặp `artifact_id + version` chỉ ánh xạ tới một `content_hash`.
3. Artifact reference dùng cho scoring MUST chứa hash; không được chỉ chứa alias như `latest` hoặc `production`.
4. Session MUST ghim một release bundle tại thời điểm bắt đầu.
5. Session đang chạy MUST NOT tự động nhận item bank, calibration hoặc scoring model mới.
6. Mỗi kết quả MUST tham chiếu một prefix xác định của event log.
7. Chỉnh sửa phản hồi hoặc kết quả MUST tạo bản ghi mới, không sửa bản ghi cũ.
8. Mọi dependency trực tiếp và gián tiếp cần cho tính toán MUST được lưu và kiểm chứng.
9. Lỗi tải hoặc kiểm chứng artifact MUST làm tác vụ chấm điểm thất bại an toàn; không được fallback sang phiên bản hiện hành.
10. Rollback MUST thay đổi con trỏ triển khai, không thay đổi artifact lịch sử.

### 3.2. Dependency closure

Dependency closure là toàn bộ artifact có thể ảnh hưởng đến kết quả, bao gồm:

- Lexical frame và quy tắc chuẩn hóa từ.
- Item bank và từng item snapshot được sử dụng.
- Stimulus, media hoặc tài nguyên hiển thị có ý nghĩa đối với câu trả lời.
- Calibration parameters, covariance/SE nếu thuật toán sử dụng.
- Answer-key và rubric.
- Scoring model, prior, estimator và stopping rules.
- Routing policy và cấu hình chọn item.
- Response reducer và feature transformation.
- Thang điểm, phép biến đổi scale, cut score và rounding policy.
- Runtime, thư viện số học và cấu hình RNG.
- Reference dataset hoặc equating artifact nếu mô hình cần.

Git commit đơn lẻ không phải dependency closure đầy đủ.

---

## 4. Định danh và phiên bản bất biến

### 4.1. Cấu trúc reference

Mỗi reference MUST có:

```yaml
artifact_id: "lex-frame-20k"
version: "1.0.0"
content_hash: "sha256:<64 lowercase hex characters>"
```

Nhãn hiển thị tương ứng:

```text
lex-frame-20k-v1.0.0
```

Hash xác định nội dung. Version phục vụ vận hành, tương thích và giao tiếp giữa các bên.

Một artifact có nội dung giống hệt MAY được tham chiếu bởi nhiều release, nhưng MUST NOT được tái xuất bản dưới cùng ID/version với nội dung khác.

### 4.2. Quy tắc SemVer

- **MAJOR:** Thay đổi contract, construct hoặc semantics không tương thích.
- **MINOR:** Thay đổi nội dung tương thích về giao diện nhưng có thể ảnh hưởng đo lường.
- **PATCH:** Thay đổi nội dung không chủ đích ảnh hưởng đo lường.

Mọi thay đổi payload, kể cả PATCH, MUST tạo hash và phiên bản mới. Classification “PATCH” không miễn kiểm thử.

### 4.3. Lexical frame

Lexical frame MUST đóng băng:

- Tập lexical entry với ID ổn định.
- Canonical order nếu thuật toán sử dụng vị trí.
- Chính sách Unicode, case-folding và normalization.
- Quy tắc lemma, inflection, homograph và đa nghĩa.
- Quy tắc inclusion/exclusion.
- Domain, tầng tần suất, weight và biến phân tầng.
- Nguồn dữ liệu và giấy phép.

Hash MUST được tính trên payload chuẩn hóa chứa toàn bộ trường ảnh hưởng tính toán, không chỉ danh sách chuỗi từ.

Ví dụ:

```text
lex-frame-20k-v1.0.0
lex-frame-20k-v1.1.0
```

Thay đổi lexical frame có thể thay đổi đại lượng cần đo, mẫu số hoặc trọng số quy đổi kích thước vốn từ. Kết quả trên hai frame MUST NOT mặc nhiên được coi là so sánh trực tiếp.

### 4.4. Item bank và item snapshot

Phân biệt:

- `item_family_id`: Định danh khái niệm item xuyên phiên bản.
- `item_snapshot_id`: Định danh một biểu hiện bất biến của item.
- `item_bank`: Tập tham chiếu tới các item snapshot cụ thể.

Ví dụ:

```yaml
item_family_id: "itm-000123"
item_snapshot_id: "itm-000123-v1.0.0"
```

Khi sửa một distractor:

```yaml
item_family_id: "itm-000123"
item_snapshot_id: "itm-000123-v1.1.0"
```

`itm-000123-v1.0.0` MUST tiếp tục tồn tại và có thể tải lại. Không được cập nhật distractor tại chỗ.

Item snapshot MUST bao gồm:

- Stem và stimulus.
- Option ID ổn định trong snapshot.
- Nội dung từng option.
- Correct option ID hoặc rubric.
- Locale, format và rendering contract liên quan.
- Lexical entry được đo.
- Các media dependency và hash.
- Ràng buộc trình bày, thời gian, exposure nếu có.

**A/B/C/D là nhãn hiển thị, không phải option identity.**

### 4.5. Calibration parameter snapshot

Calibration snapshot MUST đóng băng:

- Exact item snapshot reference cho từng dòng.
- Model family và parameterization.
- Giá trị `a`, `b`, `c`; tham số cố định cũng phải biểu diễn rõ.
- Scale ID, metric convention và hệ số scaling.
- SE/covariance nếu được sử dụng.
- Calibration dataset manifest.
- Calibration code, runtime và cấu hình.
- Inclusion/exclusion rules.
- Fit diagnostics, sample size và linking/equating references.
- Quy tắc xử lý item chưa calibration.

Sửa distractor MUST NOT tự động kế thừa calibration cũ. Việc tái sử dụng tham số đòi hỏi bằng chứng và phê duyệt đo lường được ghi trong artifact mới.

Các giá trị số dùng cho scoring SHOULD được lưu bằng chuỗi thập phân chuẩn hóa, tránh mất độ chính xác do serializer.

### 4.6. Scoring model

Scoring artifact MUST đóng băng:

- Model family: Rasch, 2PL, 3PL hoặc mô hình khác.
- Estimator: MLE, MAP, EAP hoặc phương pháp khác.
- Prior, quadrature grid và integration weights.
- Initialization, bounds, tolerances và iteration limits.
- Quy tắc hội tụ và fallback.
- Missing, skipped, timeout và invalid-response handling.
- Score transformation, interval và reporting rules.
- Rounding mode và thứ tự rounding.
- Tie-breaking và sort order.
- Feature extraction/reducer version.

### 4.7. Routing policy

Routing artifact MUST đóng băng:

- Selection objective.
- Content balancing.
- Exposure control.
- Eligibility và exclusion rules.
- Stopping rules.
- Tie-breaking.
- RNG algorithm và stream derivation.
- Quy tắc sử dụng trạng thái ngoài session.

Nếu routing phụ thuộc bộ đếm exposure toàn cục hoặc dịch vụ ngoài, seed không đủ để replay. Các input thực tế của quyết định đó MUST được ghi lại hoặc lưu dưới artifact bất biến.

---

## 5. Hash, canonicalization và lưu trữ

### 5.1. Quy tắc hash

Định dạng chuẩn:

```text
sha256:<64 lowercase hexadecimal characters>
```

Với JSON:

1. Payload MUST hợp lệ theo schema tương ứng.
2. Payload MUST được canonicalize theo RFC 8785/JCS.
3. Hash được tính trên UTF-8 bytes của kết quả canonicalization.
4. Không đưa trường chứa chính hash hoặc chữ ký bao ngoài vào payload được hash.

Với số thập phân cần chính xác, dùng canonical decimal strings theo contract riêng. JCS không tự chuẩn hóa Unicode; chính sách chuẩn hóa MUST được định nghĩa tại bước tạo artifact và có phiên bản.

Với binary blob, hash tính trên exact bytes.

Với artifact nhiều file:

```text
Artifact root
 └── Canonical file manifest
      ├── path + size + media_type + file_hash
      ├── path + size + media_type + file_hash
      └── ...
```

Root hash là hash của canonical file manifest. Mỗi file MUST được kiểm chứng độc lập.

### 5.2. Content-addressed storage

Khuyến nghị:

```text
artifacts/sha256/<digest>/payload
events/<session_id>/<segment_digest>
manifests/sha256/<digest>.json
```

Storage URI không xác định identity. Có thể di chuyển hoặc mirror dữ liệu mà không thay đổi content hash.

Mọi lần đọc phục vụ scoring MUST kiểm chứng hash. Object-store ETag không thay thế SHA-256.

### 5.3. Chữ ký

Hash phát hiện thay đổi nội dung nhưng không chứng minh nguồn phát hành. Release production MUST có attestation được ký, chứa:

- Subject content hash.
- Quyết định phê duyệt.
- Danh tính người/dịch vụ phê duyệt.
- Thời điểm.
- Signing key ID và signature algorithm.
- Chữ ký trên canonical attestation payload.

Private key MUST NOT được lưu trong registry.

---

## 6. Immutable event log

### 6.1. Event envelope

Mỗi event MUST có tối thiểu:

```yaml
event_schema_version: "1.0.0"
event_id: "globally-unique-id"
session_id: "session-id"
sequence: 17
event_type: "response.accepted"
client_occurred_at: "2026-01-15T08:30:05.123456Z"
server_received_at: "2026-01-15T08:30:05.180000Z"
idempotency_key: "client-operation-id"
previous_event_hash: "sha256:<previous hash>"
payload: {}
```

`event_hash` được lưu bên ngoài phần canonical event body trên và bằng SHA-256 của body đó.

- Sequence bắt đầu từ `1`, liên tiếp và duy nhất trong session.
- Event đầu tiên có `previous_event_hash: null`.
- Timestamp không thay thế sequence.
- Thời gian client là dữ liệu khai báo, không phải thứ tự có thẩm quyền.
- Duplicate retry với cùng idempotency key MUST không tạo thêm phản hồi có hiệu lực.
- Cùng idempotency key nhưng payload khác MUST bị từ chối và audit.

### 6.2. Các event tối thiểu

| Event | Nội dung quan trọng |
|---|---|
| `session.started` | Release bundle, RNG, locale, client contract |
| `routing.decided` | Input state, external state reference, item được chọn |
| `item.presented` | Presentation ID, item snapshot, option order thực tế |
| `response.submitted` | Phản hồi gốc từ client, presentation ID |
| `response.accepted` | Phản hồi được server chấp nhận và diễn giải chuẩn |
| `response.rejected` | Lý do từ chối |
| `response.invalidated` | Event bị vô hiệu hóa và quyết định nghiệp vụ |
| `item.timed_out` | Mốc timeout có thẩm quyền và elapsed time |
| `session.completed` | Điều kiện hoàn tất |
| `session.terminated` | Lý do chấm dứt, trạng thái validity |
| `score.requested` | Event prefix và scoring mode |

Cần phân biệt `response.submitted` với `response.accepted`: không phải mọi request client đều trở thành phản hồi dùng cho scoring.

### 6.3. Item presentation

Mỗi lần hiển thị MUST ghi:

```yaml
presentation_id: "pres-0007"
ordinal: 7
item_snapshot:
  artifact_id: "itm-000123"
  version: "1.1.0"
  content_hash: "sha256:<digest>"
option_order:
  - {display_label: "A", option_id: "opt-3"}
  - {display_label: "B", option_id: "opt-1"}
  - {display_label: "C", option_id: "opt-4"}
  - {display_label: "D", option_id: "opt-2"}
render_context:
  locale: "vi-VN"
  renderer_version: "assessment-web@2.3.0"
```

Seed và thuật toán shuffle MUST được lưu, nhưng không thay thế `option_order` thực tế.

Nếu client có thể tự shuffle, localize hoặc thay đổi nội dung, hệ thống MUST ghi nhận trạng thái thực sự được hiển thị. Thiết kế P0.5 SHOULD cấm client tự ý thay đổi nội dung semantic.

### 6.4. Chỉnh sửa và kết quả tại một thời điểm

Correction MUST là event mới, tham chiếu event bị sửa cùng reason và authority.

Historical re-scoring sử dụng đúng event prefix ban đầu. Correction xuất hiện sau prefix đó không được làm thay đổi lần tái lập lịch sử.

Chấm lại có áp dụng correction phải tạo result và manifest mới.

### 6.5. Bảo vệ tính bất biến

MUST triển khai:

- Append-only write path.
- Phân quyền không cho ứng dụng update/delete event.
- Hash chain.
- WORM/object lock hoặc cơ chế tương đương theo retention policy.
- Signed checkpoint hoặc manifest anchor nằm ngoài miền sửa đổi của event writer.
- Kiểm thử phục hồi backup định kỳ.

Hash chain đơn lẻ không ngăn được bên có quyền ghi lại toàn bộ chuỗi.

---

## 7. Assessment Session Metadata

Session metadata MUST lưu hoặc tham chiếu bất biến tới:

| Nhóm | Dữ liệu bắt buộc |
|---|---|
| Identity | Session ID, pseudonymous subject reference |
| Lifecycle | Started/completed/terminated timestamp, trạng thái |
| Release | Exact release bundle reference và activation decision |
| Content | Lexical frame, bank, item snapshots |
| Psychometrics | Calibration, scoring, scale/equating |
| Routing | Policy, config, observed external inputs |
| RNG | Algorithm, implementation, master seed, stream derivation |
| Presentation | Thứ tự item và option thực tế |
| Response | Event prefix, accepted-response semantics |
| Time | UTC wall-clock, monotonic elapsed time nếu dùng |
| Runtime | Container digest, platform, numerical profile |
| Transformation | Reducer và feature pipeline versions |
| Integrity | Event head hash, manifest hash, signature |
| Governance | Consent/retention policy reference, không chứa PII trực tiếp |

Seed MUST có biểu diễn mất mát bằng không, ví dụ chuỗi hex. Nếu dùng nhiều RNG stream, ghi danh tính và seed từng stream hoặc thuật toán dẫn xuất đã ghim phiên bản.

Nếu RNG state được ảnh hưởng bởi các lời gọi ngoài scoring, MUST tách stream hoặc lưu state/counter tại checkpoint.

---

## 8. Contract thực thi deterministic

### 8.1. Execution profile

Production scorer MUST sử dụng execution profile bất biến, bao gồm:

- Executable hoặc container image digest.
- Source commit để truy vết.
- OS/architecture và CPU feature contract.
- Interpreter/compiler và dependency lock.
- Numerical library versions.
- Thread count và reduction order.
- Floating-point mode.
- Locale và timezone.
- RNG implementation.
- Quy tắc serialize kết quả.

Container digest đơn lẻ không bảo đảm cùng floating-point behavior trên mọi CPU.

P0.5 SHOULD dùng CPU execution với thứ tự phép toán cố định và cấm kernel nondeterministic. GPU chỉ được sử dụng nếu chứng minh được bitwise reproducibility trong profile hỗ trợ.

### 8.2. Forbidden dependencies

Scorer MUST NOT phụ thuộc ngầm vào:

- Current time.
- Network response trực tiếp.
- Mutable database lookup.
- System-default locale.
- Unseeded randomness.
- Hash-map iteration order không xác định.
- Mutable `latest` image/package.
- Parallel reduction không có thứ tự cố định.

Mọi external value có ảnh hưởng MUST được materialize thành input bất biến.

### 8.3. Canonical scoring result

Ví dụ minh họa:

```json
{
  "result_schema_version": "1.0.0",
  "status": "scored",
  "theta": "0.482193",
  "standard_error": "0.317000",
  "reported_score": "642",
  "scale_id": "vocab-scale-v1",
  "n_accepted": 24,
  "n_scored": 23,
  "estimation_status": "converged",
  "stopping_reason": "precision_target",
  "flags": []
}
```

Mọi giá trị điểm trung gian được công bố qua API MUST nằm trong contract canonical result hoặc diagnostic artifact được hash.

Các số trong ví dụ không quy định độ chính xác chung. Decimal precision và rounding MUST do scoring artifact quy định.

### 8.4. Historical replay procedure

```text
1. Load and verify signed session lineage manifest.
2. Resolve all exact artifact references.
3. Verify dependency closure and content hashes.
4. Load the recorded event prefix.
5. Verify event sequence, chain and signed head anchor.
6. Execute the pinned response reducer.
7. Verify presentation and response identity mappings.
8. Run the pinned scorer in the pinned execution profile.
9. Canonicalize the scoring result.
10. Require exact equality with the original result hash.
11. Emit an immutable replay attestation.
```

Thiếu artifact, sai hash, runtime không hỗ trợ hoặc kết quả khác MUST trả lỗi rõ ràng. Không được gắn nhãn thành công một phần là “reproduced”.

---

## 9. Schema: Artifact Registry

Các schema sau sử dụng **JSON Schema Draft 2020-12, biểu diễn bằng YAML**. URI `schemas.vocabulary-research.invalid` là namespace minh họa; implementation MUST ánh xạ `$ref` bằng schema catalog nội bộ hoặc thay bằng namespace thuộc quyền quản lý dự án.

Validator MUST bật kiểm tra `date-time` và `uri` formats.

### 9.1. `artifact-registry.schema.yaml`

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
$id: "https://schemas.vocabulary-research.invalid/artifact-registry.schema.json"
title: Artifact Registry Record
type: object
additionalProperties: false

required:
  - registry_schema_version
  - artifact_id
  - version
  - artifact_type
  - content_hash
  - canonicalization
  - media_type
  - byte_size
  - payload_schema
  - created_at
  - created_by
  - dependencies
  - provenance
  - governance

properties:
  registry_schema_version:
    const: "1.0.0"
  artifact_id:
    type: string
    pattern: '^[a-z0-9][a-z0-9._-]{0,127}$'
  version:
    $ref: "#/$defs/version"
  artifact_type:
    enum:
      - lexical_frame
      - item_snapshot
      - item_bank
      - calibration_snapshot
      - calibration_dataset_manifest
      - scoring_model
      - routing_policy
      - execution_profile
      - response_reducer
      - scale_transform
      - reference_data
      - stimulus
      - validation_report
      - release_bundle
      - event_log_snapshot
      - scoring_result
      - session_lineage_manifest
      - governance_attestation
  content_hash:
    $ref: "#/$defs/hash"
  canonicalization:
    enum:
      - jcs-rfc8785
      - raw-bytes
      - jcs-file-manifest-v1
  media_type:
    type: string
    minLength: 1
  byte_size:
    type: integer
    minimum: 0
  payload_schema:
    $ref: "#/$defs/artifactRef"
  created_at:
    type: string
    format: date-time
  created_by:
    $ref: "#/$defs/actor"
  dependencies:
    type: array
    uniqueItems: true
    items:
      type: object
      additionalProperties: false
      required: [role, artifact]
      properties:
        role:
          type: string
          minLength: 1
        artifact:
          $ref: "#/$defs/artifactRef"
  provenance:
    type: object
    additionalProperties: false
    required: [producer, source_inputs]
    properties:
      producer:
        type: string
        minLength: 1
      source_commit:
        type: string
        pattern: '^([a-f0-9]{40}|[a-f0-9]{64})$'
      build_run_id:
        type: string
        minLength: 1
      source_inputs:
        type: array
        uniqueItems: true
        items:
          $ref: "#/$defs/artifactRef"
  governance:
    type: object
    additionalProperties: false
    required:
      - owner
      - data_classification
      - retention_policy_id
      - license_policy_id
    properties:
      owner:
        type: string
        minLength: 1
      data_classification:
        enum: [public, internal, restricted, highly_restricted]
      retention_policy_id:
        type: string
        minLength: 1
      license_policy_id:
        type: string
        minLength: 1

$defs:
  hash:
    type: string
    pattern: '^sha256:[a-f0-9]{64}$'
  version:
    type: string
    pattern: '^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$'
  artifactRef:
    type: object
    additionalProperties: false
    required: [artifact_id, version, content_hash]
    properties:
      artifact_id:
        type: string
        pattern: '^[a-z0-9][a-z0-9._-]{0,127}$'
      version:
        $ref: "#/$defs/version"
      content_hash:
        $ref: "#/$defs/hash"
  actor:
    type: object
    additionalProperties: false
    required: [actor_id, actor_type]
    properties:
      actor_id:
        type: string
        minLength: 1
      actor_type:
        enum: [human, service]
```

`payload_schema` cũng là artifact được lưu bất biến. Schema gốc dùng để bootstrap MUST được đóng gói trong validator release với digest đã ghim.

Storage locations, trạng thái triển khai và danh sách phê duyệt hiện hành MUST được quản lý bằng append-only operational records riêng; không sửa registry record để cập nhật chúng.

### 9.2. Semantic validation ngoài JSON Schema

JSON Schema không đủ để kiểm tra quan hệ liên bản ghi. Registry service MUST kiểm tra:

- Unique constraint trên `(artifact_id, version)`.
- Hash payload đúng với record.
- Reference trỏ tới artifact tồn tại và đúng loại.
- Dependency graph không có cycle không được phép.
- Bank không chứa hai snapshot mâu thuẫn theo bank policy.
- Calibration bao phủ mọi item có thể được scorer chấm, hoặc có fallback contract rõ.
- Calibration scale tương thích với scorer và reporting transform.
- Payload schema đúng với artifact type.
- Closure đủ để chạy trong môi trường không có network.

---

## 10. Schema: Session Lineage Manifest

Manifest là snapshot bất biến của lineage cho **một kết quả**. Một session có thể có nhiều manifest: kết quả ban đầu, corrected result, re-estimation hoặc kết quả interim.

### 10.1. `session-lineage-manifest.schema.yaml`

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
$id: "https://schemas.vocabulary-research.invalid/session-lineage-manifest.schema.json"
title: Session Lineage Manifest
type: object
additionalProperties: false

required:
  - manifest_schema_version
  - manifest_id
  - session_id
  - subject_ref
  - created_at
  - session_state
  - timestamps
  - source
  - original_bundle
  - rng
  - presentations
  - computation
  - result
  - governance

properties:
  manifest_schema_version:
    const: "1.0.0"
  manifest_id:
    type: string
    minLength: 1
  session_id:
    type: string
    minLength: 1
  subject_ref:
    type: string
    minLength: 1
  created_at:
    type: string
    format: date-time
  session_state:
    enum: [active, completed, terminated]
  timestamps:
    type: object
    additionalProperties: false
    required: [started_at, input_cutoff_received_at]
    properties:
      started_at:
        type: string
        format: date-time
      ended_at:
        type: string
        format: date-time
      input_cutoff_received_at:
        type: string
        format: date-time

  source:
    type: object
    additionalProperties: false
    required:
      - event_log_snapshot
      - first_sequence
      - through_sequence
      - event_count
      - head_event_hash
      - checkpoint_attestation
    properties:
      event_log_snapshot:
        $ref: "#/$defs/artifactRef"
      first_sequence:
        const: 1
      through_sequence:
        type: integer
        minimum: 1
      event_count:
        type: integer
        minimum: 1
      head_event_hash:
        $ref: "#/$defs/hash"
      checkpoint_attestation:
        $ref: "#/$defs/artifactRef"

  original_bundle:
    type: object
    additionalProperties: false
    required:
      - release
      - activation_attestation
      - lexical_frame
      - item_bank
      - calibration
      - scoring_model
      - routing_policy
      - response_reducer
      - execution_profile
    properties:
      release:
        $ref: "#/$defs/artifactRef"
      activation_attestation:
        $ref: "#/$defs/artifactRef"
      lexical_frame:
        $ref: "#/$defs/artifactRef"
      item_bank:
        $ref: "#/$defs/artifactRef"
      calibration:
        $ref: "#/$defs/artifactRef"
      scoring_model:
        $ref: "#/$defs/artifactRef"
      routing_policy:
        $ref: "#/$defs/artifactRef"
      response_reducer:
        $ref: "#/$defs/artifactRef"
      execution_profile:
        $ref: "#/$defs/artifactRef"
      scale_transform:
        $ref: "#/$defs/artifactRef"

  rng:
    type: object
    additionalProperties: false
    required:
      - algorithm
      - implementation
      - master_seed_hex
      - stream_derivation
      - streams
    properties:
      algorithm:
        type: string
        minLength: 1
      implementation:
        $ref: "#/$defs/artifactRef"
      master_seed_hex:
        type: string
        pattern: '^(?:[a-f0-9]{2})+$'
      stream_derivation:
        $ref: "#/$defs/artifactRef"
      streams:
        type: array
        minItems: 1
        items:
          type: object
          additionalProperties: false
          required: [stream_id, purpose, seed_hex, initial_counter]
          properties:
            stream_id:
              type: string
              minLength: 1
            purpose:
              enum: [routing, option_shuffle, scoring, other]
            seed_hex:
              type: string
              pattern: '^(?:[a-f0-9]{2})+$'
            initial_counter:
              type: string
              pattern: '^(0|[1-9][0-9]*)$'

  presentations:
    type: array
    items:
      type: object
      additionalProperties: false
      required:
        - ordinal
        - presentation_id
        - presentation_event_sequence
        - item_snapshot
        - presented_at
        - option_order
        - render_context
      properties:
        ordinal:
          type: integer
          minimum: 1
        presentation_id:
          type: string
          minLength: 1
        presentation_event_sequence:
          type: integer
          minimum: 1
        routing_event_sequence:
          type: integer
          minimum: 1
        item_snapshot:
          $ref: "#/$defs/artifactRef"
        presented_at:
          type: string
          format: date-time
        option_order:
          type: array
          items:
            type: object
            additionalProperties: false
            required: [display_label, option_id]
            properties:
              display_label:
                type: string
                minLength: 1
              option_id:
                type: string
                minLength: 1
        render_context:
          type: object
          additionalProperties: false
          required: [locale, renderer_version]
          properties:
            locale:
              type: string
              minLength: 1
            renderer_version:
              type: string
              minLength: 1
            rendered_payload:
              $ref: "#/$defs/artifactRef"

  computation:
    type: object
    additionalProperties: false
    required:
      - mode
      - scoring_model
      - calibration
      - response_reducer
      - execution_profile
      - scoring_rng_stream_ids
      - diagnostic_artifacts
    properties:
      mode:
        enum: [original, historical_replay, re_estimation]
      scoring_model:
        $ref: "#/$defs/artifactRef"
      calibration:
        $ref: "#/$defs/artifactRef"
      response_reducer:
        $ref: "#/$defs/artifactRef"
      execution_profile:
        $ref: "#/$defs/artifactRef"
      scale_transform:
        $ref: "#/$defs/artifactRef"
      scoring_rng_stream_ids:
        type: array
        uniqueItems: true
        items:
          type: string
          minLength: 1
      parent_manifest:
        $ref: "#/$defs/artifactRef"
      parent_result:
        $ref: "#/$defs/artifactRef"
      compatibility_report:
        $ref: "#/$defs/artifactRef"
      reason:
        type: string
        minLength: 1
      diagnostic_artifacts:
        type: array
        uniqueItems: true
        items:
          $ref: "#/$defs/artifactRef"

  result:
    $ref: "#/$defs/artifactRef"

  governance:
    type: object
    additionalProperties: false
    required:
      - retention_policy_id
      - processing_basis_ref
      - data_classification
    properties:
      retention_policy_id:
        type: string
        minLength: 1
      processing_basis_ref:
        type: string
        minLength: 1
      data_classification:
        enum: [restricted, highly_restricted]

allOf:
  - if:
      properties:
        session_state:
          enum: [completed, terminated]
    then:
      properties:
        timestamps:
          required: [ended_at]
  - if:
      properties:
        computation:
          properties:
            mode:
              enum: [historical_replay, re_estimation]
    then:
      properties:
        computation:
          required: [parent_manifest, parent_result, reason]
  - if:
      properties:
        computation:
          properties:
            mode:
              const: re_estimation
    then:
      properties:
        computation:
          required: [compatibility_report]

$defs:
  artifactRef:
    $ref: "https://schemas.vocabulary-research.invalid/artifact-registry.schema.json#/$defs/artifactRef"
  hash:
    $ref: "https://schemas.vocabulary-research.invalid/artifact-registry.schema.json#/$defs/hash"
```

### 10.2. Ràng buộc semantic của manifest

Manifest validator MUST kiểm tra:

1. `event_count = through_sequence` khi `first_sequence = 1`.
2. Mọi presentation trong prefix xuất hiện đúng một lần trong `presentations`.
3. `ordinal` liên tiếp; presentation ID duy nhất.
4. Event sequence tham chiếu đúng loại event và đúng session.
5. Item snapshot trong manifest trùng với item trong event.
6. Option mapping không có nhãn hoặc option ID trùng.
7. Option ID thuộc đúng snapshot; item trắc nghiệm có đúng tập option cần hiển thị.
8. Tất cả presentations thuộc prefix đã ghim.
9. Original computation dùng đúng original bundle.
10. Historical replay dùng đúng computation và event prefix của parent.
11. Re-estimation giữ nguyên observed item snapshots và option mappings.
12. Scoring RNG streams tồn tại và có purpose phù hợp.
13. Result artifact đúng loại `scoring_result`.
14. Parent lineage không tạo cycle.

Manifest không chứa chính content hash của nó. Hash và chữ ký manifest nằm trong registry record và detached attestation để tránh tham chiếu vòng.

---

## 11. Release Management và Model Governance

### 11.1. Release bundle

Release bundle là artifact ghim một tổ hợp đã được kiểm thử:

```yaml
release_id: "assessment-prod-2026-01"
lexical_frame: "<exact artifact reference>"
item_bank: "<exact artifact reference>"
calibration: "<exact artifact reference>"
scoring_model: "<exact artifact reference>"
routing_policy: "<exact artifact reference>"
response_reducer: "<exact artifact reference>"
execution_profile: "<exact artifact reference>"
validation_reports:
  - "<exact artifact reference>"
```

Không triển khai độc lập một bảng calibration mới nếu tổ hợp bank/model/calibration chưa được phê duyệt.

### 11.2. State machine

```text
DRAFT → VALIDATED → APPROVED → STAGED → ACTIVE
   └──────────────→ REJECTED

ACTIVE → SUPERSEDED
ACTIVE → QUARANTINED
SUPERSEDED → ACTIVE   # Qua activation decision mới
```

State được suy ra từ append-only governance events; không nằm trong payload artifact có thể sửa.

### 11.3. Phân quyền phê duyệt

| Vai trò | Trách nhiệm |
|---|---|
| Content owner | Chất lượng ngôn ngữ, distractor, answer-key |
| Psychometrics approver | Calibration, fit, DIF, scale và validity |
| Engineering approver | Schema, determinism, compatibility, security |
| Release operator | Thăng cấp/rollback bundle đã được duyệt |
| Data steward | Retention, privacy, license, dataset provenance |

Production MUST có ít nhất hai người phê duyệt độc lập, bao phủ engineering và psychometrics. Người tạo thay đổi MUST NOT tự mình phê duyệt toàn bộ release.

### 11.4. Offline gates bắt buộc

#### Gate A — Integrity và compatibility

- Schema hợp lệ.
- Hash và signature hợp lệ.
- Dependency closure đầy đủ.
- Không thiếu calibration hoặc answer-key.
- Scale và parameterization tương thích.
- Không tham chiếu artifact đang quarantine cho session mới.

#### Gate B — Deterministic regression

- Golden sessions cho mọi production bundle còn trong retention.
- Replay lặp lại trên worker thuộc execution profile được hỗ trợ.
- So sánh exact canonical result hash.
- Network-disabled replay.
- Backup-only recovery replay.
- Test missing/corrupted artifact và fail-closed behavior.

#### Gate C — Psychometric validation

- Sample size và độ phủ năng lực.
- Parameter uncertainty, convergence và item fit.
- Distractor analysis.
- Local dependence.
- DIF theo nhóm được phép phân tích.
- Scale linking và anchor stability.
- Bias, RMSE, coverage, SE và decision consistency.
- Test length, exposure và content balance cho adaptive testing.
- Sensitivity với extreme response patterns.

Ngưỡng MUST được định nghĩa trong validation-plan artifact trước khi đánh giá release. Không áp dụng một ngưỡng chung tùy tiện cho mọi population.

#### Gate D — Historical impact analysis

Dùng corpus phản hồi đã đóng băng để so sánh mô hình cũ và mới:

- Phân phối score delta.
- Thay đổi classification.
- Tỷ lệ không hội tụ.
- Tác động theo population và subgroup hợp lệ.
- Ảnh hưởng của item bị sửa, loại bỏ hoặc recalibrate.
- Tỷ lệ session không đủ điều kiện re-estimation.

#### Gate E — Operational readiness

- Load/latency.
- Atomic activation.
- Session pinning trong concurrent deployment.
- Rollback drill.
- Artifact restore.
- Key access và disaster recovery.
- Observability không làm lộ nội dung item hoặc PII.

Mọi gate MUST xuất immutable report chứa dataset hash, code/runtime reference, metrics, ngưỡng và kết luận.

### 11.5. Thăng cấp

1. Freeze artifact closure.
2. Chạy offline gates.
3. Thu thập signed approvals.
4. Stage bundle và preload artifact.
5. Shadow scoring trên dữ liệu được phép.
6. Canary cho session mới.
7. Theo dõi tiêu chí đã đăng ký.
8. Atomic compare-and-swap production pointer.
9. Ghi activation attestation.

Shadow output MUST NOT âm thầm thay thế điểm hiển thị cho người dùng.

---

## 12. Rollback và ứng phó sự cố

### 12.1. Các tình huống

- Distractor vô tình trở thành đáp án đúng.
- Answer-key sai.
- Calibration drift.
- Scale transform lỗi.
- Runtime nondeterminism.
- Artifact corruption hoặc mất dependency.
- Item leakage hoặc vấn đề privacy/security.

### 12.2. Quy trình rollback

```text
1. Declare incident and identify affected hashes.
2. Quarantine affected artifacts for new sessions.
3. Select the last compatible approved bundle.
4. Atomically switch the production pointer.
5. Preserve every affected artifact and event.
6. Apply an explicit policy to in-flight sessions.
7. Identify impacted results through reverse lineage.
8. Produce corrective results if justified.
9. Publish incident and remediation attestations.
```

### 12.3. Session đang chạy

Chỉ được chọn một trong các policy đã phê duyệt:

- **Finish pinned:** Hoàn tất bằng bundle cũ nếu rủi ro chấp nhận được.
- **Terminate:** Chấm dứt với reason và validity flag.
- **Restart:** Tạo session mới và liên kết session cũ.

MUST NOT hot-swap calibration hoặc bank trong cùng session rồi coi đó là một phiên đồng nhất.

Nếu phải ngăn item lỗi ngay lập tức, có thể pause/terminate session; không sửa âm thầm routing history.

### 12.4. Drift

Drift alert là tín hiệu điều tra, không phải lệnh tự động ghi đè tham số.

MUST đánh giá:

- Thay đổi population.
- Thay đổi delivery hoặc UI.
- Item exposure/leakage.
- Anchor instability.
- Sample size, uncertainty và multiple-testing effects.

Recalibration MUST tạo snapshot mới cùng validation report.

### 12.5. Kết quả bị ảnh hưởng

Kết quả gốc được giữ nguyên. Nếu cần hiệu chỉnh:

```text
original_result
  └── corrected_or_reestimated_result
        ├── parent_result
        ├── correction_reason
        ├── target_artifacts
        └── approval_attestation
```

“Current official result” là con trỏ nghiệp vụ có audit history, không phải phép cập nhật payload của kết quả cũ.

---

## 13. Re-estimation theo mô hình mới

Mỗi re-estimation MUST ghi:

- Parent manifest/result.
- Exact event prefix.
- Target scoring/calibration/runtime.
- Compatibility report.
- Item exclusions và lý do.
- Mapping/equating artifact nếu có.
- Mục đích, người yêu cầu và phê duyệt.
- So sánh với điểm lịch sử trên cùng scale hoặc cảnh báo không so sánh được.

### 13.1. Quy tắc tương thích

Không được chấm phản hồi cho `itm-000123-v1.0.0` như thể người dùng đã nhìn thấy `v1.1.0`.

Nếu target calibration không có tham số cho snapshot lịch sử, chỉ được:

1. Từ chối re-estimation.
2. Dùng fallback được định nghĩa, kiểm thử và phê duyệt.
3. Loại item theo policy mục tiêu, ghi rõ ảnh hưởng lên validity và uncertainty.
4. Dùng bridge model có artifact và bằng chứng độc lập.

Không được suy diễn các phản hồi chưa từng quan sát.

---

## 14. Data Governance, retention và quyền riêng tư

### 14.1. Phân tách dữ liệu

- PII trực tiếp MUST nằm trong identity store riêng.
- Event log và manifest chỉ dùng pseudonymous subject reference.
- Pseudonymized responses vẫn có thể là dữ liệu cá nhân.
- Answer-key, item bank và calibration có thể là tài sản restricted.
- Replay worker chỉ được cấp quyền tối thiểu cần thiết.

### 14.2. Retention

Retention policy MUST quy định:

- Thời hạn cam kết replay.
- Thời hạn giữ event, artifact, result, manifest và attestation.
- Thời hạn giữ runtime executable và schema.
- Chính sách backup, encryption key và legal hold.
- Quy trình kết thúc khả năng replay.

Garbage collection MUST kiểm tra reachability từ toàn bộ session/result còn retention, bao gồm dependency gián tiếp. Artifact bị rollback hoặc superseded không được mặc nhiên xóa.

### 14.3. Xóa dữ liệu

Khi có yêu cầu xóa hợp lệ:

1. Data steward quyết định phạm vi theo căn cứ pháp lý.
2. Xóa hoặc crypto-shred các dữ liệu thuộc phạm vi.
3. Ghi deletion attestation tối thiểu, không giữ lại dữ liệu phải xóa.
4. Đánh dấu trạng thái replay là `unavailable_due_to_authorized_deletion`.
5. Không báo lỗi này như một replay thành công.

Immutability là contract chống sửa lịch sử trong thời hạn lưu hợp lệ, không phải lý do để lưu dữ liệu trái pháp luật.

---

## 15. Observability và audit

MUST theo dõi:

- `historical_replay_success_rate`
- `replay_hash_mismatch_count`
- `artifact_hash_verification_failure_count`
- `missing_dependency_count`
- `unsigned_production_activation_count`
- `session_bundle_mismatch_count`
- `event_sequence_gap_count`
- `calibration_compatibility_failure_count`
- `authorized_deletion_replay_unavailable_count`

Một `replay_hash_mismatch` MUST tạo incident; không chỉ là warning.

Audit API MUST hỗ trợ:

- Truy ngược result → manifest → events/artifacts.
- Truy xuôi artifact → affected bundles → sessions → results.
- Liệt kê quyết định activation/quarantine/rollback.
- Xuất replay verification report.

Logs vận hành MUST NOT chứa raw answers, answer-key, PII hoặc seed một cách không cần thiết.

---

## 16. Acceptance Criteria P0.5

P0.5 chỉ được nghiệm thu khi toàn bộ điều kiện sau đạt:

- [ ] Artifact registry từ chối overwrite cùng ID/version.
- [ ] Sửa distractor tạo item snapshot mới; snapshot cũ vẫn đọc và replay được.
- [ ] Bank ghim exact item snapshot references.
- [ ] Calibration ghim exact snapshot và scale convention.
- [ ] Session ghim release tại thời điểm bắt đầu.
- [ ] Event log append-only, có sequencing, idempotency, hash chain và signed anchor.
- [ ] Thứ tự item thực tế được lưu.
- [ ] Thứ tự option thực tế được lưu bằng option identity.
- [ ] RNG algorithm, implementation, seeds và streams được lưu.
- [ ] Scoring không phụ thuộc clock/network/mutable lookup.
- [ ] Manifest schema và semantic validator hoạt động.
- [ ] Historical replay tạo exact canonical result hash.
- [ ] Golden tests bao phủ completed, terminated, timeout, skipped, duplicate retry và corrections.
- [ ] Test bao phủ all-correct, all-incorrect, zero-scorable-response và nonconvergence.
- [ ] Thiếu/sai artifact làm replay fail closed.
- [ ] Re-estimation tạo result mới với parent lineage.
- [ ] Re-estimation không thay thế observed item snapshot bằng item mới.
- [ ] Production promotion có offline reports và approvals.
- [ ] Atomic rollback không thay bundle của session đang chạy.
- [ ] Reverse lineage xác định được mọi kết quả bị ảnh hưởng.
- [ ] Backup restore chứng minh replay được khi không có network.
- [ ] Retention bảo toàn cả dependency closure và khóa giải mã cần thiết.
- [ ] Authorized deletion có trạng thái replay rõ ràng.
- [ ] Không có `latest`, mutable URL hoặc mutable package dependency trong production scoring closure.

---

## 17. Các quyết định không được trì hoãn sau P0.5

Trước production, dự án MUST chốt và triển khai:

1. Canonicalization profile và decimal contract.
2. Event sequencing, idempotency và response acceptance semantics.
3. Artifact storage, signed checkpoints và trust model.
4. Execution profile đủ điều kiện deterministic.
5. Historical replay API và golden corpus.
6. Release bundle format và approval workflow.
7. Item revision/calibration compatibility policy.
8. Retention period và replay availability contract.

Việc thu thập phản hồi production trước khi có các quyết định này có thể làm mất vĩnh viễn khả năng tái lập. Không thể khôi phục chính xác một distractor đã bị ghi đè, một option order chưa từng được ghi, hoặc một runtime dependency không còn tồn tại.

---

## 18. Nguyên tắc kết luận

> **Một điểm số không chỉ là một giá trị. Nó là kết quả của một phép tính có bằng chứng: phản hồi bất biến, nội dung đã hiển thị, mô hình đã ghim, môi trường xác định và chuỗi phê duyệt có thể kiểm toán.**

Trong `vocabulary-research`, chỉ một kết quả có dependency closure được kiểm chứng và historical replay thành công mới được gắn nhãn **reproducible**.