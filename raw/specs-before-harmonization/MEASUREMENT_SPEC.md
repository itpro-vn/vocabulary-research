# MEASUREMENT_SPEC.md

> **Source-data evidence:** [Actual LazzyBee snapshot audit](../data/LAZZYBEE_SNAPSHOT_AUDIT.md): 3,885 source headword records are available privately. They are not yet a reviewed lemma-POS/target-sense universe. The 20,000-unit target below remains a design decision, not an acquired dataset; no scope change is silently approved by this audit.

> **Dự án:** `itpro-vn/vocabulary-research`  
> **Mã đặc tả:** P0.1 — Measurement Contract  
> **Phiên bản:** 1.0.0-draft  
> **Trạng thái:** Đặc tả đề xuất; chỉ được chuyển sang `approved` sau khi các cổng nghiệm thu trong tài liệu được đáp ứng.  
> **Phạm vi:** Định nghĩa cấu trúc cần đo, tập từ vựng tham chiếu, đơn vị đếm, mô hình ước lượng và hợp đồng báo cáo điểm.

---

## 1. Mục đích và nguyên tắc bắt buộc

Tài liệu này quy định chính xác:

1. Sản phẩm đo năng lực từ vựng nào.
2. Một đơn vị từ vựng được nhận diện và đếm ra sao.
3. Tổng thể từ vựng nào được phép ngoại suy.
4. Cách chuyển bằng chứng trả lời thành ước lượng quy mô vốn từ.
5. Những diễn giải nào được phép và không được phép đưa ra.

Các từ khóa:

- **MUST / MUST NOT:** yêu cầu bắt buộc / hành vi bị cấm.
- **SHOULD / SHOULD NOT:** khuyến nghị mạnh; ngoại lệ cần được ghi nhận.
- **MAY:** tùy chọn không làm thay đổi hợp đồng đo lường.

> **Lưu ý triển khai:** Tài liệu này không xác nhận repository đã có corpus, danh mục từ, ngân hàng câu hỏi hoặc mô hình hiệu chuẩn tương ứng. Những thành phần đó MUST được xây dựng, kiểm chứng và gắn phiên bản trước khi phát hành điểm số chính thức.

### 1.1. Tuyên bố đo lường

Sản phẩm ước lượng:

> **Số đơn vị lemma–từ loại trong một tập từ vựng tiếng Anh hữu hạn mà người làm bài có khả năng nhận biết nghĩa đích phổ biến, trong điều kiện kiểm tra nhận biết tiếp nhận được chuẩn hóa.**

Đây là phép đo **receptive meaning recognition**, không phải phép kiểm kê toàn bộ những từ người dùng “biết” theo mọi nghĩa của từ *biết*.

### 1.2. Những năng lực không thuộc phép đo chính

Điểm chính MUST NOT được diễn giải là phép đo trực tiếp của:

- Khả năng tự nhớ và tạo ra từ khi không có lựa chọn gợi ý.
- Khả năng nói, viết, phát âm hoặc đánh vần.
- Khả năng sử dụng collocation, sắc thái, register hoặc ngữ dụng.
- Khả năng hiểu mọi nghĩa của một từ.
- Năng lực ngữ pháp hoặc năng lực giao tiếp tổng thể.
- Tổng số word families theo hệ đo Vocabulary Size Test của Paul Nation.

---

## 2. Lexical Universe — tổng thể từ vựng tham chiếu

### 2.1. Định nghĩa hình thức

Gọi `U` là danh mục từ vựng hữu hạn, đã làm sạch, đóng băng theo phiên bản:

```text
U = {u₁, u₂, ..., u_N}

N = |U|

u = (
    canonical_lemma,
    lexical_pos
)
```

Mỗi đơn vị `u` có một nghĩa đích được chọn theo chính sách tại mục 4.

**N là số đơn vị lemma–POS đủ điều kiện trong bản phát hành universe, không phải:**

- Số token trong corpus.
- Số chuỗi ký tự khác nhau trước khi chuẩn hóa.
- Số item có trong ngân hàng câu hỏi.
- Số word families.
- Số nghĩa trong từ điển.

### 2.2. Kích thước N và chính sách phát hành

Đối với universe đầu tiên:

```text
N_target = 20_000 lemma–POS units
```

`N_target` là **quyết định phạm vi sản phẩm**, không phải tuyên bố rằng tiếng Anh có đúng 20.000 từ.

Quy tắc bắt buộc:

1. Pipeline xây dựng MUST tạo danh sách ứng viên đủ lớn trước khi làm sạch.
2. Sau làm sạch và xếp hạng, chọn 20.000 đơn vị đủ điều kiện đầu tiên.
3. Bản phát hành chuẩn chỉ được công bố với `N = 20_000` khi danh mục thực sự có đúng 20.000 đơn vị hợp lệ.
4. Nếu chưa đủ, MUST tiếp tục hoàn thiện dữ liệu hoặc phê duyệt một universe có kích thước khác.
5. MUST NOT gán `N = 20_000` trong mã nguồn khi manifest thực tế có số lượng khác.
6. Mọi lần chấm điểm MUST lấy `N` từ manifest bất biến của universe tương ứng.

Mốc 20.000 SHOULD được đánh giá lại sau nghiên cứu pilot, đặc biệt về chất lượng miền tần suất thấp và hiệu ứng trần.

### 2.3. Corpus tham chiếu

Universe dùng **hỗn hợp tham chiếu tiếng Anh đương đại**, gồm:

