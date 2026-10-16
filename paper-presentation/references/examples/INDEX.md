# 範例頁面索引

以下是實際完成並經使用者修正後的簡報頁（論文：Real-Time Weakly Supervised Video Anomaly Detection，WACV 2024）。這是一篇方法型論文、繁體中文版。內容是該論文專屬的，**沿用的是版面、元件、字級、色彩與講稿寫法**，不是內容。用於其他語言時，替換字型與固定字串（`languages.md`）；用於評測型論文時，頁面結構依 `slide-plan.md` 的 B 型架構調整，元件樣式仍照這些範例。

| 檔案 | 頁型 | 看什麼 |
|---|---|---|
| deck.json | 索引 | order、sections（五段）、faces 的寫法 |
| cover.html | 封面（深色） | 標題區、報告人／日期、裝飾 SVG 曲線 |
| agenda.html | 大綱 | 五欄卡片＋時間預算，方法卡橘框 |
| question.html | 研究問題（深色） | 80px 大字＋兩個對比大數字 |
| bottleneck.html | 問題成因 | 左右對比卡＋底部深色結論條 |
| idea.html | 方法總覽 | 步驟卡＋箭頭＋弱→強漸層條 |
| knn.html | 方法步驟（左文右動畫） | 編號步驟、公式卡、散點動畫 |
| smoothing.html | 方法步驟（上公式下動畫） | 三張公式卡、累積和動畫、反直覺標註 |
| mlp.html | 方法步驟（左文右對照卡） | 兩個門檻設計的對照 |
| details.html | 實作細節 | 設定表格＋資料陷阱卡 |
| datasets.html | 資料集 | 大數字卡片＋比較設定註記 |
| results.html | 主結果 | 雙面板長條圖動畫 |
| efficiency.html | 效率 | 三個大數字＋等比例延遲長條 |
| ablation.html | 消融 | 舊值→新值大數字＋差距膠囊 |
| summary.html | 結論 | 2×2 卡片，標題「結論」 |
| limits.html | 限制與盲點 | 三欄大卡，最重要的一點橘框 |
| closing.html | 結尾（深色） | 謝謝聆聽＋Q&A＋引用，無 take-aways |

每頁的 `<aside>` 就是該頁講稿，可參考語氣與長度。
