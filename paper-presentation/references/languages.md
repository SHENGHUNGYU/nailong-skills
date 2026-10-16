# 語言設定

**預設輸出語言是英文。** 使用者明確指定其他語言時（例如「用繁體中文」「简体中文」「日本語で」「한국어로」），改用該語言。開工時的一行假設說明中要寫出採用的語言，讓使用者有機會更正。

支援的語言代碼：`en`（英文，預設）、`zh-TW`（繁體中文）、`zh-CN`（简体中文）、`ja`（日本語）、`ko`（한국어）。

一份產出內的三樣東西（快報、簡報、講稿）都用同一種語言。專有名詞、模型名稱、資料集名稱、指標名稱保留英文原文；非英文版本中，術語第一次出現時附上英文。

## 字型（deck.json 的 faces）

每種語言用三個字型：標題用襯線、內文用無襯線、數字與公式用 JetBrains Mono（各語言共用）。

| 語言 | 標題（serif） | 內文（sans） |
|---|---|---|
| en | `Source Serif 4`（wght 600;700） | `IBM Plex Sans`（wght 400;500;700） |
| zh-TW | `Noto Serif TC`（500;700） | `Noto Sans TC`（400;500;700） |
| zh-CN | `Noto Serif SC`（500;700） | `Noto Sans SC`（400;500;700） |
| ja | `Noto Serif JP`（500;700） | `Noto Sans JP`（400;500;700） |
| ko | `Noto Serif KR`（500;700） | `Noto Sans KR`（400;500;700） |

`faces` 的 key 是字型名稱轉小寫、空白換成 `-`；`href` 格式為 `https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@500;700&display=swap`（空白換成 `+`）。投影片中的字型堆疊：標題 `'<Serif>', Georgia, serif`，內文 `'<Sans>', Arial, sans-serif`。

## 動畫（x-embed）中的系統字型堆疊

x-embed 讀不到簡報字型，要用系統字型：

| 語言 | font-family |
|---|---|
| en | `-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,sans-serif` |
| zh-TW | `-apple-system,BlinkMacSystemFont,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif` |
| zh-CN | `-apple-system,BlinkMacSystemFont,"PingFang SC","Noto Sans SC","Microsoft YaHei",sans-serif` |
| ja | `-apple-system,BlinkMacSystemFont,"Hiragino Sans","Noto Sans JP","Yu Gothic",sans-serif` |
| ko | `-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",sans-serif` |

## 輸出檔名

| 語言 | 快報 | 講稿 |
|---|---|---|
| en | `Paper-Brief.md` | `Speaker-Script.md` |
| zh-TW | `論文閱讀快報.md` | `講稿.md` |
| zh-CN | `论文阅读快报.md` | `讲稿.md` |
| ja | `論文要約.md` | `発表原稿.md` |
| ko | `논문요약.md` | `발표원고.md` |

工作目錄中若已有同名檔案（例如上一篇論文的），放進以論文簡稱命名的子資料夾，不要覆蓋。

## 講稿長度上限（20 分鐘）

講稿長度依語速估算，上限 = 語速 × 目標分鐘數。目標不是 20 分鐘時等比例調整。

| 語言 | 計數單位 | 語速（每分鐘） | 20 分鐘上限 |
|---|---|---|---|
| en | 英文單字 | 140 | 約 2,800 words |
| zh-TW／zh-CN | 非空白字元 | 350 | 約 7,000 字 |
| ja | 非空白字元 | 330 | 約 6,600 字 |
| ko | 非空白字元 | 280 | 約 5,600 字 |

把上限當作總預算來分配：封面、大綱、結尾各約 0.5 分鐘；方法段最多；其餘每頁約 1 分鐘。`scripts/build_script.py` 會依同樣的語速估算總時長，並在超過目標時提出警告；超過時請刪減講稿，而不是加快語速。

## 固定字串

各頁型用到的固定文字。`{n}`、`{v}` 代入圖號或數值。

| 用途 | en | zh-TW | zh-CN | ja | ko |
|---|---|---|---|---|---|
| 大綱頁標題 | Today’s Roadmap | 今天的報告路線 | 今天的报告路线 | 本日の流れ | 오늘의 발표 순서 |
| 段落名 01–05 | Background / Problem / Method / Experiments / Critique | 背景 / 問題 / 方法 / 實驗 / 評析 | 背景 / 问题 / 方法 / 实验 / 评析 | 背景 / 課題 / 手法 / 実験 / 考察 | 배경 / 문제 / 방법 / 실험 / 평가 |
| 結論頁標題 | Conclusion | 結論 | 结论 | 結論 | 결론 |
| 限制頁標題 | Limitations & Blind Spots | 潛在限制與盲點 | 潜在局限与盲点 | 限界と盲点 | 한계와 맹점 |
| 結尾頁大字 | Thank You | 謝謝聆聽 | 谢谢聆听 | ご清聴ありがとうございました | 경청해 주셔서 감사합니다 |
| 封面報告人 | Presenter: | 報告人： | 报告人： | 発表者： | 발표자: |
| 示意資料 | Illustrative data | 示意數據 | 示意数据 | 説明用データ | 예시 데이터 |
| 截斷座標軸 | Axis starts at {v} | 軸自 {v} 起 | 轴自 {v} 起 | 軸は {v} から | 축은 {v}부터 |
| 重繪圖表 | Redrawn by eye from Fig. {n} | 依原文 Fig. {n} 目測重繪 | 依原文 Fig. {n} 目测重绘 | 原論文 Fig. {n} を目視で再描画 | 원문 Fig. {n}을 육안으로 재작성 |
| 限制頁頁尾 | Presenter’s critique, not from the paper | 報告人評析，非原文內容 | 报告人评析，非原文内容 | 発表者による考察（論文の記述ではない） | 발표자 평가(원문 내용 아님) |

`AGENDA`、`RESEARCH QUESTION`、`STEP 1`、`Q & A` 這類 mono 字型的英文小標，所有語言都保留英文。

## 版面差異

- **字寬**：中日韓文字每字約 1 × 字級寬；英文平均每字元約 0.5–0.55 × 字級。同樣框寬下，英文每行可容納的字元數約是中文的兩倍，但同一句話的英文通常也長約 1.5–2 倍。
- **標題長度**：60px 標題在 1664px 寬內，中日韓約 26 字、英文約 50 字元以內可放一行；超過就改寫得更短，不要縮字級。
- **英文的單字不會斷行**：卡片寬度要能放下最長的單字（約 0.6 × 字級 × 字元數），尤其注意 `RLCDAlignBench` 這類長名稱。
- **英文標點**：用彎引號 “ ” 與撇號 ’，HTML 屬性與程式碼中才用直引號。
- **快報的區塊標題**：英文版用 `1. Core Research Problem`、`2. Key Contributions & Novelty`、`3. Methodology & Pipeline`、`4. Main Findings — Do the Results Support the Claims?`、`5. Limitations & Blind Spots`、`6. Reviewer Verdict`；其他語言照 `brief-template.md` 的結構翻譯。