| Nguồn | Vai trò chính | Hạn chế cần kiểm soát |
|---|---|---|
| SUBTLEX-US | Ngôn ngữ hội thoại gần đời sống, tần suất phụ đề | Phụ đề không đại diện hoàn toàn cho lời nói tự nhiên |
| BNC | Bổ sung tiếng Anh Anh và nhiều thể loại | Một phần dữ liệu không phản ánh đầy đủ ngôn ngữ hiện tại |
| COCA | Bổ sung tiếng Anh Mỹ và độ phủ thể loại | Phân bố phụ thuộc phiên bản và lát cắt được sử dụng |

Mỗi nguồn MUST có:

- Tên và phiên bản cụ thể.
- Thời điểm phát hành hoặc thời gian dữ liệu.
- Phạm vi lát cắt được sử dụng.
- Số token trong mẫu tham chiếu.
- Điều kiện cấp phép.
- Phương pháp gán lemma và POS.
- Checksum hoặc định danh snapshot có thể tái lập.

MUST NOT dùng nhãn chung như “COCA mới nhất” trong manifest phát hành.

Việc dùng corpus MUST tuân thủ giấy phép. Không được giả định rằng dữ liệu nguồn có thể được phân phối công khai cùng repository.

### 2.4. Tổng hợp tần suất

Sau khi chuẩn hóa và gộp biến thể:

```text
f_c(u) = 1_000_000 × count_c(u) / token_count_c

score(u) =
    0.50 × f_SUBTLEX_US(u)
  + 0.25 × f_BNC(u)
  + 0.25 × f_COCA(u)
```

Các trọng số trên định nghĩa một **hỗn hợp tham chiếu quy ước**, không phải ước lượng khách quan duy nhất về tần suất tiếng Anh toàn cầu.

Quy tắc:

- MUST cộng số lần xuất hiện của các biến thể thuộc cùng đơn vị trước khi xếp hạng.
- Không xuất hiện trong một nguồn hoàn chỉnh được tính là `0`.
- Nguồn bị thiếu, không đọc được hoặc chỉ cung cấp danh sách cắt ngọn MUST NOT bị hiểu là tần suất bằng `0`.
- MUST NOT trộn số đếm lemma của một nguồn với số đếm word form của nguồn khác.
- Nếu hòa điểm, dùng quy tắc phá hòa xác định trước, ví dụ: số nguồn ghi nhận, sau đó `unit_id`.
- Thay đổi nguồn, trọng số hoặc pipeline MUST tạo phiên bản universe mới.

### 2.5. Tiêu chuẩn đưa vào

Một ứng viên chỉ đủ điều kiện khi:

1. Là mục từ tiếng Anh có nghĩa được từ điển uy tín ghi nhận.
2. Có bằng chứng sử dụng thực tế, không chỉ xuất hiện do lỗi hoặc trích dẫn tên.
3. Có lemma và POS xác định được.
4. Có ít nhất một nghĩa đương đại có thể xây dựng phép kiểm tra nhận biết.
5. Được ghi nhận trong ít nhất hai corpus tham chiếu; hoặc có ngoại lệ được chuyên gia phê duyệt kèm bằng chứng độc lập.
6. Nếu có dữ liệu phân tán, đạt ngưỡng tối thiểu đã đóng băng trong cấu hình xây dựng, mặc định là xuất hiện trong ít nhất năm đơn vị tài liệu/chương trình độc lập ở một nguồn.

Tần suất thấp không tự động đồng nghĩa với “rác”. Việc loại bỏ MUST dựa trên tiêu chí minh bạch.

### 2.6. Làm sạch và loại trừ

| Nhóm | Quy tắc |
|---|---|
| URL, email, markup, mã hệ thống | Loại |
| Lỗi OCR, token vỡ, lỗi mã hóa | Loại |
| Chuỗi số thuần, ký hiệu không có nghĩa từ vựng | Loại |
| Lỗi chính tả không được công nhận | Loại |
| Tên người, địa danh, tổ chức, thương hiệu dùng như tên riêng | Loại |
| Từ được đánh dấu `obsolete` hoặc `archaic` ở toàn bộ các nghĩa | Loại |
| Từ ngoại ngữ chỉ xuất hiện do code-switching | Loại |
| Từ vay mượn đã được từ vựng hóa trong tiếng Anh | Có thể giữ |
| Slang hoặc từ không trang trọng còn được sử dụng | Có thể giữ, phải gắn nhãn register |
| Từ chuyên ngành còn hiện hành | Có thể giữ nếu đạt tiêu chuẩn dữ liệu; không tự động gọi là vốn từ phổ thông |
| Viết tắt đã từ vựng hóa, có cách dùng và nghĩa ổn định | Có thể giữ sau xét duyệt |
| Tiếng cảm thán hoặc từ chức năng có nghĩa sử dụng ổn định | Có thể giữ nếu đo được mà không biến thành bài ngữ pháp |

**Không được loại tên riêng chỉ bằng viết hoa.** `May` và `may`, hoặc `Turkey` và `turkey`, phải được xử lý theo ngữ cảnh và nghĩa.

Nếu chỉ một nghĩa của lemma là cổ, đơn vị vẫn có thể được giữ khi còn nghĩa hiện hành đủ điều kiện.

### 2.7. Quy trình xét duyệt

Các trường hợp mơ hồ MUST có:

- Quyết định `include`, `exclude` hoặc `needs_review`.
- Mã lý do.
- Bằng chứng nguồn.
- Người xét duyệt.
- Kết quả phân xử khi có bất đồng.

