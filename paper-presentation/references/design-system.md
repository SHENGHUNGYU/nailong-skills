# 視覺規範

簡約、學術、留白充足。顏色有固定語意：**橘色 = 異常／重點／本文方法**，**藍色 = 正常／對照**，灰色 = baseline 或次要資訊。同一份簡報內不要改變這個對應。

## 色票

| 用途 | Hex |
|---|---|
| 主背景（淺） | `#F6F5F1` |
| 次背景（概覽頁、結論頁） | `#ECEBE5` |
| 卡片底色 | `#FBFAF7` |
| 卡片邊框 | `#DEDCD4` |
| 深色（標題字、深色頁背景） | `#1C2430` |
| 內文字 | `#4A5361` |
| 註腳／頁碼 | `#646C78` |
| 強調橘（淺底上的字） | `#B4461A` |
| 強調橘（深底上的字） | `#F08A4B` |
| 橘色淺底（標籤、選取區） | `#F3DCCD` |
| 對照藍 | `#2C5F93` |
| 藍色淺底 | `#D6E3F0` |
| baseline 灰 | `#9AA1AB` |
| 深色頁上的次要字 | `#B9C2CE` |
| 深色頁上的註腳 | `#9AA4B2` |

深色頁（封面、研究問題、結尾）用 `#1C2430` 背景。

## 字型（deck.json 的 faces）

字型隨輸出語言而定，完整對照表在 `languages.md`。以下以繁體中文為例（範例頁面 `examples/` 也是繁中）：

```json
"faces": {
  "noto-serif-tc": {"family": "Noto Serif TC", "href": "https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@500;700&display=swap"},
  "noto-sans-tc": {"family": "Noto Sans TC", "href": "https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap"},
  "jetbrains-mono": {"family": "JetBrains Mono", "href": "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap"}
}
```

英文版改成 `source-serif-4`（Source Serif 4）與 `ibm-plex-sans`（IBM Plex Sans），JetBrains Mono 不變。

- **標題**：所選語言的襯線字型，例如 `'Noto Serif TC', Georgia, serif`，700
- **內文**：所選語言的無襯線字型，例如 `'Noto Sans TC', Arial, sans-serif`（設在 section 上）
- **數字、公式、章節標籤、頁碼**：`'JetBrains Mono', 'Courier New', monospace`（各語言共用）

沿用範例頁面時，用文字取代把所有 `Noto Serif TC`、`Noto Sans TC` 換成所選語言的字型，並把頁面上的固定字串換成 `languages.md` 的對應版本。

## 字級

| 用途 | 大小 |
|---|---|
| 封面標題、結尾「謝謝聆聽」 | 96–120px |
| 研究問題頁大字 | 80px |
| 頁面標題 h2 | 60px |
| 大數字 | 56–80px（mono） |
| 卡片標題 h3 | 32–40px |
| 內文 | 26–28px |
| 標籤、註腳、頁碼 | 24px（最小字級，不得更小） |

## 版面尺寸

- 畫布 1920×1080；內容頁 `padding:128px 128px 160px`，頁尾固定在 `bottom:64px`。
- 頁首區塊（章節標籤＋標題）高約 115px，加上 40px gap，**內容從 y ≈ 284 開始，到 y = 920 結束**（可用高度約 630px）。
- 估算：文字高 ≈ 字級 × 行數 × 行高；卡片高 ≈ 上下 padding + 各行高度總和。中文每行可容納字數 ≈ 框寬 ÷ 字級。
- 放 x-embed 時先算好它上方流式內容的底部 y，再把 embed 的 `top` 設在其下 30–40px，`top + height ≤ 920`。

## 標準內容頁骨架

