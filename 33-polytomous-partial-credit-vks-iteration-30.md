# Iteration 30 — Partial credit, VKS và ngưỡng mastery

## Phạm vi và câu hỏi

Iteration này tách **breadth count** (số lexical units được coi là biết theo một tiêu chí nhị phân) khỏi **depth/strength** (mức độ biết một từ). Mục tiêu là kiểm tra liệu các mức “quen mặt → biết nghĩa → dùng được” có thể cộng trực tiếp vào vocabulary size hay phải được mô hình hóa và báo cáo riêng.

## Bằng chứng đã xác minh

### 1. VKS là công cụ đo tiến bộ/depth, không phải bộ ước lượng general vocabulary size

Bản ERIC lưu trữ bài Wesche & Paribakht mô tả Vocabulary Knowledge Scale (VKS) là công cụ theo dõi mức tăng của số từ có một mức hiểu biết nào đó **và** độ sâu hiểu biết. Năm mức đi từ hoàn toàn xa lạ, nhận diện từ, có ý tưởng về nghĩa, biết nghĩa, đến dùng từ đúng ngữ nghĩa và ngữ pháp trong câu. Bài viết đặt VKS trong một thí nghiệm ESL với các từ mục tiêu và dùng nó để theo dõi gain trong chương trình đọc; mô tả này không phải một quy trình lấy mẫu toàn bộ lexical universe để suy ra số word families.