SHOULD có ít nhất hai người xét duyệt độc lập cho các trường hợp về tên riêng, từ cổ, gộp lemma và chọn nghĩa đích.

### 2.8. Manifest bắt buộc

```yaml
universe_id: en-lemma-pos-20k-v1
status: draft
language: en
unit_type: lemma_pos
target_size: 20000
actual_size: null  # MUST be an integer before release
sense_policy: primary_sense_per_lemma_pos
reference_mix:
  SUBTLEX_US: 0.50
  BNC: 0.25
  COCA: 0.25
sources: []        # MUST contain pinned source snapshots
normalization_version: null
pos_mapping_version: null
cleaning_rules_version: null
ranking_version: null
unit_list_sha256: null
strata: []
```

Manifest còn `null` ở trường bắt buộc MUST NOT được sử dụng để phát hành điểm chính thức.

---

## 3. Đơn vị đếm: lemma, headword và word family

### 3.1. Lựa chọn chuẩn: lemma–POS

Đơn vị đếm chính là:

```text
unit_id = canonical_lemma + lexical_pos
```

Trong tài liệu và UI, “lemma/headword” có thể được dùng như nhãn giản lược, nhưng định danh nội bộ MUST giữ POS.

**Headword** là dạng mục từ hiển thị. Nó không tự động xác định một đơn vị đo, vì mỗi từ điển có thể tổ chức mục từ khác nhau.

### 3.2. Phân biệt POS

Ví dụ:

| Biểu thức | Cách đếm |
|---|---|
| `work` — noun | Một đơn vị |
| `work` — verb | Một đơn vị khác |
| `run`, `runs`, `ran`, `running` với chức năng động từ | Một lemma–POS: `run/VERB` |
| `running` dùng như danh từ đã từ vựng hóa | Có thể là đơn vị riêng nếu đạt tiêu chuẩn |
| `happy`, `happier`, `happiest` | Một đơn vị tính từ |
| `happy`, `happiness`, `unhappy` | Các đơn vị riêng |

Hệ POS chuẩn SHOULD dựa trên một tập tag công khai như Universal POS, nhưng MUST có bảng ánh xạ từ từng nguồn.

`PROPN`, dấu câu và token phi từ vựng bị loại. Việc phân biệt `AUX` với `VERB` và các lớp từ chức năng khác MUST được quy định trong bảng ánh xạ; không được tùy tiện theo từng corpus.

### 3.3. Biến thể chính tả và hình thái

- `color` và `colour` → một đơn vị.
- Biến thể viết hoa không đổi nghĩa → một đơn vị.
- Biến thể chia động từ hoặc số nhiều → gộp về lemma tương ứng.
- Dạng bất quy tắc → gộp theo bảng hình thái được kiểm chứng.
- Biến thể không có cùng nghĩa và cách dùng → không tự động gộp.
- Việc nhận biết lemma qua một dạng bề mặt không chứng minh người dùng nhận biết mọi dạng hình thái.

### 3.4. Đồng âm/đồng tự khác nguồn gốc

Trong phiên bản này, những mục có cùng lemma và POS nhưng khác nguồn gốc từ nguyên vẫn được gom vào một đơn vị đếm; chính sách nghĩa đích quyết định phần nội dung được kiểm tra.

Ví dụ `bank/NOUN` không được đếm hai lần chỉ vì từ điển tách thành hai headword đồng tự.

Đây là quy ước đo lường nhằm tránh phụ thuộc cách chia mục từ của từng nhà xuất bản.

### 3.5. Từ ghép và biểu thức nhiều từ

Phiên bản đầu:

- MAY bao gồm từ ghép viết liền hoặc có gạch nối được từ điển ghi nhận.
- MUST áp dụng bảng alias nhất quán cho biến thể khoảng trắng/gạch nối.
- MUST NOT đếm cùng một mục hai lần vì khác kiểu viết.
- Loại thành ngữ, phrasal verbs và biểu thức nhiều từ chưa nằm trong chính sách alias.

Nếu mở rộng sang multiword expressions, MUST tạo loại đơn vị hoặc thang đo riêng. Không được âm thầm cộng chúng vào `N`.

### 3.6. Vì sao không dùng word family

Một word family có thể gộp lemma gốc với nhiều dạng phái sinh dựa trên quy tắc hình thái và mức độ kiến thức giả định.

Biết `act` không bảo đảm biết `inaction`, `activation` hoặc mọi thành viên cùng họ.

Chọn lemma–POS vì:

1. Đơn vị có thể định danh và kiểm toán rõ ràng.
2. Giảm giả định về khả năng suy ra nghĩa từ hình thái.
3. Phù hợp hơn với ngân hàng item nhắm đến một nghĩa cụ thể.
4. Tránh khuếch đại số lượng từ được biết từ một đáp án đơn lẻ.

> Điểm của hệ thống MUST NOT được gọi là “điểm VST Paul Nation” hoặc chuyển trực tiếp sang số word families. Không tồn tại hệ số chuyển đổi phổ quát giữa hai đơn vị.

---

## 4. Polysemy — chính sách đa nghĩa

### 4.1. Phân biệt đơn vị đếm và đơn vị quan sát

- **Đơn vị đếm:** lemma–POS.
- **Đơn vị nội dung của item:** lemma–POS–target-sense.
- **Đơn vị quan sát:** một lần người dùng trả lời một item.

Một lemma có thể có nhiều nghĩa, nhưng trong thang đo chính mỗi lemma–POS đóng góp tối đa `1`.

### 4.2. Chính sách phiên bản đầu: một primary sense

