# Agent Skills installation and invocation research

Verified 2026-10-16 against opened official documentation. Paths below contain one child directory per skill, with `SKILL.md` and bundled resources inside that directory. Copy the entire skill directory.

| Tool | Recommended project root | Recommended user root | Invocation |
| --- | --- | --- | --- |
| Codex | `.agents/skills/` | `~/.agents/skills/` | CLI/IDE: `$paper-presentation` or `/skills`; desktop: select with `@` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | `/paper-presentation <request>` or matching natural language |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` | `/paper-presentation` or select with `@`; matching tasks can activate automatically |
| GitHub Copilot (VS Code agent mode and CLI) | `.github/skills/` | `~/.copilot/skills/` | `/paper-presentation <request>` or matching natural language |
| Gemini CLI | `.gemini/skills/` | `~/.gemini/skills/` | Ask explicitly to use `paper-presentation`; model calls `activate_skill`, with UI consent; `/skills list` and `/skills reload` manage discovery |
| Windsurf / Cascade | `.windsurf/skills/` (legacy, supported); current successor docs prefer `.devin/skills/` | `~/.codeium/windsurf/skills/` | `@paper-presentation <request>` or automatic matching |
| OpenCode | `.opencode/skills/` | `~/.config/opencode/skills/` | Ask agent to use `paper-presentation`; native `skill` tool loads it. A slash command is only exposed if `metadata: { opencode/slash: "true" }` is set |

## Official sources and important limitations

- [Claude Code skills](https://code.claude.com/docs/en/skills): local user skills do not automatically reach Cowork or cloud sessions. Project skills committed to repository are available to cloud sessions. Skill child directories may be symlinks. Plugin skills use `/plugin-name:skill-name`.
- [Cursor skills](https://cursor.com/docs/skills): `.agents/skills/` and `~/.agents/skills/` are supported, along with Claude/Codex compatibility roots. Only `~/.cursor/skills/` participates in optional Cloud Agent sync. Other global roots and unsynced personal skills stay local. Per-skill `disable-model-invocation: true` disables automatic invocation. [Cursor usage help](https://cursor.com/help/customization/skills) explicitly documents `/name` and `@` selection.
- [GitHub skills installation](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills): project alternatives `.claude/skills/` and `.agents/skills/`; personal alternative `~/.agents/skills/`. Skills work in agent mode, CLI, cloud agent, and code review. [VS Code agent skills](https://code.visualstudio.com/docs/agent-customization/agent-skills) also accepts `~/.claude/skills/` and documents slash invocation, `/skills` configuration, and frontmatter controls. Do not promise availability in every Copilot completion/chat mode.
- [Copilot CLI reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference): CLI supports `copilot skill` management and `/SKILL-NAME` direct invocation. Project `.github/skills/` is preferred, personal `~/.copilot/skills/`; `COPILOT_SKILLS_DIRS` permits extra roots.
- [Gemini CLI skills](https://geminicli.com/docs/cli/skills/): supports `.agents/skills/` and `~/.agents/skills/` aliases. Workspace wins over user; `.agents` wins over `.gemini` in the same scope. Native alternative: `gemini skills install https://github.com/SHENGHUNGYU/nailong-skills.git --path <skill-subdirectory> --scope user`; use `--scope workspace` for project installation. Native installation prompts for consent; do not include `--consent` by default. Natural-language activation is documented; do not invent `/paper-presentation` slash invocation.
- [Windsurf official skills URL](https://docs.windsurf.com/windsurf/cascade/skills) redirects to [Devin Desktop Cascade skills](https://docs.devin.ai/desktop/cascade/skills). Current preferred project root is `.devin/skills/`, while `.windsurf/skills/` remains explicitly supported. Alternative user root `~/.config/devin/skills/` is shared with Devin CLI. Current docs also support `.agents/skills/` and `~/.agents/skills/`. UI: Cascade → customization menu → Skills → Workspace / Global. Explicit invocation is `@skill-name`.
- [OpenCode skills](https://opencode.ai/docs/skills/): supports `.claude/skills/`, `~/.claude/skills/`, `.agents/skills/`, `~/.agents/skills/`. Requires frontmatter `name` to match directory (lowercase alphanumeric/hyphens) and description. Per-agent permission configuration may deny skill access. `metadata["opencode/slash"]: "true"` opt-in makes `/name` appear; plain standard skills should be invoked through natural language and the native tool.

## Installer design implications

Offer explicit tool target and project/user scope, preserve whole resource folders, refuse existing destinations unless user passes a replacement flag, and support dry-run. An `agents` shared target can cover many tools but not Claude Code's documented native discovery, so tool-specific roots are clearer. Never claim that copying skills installs agent applications or runtime dependencies. Reopening an agent session is a safe generic discovery refresh; Gemini additionally has `/skills reload`.

## Codex

[Official OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills) confirms `.agents/skills` discovery from the working directory up to the repository root, plus `~/.agents/skills` for user skills. CLI/IDE support `$name` and `/skills`; desktop selection uses `@`. Changes are detected automatically; restart if missing. `$skill-installer` can also download skills from other repositories. These paths support local authoring and setup; OpenAI recommends plugins for reusable distribution.

## Native installer alternatives

For Codex, ask `$skill-installer` to install `paper-presentation` from `https://github.com/SHENGHUNGYU/nailong-skills/tree/main/paper-presentation`.

For Gemini CLI, its documented native installer can download directly without cloning this repository first:

```bash
gemini skills install https://github.com/SHENGHUNGYU/nailong-skills.git --path paper-presentation --scope user
```

Run from your target workspace and use `--scope workspace` for a project installation. Native installation may request consent. Do not confuse Gemini's native `workspace` scope with this repository installer's `project` scope.

## 本專案的相容性摘要

- 安裝程式會保留完整資料夾；上方表格提供各工具的專案／個人路徑與官方使用來源。
- Claude Code、Cursor、Copilot 可用 `/paper-presentation`；Codex CLI/IDE 用 `$paper-presentation`；Windsurf 用 `@paper-presentation`。
- Gemini CLI 與 OpenCode 請使用自然語言指定 skill；不要假設所有工具都支援相同的 slash command。
- Windsurf 文件目前轉向 Devin Desktop；本安裝程式保留仍受支援的 Windsurf 路徑。
- 個人安裝不保證同步到雲端。PDF、網頁、動畫與 artifact 能力仍取決於 agent 的工具及權限。
- 本專案的 Gemini 安裝參數為 `--scope project`；官方原生安裝器的對應參數是 `--scope workspace`。

## Verification

The installer is tested with temporary directories, not by launching every agent application. Run `python3 -B -m unittest discover -s tests -v` from the repository root. The PowerShell wrapper is provided for Windows; live Windows execution must be verified on Windows.
