#!/usr/bin/env python3
"""Compile the speaker notes (<aside>) of a Slides artifact deck into a speaker-script Markdown file.

Usage:
    python3 -I build_script.py <deck-root> <output.md> [--lang en|zh-TW|zh-CN|ja|ko]
                               [--minutes 20] [--rate N] [--title TITLE]

<deck-root> is the folder that holds project/deck.json and project/slides/<id>.html.
Time per slide is estimated from the length of its notes: English counts words,
Chinese/Japanese/Korean count non-whitespace characters. Default speaking rates
(per minute): en 140 words, zh 350 chars, ja 330 chars, ko 280 chars.
Each slide gets at least 0.3 minutes. A warning is printed when the total exceeds --minutes.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

RATES = {"en": 140.0, "zh-TW": 350.0, "zh-CN": 350.0, "ja": 330.0, "ko": 280.0}

STR = {
    "en": {"title": "Speaker Script: {t}", "cover": "Cover", "page": "Slide {i} | {h}",
           "time": "*Suggested time: about {m} min (running total {a:.1f} min)*",
           "head": "> {n} slides, about {tot} min at roughly {r} {u} per minute. Adjust the pace on the day.",
           "unit": "words", "none": "(No notes on this slide.)"},
    "zh-TW": {"title": "講稿：{t}", "cover": "封面", "page": "第 {i} 頁｜{h}",
              "time": "*建議時間：約 {m} 分鐘（累計 {a:.1f} 分）*",
              "head": "> 共 {n} 頁，預估約 {tot} 分鐘（以每分鐘約 {r} {u}估算）。每頁標註建議時間，可依現場節奏調整。",
              "unit": "字", "none": "（本頁沒有講稿）"},
    "zh-CN": {"title": "讲稿：{t}", "cover": "封面", "page": "第 {i} 页｜{h}",
              "time": "*建议时间：约 {m} 分钟（累计 {a:.1f} 分）*",
              "head": "> 共 {n} 页，预估约 {tot} 分钟（以每分钟约 {r} {u}估算）。每页标注建议时间，可依现场节奏调整。",
              "unit": "字", "none": "（本页没有讲稿）"},
    "ja": {"title": "発表原稿：{t}", "cover": "表紙", "page": "スライド {i}｜{h}",
           "time": "*目安時間：約 {m} 分（累計 {a:.1f} 分）*",
           "head": "> 全 {n} 枚、約 {tot} 分（1 分あたり約 {r} {u}で試算）。当日のペースに合わせて調整してください。",
           "unit": "字", "none": "（このスライドには原稿がありません）"},
    "ko": {"title": "발표 원고: {t}", "cover": "표지", "page": "슬라이드 {i} | {h}",
           "time": "*권장 시간: 약 {m}분 (누적 {a:.1f}분)*",
           "head": "> 총 {n}장, 약 {tot}분 (분당 약 {r}{u} 기준). 현장 속도에 맞춰 조정하세요.",
           "unit": "자", "none": "(이 슬라이드에는 원고가 없습니다)"},
}


def plain(s: str) -> str:
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()


def detect(text: str) -> str:
    hangul = len(re.findall(r"[가-힯]", text))
    kana = len(re.findall(r"[぀-ヿ]", text))
    han = len(re.findall(r"[一-鿿]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    if hangul > 0.2 * (hangul + han + latin + 1):
        return "ko"
    if kana > 0.05 * (kana + han + 1):
        return "ja"
    if han > 0.3 * (han + latin + 1):
        return "zh-TW"
    return "en"


def length(text: str, lang: str) -> int:
    if lang == "en":
        return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-]*", text))
    return len(re.sub(r"\s", "", text))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("out")
    ap.add_argument("--lang", choices=sorted(RATES), default=None)
    ap.add_argument("--minutes", type=float, default=20.0)
    ap.add_argument("--rate", type=float, default=None)
    ap.add_argument("--title", default=None)
    a = ap.parse_args()

    root = Path(a.root)
    deck = json.loads((root / "project" / "deck.json").read_text(encoding="utf-8"))
    order = deck["order"]
    starts = {v["start"]: v["description"] for v in deck.get("sections", {}).values()}
    cover_id = deck.get("cover", order[0])

    raw = []
    for sid in order:
        src = (root / "project" / "slides" / f"{sid}.html").read_text(encoding="utf-8")
        m = re.search(r"<h[12][^>]*>(.*?)</h[12]>", src, re.S)
        n = re.search(r"<aside>(.*?)</aside>", src, re.S)
        raw.append((sid, plain(m.group(1)) if m else sid, html.unescape(n.group(1).strip()) if n else None))

    lang = a.lang or detect(" ".join(r[2] or "" for r in raw))
    L = STR[lang]
    rate = a.rate or RATES[lang]
    title = a.title or deck.get("title", "")

    pages = []
    for sid, head, note in raw:
        if sid == cover_id:
            head = L["cover"]
        size = length(note or "", lang)
        pages.append((sid, head, note or L["none"], max(0.3, round(size / rate, 1)), size))

    total = sum(p[3] for p in pages)
    total_size = sum(p[4] for p in pages)
    lines = [f"# {L['title'].format(t=title)}", "",
             L["head"].format(n=len(pages), tot=round(total), r=int(rate), u=L["unit"]), ""]
    acc = 0.0
    for i, (sid, head, note, mins, _) in enumerate(pages, 1):
        if sid in starts:
            lines += ["---", "", f"## {starts[sid]}", ""]
        acc += mins
        lines += [f"### {L['page'].format(i=i, h=head)}", "", L["time"].format(m=mins, a=acc), "", note, ""]
    Path(a.out).write_text("\n".join(lines), encoding="utf-8")

    cap = int(rate * a.minutes)
    print(f"[{lang}] {len(pages)} slides, {total_size} {STR['en']['unit'] if lang == 'en' else 'chars'}, "
          f"about {total:.1f} min (cap for {a.minutes:g} min: {cap}) -> {a.out}")
    if total > a.minutes * 1.05:
        print(f"WARNING: script runs about {total - a.minutes:.1f} min over the {a.minutes:g}-minute target; "
              f"trim roughly {total_size - cap} {'words' if lang == 'en' else 'characters'} from the notes.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