Mỗi đơn vị MUST có đúng một `primary_target_sense`.

Primary sense được chọn theo:

1. Nghĩa chiếm ưu thế trong hỗn hợp corpus tham chiếu.
2. Bằng chứng từ concordance hoặc mẫu ngữ cảnh được gán nhãn.
3. Đối chiếu từ điển có thứ tự nghĩa theo tần suất, nếu có.
4. Xét duyệt chuyên gia và ghi nhận mức độ chắc chắn.

MUST NOT mặc định “nghĩa đầu tiên trong từ điển” là nghĩa phổ biến nhất.

Nếu hai nghĩa gần ngang nhau:

- Gắn `primary_sense_ambiguous: true`.
- Chọn một nghĩa theo quy tắc phân xử đã công bố.
- Giữ ổn định nghĩa đó trong phiên bản universe.
- Không luân phiên hai nghĩa như thể chúng đo cùng một nội dung.

### 4.3. Hệ quả diễn giải

Nhận biết nghĩa tài chính của `bank/NOUN`:

- Có thể tạo bằng chứng tích cực cho đơn vị này.
- Không chứng minh người dùng biết nghĩa “bờ sông”.
- Không được cộng hai đơn vị vì người dùng biết cả hai nghĩa.

Không nhận biết nghĩa đích cũng không chứng minh người dùng không biết bất kỳ nghĩa nào khác.

### 4.4. Mở rộng theo sense

Nếu nghiên cứu chiều sâu đa nghĩa, MAY định nghĩa thang riêng:

```text
q_u = Σ_s w_us × q_us

Σ_s w_us = 1

V_depth = Σ_u q_u
```

Hoặc đếm số sense đã biết trên một universe sense riêng.

Hai cách này có estimand khác nhau và MUST có tên, universe và phiên bản riêng. Không được trộn vào điểm primary-sense hiện tại.

---

## 5. Điều kiện quan sát chuẩn hóa

### 5.1. Dạng bài chính

Dạng bài mặc định:

- Hiển thị từ tiếng Anh mục tiêu.
- Cung cấp POS hoặc ngữ cảnh tối thiểu để khóa nghĩa.
- Cho bốn lựa chọn nghĩa và một lựa chọn “Không biết”.
- Chỉ có một đáp án đúng rõ ràng.
- Không giới hạn thời gian gắt đến mức đo tốc độ thay cho nhận biết.

Ngôn ngữ của đáp án MUST được gắn phiên bản trong `assessment_form`.

Nếu dùng tiếng Việt, kết quả phụ thuộc một phần vào khả năng hiểu tiếng Việt của người dùng. Nếu dùng định nghĩa tiếng Anh, kết quả phụ thuộc thêm vào khả năng đọc định nghĩa. Hai form MUST NOT được xem là tương đương khi chưa có nghiên cứu liên kết thang.

### 5.2. Ngữ cảnh

Ngữ cảnh MUST:

- Phân biệt POS và nghĩa đích.
- Không chứa diễn giải trực tiếp đáp án.
- Không cho phép suy ra đáp án chỉ bằng kiến thức đời sống hoặc mẹo ngữ pháp.

Nếu người không biết từ vẫn giải được nhờ ngữ cảnh, item đang đo thêm suy luận đọc hiểu và MUST được sửa hoặc mô hình hóa riêng.

### 5.3. Đáp án nhiễu

Distractor SHOULD tương đồng về:

- POS.
- Độ dài.
- Register.
- Tính hợp lý trong ngữ cảnh.

MUST tránh:

- Hai đáp án cùng đúng.
- Đáp án đúng luôn dài hơn.
- Gợi ý hình thái hoặc bản dịch quá hiển nhiên.
- Mẫu vị trí đáp án có thể dự đoán.

---

## 6. Primary Estimand — đại lượng ước lượng chính

### 6.1. Phân tầng

Chia universe thành `H` tầng không giao nhau:

```text
U = U₁ ∪ U₂ ∪ ... ∪ U_H

U_h ∩ U_k = ∅, khi h ≠ k

N_h = |U_h|

N = Σ_h N_h
```

Mặc định với `N = 20_000`:

```text
H = 20
N_h = 1_000
```

Tầng được xác định theo thứ hạng tần suất của **lemma–POS**, không phải word family.

Các tầng có thể được tái thiết kế sau pilot, nhưng MUST đóng băng trước khi chấm một form chính thức.

### 6.2. Xác suất nhận biết

Với người dùng `a` và đơn vị `u`, định nghĩa:

```text
q_au = xác suất nhận biết nghĩa đích của u
       trong điều kiện đo chuẩn hóa,
       tách khỏi thành công chỉ do đoán đáp án

0 ≤ q_au ≤ 1
```

Đây là biến tiềm ẩn cần suy luận từ mô hình đo lường, không phải giá trị quan sát trực tiếp.

Xác suất nhận biết trung bình ở tầng `h`:

```text
p_ah = (1 / N_h) × Σ_{u ∈ U_h} q_au
```

Đại lượng chính:

```text
V_a = Σ_h N_h × p_ah

V_hat_a = Σ_h N_h × p_hat_ah
```

Trong ngữ cảnh một người dùng, có thể viết gọn:

```text
V_hat = sum(h = 1..H, N_h * p_hat_h)
```

### 6.3. Ý nghĩa

`V_hat` là ước lượng tổng mức nhận biết kỳ vọng trên universe:

```text
0 ≤ V_hat ≤ N
```

