---
name: paper-presentation
description: Turn an academic paper (PDF, arXiv link, or pasted text) into a complete journal-club / seminar package — ① a reviewer-style paper brief (Markdown), ② a ~20-minute minimal slide deck with animated diagrams of the method and key results (Slides artifact, exportable to PDF), and ③ a full slide-by-slide speaker script. Output is in English by default, or in Traditional Chinese, Simplified Chinese, Japanese or Korean on request. Handles both method papers and evaluation/benchmark papers. Use this whenever the user shares a paper and mentions a paper presentation, journal club, seminar, reading group, 書報討論, 論文報告, 論文快報, 讲稿, 論文紹介, 논문 발표, speaker notes or script, or wants to explain a paper to classmates or an advisor — even if they ask for only one of the three outputs (then produce just that part).
---

# Paper presentation: brief + deck + speaker script

This skill turns one paper into journal-club material ready to present. The style and quality bar come from a finished deck that the user reviewed and corrected item by item. Those corrections are written into the rules below; follow them rather than reinventing the approach.

Default outputs (produce only the parts the user asks for, if they ask for fewer):

| Output | Form | Notes |
|---|---|---|
| Paper brief | Markdown file in the working directory | Reviewer-style analysis: five sections plus a verdict |
| Slide deck | Slides artifact (one HTML file per slide) | About 20 slides / 20 minutes, minimal, animated mechanisms |
| Speaker script | Markdown file | Compiled automatically from each slide's speaker notes, with time estimates |
| PDF | Exported from the deck | Share › Export › PDF (animations become still frames) |

## Language

**Default to English.** Switch only when the user asks for another language: Traditional Chinese (`zh-TW`), Simplified Chinese (`zh-CN`), Japanese (`ja`) or Korean (`ko`). All three outputs use the same language. Fonts, file names, fixed on-slide strings, script length caps and layout differences per language are in `references/languages.md`; read it before planning.

Keep model names, dataset names, metrics and technical terms in their original English. In non-English output, give the English term in parentheses the first time it appears. Word choice should be professional but not obscure.

## Workflow

### 1. Read the whole paper and build a fact list

- Read every page (PDFs in batches of ≤ 20 pages with `pages`), including figures, tables, appendices and footnotes.
- Record as you go: every table number (copied exactly, including decimals), what each figure is meant to show, equation numbers and symbol definitions, hyperparameters, dataset sizes, hardware and speed, and limitations the authors admit.
- This list is the only source for everything that follows. **Never invent numbers or quotes.** Values read off a plot are always labelled as read by eye from Fig. N. Where the paper is unclear (for example, a table with no dataset named), say so plainly and explain how you inferred it.

### 2. Decide the paper type and the language

- **Paper type:** method paper (proposes a model or algorithm) or evaluation/benchmark paper (builds a benchmark or systematically evaluates existing systems). The decision rule and an outline for each are in `references/slide-plan.md`.
- **Language:** English unless the user named another (see above).

State both in your one-line assumption before you start, so the user can correct you. Don't wait for a reply.

### 3. Write the paper brief

Follow the structure in `references/brief-template.md` (section headings in the chosen language: `references/languages.md`). The key is a **reviewer's critical eye**:

- Section 4 must judge whether the data actually support each claim (supported / partly supported / only on par).
- Section 5 must point out design flaws, unverified assumptions, fairness problems and situations the paper didn't consider.

This critique also feeds the limitations slide and the script.

### 4. Plan the deck

Use the outline in `references/slide-plan.md` that matches the paper type. Adapt the number of method or evaluation-design slides to the paper, but keep the deck at about 18–22 slides and the script within the length cap for the chosen language.

If the presenter's name or date is unknown, use placeholders (`[Name]`, `[Date]`, or the chosen language's equivalent) and list them in your final reply. If the working directory already holds outputs from another paper, put this paper's files in a subfolder named after it rather than overwriting.

### 5. Build the deck

**Medium:** if the Artifact tool is available, create an artifact from the Slides type and write `project/deck.json` and `project/slides/<id>.html` as the type's returned instructions describe (send deck.json plus the cover first, then three slides per batch). Without the Artifact tool, build a single HTML file instead: one 1920×1080 `<section>` per slide, left/right arrow keys to change slides, and `@media print` so each slide prints on its own page for PDF output.