```html
<section id="ID" data-transition="fade" style="background:#F6F5F1;color:#1C2430;font-family:'Noto Sans TC', Arial, sans-serif;padding:128px 128px 160px;display:flex;flex-direction:column;gap:40px">
<div style="display:flex;flex-direction:column;gap:12px">
<p style="font-family:'JetBrains Mono', 'Courier New', monospace;font-size:24px;color:#B4461A;letter-spacing:2px">03 · 方法 · STEP 1</p>
<h2 style="font-family:'Noto Serif TC', Georgia, serif;font-size:60px;font-weight:700;line-height:1.15;color:#1C2430">頁面標題（一句話講重點）</h2>
</div>
<!-- 內容 -->
<p style="position:absolute;left:128px;bottom:64px;width:1200px;font-size:24px;color:#646C78">作者 · 會議 年份｜原文 §3.2、Table 1</p>
<p style="position:absolute;right:128px;bottom:64px;width:240px;text-align:right;font-family:'JetBrains Mono', 'Courier New', monospace;font-size:24px;color:#646C78">09 / 20</p>
<aside>講稿……</aside>
</section>
```

- **章節標籤**格式：`NN · 章節名` 或 `NN · 章節名 · 子標題`，NN 對應大綱頁的段落編號（01 背景、02 問題、03 方法、04 實驗、05 評析；各語言的段落名見 `languages.md`）。
- **標題**寫成一句帶觀點的話（「決策週期一縮短，現有方法就掉分」），不要只寫名詞（「實驗結果」）。
- **頁尾左側**寫出處（原文章節、表格、圖號）；沒有特定出處時寫「作者 · 會議 年份」。

## 常用元件

**卡片**
```html
<div style="flex:1;display:flex;flex-direction:column;gap:10px;background:#FBFAF7;border:1px solid #DEDCD4;border-radius:16px;padding:28px">
<h3 style="font-size:32px;font-weight:700;line-height:1.2;color:#1C2430">標題</h3>
<p style="font-size:26px;line-height:1.5;color:#4A5361">說明</p>
</div>
```
強調卡（本文方法、最重要的一點）改用 `border:2px solid #B4461A`；深色重點卡用 `background:#1C2430`，字色 `#F6F5F1`／`#B9C2CE`，標籤用 `#F08A4B`。

**膠囊標籤**（如「輸出：初始集合 I₁」「+1.64 個百分點」）
```html
<p style="font-size:24px;color:#1C2430;background:#F3DCCD;border-radius:8px;padding:8px 14px;align-self:flex-start">輸出：初始集合 I₁</p>
```

**大數字**：mono 字型 56–80px，下方接 26px 說明文字；三個並排成一列最有力。

**公式卡**：三張並排的小卡，上方 24px 灰色步驟名（① 置中），下方 28px mono 公式。

**深色結論條**：`background:#1C2430;border-radius:16px;padding:32px 40px`，左側 `<x-icon name="Lightbulb">`（`#F08A4B`），右側 30px 白字，關鍵詞用 `<span style="color:#F08A4B">`。

**表格**：表頭列 `background:#1C2430`、白字；資料列交替 `#ECEBE5` 底；本文方法那一列用 `#F3DCCD` 底並加粗；數字欄靠右；字級 26px。

**圖示**：`<x-icon>` 只能用固定名稱（CheckCircle、Warning、Lightbulb、Clock、Search 等），顏色跟隨語意。

## 深色頁

- **封面**：深底，左上到中間放標題（96px serif；非英文版用譯名）、原文標題（30–36px；英文版若標題很長，可在這裡放副標題）、作者｜單位｜會議（28px），左下放「報告人：…　·　日期」（各語言字串見 `languages.md`）。下半部放一條全寬裝飾 SVG，內容要與主題相關，例如平穩基線中有一段升高的訊號曲線，或門檻線上下的偵測分數點。不放任何「書報討論」「PAPER READING」之類的標籤。
- **研究問題頁**：上方小標籤 `RESEARCH QUESTION`，一句 72–80px 大字的研究問題（關鍵詞橘色），下方兩個對比大數字。
- **結尾頁**：該語言的「謝謝聆聽」（120px；日、韓文字串較長時可降到 96px）＋「Q & A」44px 橘色 mono，下方用與封面相同的裝飾圖形，頁尾放完整引用。