Nếu một đơn vị có xác suất nhận biết `0,8`, nó đóng góp `0,8` vào kỳ vọng, không có nghĩa sản phẩm đã xác định chắc chắn một “phần của từ” mà người dùng biết.

Điểm là một ước lượng tổng hợp. Nó không cung cấp danh sách chắc chắn những từ đã biết hoặc chưa biết.

### 6.4. Không phải điểm có trọng số token

Mỗi lemma–POS trong universe có trọng số đếm bằng nhau.

Tần suất được dùng để xếp hạng và phân tầng, không làm một từ phổ biến đóng góp nhiều đơn vị hơn.

Do đó `V_hat` không đồng nghĩa với phần trăm từ người dùng hiểu khi đọc một văn bản. **Lexical coverage** là đại lượng khác và cần công thức riêng.

---

## 7. Recognition probability không phải raw percent correct

### 7.1. Mô hình quan sát tối thiểu

Gọi:

- `Y_ai = 1` nếu trả lời đúng item `i`.
- `q_au` là xác suất nhận biết nghĩa đích.
- `g_i` là xác suất trả lời đúng khi không nhận biết.
- `s_i` là xác suất trả lời sai dù có nhận biết.

Mô hình đơn giản:

```text
P(Y_ai = 1) =
    q_au × (1 − s_i)
  + (1 − q_au) × g_i

P(Y_ai = 1) =
    g_i + (1 − s_i − g_i) × q_au
```

Yêu cầu:

```text
0 ≤ g_i < 1 − s_i ≤ 1
```

Trong trường hợp tham số đồng nhất và đã biết:

```text
q_hat = (r_hat − g) / (1 − s − g)
```

Trong đó `r_hat` là tỷ lệ đúng thô.

### 7.2. Ví dụ minh họa

Giả sử:

```text
raw_accuracy = 0.70
g = 0.25
s = 0
```

Khi đó:

```text
recognition_estimate =
    (0.70 − 0.25) / (1 − 0.25)
  = 0.60
```

Một tầng có 1.000 đơn vị đóng góp khoảng 600 đơn vị nhận biết, không phải 700.

**Đây chỉ là ví dụ dưới giả định đã nêu.** Không phải công thức mặc định áp dụng cho mọi item.

### 7.3. Các giới hạn bắt buộc phải công bố

- Bốn lựa chọn không bảo đảm `g_i = 0,25`.
- Loại trừ một phần đáp án có thể làm xác suất đúng khi chưa nhận biết đầy đủ lớn hơn `0,25`.
- Distractor kém có thể làm `g_i` cao hơn nhiều.
- Lựa chọn “Không biết” thay đổi hành vi đoán.
- Một đáp án đúng không đủ để kết luận người dùng biết từ.
- Một đáp án sai không đủ để kết luận người dùng không biết từ.

Không thể nhận diện riêng `q`, `g` và `s` từ một đáp án nhị phân khi thiếu dữ liệu hiệu chuẩn và ràng buộc mô hình.

### 7.4. Chính sách suy luận

Production MUST sử dụng một mô hình đã hiệu chuẩn và được kiểm chứng. Ví dụ:

```text
q_ai = logistic(a_i × (θ_a − b_i))

P(Y_ai = 1) =
    g_i + (1 − s_i − g_i) × q_ai
```

Trong đó:

- `θ_a`: năng lực tiềm ẩn của người dùng.
- `b_i`: độ khó item.
- `a_i`: độ phân biệt.
- `g_i`: thành công khi chưa nhận biết.
- `s_i`: sai sót khi có nhận biết.

Mô hình MAY đơn giản hóa hoặc mở rộng, nhưng MUST ghi rõ:

- Tham số nào được cố định.
- Tham số nào được ước lượng.
- Nguồn dữ liệu hiệu chuẩn.
- Prior hoặc regularization.
- Bằng chứng về khả năng nhận diện tham số.
- Độ phù hợp và độ ổn định ngoài mẫu.

Không được coi thành phần logistic trong IRT tự động là “xác suất biết thật”. Cách diễn giải recognition cần được hỗ trợ bằng nghiên cứu hiệu lực, thí nghiệm distractor và dữ liệu đối chiếu.

### 7.5. “Không biết”, bỏ qua và hết giờ

- “Không biết” MUST được lưu thành một response category riêng.
- Bỏ qua và hết giờ MUST có mã riêng.
- Không được âm thầm gộp mọi loại thiếu dữ liệu thành “không biết”.
- Mô hình nhị phân chỉ được gộp các trạng thái khi đã hiệu chuẩn dưới cùng quy tắc.
- Nếu dùng mô hình đa thức, MUST mô tả xác suất của từng loại phản hồi.

---

## 8. Lấy mẫu và ngoại suy

### 8.1. Nguyên tắc đại diện

Các item dễ xây dựng không được mặc nhiên đại diện cho toàn bộ universe.

Nếu chỉ hỏi danh từ cụ thể nhưng ngoại suy sang động từ trừu tượng, từ chức năng và các mục đa nghĩa, kết quả có nguy cơ lệch hệ thống.

Ngân hàng item MUST được kiểm toán theo ít nhất:

- Tầng tần suất.
- POS.
- Mức độ trừu tượng.
- Register.
- Số nghĩa và mức mơ hồ của primary sense.
- Phương ngữ.
- Khả năng dịch hoặc viết định nghĩa.

### 8.2. Lấy mẫu xác suất

Với thiết kế lấy mẫu theo đơn vị từ vựng, xác suất chọn `π_u` MUST được biết và lớn hơn `0` đối với các đơn vị thuộc miền suy luận.

