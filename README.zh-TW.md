# nailong-skills

[English](README.md) | 繁體中文

這是我在日常使用 AI、實驗與反覆修正的過程中，逐漸建立的個人 skills 集合。

我把值得重複使用的工作流程整理成指令、參考資料、範例與輔助腳本，讓 AI 助理更穩定地產出實用成果，也保留實際任務中累積的經驗。這些 skills 會隨著使用經驗持續調整與擴充。

## 現有 skills

| Skill | 用途 | 主要產出 |
| --- | --- | --- |
| [paper-presentation](paper-presentation/SKILL.md) | 將學術論文轉為書報討論、研討課或讀書會素材。 | 論文摘要與評論、簡報、逐頁講稿。 |

## 安裝方式

透過 HTTPS 下載：

```bash
git clone https://github.com/SHENGHUNGYU/nailong-skills.git
cd nailong-skills
```

如果已設定 GitHub SSH 金鑰，也可以使用：

```bash
git clone git@github.com:SHENGHUNGYU/nailong-skills.git
```

將完整的 skill 資料夾複製到 AI 工具支援的 skills 目錄。安裝位置與自動載入規則依工具而異，請依該工具的安裝說明操作。請保留 `SKILL.md`、`references/` 與 `scripts/`，避免缺少流程需要的資料與工具。

如果 AI 助理能讀取本機檔案，也能直接指定 `paper-presentation/SKILL.md`，要求依照指令與引用檔案執行，不需要依賴自動載入功能。

### 使用需求

- 能讀取指令與相關檔案的 AI 助理。
- 可存取的論文來源：PDF、可讀取的連結或貼上的文字。
- 製作簡報時，需要產生 HTML 或投影片的能力。
- 執行講稿輔助腳本需要 Python 3；腳本僅使用標準函式庫。

## 使用方式

提供論文、需要的產出、語言與報告限制：

```text
請使用這個專案中的 paper-presentation skill。
先閱讀 paper-presentation/SKILL.md 與它引用的檔案。

論文：[附上 PDF 或貼上 arXiv 連結]
請製作約 20 分鐘的繁體中文書報討論報告，
包含論文摘要與評論、簡報及完整逐頁講稿。
```

需要英文產出時：

```text
Use the paper-presentation skill to turn the attached paper
into a 20-minute English journal-club presentation.
Include a critical paper brief, a slide deck, and a full speaker script.
```

也可以只要求其中一項，例如只產出論文摘要與評論。預設產出語言為英文；目前的 skill 也支援依要求使用繁體中文、簡體中文、日文或韓文。

## 產出內容

| 產出 | 格式 | 內容 |
| --- | --- | --- |
| 論文摘要與評論 | Markdown | 以審稿角度分析論文、評估證據與限制，並提出整體判斷。 |
| 簡報 | 支援時使用 Slides artifact，否則產生獨立 HTML | 約 18–22 頁、20 分鐘，包含方法與重要結果的動畫說明。 |
| 逐頁講稿 | Markdown | 各頁口語講解、建議時間與總時長估算。 |
| PDF | 由簡報介面匯出，或從 HTML 列印 | 靜態投影片；動畫會轉為靜態畫面。 |

以上是執行 skill 後生成的成果，並非專案已附上的完整簡報。Artifact、分享與匯出功能取決於使用的平台，實際檔案命名以 skill 的語言規則為準。

### 從投影片筆記產生講稿

若簡報具有 `project/deck.json` 與 `project/slides/<id>.html` 結構，可在專案根目錄執行：

```bash
python3 -I paper-presentation/scripts/build_script.py \
  /path/to/deck-root \
  /path/to/speaker-script.md \
  --lang zh-TW --minutes 20
```

請將範例路徑換成簡報資料夾與講稿輸出檔名。英文講稿使用 `--lang en`。腳本會擷取每頁 `<aside>` 中的筆記、估算講述時間，並在超過目標時長時提出提醒。此工具需要上述結構；獨立 HTML 簡報需要另外擷取筆記。

## 專案結構

```text
nailong-skills/
├── README.md
├── README.zh-TW.md
└── paper-presentation/
    ├── SKILL.md
    ├── references/
    │   ├── brief-template.md
    │   ├── design-system.md
    │   ├── embeds.md
    │   ├── examples/
    │   ├── languages.md
    │   └── slide-plan.md
    └── scripts/
        └── build_script.py
```

## 持續改進與回饋

這些 skills 來自實際任務與使用後的修正。新增或調整 skill 時，請說明適用情境、輸入需求、工作流程、預期產出與相依工具，並將可重複使用的範例與參考資料放在同一個 skill 資料夾中。

歡迎透過 [GitHub issues](https://github.com/SHENGHUNGYU/nailong-skills/issues) 提供建議或可重現的問題，附上 skill 名稱、相關輸入、預期行為與實際結果。