Nguồn: [Wesche & Paribakht, bản ERIC lưu trữ](https://archive.org/stream/ERIC_ED369291/ERIC_ED369291_djvu.txt) — HTTP 200, nội dung văn bản đã fetch và đọc.

### 2. Mức cao của VKS cần bằng chứng thực hiện, không chỉ tự khai

Phụ lục C tách self-report categories khỏi scoring categories. Mức I/II lần lượt biểu thị không quen và quen nhưng chưa biết nghĩa. Mức III yêu cầu synonym/translation đúng; mức IV yêu cầu dùng từ phù hợp ngữ nghĩa trong câu; mức V yêu cầu phù hợp cả ngữ nghĩa và ngữ pháp. Trang JALT mô tả VKS là thang 5 điểm của Wesche & Paribakht và phiên bản rút gọn cũng yêu cầu giải thích nghĩa hoặc tạo câu cho lựa chọn cao hơn.

Hệ quả: nếu sản phẩm có lớp partial/depth, response phải lưu `self_report_level` và `demonstrated_level` riêng. Không nên coi tự khai “I know this word” là một câu breadth đúng ngang với nhận diện nghĩa qua item đã kiểm soát.

Nguồn: [ERIC ED369291](https://archive.org/stream/ERIC_ED369291/ERIC_ED369291_djvu.txt), [JALT, Brown 2008](https://jalt-publications.org/tlt/departments/myshare/articles/628-using-modified-version-vocabulary-knowledge-scale-aid-vocabular) — cả hai HTTP 200.

### 3. Không được giả định 5 mức là một thang tiến triển đơn điệu

Meara phân tích VKS và chỉ ra rằng tiến trình từ chưa biết đến có nghĩa có vẻ hợp lý hơn, nhưng thứ tự nghiêm ngặt giữa biết nghĩa, dùng đúng ngữ nghĩa và dùng đúng ngữ pháp không được bảo đảm. Một câu có thể được tái tạo từ ngữ cảnh đã gặp mà không chứng minh đầy đủ nghĩa. Ông cũng nêu VKS không nhằm ước lượng general vocabulary knowledge; mức dùng câu cần người chấm nên khó mở rộng cho hàng nghìn từ.

Hệ quả: điểm 0–4 của depth không được mặc định là một đơn vị interval, cũng không được quy đổi tuyến tính thành “0.2 từ”. Phải kiểm tra category ordering, threshold và độ nhạy với các rubric khác.

Nguồn: [Meara 1996, The vocabulary knowledge framework](https://lognostics.co.uk/vlibrary/meara1996c.pdf) — HTTP 200, PDF đã fetch và extract.

### 4. Partial Credit Model mô hình hóa các ngưỡng kề nhau

Stanke & Bulut trình bày PCM cho response categories có thứ tự. Với item `i`, người `n` và category `j`, log-odds chọn `j` thay vì `j−1` phụ thuộc vào latent trait `theta_n`, ngưỡng item và step threshold. Ngưỡng đầu thường là ranh giới để đạt ít nhất partial credit. PCM cho phép khoảng cách threshold khác nhau theo item; Rating Scale Model (RSM) áp đặt khoảng cách giống nhau giữa các item.

Công thức PCM dạng tổng quát:

```text
P(Y_ni = k | theta_n) =
  exp(Σ[h=0..k] (theta_n - delta_i - tau_ih))
  / Σ[r=0..K] exp(Σ[h=0..r] (theta_n - delta_i - tau_ih))
```

Trong triển khai thực tế cần dùng đúng parameterization của thư viện, nhưng nguyên tắc là mỗi bước category có thể có difficulty riêng. Không nên fit một đường logistic binary rồi gọi các mức depth là partial credit mà không kiểm tra thresholds.

Nguồn: [Stanke & Bulut 2019, Explanatory Item Response Models for Polytomous Item Responses](https://files.eric.ed.gov/fulltext/EJ1246351.pdf) — HTTP 200, PDF đã fetch và extract. Đây là bằng chứng psychometric tổng quát, không phải calibration vocabulary-specific.

### 5. Gộp category thành binary có thể làm mất thông tin và gây bias

Stanke & Bulut ghi rõ việc chuyển dữ liệu polytomous thành binary làm mất cấu trúc gốc và có thể thêm bias; chỉ giải thích threshold đầu cũng bỏ sót quan hệ ở các threshold sau. Vì vậy raw category phải được giữ trong response log. Việc xuất `known = 1/0` là một lớp diễn giải riêng, với criterion đã định trước, không phải lý do để xóa partial response trước khi calibration.

### 6. Calibration polytomous cần mẫu độc lập đủ lớn; con số 300 không phải quy tắc của sản phẩm

Trong minh họa PCM/RSM/EPCM, tác giả dẫn các khuyến nghị rằng item có ba category có thể cần khoảng 300 người, và nhiều hơn khi số category tăng, để ước lượng threshold ổn định. Bộ dữ liệu minh họa 316 người chỉ vừa vượt mức cảnh báo và tác giả cố ý tránh diễn giải mạnh các tham số truyền thống. Đây là gate thiết kế calibration, không được chuyển nguyên thành `n=300` cho vocabulary test hoặc coi đó là bằng chứng đủ cho Preply.

Production cần calibration sample độc lập theo item/category, hold-out sample và báo SE của thresholds; nếu category hiếm hoặc thresholds đảo thứ tự, phải gộp category có lý do hoặc bỏ depth model.

### 7. WAT cho thấy scoring nhiều đáp án là construct-specific

Nghiên cứu Ehsanzadeh mô tả Word Associates Test (WAT) gồm 40 item, mỗi item có 4 đáp án đúng, mỗi lựa chọn đúng được 1 điểm, tối đa 160; chính tác giả cũng ghi cách chấm WAT còn được tranh luận. Đây là cảnh báo rằng điểm nhiều lựa chọn đúng/partial không có penalty và quy đổi phổ quát. WAT đo depth/association, không được dùng thay cho vocabulary-size count.

Nguồn: [Ehsanzadeh, Assessing Threshold Level of L2 Vocabulary Depth](https://files.eric.ed.gov/fulltext/EJ1290239.pdf) — HTTP 200, PDF đã fetch và extract.

### 8. Preply: partial-credit và mastery threshold chưa xác minh được

Endpoint methodology được kiểm tra lại trong iteration này và trả HTTP 403 Cloudflare. Không thể xác minh Preply có self-report, sentence evidence, depth score, ordered-category model hay chỉ chấm binary. Do đó bảng dưới đây chỉ ghi “unknown”, không suy đoán từ UX hoặc kết quả điểm.

Nguồn kiểm tra: [Preply methodology](https://preply.com/en/learn/english/test-your-vocab/how-it-works) — HTTP 403, không phải nguồn citable cho claim về scoring.

## Thuật toán đề xuất

### Hai output không trộn lẫn

1. **Breadth count**: ước lượng trên đúng `unit` và `universe_version` đã khai báo. Item có response nhị phân hoặc rubric evidence rõ ràng; partial depth không tự động cộng vào count.
2. **Depth profile**: lưu phân phối các category và/hoặc latent `theta_depth`, theo band/domain nếu có đủ item. Profile mô tả độ mạnh của kiến thức, không đổi thành word families.

Nếu muốn đặt một ngưỡng mastery cho breadth, định nghĩa trước `K_breadth`, ví dụ “đúng meaning criterion” hoặc “P(demonstrated meaning >= threshold) >= q”. `K_breadth` và `q` phải được chọn bằng calibration/criterion study, không chọn sau khi thấy dữ liệu.

### Công thức breadth theo band

Với `N_b` lexical units trong band `b`, `z_ni ∈ {0,1}` là breadth evidence theo rubric đã khóa và `n_b` item được chọn theo design:

```text
p_hat_b = mean(z_ni trong band b)
V_hat_b = N_b * p_hat_b
V_hat = Σ_b V_hat_b
```

Nếu lấy mẫu không đều, dùng inclusion probability/weight tương ứng. Nếu dùng model-based `P(known | theta, item)`, phải báo đây là model-assisted estimate và kiểm tra sensitivity với estimator design-based; không gọi hai kết quả là cùng một estimand.

### Công thức depth không cộng vào count

```text
D_hat_b = mean(theta_depth_i hoặc E[Y_i | theta_depth])
Profile_b = {P(Y=0), ..., P(Y=K)}
```

`D_hat_b` chỉ được so sánh trong cùng phiên bản item bank và scale linking. Không đặt `V_hat + c * D_hat` nếu chưa có external criterion chứng minh hệ số `c`.

### Pseudocode

```text
function score_vocab(response, item, mode):
    if mode == "breadth":
        return rubric_known(response, item)       # 0/1, criterion frozen
    if mode == "depth":
        level = classify_vks_response(response, item)
        return {"self_report": level.self,
                "demonstrated": level.demonstrated,
                "category": level.category}

function estimate(session, bank, universe):
    assert session.universe_version == universe.version
    raw = collect_responses(session)
    breadth = []
    depth = []
    for r in raw:
        breadth.append(score_vocab(r, bank[r.item_id], "breadth"))
        depth.append(score_vocab(r, bank[r.item_id], "depth"))

    V = design_weighted_band_total(breadth, bank, universe)
    if calibrated_pcm_exists(bank.version):
        depth_theta, se = fit_or_score_pcm(depth, bank.pcm_parameters)
        category_profile = posterior_category_profile(depth_theta, bank)
    else:
        depth_theta = null
        se = null
        category_profile = empirical_category_profile(depth)

    diagnostics = category_functioning_and_quality_checks(depth, raw)
    return {"breadth_count": V,
            "depth_theta": depth_theta,
            "depth_profile": category_profile,
            "uncertainty": uncertainty(V, se, diagnostics),
            "flags": diagnostics}
```

## Uncertainty và validation

- **Breadth sampling/response uncertainty**: dùng variance theo band hoặc replicate/cluster bootstrap như algorithm chung; không lấy SD của category 0–4 làm CI cho count.
- **Depth model uncertainty**: báo `SE_theta`/posterior interval và sensitivity giữa PCM, GRM và rubric binary. Interval này không phải CI của số word families.
- **Category uncertainty**: báo tỉ lệ category thấp, missing/ambiguous evidence và inter-rater disagreement của câu tự tạo.
- **Construct uncertainty**: nếu “biết nghĩa” không đồng nghĩa “dùng được”, báo breadth và depth riêng; không gộp interval.
- **Calibration**: dùng sample đa dạng theo proficiency/L1; kiểm tra category usage, monotonic probability curves, ordered thresholds, item fit, DIF, local dependence và hold-out predictive accuracy.
- **External validity**: correlate breadth với một vocabulary-size criterion độc lập; validate depth với task phù hợp như meaning recall/use, không dùng một reading criterion để hợp thức hóa mọi depth claim.
- **Decision consistency**: nếu sản phẩm cần nhãn `mastered`, bootstrap/person-level repeat hoặc classification accuracy phải đạt ngưỡng định trước. Không có nguồn xác thực cho ngưỡng production chung.
- **Calibration size**: mốc khoảng 300 người/3 categories chỉ là cảnh báo từ psychometric literature tổng quát; cần power/simulation trên item bank mục tiêu.

## So sánh với Preply

| Thành phần | Thiết kế đề xuất | Preply đã xác minh được |
|---|---|---|
| Estimand | Breadth count trên `headword/lemma/word_family` khai báo; depth là output riêng | Các iteration trước ghi nhận Preply dùng headword-oriented scale và midpoint/log-rank product method; partial/depth hiện **chưa xác minh** |
| Item score | Breadth binary theo rubric; raw VKS/depth categories giữ riêng | Không xác minh được do methodology HTTP 403 |
| Quy đổi | `Σ N_b p_hat_b` cho breadth; PCM/GRM chỉ cho depth sau calibration | Vendor-stated margin/midpoint từ nguồn methodology đã bị hạn chế truy cập; không có dữ liệu mới để kiểm định |
| Partial credit | Không cộng vào vocabulary count; fit ordered model hoặc báo profile | Unknown |
| Mastery threshold | Chọn trước, calibrate với criterion/hold-out, báo classification uncertainty | Unknown |
| Uncertainty | Tách sampling/response, model, category/rater và construct uncertainty | Không có response-level/item-bank data công khai để re-estimate |
| Claim an toàn | “Ước lượng breadth receptive theo universe X; depth profile riêng” | Không được gán cho Preply các control/threshold chưa fetch được |

## Gaps và bước tiếp theo

Chưa có item bank, response-level data, sentence rubric, category labels hoặc calibration sample của Preply. Chưa tìm được nguồn xác thực cho ngưỡng mastery/partial-credit và hệ số biến depth thành word count của Preply. Bước kế tiếp hợp lý là thiết kế pilot: một subset item có breadth key và depth rubric độc lập, hai người chấm câu tự tạo, calibration PCM/GRM trên sample đủ lớn, rồi kiểm tra xem partial layer có tăng validity/decision consistency mà không làm thay đổi estimand breadth hay không.
