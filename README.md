# nailong-skills

English | [繁體中文](README.zh-TW.md)

A personal collection of AI skills, built gradually through everyday use, experimentation, and feedback.

This repository turns workflows I want to reuse into instructions, reference material, examples, and helper scripts. The goal is to help AI assistants produce more consistent, useful results, while preserving lessons learned from real tasks.

## Available skills

| Skill | Purpose | Main outputs |
| --- | --- | --- |
| [paper-presentation](paper-presentation/SKILL.md) | Turn academic papers into journal-club, seminar, or reading-group material. | Critical paper brief, slide deck, and speaker script. |

## Installation

Clone with HTTPS:

```bash
git clone https://github.com/SHENGHUNGYU/nailong-skills.git
cd nailong-skills
```

Or use SSH with a configured GitHub SSH key:

```bash
git clone git@github.com:SHENGHUNGYU/nailong-skills.git
```

Copy the complete skill folder into the skills directory supported by your AI tool. Installation paths and discovery rules depend on the tool; follow its installation instructions. Keep `SKILL.md`, `references/`, and `scripts/` together.

Alternatively, use an assistant that can read local files and ask it to follow `paper-presentation/SKILL.md` and its referenced files directly. Automatic skill discovery is optional for this approach.

### Requirements

- An AI assistant that can read the instructions and supporting files.
- A paper provided as a PDF, a reachable link, or pasted text.
- HTML or slide generation capabilities for presentation output.
- Python 3 for the speaker-script helper, which uses only the standard library.

## Usage

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
