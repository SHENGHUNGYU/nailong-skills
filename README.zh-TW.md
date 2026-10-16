# nailong-skills

[English](README.md) | 繁體中文

這是我在日常使用 AI、實驗與反覆修正的過程中，逐漸建立的個人 skills 集合。

我把值得重複使用的工作流程整理成指令、參考資料、範例與輔助腳本，讓 AI 助理更穩定地產出實用成果，也保留實際任務中累積的經驗。這些 skills 會隨著使用經驗持續調整與擴充。

## 現有 skills

| Skill | 用途 | 主要產出 |
| --- | --- | --- |
| [paper-presentation](paper-presentation/SKILL.md) | 將學術論文轉為書報討論、研討課或讀書會素材。 | 論文摘要與評論、簡報、逐頁講稿。 |

## 安裝方式

下載專案後，選擇對應工具執行安裝程式。需要 Python 3，不需要額外套件。

```bash
git clone https://github.com/SHENGHUNGYU/nailong-skills.git
cd nailong-skills

# 先預覽，再將所有 skills 安裝到個人帳號範圍
sh scripts/install.sh --agent codex --scope user --dry-run
sh scripts/install.sh --agent codex --scope user
```

SSH 替代方式：`git clone git@github.com:SHENGHUNGYU/nailong-skills.git`。

### 支援的 agent 工具

官方文件查核日期：**2026-10-16**。每個安裝目錄下都會放入完整的 `<skill-name>/` 資料夾。請從下表選擇 `--agent`；需要其他工具時，再執行一次安裝。

| 工具 | `--agent` | 專案安裝目錄 | 個人安裝目錄 |
| --- | --- | --- | --- |
| Codex | `codex` | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `cursor` | `.cursor/skills/` | `~/.cursor/skills/` |
| GitHub Copilot | `copilot` | `.github/skills/` | `~/.copilot/skills/` |
| Gemini CLI | `gemini-cli` | `.gemini/skills/` | `~/.gemini/skills/` |
| Windsurf / Cascade | `windsurf` | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| OpenCode | `opencode` | `.opencode/skills/` | `~/.config/opencode/skills/` |

表格列出本安裝程式選用的原生路徑，並非各工具支援的全部位置。OpenCode 會遵循已設定的 `XDG_CONFIG_HOME`。Windsurf 目前的文件已導向 Devin Desktop，上表的舊版 Windsurf 路徑仍列為支援。詳見[官方來源與相容性說明](docs/agent-compatibility.md)。

### 安裝到既有專案

```bash
sh scripts/install.sh --agent claude-code --scope project \
  --project /path/to/your-project --skill paper-presentation
```

預設範圍為 `--scope user`。專案範圍必須明確提供已存在的 `--project` 目錄，不會自動安裝到剛下載的 skills 專案中。不指定 `--skill` 時安裝全部，也可以重複使用此參數選擇多個 skills。

### Windows / PowerShell

```powershell
.\scripts\install.ps1 --agent cursor --scope user --dry-run
.\scripts\install.ps1 --agent cursor --scope user
# 也可以直接執行 Python
py -3 scripts/install.py --agent copilot --scope project --project "C:\work\my-project"
```

如果 PowerShell 執行原則阻擋腳本，請直接執行 Python 指令。macOS/Linux 的對應方式為 `python3 scripts/install.py ...`。

### 更新或移除已安裝的 skill

```bash
git pull --ff-only
sh scripts/install.sh --agent codex --scope user --skill paper-presentation --force
```

安裝程式會複製 `SKILL.md`、參考資料、範例與腳本，不會連線下載，也不會安裝 agent 工具或 Python。目的資料夾已存在時會回報錯誤；加上 `--force` 才會先將舊資料夾移到 `skills/` 同層的 `nailong-skills-backups/`，再安裝新版，並顯示備份路徑。備份放在載入目錄外，避免被重複辨識為 skill。每個 skill 都會先完成暫存複製，但多個 skills 的安裝不是單一交易。程式不接受含符號連結的目的路徑或 skill 內容；遇到此情況請改用一般目錄。

移除時，只需刪除上表目錄下對應的 `<skill-name>/`。還原時，先將目前版本移出載入目錄，再將顯示的備份資料夾搬回 `skills/<skill-name>/`。修改或更新本專案不會自動同步到已安裝副本。

### 使用需求

- 支援 Agent Skills 的 agent 版本，以及讀取 skill 與相關檔案的權限。
- 論文來源可以是 PDF、可讀取的連結或貼上的文字；讀取能力依 agent 提供的工具而異。
- 產生 HTML 或投影片的能力；專用 Slides artifact 並非必要，skill 提供 HTML 替代流程。
- 安裝與講稿輔助腳本需要 Python 3，兩者都僅使用標準函式庫。

## 使用方式

### 在各 agent 中呼叫

安裝後，請在 agent 中開啟目標專案。如果沒有出現 skill，請開始新工作階段，或使用下列重新載入方式。

| 工具 | 使用方式 |
| --- | --- |
| Codex CLI / IDE | 輸入 `$paper-presentation` 並附上需求，或透過 `/skills` 選擇；桌面版有提供 skill 選單時可用 `@` 選取。 |
| Claude Code | `/paper-presentation 請根據這篇論文製作 20 分鐘的報告。` |
| Cursor | 選擇 `/paper-presentation`，或使用 `@` 提及 skill。 |
| Copilot VS Code agent 模式 / CLI | `/paper-presentation 請根據這篇論文製作 20 分鐘的報告。` |
| Gemini CLI | 輸入「請使用 paper-presentation skill 處理這篇論文」，依提示核准啟用；用 `/skills list` 查看、`/skills reload` 重新載入。 |
| Windsurf / Cascade | 輸入 `@paper-presentation` 後接需求。 |
| OpenCode | 輸入「請使用 paper-presentation skill 處理這篇論文」，由 agent 使用 skill 工具載入。本專案未啟用 OpenCode 選用的 slash command metadata。 |

工具允許時，也能透過自然語言自動匹配。檔案安裝成功不代表雲端工作階段、PDF 讀取、artifact 或其他工具一定可用。[相容性與官方使用來源](docs/agent-compatibility.md)另有能力限制與原生安裝方式。

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
├── scripts/                  # Installer: Python, sh, PowerShell
├── tests/                    # Installer tests
├── docs/agent-compatibility.md
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