Dạng ước lượng có trọng số:

```text
p_hat_h =
    (1 / N_h) × Σ_{u ∈ sample_h} q_hat_au / π_u
```

Sai số của `q_hat_au` và thiết kế lấy mẫu đều phải được tính vào độ bất định.

### 8.3. Chấm điểm thích ứng

Trong CAT, tỷ lệ đúng trên các item đã chọn không phải ước lượng không chệch của tầng, vì item được chọn theo phản hồi trước đó.

CAT MUST:

1. Suy luận năng lực bằng mô hình hiệu chuẩn.
2. Dự đoán recognition cho universe hoặc mẫu tham chiếu đại diện.
3. Tổng hợp dự đoán theo `N_h`.
4. Kiểm chứng sai lệch và độ bao phủ khoảng bất định bằng mô phỏng và dữ liệu ngoài mẫu.

Nếu một phần universe chưa có item, mô hình ngoại suy MUST có bằng chứng đại diện cho phần đó. Tăng số item ở phần đã có không khắc phục được độ lệch do thiếu miền nội dung.

### 8.4. Tầng không có quan sát

Không có item ở tầng `h` không có nghĩa `p_hat_h = 0`.

Mô hình MAY suy luận tầng đó từ cấu trúc liên tầng, nhưng MUST:

- Đánh dấu đây là suy luận gián tiếp.
- Tăng độ bất định phù hợp.
- Không phát hành điểm nếu kết quả chủ yếu do prior mà chưa được kiểm chứng.

---

## 9. Độ bất định và quy tắc dừng

### 9.1. Tổng hợp posterior

Với mô hình Bayesian, ở mỗi mẫu posterior `b`:

```text
V_a^(b) = Σ_h N_h × p_ah^(b)
```

Báo cáo:

```text
V_hat = mean(V_a^(b))

interval_95 = [
    quantile(V_a^(b), 0.025),
    quantile(V_a^(b), 0.975)
]
```

Cách này giữ lại tương quan giữa các tầng.

Với cách tiếp cận frequentist:

```text
Var(V_hat) =
    Σ_h N_h² × Var(p_hat_h)
  + 2 × Σ_{h<k} N_h × N_k × Cov(p_hat_h, p_hat_k)
```

Không được bỏ covariance chỉ vì công thức đơn giản hơn.

### 9.2. Những nguồn bất định cần phân biệt

- Số lượng phản hồi hữu hạn.
- Lựa chọn item.
- Sai số hiệu chuẩn item.
- Tham số đoán và sai sót.
- Ngoại suy sang đơn vị chưa được kiểm tra.
- Đặc tả mô hình.
- Làm sạch universe và lựa chọn primary sense.

Khoảng điểm thống kê thông thường không tự động bao gồm hai nguồn cuối. Báo cáo kỹ thuật MUST nêu rõ khoảng đã bao gồm những nguồn nào.

### 9.3. Quy tắc dừng

Form chính thức MUST có cấu hình được phê duyệt gồm:

- Số item tối thiểu.
- Số item tối đa.
- Ngưỡng độ rộng khoảng bất định.
- Điều kiện bao phủ nội dung.
- Ngưỡng phát hiện phản hồi không đáng tin.

Không được dừng chỉ vì điểm trung bình “trông ổn định” khi độ bất định vẫn lớn hoặc các tầng chưa được bao phủ.

---

## 10. Hợp đồng báo cáo điểm

### 10.1. Các trường bắt buộc

| Trường | Ý nghĩa |
|---|---|
| `estimand_id` | Định danh đại lượng đo |
| `universe_id` | Phiên bản universe |
| `universe_size` | N thực tế |
| `unit_type` | `lemma_pos` |
| `sense_policy` | Chính sách nghĩa đích |
| `estimate` | `V_hat` |
| `interval` | Khoảng bất định và loại khoảng |
| `recognition_fraction` | `V_hat / N` |
| `raw_accuracy` | Chỉ số mô tả riêng, không phải recognition |
| `model_version` | Phiên bản mô hình |
| `calibration_version` | Phiên bản hiệu chuẩn |
| `assessment_form` | Dạng bài và ngôn ngữ đáp án |
| `quality_status` | Trạng thái chất lượng kết quả |
| `cefr` | Kết quả liên kết CEFR hoặc `null` |

Ví dụ minh họa, không phải kết quả thực nghiệm:

```json
{
  "estimand_id": "primary_sense_receptive_recognition",
  "universe_id": "en-lemma-pos-20k-v1",
  "universe_size": 20000,
  "unit_type": "lemma_pos",
  "sense_policy": "primary_sense_per_lemma_pos",
  "estimate": 6240,
  "interval": {
    "level": 0.95,
    "type": "bayesian_credible",
    "lower": 5450,
    "upper": 7060,
    "scope": "response_and_calibration_uncertainty"
  },
  "recognition_fraction": 0.312,
  "raw_accuracy": {
    "correct": 49,
    "scored_responses": 70,
    "value": 0.7
  },
  "model_version": "recognition-model-v1",
  "calibration_version": "calibration-v1",
  "assessment_form": "en-to-vi-4choice-v1",
  "quality_status": "reportable",
  "cefr": null
}
```

### 10.2. Làm tròn

- Backend MUST giữ giá trị chưa làm tròn.
- UI SHOULD làm tròn đến hàng trăm đối với universe 20.000.
- Cận khoảng hiển thị SHOULD làm tròn ra ngoài.
- Không hiển thị độ chính xác giả như “Bạn biết chính xác 6.243 từ”.

