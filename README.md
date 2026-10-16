# nailong-skills

English | [繁體中文](README.zh-TW.md)

A personal collection of AI skills, built gradually through everyday use, experimentation, and feedback.

This repository turns workflows I want to reuse into instructions, reference material, examples, and helper scripts. The goal is to help AI assistants produce more consistent, useful results, while preserving lessons learned from real tasks.

## Available skills

| Skill | Purpose | Main outputs |
| --- | --- | --- |
| [paper-presentation](paper-presentation/SKILL.md) | Turn academic papers into journal-club, seminar, or reading-group material. | Critical paper brief, slide deck, and speaker script. |

## Installation

Clone the repository, then run the installer for your tool. Python 3 is required; no extra packages are needed.

```bash
git clone https://github.com/SHENGHUNGYU/nailong-skills.git
cd nailong-skills

# Preview, then install all bundled skills for your user account
sh scripts/install.sh --agent codex --scope user --dry-run
sh scripts/install.sh --agent codex --scope user
```

SSH alternative: `git clone git@github.com:SHENGHUNGYU/nailong-skills.git`.

### Supported agents

Official documentation checked on **2026-10-16**. Each destination contains a complete `<skill-name>/` directory. Pick one `--agent` value below; run the installer again for another tool.

| Tool | `--agent` | Project destination | User destination |
| --- | --- | --- | --- |
| Codex | `codex` | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `cursor` | `.cursor/skills/` | `~/.cursor/skills/` |
| GitHub Copilot | `copilot` | `.github/skills/` | `~/.copilot/skills/` |
| Gemini CLI | `gemini-cli` | `.gemini/skills/` | `~/.gemini/skills/` |
| Windsurf / Cascade | `windsurf` | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| OpenCode | `opencode` | `.opencode/skills/` | `~/.config/opencode/skills/` |

These are the installer's selected native paths, not every directory each tool supports. OpenCode respects `XDG_CONFIG_HOME` when set. Windsurf's current documentation redirects to Devin Desktop; the legacy Windsurf paths above remain documented as supported. See [official sources and compatibility notes](docs/agent-compatibility.md).

### Install into an existing project

```bash
sh scripts/install.sh --agent claude-code --scope project \
  --project /path/to/your-project --skill paper-presentation
```

`--scope user` is the default. Project scope requires an explicit existing `--project` directory; it does not silently install into the cloned skills repository. Omit `--skill` to install all skills, or repeat it to select several.

### Windows / PowerShell

```powershell
.\scripts\install.ps1 --agent cursor --scope user --dry-run
.\scripts\install.ps1 --agent cursor --scope user
# Direct Python alternative (also works on macOS/Linux)
py -3 scripts/install.py --agent copilot --scope project --project "C:\work\my-project"
```

If your PowerShell policy blocks scripts, use the direct Python command. On macOS/Linux, the equivalent is `python3 scripts/install.py ...`.

### Update or remove an installed skill

```bash
git pull --ff-only
sh scripts/install.sh --agent codex --scope user --skill paper-presentation --force
```

The installer copies `SKILL.md`, references, examples, and scripts. It makes no network requests and does not install agent applications or Python. Existing destinations cause an error; `--force` moves each previous folder to `nailong-skills-backups/` beside the `skills/` directory before replacement, and prints the backup path. Backups sit outside discovery to avoid duplicate skills. Copying is staged per skill; a multi-skill install is not one transaction. Symlinked destinations and skill contents are rejected; choose a regular directory if this applies to your setup.

To uninstall, remove only the installed `<skill-name>/` folder at the destination shown in the table. To restore a backup, move the current skill out of discovery and move the printed backup folder back under `skills/<skill-name>/`. Copies do not update automatically when you edit or pull this repository.

### Requirements

