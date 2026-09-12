# Iteration 54 — Accessibility, accommodations và invariance trong vocabulary-size testing

## Phạm vi và direction

Direction của iteration này là kiểm tra một lớp thường bị bỏ sót trong VST online: accessibility và accommodations có thể làm giảm construct-irrelevant variance, nhưng cũng có thể thay đổi presentation, timing hoặc response process. Mục tiêu không phải chọn một hệ số cộng/trừ cho người dùng screen reader, keyboard, read-aloud hay zoom. Mục tiêu là thiết kế administration có thể tiếp cận, ghi nhận mode một cách tái lập, và chỉ so sánh các mode sau khi có bằng chứng equivalence.

Các URL dưới đây đã được HTTP-verify trong iteration này bằng `curl -L` với browser user-agent và trả `200`:

| Nguồn | Loại bằng chứng | HTTP |
|---|---|---:|
| [NCEO, Don't Forget Accommodations (ED520824)](https://files.eric.ed.gov/fulltext/ED520824.pdf) | hướng dẫn dựa trên nghiên cứu về accommodation trong assessment công nghệ | 200 |
| [NCEO, Summary of Research on Test Accommodations (ED605768)](https://files.eric.ed.gov/fulltext/ED605768.pdf) | tổng quan 11 nghiên cứu, hiệu quả accommodation theo điều kiện | 200 |
| [PARCC Accessibility Features and Accommodations Manual](https://archive.org/stream/ERIC_ED561902/ERIC_ED561902_djvu.txt) | universal design, validity, comparability và quy trình quyết định | 200 |
| [W3C WCAG 2.2 — Keyboard, SC 2.1.1](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html) | yêu cầu thao tác keyboard | 200 |
| [ETS GRE — Test Prep Materials in Accessible Formats](https://www.ets.org/gre/test-takers/general-test/prepare/test-prep-accessible-formats.html) | precedent delivery cho screen reader, braille, zoom, breaks và accessible documents | 200 |

## Bằng chứng đã xác minh

### 1. Delivery công nghệ không tự động loại bỏ accommodation

NCEO mô tả accommodation là cách tạo access để điểm phản ánh tốt hơn điều người làm bài biết. Chuyển từ paper sang technology mở ra embedded features, nhưng không xóa nhu cầu hỗ trợ riêng. Ví dụ pop-up glossary có thể nhúng vào platform; frequent breaks hoặc scribe vẫn cần lập kế hoạch và theo dõi. NCEO cũng cảnh báo màn hình có thể hiển thị ít thông tin đồng thời hơn trang giấy, làm tăng working-memory burden hoặc tạo nhu cầu navigation mới.

**Hàm ý cho VST:** accessibility thuộc về administration và interaction layer. Không được coi người dùng assistive technology là một subgroup cần tự động điều chỉnh K_hat. Trước tiên phải bảo đảm người đó có thể truy cập cùng stimulus, option và response function; sau đó mới kiểm tra mode effect bằng dữ liệu.

### 2. Hiệu quả accommodation là conditional, không có correction factor chung

Tổng quan NCEO năm 2020 bao gồm 11 nghiên cứu về accommodation cho English Learners/English Learners with disabilities. Bốn nghiên cứu thấy điểm cải thiện cho tất cả ELs dùng accommodation; ba nghiên cứu thấy cải thiện chỉ ở một số ELs trong một số điều kiện; hai nghiên cứu không thấy điểm tăng. Tổng quan mô tả các dạng như translation, modified English, glossary, read-aloud và visuals.

Kết quả này không phải nghiên cứu riêng cho vocabulary-size testing và không cho phép suy ra hệ số correction cho VST. Nó đủ mạnh để loại bỏ thiết kế kiểu `K_accessible = K_raw + c` hoặc `K_accessible = K_raw - c` nếu c chưa được calibration theo mode, population và construct.

### 3. Chuẩn hóa việc cung cấp accommodation ảnh hưởng đến diễn giải

Trong cùng tổng quan, read-aloud có kết quả lẫn lộn. Một nguyên nhân được nêu là delivery không có hệ thống; script cho administrator giúp đưa người làm bài vào điều kiện chuẩn hơn. Sự quen thuộc với accommodation cũng là yếu tố liên quan đến kết quả.

**Hàm ý:** event log cần phân biệt ít nhất:

- accommodation được cho phép;
- feature đã bật;
- người dùng có thực sự dùng hay không;
- tool/browser/OS/version;
- timing, pause và break;
- lỗi kỹ thuật hoặc fallback sang người hỗ trợ.

Nếu chỉ biết `has_accommodation=true` mà không biết feature có hoạt động, không thể dùng record đó cho equating hay audit validity.

### 4. Universal design là release gate, không phải hậu xử lý

PARCC manual đặt các mục tiêu: áp dụng universal design từ lúc phát triển assessment/item/task; giảm hoặc loại bỏ feature không liên quan đến construct; dùng technology để delivery accessible; xây accessibility mà không hy sinh validity; và tạo comparability qua policy/quy trình chung. Manual mô tả một chu trình năm bước: kỳ vọng về construct, tìm hiểu feature, chọn feature cho từng người, administer, rồi evaluate/improve.

**Hàm ý:** item bank VST phải có accessibility review trước calibration. Với một item written receptive vocabulary, bản screen-reader/keyboard/zoom phải truyền cùng target word, sentence, option và trạng thái câu hỏi; nếu một accommodation dịch, giải thích, đơn giản hóa hoặc đọc thêm nội dung làm thay đổi lexical cue thì đó không còn là presentation-equivalent một cách hiển nhiên.

### 5. WCAG cung cấp acceptance tests có thể tự động hóa một phần

W3C WCAG 2.2 SC 2.1.1 yêu cầu mọi chức năng, trừ trường hợp bản chất phụ thuộc đường đi, vận hành được qua keyboard interface mà không đòi timing cụ thể cho từng keystroke. SC 3.3.2 yêu cầu label hoặc instruction khi content cần user input; mỗi radio/checkbox/combobox cần label phù hợp để người dùng biết mình đang chọn gì.

Đây là yêu cầu accessibility của web, không phải bằng chứng psychometric rằng điểm các mode bằng nhau. Tuy nhiên, nó chuyển thành gate rõ ràng cho VST:

1. focus đi qua stem, tất cả option, navigation và submit theo thứ tự logic;
2. không có keyboard trap;
3. chọn option và chuyển item không cần thao tác chuột;
4. option được assistive technology đọc với label/selected state đúng;
5. lỗi/hoàn tất được thông báo không chỉ bằng màu hoặc vị trí;
6. thao tác không bị fail chỉ vì người dùng không kịp nhấn một phím trong khoảng thời gian tùy ý.

### 6. Hỗ trợ assistive technology phải kiểm tra theo tổ hợp thực tế

ETS mô tả tài liệu GRE accessible ở các dạng có thể dùng với nhiều assistive technologies, với links, table of contents, enlarged figures, figure descriptions và heading styles. ETS đồng thời nêu rõ mức hỗ trợ enhancement thay đổi theo loại assistive technology. Trang practice test của ETS liệt kê extended time, extra breaks, screen magnification, selectable colors, screen reader và refreshable braille compatibility.

Đây là precedent từ GRE, không phải evidence riêng cho VST. Nó củng cố yêu cầu test compatibility matrix theo browser/OS/reader, thay vì ghi chung một nhãn “accessible”. Các mode có extended time hoặc break cũng phải được tách khỏi mode chỉ thay đổi presentation khi phân tích response process.

### 7. Event log cần đủ để QA nhưng không biến interaction thành điểm vocabulary

NCEO thảo luận việc platform có thể ghi feature bật/tắt, keystrokes, mouse moves và lựa chọn/bỏ chọn tool, nhưng khuyến nghị cân nhắc giá trị và chi phí phân tích thay vì thu thập vô hạn. Với VST, keystroke và screen-reader usage không phải quan sát trực tiếp về lexical knowledge.

Schema tối thiểu được đề xuất:

```text
response_id
person_id_hash
form_id
item_id
lexical_unit_id
band_id
presentation_mode       # standard, zoom, high_contrast, screen_reader...
accommodation_mode      # none, keyboard, reader, extra_time, break...
assistive_technology    # optional, declared or detected
browser_os_version
feature_enabled
feature_used
response_status         # ANSWERED, OMITTED, TIMEOUT, TECHNICAL_MISSING
latency_ms              # diagnostic, not score correction
break_count / break_ms
option_order_id
quality_flags
```

Các field nhạy cảm phải được tối giản, bảo vệ và retention-limited theo policy dữ liệu của sản phẩm. `latency_ms`, keystroke pattern và feature usage chỉ dùng cho QA, missingness, DIF/sensitivity và nghiên cứu mode effect; không đưa trực tiếp vào công thức số từ biết.

## Thuật toán đề xuất được bổ sung

### A. Tách ba lớp

1. **Access layer:** WCAG/keyboard/label/focus/reader compatibility và fidelity của stimulus.
2. **Measurement layer:** chấm đúng/sai và ước lượng latent breadth trên đúng construct đã khai báo.
3. **Validity/equating layer:** kiểm tra mode/accommodation effect, DIF, item fit, SE và common-person/common-item linking.

Không cho phép một failure ở access layer được “chữa” bằng correction ở measurement layer.

### B. Pseudocode administration và scoring

```text
function administer_vst(person, form):
    mode = choose_declared_or_supported_mode(person)
    run_accessibility_smoke_test(mode)
    log_session_start(form, mode, browser_os_reader)

    for item in form.items:
        if not focus_and_label_check(item, mode):
            flag(item, ACCESS_FAILURE)
            stop_or_route_to_supported_form()

        t0 = monotonic_clock()
        status, answer = present_and_collect(item, mode)
        t1 = monotonic_clock()
        append_response(
            item_id=item.id,
            answer=answer,
            status=status,
            latency_ms=t1-t0,
            mode=mode,
            feature_used=current_feature_state(),
            option_order_id=item.option_order_id)

    return score_session_with_flags()

function score_session(responses, calibrated_bank, mode_linking):
    if any(response.flag == ACCESS_FAILURE):
        return {status: "invalid_access", K_hat: null}

    observed = responses where status == ANSWERED
    planned_missing = responses where status == NA_BY_DESIGN
    technical_missing = responses where status == TECHNICAL_MISSING

    # Do not count planned/technical missing as wrong.
    theta, se = estimate_latent_breadth(observed, calibrated_bank,
                                        mode=responses.mode,
                                        missing=planned_missing)
    K_hat = transform_to_declared_unit(theta, calibrated_bank)

    if mode != STANDARD:
        if not mode_linking.has_valid_common_scale(mode):
            return {status: "mode_not_equated", K_hat: K_hat,
                    reportable: false, flags: [MODE_UNLINKED]}
        K_hat = mode_linking.transform(mode, theta)

    return {
        status: "reportable_with_flags",
        K_hat: K_hat,
        se: se,
        flags: derive_quality_flags(responses, technical_missing),
        sensitivity: recompute_under_missingness_scenarios(responses)
    }
```

### C. Release gates

**Gate 1 — interface access:** pass keyboard, focus, labels, screen reader announcement, zoom/contrast và recovery from refresh/network interruption.

**Gate 2 — stimulus equivalence:** expert review xác nhận target word, sentence context, option text, order và required lexical cue không bị dịch/đơn giản hóa/đọc thêm theo cách đổi construct.

**Gate 3 — delivery fidelity:** pilot xác nhận accommodation được bật và dùng đúng; tool/version và break/timing được log; lỗi kỹ thuật có status riêng.

**Gate 4 — psychometric invariance:** so sánh item difficulty, person scores, DIF và response process giữa standard và accessible modes trên common-person/common-item sample. Không pass thì giữ score ở dạng `mode-specific`, không gộp vào Preply-like scale.

**Gate 5 — uncertainty:** SE của mode-specific estimate và uncertainty của linking phải được báo riêng. CI từ model không bao gồm bias do accessibility implementation hoặc selection vào nhóm accommodation.

## So sánh với Preply-like midpoint estimator

| Thành phần | Preply được ghi nhận trong state hiện có | Thiết kế đề xuất sau iteration 54 |
|---|---|---|
| Estimand | dictionary/headword scale theo methodology vendor đã được proxy-fetch trước đây | khai báo rõ lexical unit; written receptive breadth là output chính |
| Sampling/scoring | two-stage, frequency-ranked midpoint và vendor-stated khoảng ±10% theo methodology đã ghi nhận | frequency/IRT estimator vẫn giữ; thêm mode và accommodation metadata |
| Accessibility | current implementation, exact item behavior và controls chưa xác minh; direct endpoint trước đó trả 403 | universal-design item review + WCAG interface gates + compatibility matrix |
| Accommodation correction | chưa có hệ số production được xác thực | không correction cố định; mode link bằng common-person/common-item calibration hoặc báo mode-specific |
| Missingness | production status/routing chưa xác minh | `NA_BY_DESIGN`, `TECHNICAL_MISSING`, `TIMEOUT`, `OMITTED` tách riêng; không chấm planned missing là sai |
| Quality | chưa xác minh current accessibility/event-log policy | log feature state, tool/version, timing/break và access failures; dùng cho flags/QA, không cộng vào K_hat |
| Comparability | không được suy ra từ vendor midpoint description | chỉ so sánh mode/form sau invariance, equating và hold-out coverage |

Bảng này không khẳng định Preply có hay không có một accessibility feature cụ thể. **Chưa tìm được nguồn xác thực cho chính sách accessibility, accommodation, compatibility matrix hoặc mode-equating hiện tại của Preply.**

## Kế hoạch validation cho mode/accommodation

1. **Accessibility conformance test:** dùng keyboard-only và tối thiểu một screen reader trên các browser/OS được hỗ trợ; kiểm tra WCAG 2.2 SC 2.1.1, 3.3.2, focus, labels, selected state và error announcement.
2. **Content review:** panel gồm language assessor, accessibility specialist và người dùng assistive technology; blind-review standard/accessibility rendering của cùng item.
3. **Cognitive walkthrough:** ghi nhận nơi mode làm mất, thêm hoặc thay đổi lexical cue; item nào không giữ được construct phải thay hoặc loại khỏi common anchor.
4. **Randomized common-person pilot:** mỗi người làm các form/mode theo thiết kế counterbalanced; lưu actual feature use, không chỉ eligibility. Dùng common items để kiểm tra item/person linking.
5. **Model checks:** fit Rasch/IRT theo mode; kiểm tra item difficulty shift, DIF conditional on theta, local dependence, response status và latency. Không dùng latency để bù điểm nếu chưa có calibration độc lập.
6. **Equivalence decision:** nếu mode effect nhỏ và CI của chênh lệch nằm trong margin đã định trước, link scale; nếu không, phát hành mode-specific estimate với uncertainty riêng.
7. **Operational monitoring:** theo dõi access failure rate, technical missingness, mode-specific completion, item exposure và change theo browser/reader version. Mỗi platform update cần regression test và drift review.
8. **Reporting:** hiển thị `K_hat`, SE/CI, declared lexical unit, administration mode, accommodation flag và cảnh báo “not comparable across modes” nếu linking gate chưa pass. Không map accessibility flag thành trình độ thấp/cao.

## Assumptions và gap

- Các nguồn accommodation được verify chủ yếu là assessment K-12/EL hoặc GRE, không phải vocabulary-size-specific; chúng hỗ trợ nguyên tắc delivery và validation chứ không cung cấp correction factor cho VST.
- WCAG conformance không chứng minh psychometric equivalence.
- Chưa có response-level data, item bank, mode assignment, actual feature-use log hoặc common-person sample của Preply.
- Chưa có hệ số xác thực để chuyển standard score sang screen-reader/read-aloud/extra-time score trong vocabulary-size testing; **chưa tìm được nguồn xác thực cho ý này**.
- Cần calibration riêng cho population, L1, device và assistive-technology combinations mục tiêu; không suy rộng trực tiếp từ GRE/PARCC sang Preply.

## Kết luận iteration

Accessibility nên là một release và validity gate độc lập. Thiết kế an toàn nhất là universal-accessible item delivery, status-aware event log, không correction trực tiếp từ accommodation, và common-person/common-item equating trước khi gộp mode vào một vocabulary scale. Với dữ liệu hiện có, có thể bổ sung các rule này vào algorithm specification; chưa thể tuyên bố rằng Preply hiện tại đáp ứng chúng.