### 10.3. Cách diễn đạt được phép

> Bạn được ước lượng có khả năng nhận biết nghĩa đích của khoảng **6.200 đơn vị lemma–từ loại**, trong tập tham chiếu **20.000 đơn vị**. Khoảng bất định 95%: **5.400–7.100**.

Kèm giải thích:

> Kết quả phản ánh khả năng nhận biết nghĩa khi có lựa chọn trong điều kiện bài kiểm tra. Kết quả không chứng minh khả năng tự sử dụng các từ đó khi nói hoặc viết, và không cho biết bạn hiểu mọi nghĩa của mỗi từ.

### 10.4. Cách diễn đạt bị cấm

- “Bạn biết chính xác 6.200 từ tiếng Anh.”
- “Bạn có 6.200 word families.”
- “Bạn hiểu 31% mọi văn bản tiếng Anh.”
- “Bạn đạt B2” chỉ từ tổng số đơn vị nhận biết.
- “Bạn thành thạo 6.200 từ.”
- “Đây là tổng vốn từ tiếng Anh của bạn”, không giới hạn universe.

### 10.5. Trạng thái không đủ điều kiện báo cáo

Các trạng thái tối thiểu:

```text
reportable
insufficient_evidence
low_response_quality
out_of_calibration_population
ceiling_limited
floor_limited
model_unavailable
```

Khi không đủ bằng chứng, hệ thống MUST ưu tiên không phát hành điểm hơn là tạo một con số có vẻ chính xác.

Điểm chạm trần universe không có nghĩa người dùng không biết thêm từ ngoài universe.

---

## 11. CEFR mapping

### 11.1. Mặc định

```text
cefr_mapping_enabled = false
```

Không tồn tại bảng quy đổi phổ quát từ số lemma–POS được nhận biết sang CEFR.

CEFR mô tả năng lực sử dụng ngôn ngữ rộng hơn đáng kể so với recognition.

### 11.2. Điều kiện bật mapping

Chỉ được bật khi có nghiên cứu trên quần thể mục tiêu với:

1. Thước đo CEFR ngoài bài vocabulary và có chất lượng đã biết.
2. Đủ dữ liệu ở các mức cần báo cáo.
3. Phân tách dữ liệu xây dựng và kiểm định.
4. Đánh giá sai số phân loại và calibration.
5. Đánh giá khác biệt theo L1, tuổi và bối cảnh học.
6. Phiên bản mapping riêng.

SHOULD trả phân bố:

```text
P(CEFR level | vocabulary evidence, validated population)
```

Thay vì một nhãn cứng không kèm bất định.

### 11.3. Nhãn được phép

> Chỉ báo từ vựng có mức tương đồng với nhóm người học B1–B2 trong mẫu nghiên cứu đối chiếu.

Không được gọi đây là chứng chỉ hoặc kết luận CEFR tổng thể.

Nếu chưa có nghiên cứu:

```json
{
  "cefr": null,
  "cefr_status": "not_validated"
}
```

---

## 12. Lược đồ dữ liệu đo lường

### 12.1. Lexical unit

```text
unit_id
universe_id
canonical_lemma
lexical_pos
orthographic_variants[]
primary_target_sense_id
primary_sense_ambiguous
sense_selection_evidence[]
frequency_by_source{}
reference_score
frequency_rank
stratum_id
register_labels[]
inclusion_reason
review_status
```

### 12.2. Item

```text
item_id
item_version
unit_id
target_sense_id
assessment_form
surface_form
context
options[]
correct_option_id
dont_know_enabled
item_parameters
calibration_version
review_status
exposure_status
```

### 12.3. Response

```text
session_id
anonymous_participant_id
item_id
item_version
selected_option_id
response_category
is_correct
response_time_ms
selection_policy_version
position_in_session
timestamp
```

MUST lưu đủ thông tin để phân biệt thay đổi item với thay đổi năng lực. Dữ liệu cá nhân SHOULD được tối thiểu hóa và tách khỏi dữ liệu hiệu chuẩn.

---

## 13. Hiệu lực, độ tin cậy và công bằng

Trước khi phát hành chính thức, nghiên cứu MUST bao gồm:

### 13.1. Hiệu lực nội dung

- Đánh giá chất lượng lemma, POS và primary sense.
- Đánh giá độ đại diện của ngân hàng item.
- Phỏng vấn nhận thức để xác định người dùng dựa vào từ vựng hay mẹo đáp án.

### 13.2. Hiệu lực mô hình

- Kiểm tra độ phù hợp item.
- Kiểm tra local dependence.
- Đánh giá độ ổn định tham số.
- Kiểm tra mô hình guessing/slip.
- So sánh độ nhạy giữa các đặc tả hợp lý.

Một mô hình đơn chiều MUST NOT được coi là đúng chỉ vì thuận tiện triển khai.

### 13.3. Độ tin cậy

- Sai số theo vùng năng lực.
- Test–retest với kiểm soát hiệu ứng nhớ.
- Độ ổn định giữa các form tương đương.
- Độ bao phủ thực nghiệm của khoảng bất định.

Cronbach’s alpha đơn lẻ không đủ để nghiệm thu thang đo.

### 13.4. Công bằng

Đánh giá DIF theo các nhóm có đủ dữ liệu, đặc biệt:

- Ngôn ngữ mẹ đẻ.
- Ngôn ngữ đáp án.
- Mức tiếp xúc Anh–Mỹ.
- Bối cảnh giáo dục.
- Thiết bị và nhu cầu tiếp cận.