- An agent version with Agent Skills support and permission to read the skill and its supporting files.
- A paper provided as a PDF, reachable link, or pasted text; PDF/link reading depends on the agent's tools.
- HTML or slide generation capabilities for presentation output. A dedicated Slides artifact is optional because the skill includes an HTML fallback.
- Python 3 for installation and the bundled speaker-script helper; both use only the standard library.

## Usage

### Invoke in your agent

After installation, open your target project in the agent. If the skill is not discovered, start a new session or reload as noted below.

| Tool | Usage |
| --- | --- |
| Codex CLI / IDE | Type `$paper-presentation` with your request, or select it through `/skills`. In the desktop skill selector, use `@` when available. |
| Claude Code | `/paper-presentation Prepare a 20-minute talk from this paper.` |
| Cursor | Select `/paper-presentation` or mention the skill with `@`. |
| Copilot in VS Code agent mode / CLI | `/paper-presentation Prepare a 20-minute talk from this paper.` |
| Gemini CLI | Ask `Use the paper-presentation skill for this paper.` Approve activation when prompted; `/skills list` and `/skills reload` inspect and refresh skills. |
| Windsurf / Cascade | `@paper-presentation` followed by the request. |
| OpenCode | Ask `Use the paper-presentation skill for this paper.` The agent loads it with its skill tool. This repository does not enable OpenCode's optional slash-command metadata. |

Natural-language matching is also available when enabled by the host. A successful file installation does not guarantee access to cloud sessions, PDF readers, artifact creation, or other tools. [Compatibility notes and official usage sources](docs/agent-compatibility.md) describe the boundaries and native installer alternatives.

Provide the paper, desired outputs, language, and presentation constraints:

```text
Use the paper-presentation skill in this repository.
Read paper-presentation/SKILL.md and its referenced files.

Paper: [attach a PDF or paste an arXiv link]
Create an English journal-club presentation for about 20 minutes.
Include a critical paper brief, a slide deck, and a full speaker script.
```

For Traditional Chinese:

```text
請使用 paper-presentation skill，閱讀附上的論文，
製作約 20 分鐘的繁體中文書報討論報告，
包含論文摘要與評論、簡報及逐頁講稿。
```

You can request just one deliverable, such as only the brief. Outputs default to English; the current skill also supports Traditional Chinese, Simplified Chinese, Japanese, and Korean on request.

## Outputs

| Deliverable | Format | Contents |
| --- | --- | --- |
| Paper brief | Markdown | Reviewer-style analysis, evidence assessment, limitations, and verdict. |
| Slide deck | Slides artifact when available; otherwise standalone HTML | About 18–22 slides for a 20-minute talk, with animated method and result explanations. |
| Speaker script | Markdown | Slide-by-slide narration, timing estimates, and total duration. |
| PDF | Exported from the slide interface or printed from HTML | Static slides; animations become still frames. |

These are generated deliverables, not prebuilt presentations bundled with the repository. Artifact availability, sharing, and export controls depend on the host application. File naming follows the skill's language-specific instructions.

### Compile speaker notes

For a structured deck containing `project/deck.json` and `project/slides/<id>.html`, run from the repository root:

```bash
python3 -I paper-presentation/scripts/build_script.py \
  /path/to/deck-root \
  /path/to/speaker-script.md \
  --lang en --minutes 20
```

Replace the example paths with your deck directory and output filename. Use `--lang zh-TW` for Traditional Chinese. The helper extracts each slide's `<aside>` notes, estimates speaking time, and warns if the total exceeds the target. It expects the structured deck layout above; standalone HTML requires separate notes extraction.

## Repository structure

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

## Development and feedback

These skills evolve through practical use and corrections. When adding or improving a skill, document its purpose, input requirements, workflow, expected outputs, and dependencies. Keep reusable examples and references alongside the instructions.

Suggestions and reproducible feedback are welcome through [GitHub issues](https://github.com/SHENGHUNGYU/nailong-skills/issues). Include the skill name, relevant input, expected behavior, and actual result.