**Visual rules:** read `references/design-system.md` (palette, type scale, header and footer, card styles, layout arithmetic) and `references/languages.md` (fonts and fixed strings). `references/examples/` holds real finished slides (start with its `INDEX.md`). They are the most direct template: new slides of the same kind should look the same. Copy their structure and styling and replace only the content.

**Animation:** use `<x-embed>` for small auto-looping animations of the method, key mechanisms and result charts. Read `references/embeds.md` for the boilerplate and how to draw each chart type.

**Rules the user corrected** (each one is real feedback, and each has a reason):

1. **No click-to-reveal.** Don't use `data-build-in`; everything appears as soon as the slide opens. Stepwise reveals make the presenter click repeatedly on stage and invite mistakes.
2. **Nothing in the normal flow below an animation (x-embed).** In testing, an x-embed covered the flow content beneath it, and it flashed during slide changes. Put cards and text above or beside the animation; the animation takes the bottom block of the slide.
3. **No "seminar / paper reading" label on the cover.** The cover holds only the title, the original title (if translated), authors / affiliations / venue and year, the presenter and date, and one decorative graphic related to the topic.
4. **The conclusion slide is titled simply "Conclusion"** (in the chosen language), and the deck never mentions the paper brief (it's a separate document).
5. **The limitations slide holds only the 3 most important points**, as three large columns. Put the rest of the critique in the brief.
6. **No separate "discussion questions" slide.**
7. **The last slide holds only "Thank You", "Q & A" and the full citation** — no take-aways.
8. **At most 4 experiment slides.** Secondary analyses go into the script or the brief, not onto extra slides.
9. **Animations must apply the paper's formulas faithfully.** Label illustrative data as illustrative on the slide. If a formula produces a counter-intuitive result (for example, a cumulative sum that shifts the selected segment later), don't tune the data to make it "look right". Annotate the animation to explain why, and explain it in the script too — the audience will ask.
10. **Credit redrawn charts**, e.g. "Curves redrawn by eye from Fig. 1; endpoints from Table 1". If an axis doesn't start at 0, say so on the chart ("Axis starts at 60").
11. **Page numbers as `NN / total`.** Update all of them when slides are added or removed. When the script says "we'll come back to this later", that later slide must actually exist.

When the deck is done, don't keep taking screenshots to check it yourself. Give the user the link and ask them to flip through it once; fix what they report.

### 6. Speaker script

Each slide's speaker notes go in the `<aside>` at the end of its `<section>`, as plain text. The notes are the script:

- Spoken and plain-spoken. Walk the audience through the animation ("In the animation below, the orange dot is…"), use analogies for abstract mechanisms, and explain anything counter-intuitive before someone asks.
- On results slides, say the exact numbers and gaps, and point out what deserves doubt.
- **Keep the total within the cap for the chosen language** (`references/languages.md`: about 2,800 English words or 7,000 Chinese characters for 20 minutes). Budget about 0.5 minutes each for the cover, roadmap and closing, the most time for the method section, and about 1 minute for every other slide.

When all slides are done, compile the notes into the script file with the bundled script. It detects the language, estimates time per slide, and warns if the total exceeds the target:

```bash
python3 -I <skill-dir>/scripts/build_script.py <deck-root> <output-dir>/<script-file-name> --lang en --minutes 20
```

`<deck-root>` is the folder containing `project/deck.json`. `--lang` takes `en`, `zh-TW`, `zh-CN`, `ja` or `ko` (detected automatically if omitted); `--minutes` is the target length. If it warns that the script is too long, trim the notes and rerun. Rerun it after any change to the notes.

### 7. PDF and handoff

The user exports the PDF from the deck page via Share › Export › PDF. Animations are flattened to still frames, so suggest presenting from the web deck's present mode.

The final reply includes: the deck link, links to both Markdown files, the paper type and language used, placeholders still to fill in, which charts were redrawn by eye or use illustrative data, the estimated total time, and a note that the deck is private until shared.