Nếu một item thuận lợi bất thường do cognate hoặc bản dịch, MUST ghi nhận, sửa hoặc xử lý trong mô hình.

---

## 14. Versioning và khả năng so sánh

Mỗi kết quả MUST gắn với bộ định danh:

```text
measurement_spec_version
universe_id
item_bank_version
model_version
calibration_version
assessment_form
cefr_mapping_version, nếu có
```

Những thay đổi sau có thể làm đổi nghĩa điểm:

- Đổi đơn vị lemma–POS sang word family.
- Đổi chính sách sense.
- Thêm multiword expressions.
- Đổi corpus hoặc trọng số.
- Đổi ngôn ngữ đáp án.
- Đổi mô hình correction cho guessing.
- Đổi thành phần universe dù N không thay đổi.

Điểm trước và sau thay đổi MUST NOT được so sánh trực tiếp khi chưa có nghiên cứu linking/equating.

Chia cho N để thành phần trăm không tự động làm hai universe tương đương.

---

## 15. Cổng nghiệm thu P0.1

### 15.1. Cổng A — định nghĩa và dữ liệu

- [ ] Universe có danh mục đầy đủ, bất biến và checksum.
- [ ] `actual_size` bằng số `unit_id` duy nhất.
- [ ] `Σ_h N_h = N`.
- [ ] Các tầng không giao nhau.
- [ ] Mỗi đơn vị có đúng một POS chuẩn.
- [ ] Mỗi đơn vị có đúng một primary target sense.
- [ ] Không đếm trùng biến thể chính tả hoặc biến tố.
- [ ] Corpus snapshot và giấy phép được ghi nhận.
- [ ] Quyết định loại rác, tên riêng và từ cổ có thể kiểm toán.

### 15.2. Cổng B — item và mô hình

- [ ] Item kiểm tra đúng nghĩa đích.
- [ ] Có dữ liệu hiệu chuẩn phù hợp với form.
- [ ] Không sử dụng raw percent correct làm recognition probability.
- [ ] Giả định guessing/slip được công bố và kiểm chứng.
- [ ] Độ đại diện cho các tầng được chứng minh.
- [ ] Quy tắc xử lý “Không biết” và missing được đóng băng.
- [ ] Quy tắc dừng được kiểm chứng.

### 15.3. Cổng C — kiểm thử toán học và suy luận

- [ ] `0 ≤ p_hat_h ≤ 1`.
- [ ] `0 ≤ V_hat ≤ N`.
- [ ] Nếu mọi `p_hat_h = 0`, thì `V_hat = 0`.
- [ ] Nếu mọi `p_hat_h = 1`, thì `V_hat = N`.
- [ ] Nếu mọi `p_hat_h = p`, thì `V_hat = N × p`.
- [ ] Thêm bản sao item không làm tăng N.
- [ ] Chỉ thay số lượng câu hỏi không làm đổi estimand.
- [ ] Mô phỏng người chỉ đoán không tạo ra ước lượng recognition cao có hệ thống.
- [ ] Khoảng bất định đạt mức bao phủ được đăng ký trước.
- [ ] Hành vi ở sàn, trần và ngoài mẫu hiệu chuẩn được kiểm tra.

### 15.4. Cổng D — báo cáo

- [ ] UI nêu rõ universe và đơn vị đếm.
- [ ] Điểm có khoảng bất định.
- [ ] Raw accuracy được tách khỏi recognition.
- [ ] Có disclaimer receptive, không productive.
- [ ] CEFR mặc định `null` khi chưa được xác thực.
- [ ] Không sử dụng nhãn VST/word family cho điểm lemma–POS.
- [ ] Kết quả có đủ version metadata để tái lập.

**Thiếu cổng A:** không được tuyên bố đã xác định universe.  
**Thiếu cổng B hoặc C:** chỉ được phát hành trải nghiệm pilot; không được công bố ước lượng quy mô vốn từ như điểm đã xác thực.  
**Thiếu cổng D:** không được phát hành báo cáo cho người dùng cuối.

---

## 16. Tóm tắt hợp đồng đo lường

```text
ĐO GÌ?
    Khả năng nhận biết tiếp nhận nghĩa đích phổ biến
    của các đơn vị lemma–POS trong universe đã đóng băng.

ĐẾM GÌ?
    Mỗi lemma–POS tối đa một đơn vị.
    Không đếm biến tố, biến thể chính tả hoặc mọi sense riêng.
    Không đồng nhất với word family.

NGOẠI SUY ĐẾN ĐÂU?
    Chỉ đến universe có N được ghi trong manifest.
    Không đến toàn bộ tiếng Anh.

ƯỚC LƯỢNG THẾ NÀO?
    V_hat = Σ_h N_h × p_hat_h

    p_hat_h là recognition probability được suy luận
    bằng mô hình đã hiệu chuẩn, không phải tỷ lệ đúng thô.

BÁO CÁO THẾ NÀO?
    Điểm ước lượng + khoảng bất định + universe + phiên bản
    + điều kiện kiểm tra + giới hạn diễn giải.

KHÔNG ĐƯỢC SUY DIỄN GÌ?
    Không suy ra productive vocabulary.
    Không suy ra biết mọi nghĩa.
    Không suy ra lexical coverage.
    Không suy ra CEFR tổng thể nếu chưa có xác thực.
```

> **Nguyên tắc tối hậu:** Một con số chỉ là điểm đo có ý nghĩa khi đơn vị đếm, tổng thể ngoại suy, điều kiện quan sát và giả định suy luận đều được định nghĩa, kiểm chứng và công bố.