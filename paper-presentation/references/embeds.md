# 動畫（x-embed）寫法

`<x-embed>` 是放在投影片上的小型沙盒網頁（iframe），可以跑 JS 與 SVG 動畫。用它來演示方法機制與關鍵數據。

## 限制與規則

- 必須是 `<section>` 的**直接子元素**，且 `position:absolute` 並給 `left/top/width/height`。
- 每個 ≤ 16 KB，每頁 ≤ 8 個；無網路、不能載入外部字型，用所選語言的系統字型堆疊（見 `languages.md`；英文為 `-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,sans-serif`）。下方範例用的是繁中字型堆疊，沿用時記得替換。
- 文字 ≥ 24px（以 viewBox 座標計）。
- **SVG 的 `viewBox` 設成與 embed 相同的寬高**（例如 embed 1664×330，就用 `viewBox="0 0 1664 330"`），座標可直接對應投影片像素。
- **embed 下方不能有流式內容**（會被蓋住、切頁時閃爍）。卡片和文字放在 embed 上方或側邊。若需要佔位讓側邊內容排版，在流式版面中放同尺寸的空 `<div>`，但它只能與 embed 並排，不能在 embed 之上把其他內容往下推到 embed 底下。
- 動畫要**自動循環**：`run()` 結尾 `setTimeout(run, 週期)`，週期 10–16 秒，讓講者講解時隨時看得到完整過程。
- PDF 匯出時 embed 會被攤平成某一瞬間的靜態畫面。
- 顏色沿用簡報色票：橘 `#B4461A`、淺橘 `#F3DCCD`、亮橘 `#F08A4B`、藍 `#2C5F93`、淺藍 `#D6E3F0`、灰 `#9AA1AB`、深 `#1C2430`、內文 `#4A5361`、註腳 `#646C78`、卡片 `#FBFAF7`、邊框 `#DEDCD4`。

## 忠實性

- 機制動畫要**直接套用論文公式**計算（在 JS 裡實作 Eq.），而不是手畫出「理想」的樣子。
- 示意資料用固定種子的亂數（`let sd=5;const R=()=>(sd=(sd*16807)%2147483647)/2147483647;`），每次播放都一樣，並在畫面角落標「示意數據」。
- 若公式產生反直覺結果，在動畫最後一段加文字標註解釋（例如「證據要累積到異常尾端才達峰 → 選取偏後（拖尾）」），講稿也要說明。
- 重繪論文的圖時，在頁尾註明「依原文 Fig. N 目測重繪；端點取自 Table M」。截斷座標軸要在圖上標示。

## 骨架

```html
<x-embed style="position:absolute;left:128px;top:530px;width:1664px;height:330px"><!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;height:100%;background:transparent;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}svg{display:block;width:100%;height:100%}.f{transition:opacity .6s}</style></head><body><svg viewBox="0 0 1664 330"></svg><script>
const S=document.querySelector('svg'),N='http://www.w3.org/2000/svg';
function E(t,a,p){const e=document.createElementNS(N,t);for(const k in a)e.setAttribute(k,a[k]);(p||S).appendChild(e);return e}
function T(x,y,s,a,p){const e=E('text',Object.assign({x:x,y:y,'font-size':24,fill:'#4A5361'},a),p);e.textContent=s;return e}
function tw(d,f,cb){const t0=performance.now();(function s(t){const p=Math.min(1,(t-t0)/d);f(1-Math.pow(1-p,3));if(p<1)requestAnimationFrame(s);else if(cb)cb()})(t0)}
// 建立靜態元素……
function run(){ /* 重設狀態 → 用 setTimeout 排程各階段 */ setTimeout(run,12000) }
run();
</script></body></html></x-embed>
```

- `E()` 建立 SVG 元素，`T()` 建立文字，`tw()` 做補間動畫（ease-out）。
- 淡入淡出：元素加 `class:'f'`，改 `style.opacity`。
- 長條成長：`tw(700,p=>rect.setAttribute('width',w*p))`。
- 折線逐步畫出：用 `clipPath` 的 rect 寬度從 0 長到全寬。
- 純 SVG 的循環移動（不需 JS）：`<circle><animate attributeName="cx" values="75;1450" dur="6s" begin="-2s" repeatCount="indefinite"/></circle>`；負的 `begin` 可讓多個點錯開。

## 圖型對照

| 想演示的東西 | 做法 | 範例 |
|---|---|---|
| 任務設定（片段、標籤、看不到的真值） | 一排方格依序淡入 → 標籤膠囊出現 → 真值片段變色＋括號註解 | 範例 1 |
| 流程比較 | 方塊＋箭頭，資料點用 SMIL 沿線移動，色塊框出可訓練範圍，第二列延遲淡入 | 範例 2 |
| 動機圖（效能 vs 參數） | 對數 x 軸折線，clipPath 逐步畫出 → 關鍵區間淡入 → 本文星號彈出 | 範例 3 |
| 距離／鄰居類機制 | 散點圖＋移動中的查詢點，連線到 k 個最近鄰，右側長條同步成長 | 範例 4 |
| 時序累積／平滑／門檻選取 | 上排長條（正負）、下排累積曲線逐點延伸、門檻虛線、選取區段底色、反直覺處加註 | 範例 5 |
| 推論過程（滑動視窗） | 底片條＋移動的視窗框，每移一格下方長條成長，超過門檻變橘 | 範例 6 |
| 主結果比較 | 雙面板水平長條，baseline 先長、本文最後長，虛線標最佳 baseline，最後浮現差距 | 範例 7 |

以下範例取自實際完成的簡報（REWARD，WACV 2024，方法型論文，繁中），可直接改數值與文字沿用；動畫中的文字與「示意數據」等字串要換成所選語言。評測型論文常用的圖型（多列流程比較、成對條件比較、split-half 選擇膨脹）可用同樣的骨架組合：成對比較是「灰色基準長條＋彩色增量長條」，split-half 是「上下兩排長條，上排標出被選者、下排標出它的實際分數與最佳者的差距」。

## 範例 1：任務設定：片段與看不到的真值

```html
<x-embed style="position:absolute;left:128px;top:530px;width:1664px;height:330px"><!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;height:100%;background:transparent;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}svg{display:block;width:100%;height:100%}</style></head><body><svg viewBox="0 0 1664 330"></svg><script>
const S=document.querySelector('svg'),N='http://www.w3.org/2000/svg';
function E(t,a,p){const e=document.createElementNS(N,t);for(const k in a)e.setAttribute(k,a[k]);(p||S).appendChild(e);return e}
function T(x,y,s,a,p){const e=E('text',Object.assign({x:x,y:y},a),p);e.textContent=s;return e}
function F(e){e.style.transition='opacity .5s, fill .6s';e.style.opacity=0;return e}
T(0,98,'異常影片',{'font-size':30,'font-weight':700,fill:'#1C2430'});
T(0,258,'正常影片',{'font-size':30,'font-weight':700,fill:'#1C2430'});
const A=[],Q=[],B=[];
for(let i=0;i<16;i++){const x=200+i*75;
A.push(F(E('rect',{x:x,y:40,width:68,height:90,rx:8})));
Q.push(F(T(x+34,97,'?',{'font-size':32,'text-anchor':'middle','font-weight':700})));
B.push(F(E('rect',{x:x,y:200,width:68,height:90,rx:8,fill:'#D6E3F0'})));}
function pill(y,s,c){const g=F(E('g',{}));E('rect',{x:1424,y:y,width:236,height:54,rx:27,fill:c},g);T(1542,y+36,s,{'font-size':26,'text-anchor':'middle',fill:'#FBFAF7','font-weight':700},g);return g}
const t1=pill(58,'影片標籤：異常','#B4461A'),t2=pill(218,'影片標籤：正常','#2C5F93');
const br=F(E('path',{d:'M800 136 v8 h293 v-8',fill:'none',stroke:'#B4461A','stroke-width':3}));
const cap=F(T(946,176,'真正的異常片段（訓練時看不到）',{'font-size':24,'text-anchor':'middle',fill:'#B4461A','font-weight':700}));
const goal=F(T(832,326,'目標：只靠「影片層級」標籤，學會判斷每一個片段是否異常',{'font-size':26,'text-anchor':'middle',fill:'#4A5361'}));
function run(){
A.forEach((r,i)=>{r.style.opacity=0;r.style.fill='#E2E0D8';Q[i].style.opacity=0;Q[i].textContent='?';Q[i].style.fill='#646C78';B[i].style.opacity=0});
[t1,t2,br,cap,goal].forEach(e=>e.style.opacity=0);
A.forEach((r,i)=>setTimeout(()=>{r.style.opacity=1;Q[i].style.opacity=1;B[i].style.opacity=1},200+i*90));
setTimeout(()=>{t1.style.opacity=1;t2.style.opacity=1},2000);
setTimeout(()=>{for(let i=8;i<12;i++){A[i].style.fill='#F3DCCD';Q[i].textContent='!';Q[i].style.fill='#B4461A'}br.style.opacity=1;cap.style.opacity=1},3600);
setTimeout(()=>{goal.style.opacity=1},5000);
setTimeout(run,10500)}
run();
</script></body></html></x-embed>
```

## 範例 2：流程比較（純 SVG／SMIL）

```html
<x-embed style="position:absolute;left:128px;top:284px;width:1664px;height:620px"><!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;height:100%;background:transparent;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}svg{display:block;width:100%;height:100%}</style></head><body>
<svg viewBox="0 0 1664 620" font-family="-apple-system,BlinkMacSystemFont,'PingFang TC','Noto Sans TC','Microsoft JhengHei',sans-serif">
<text x="0" y="34" font-size="30" font-weight="700" fill="#1C2430">主流 wVAD 流程</text>
<rect x="780" y="58" width="530" height="144" rx="16" fill="#D6E3F0" stroke="#2C5F93" stroke-width="2" stroke-dasharray="10 8"/>
<text x="1045" y="240" text-anchor="middle" font-size="24" font-weight="700" fill="#2C5F93">只有這段可訓練 · MIL／度量學習損失</text>
<line x1="75" y1="130" x2="1450" y2="130" stroke="#9AA1AB" stroke-width="3"/>
<g fill="#B4461A">
<circle cy="130" r="10"><animate attributeName="cx" values="75;1450" dur="6s" begin="0s" repeatCount="indefinite"/></circle>
<circle cy="130" r="10"><animate attributeName="cx" values="75;1450" dur="6s" begin="-2s" repeatCount="indefinite"/></circle>
<circle cy="130" r="10"><animate attributeName="cx" values="75;1450" dur="6s" begin="-4s" repeatCount="indefinite"/></circle>
</g>
<g fill="#9AA1AB"><polygon points="196,122 210,130 196,138"/><polygon points="556,122 570,130 556,138"/><polygon points="786,122 800,130 786,138"/><polygon points="1056,122 1070,130 1056,138"/><polygon points="1336,122 1350,130 1336,138"/></g>
<g stroke="#1C2430" stroke-width="2" font-size="26" text-anchor="middle">
<rect x="0" y="70" width="150" height="120" rx="12" fill="#FBFAF7"/>
<rect x="210" y="70" width="300" height="120" rx="12" fill="#E2E0D8" stroke="#9AA1AB"/>
<rect x="570" y="70" width="150" height="120" rx="12" fill="#FBFAF7"/>
<rect x="800" y="70" width="240" height="120" rx="12" fill="#FBFAF7"/>
<rect x="1070" y="70" width="220" height="120" rx="12" fill="#FBFAF7"/>
<rect x="1350" y="70" width="200" height="120" rx="12" fill="#FBFAF7"/>
</g>
<g font-size="26" text-anchor="middle" fill="#1C2430">
<text x="75" y="139">影片</text>
<text x="360" y="122">預訓練擷取器</text><text x="360" y="158" fill="#646C78">I3D（凍結）</text>
<text x="645" y="139">特徵</text>
<text x="920" y="122">特徵編碼器</text><text x="920" y="158" fill="#646C78">（如 MTN）</text>
<text x="1180" y="139">分類器</text>
<text x="1450" y="139">異常分數</text>
</g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="1.2s" dur="0.8s" fill="freeze"/>
<text x="0" y="334" font-size="30" font-weight="700" fill="#B4461A">REWARD 流程</text>
<rect x="190" y="358" width="1120" height="144" rx="16" fill="#F3DCCD" stroke="#B4461A" stroke-width="2" stroke-dasharray="10 8"/>
<text x="750" y="540" text-anchor="middle" font-size="24" font-weight="700" fill="#B4461A">整個模型端到端訓練 · BCE 損失（片段偽標籤）</text>
<line x1="75" y1="430" x2="1450" y2="430" stroke="#9AA1AB" stroke-width="3"/>
<g fill="#B4461A">
<circle cy="430" r="10"><animate attributeName="cx" values="75;1450" dur="3s" begin="0s" repeatCount="indefinite"/></circle>
<circle cy="430" r="10"><animate attributeName="cx" values="75;1450" dur="3s" begin="-1s" repeatCount="indefinite"/></circle>
<circle cy="430" r="10"><animate attributeName="cx" values="75;1450" dur="3s" begin="-2s" repeatCount="indefinite"/></circle>
</g>
<g fill="#9AA1AB"><polygon points="196,422 210,430 196,438"/><polygon points="1336,422 1350,430 1336,438"/></g>
<g stroke="#1C2430" stroke-width="2">
<rect x="0" y="370" width="150" height="120" rx="12" fill="#FBFAF7"/>
<rect x="210" y="370" width="1080" height="120" rx="12" fill="#FBFAF7"/>
<rect x="1350" y="370" width="200" height="120" rx="12" fill="#FBFAF7"/>
</g>
<g font-size="26" text-anchor="middle" fill="#1C2430">
<text x="75" y="439">影片</text>
<text x="750" y="422" font-weight="700">特徵擷取器 ＋ 分類器</text><text x="750" y="458" fill="#646C78">Uniformer-32 · 單一模型</text>
<text x="1450" y="439">異常分數</text>
</g>
<text x="832" y="604" text-anchor="middle" font-size="26" fill="#4A5361">推論時：主流需兩段模型＋聚合整段影片；REWARD 只需一個模型、看 6.4 秒</text>
</g>
</svg></body></html></x-embed>
```

## 範例 3：動機圖：對數軸折線＋星號

```html
<x-embed style="position:absolute;left:128px;top:284px;width:1040px;height:620px"><!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;height:100%;background:transparent;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}svg{display:block;width:100%;height:100%}#star{transform-box:fill-box;transform-origin:center;transition:opacity .5s,transform .6s cubic-bezier(.3,1.6,.5,1)}.f{transition:opacity .6s}</style></head><body><svg viewBox="0 0 1040 620"></svg><script>
const S=document.querySelector('svg'),N='http://www.w3.org/2000/svg';
function E(t,a,p){const e=document.createElementNS(N,t);for(const k in a)e.setAttribute(k,a[k]);(p||S).appendChild(e);return e}
function T(x,y,s,a,p){const e=E('text',Object.assign({x:x,y:y,'font-size':24,fill:'#4A5361'},a),p);e.textContent=s;return e}
const L0=Math.log2(4.266),L1=Math.log2(273);
const X=v=>140+(Math.log2(v)-L0)/(L1-L0)*800, Y=v=>520-(v-72)/16*480;
const zone=E('g',{class:'f'});
E('rect',{x:120,y:40,width:X(30)-120,height:480,fill:'#F3DCCD',opacity:.6},zone);
T(318,508,'即時區間（< 30 s）',{'text-anchor':'middle',fill:'#B4461A','font-weight':700},zone);
[74,78,82,86].forEach(v=>{E('line',{x1:120,x2:960,y1:Y(v),y2:Y(v),stroke:'#DEDCD4','stroke-width':1.5});T(108,Y(v)+8,v,{'text-anchor':'end'})});
E('line',{x1:120,x2:960,y1:520,y2:520,stroke:'#9AA1AB','stroke-width':2});
const xs=[4.266,8.533,17.066,34.133,68.266,136.533,273],xl=['4.3','8.5','17','34','68','137','273'];
xs.forEach((v,i)=>T(X(v),556,xl[i],{'text-anchor':'middle'}));
T(540,604,'決策週期（秒，對數座標）',{'text-anchor':'middle'});
T(0,0,'AUC (%)',{transform:'translate(34 280) rotate(-90)','text-anchor':'middle'});
const defs=E('defs',{}),cp=E('clipPath',{id:'c'},defs),cr=E('rect',{x:100,y:0,width:0,height:620},cp);
const G=E('g',{'clip-path':'url(#c)'});
const ser=[{n:'S3R',c:'#2C5F93',d:[81.8,81.34,82.0,83.5,85.0,85.8,85.99],s:''},
{n:'RTFM',c:'#1C2430',d:[81.6,80.63,81.9,82.8,83.7,84.0,84.3],s:'10 7'},
{n:'MGFN',c:'#8A919B',d:[73.5,81.76,81.3,82.0,82.9,83.4,83.45],s:'4 6'}];
ser.forEach(o=>{E('polyline',{points:o.d.map((v,i)=>X(xs[i])+','+Y(v)).join(' '),fill:'none',stroke:o.c,'stroke-width':4,'stroke-dasharray':o.s,'stroke-linejoin':'round'},G);
o.d.forEach((v,i)=>E('circle',{cx:X(xs[i]),cy:Y(v),r:6,fill:o.c},G));
T(X(273)+14,Y(o.d[6])+8,o.n,{fill:o.c,'font-weight':700},G)});
const sx=X(6.4),sy=Y(86.94),pk=[];
for(let i=0;i<10;i++){const r=i%2?9:22,a=-Math.PI/2+i*Math.PI/5;pk.push((sx+r*Math.cos(a)).toFixed(1)+','+(sy+r*Math.sin(a)).toFixed(1))}
const sg=E('g',{class:'f'});
E('line',{x1:sx,x2:sx,y1:sy,y2:520,stroke:'#B4461A','stroke-dasharray':'6 6','stroke-width':2},sg);
E('line',{x1:120,x2:sx,y1:sy,y2:sy,stroke:'#B4461A','stroke-dasharray':'6 6','stroke-width':2},sg);
T(sx+30,sy+10,'REWARD 86.94% · 6.4 s',{fill:'#B4461A','font-weight':700,'font-size':26},sg);
const st=E('polygon',{id:'star',points:pk.join(' '),fill:'#B4461A',stroke:'#FBFAF7','stroke-width':2});
function run(){cr.setAttribute('width',0);zone.style.opacity=0;sg.style.opacity=0;st.style.opacity=0;st.style.transform='scale(.2)';
const t0=performance.now();
(function step(t){const p=Math.min(1,(t-t0)/2600);cr.setAttribute('width',p*900);if(p<1)requestAnimationFrame(step)})(t0);
setTimeout(()=>{zone.style.opacity=1},2900);
setTimeout(()=>{st.style.opacity=1;st.style.transform='scale(1)';sg.style.opacity=1},4000);
setTimeout(run,13000)}
run();
</script></body></html></x-embed>
```

## 範例 4：kNN 散點與距離長條

```html
<x-embed style="position:absolute;left:812px;top:284px;width:980px;height:632px"><!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;height:100%;background:transparent;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}svg{display:block;width:100%;height:100%}.f{transition:opacity .4s}</style></head><body><svg viewBox="0 0 980 632"></svg><script>
const S=document.querySelector('svg'),N='http://www.w3.org/2000/svg';
function E(t,a,p){const e=document.createElementNS(N,t);for(const k in a)e.setAttribute(k,a[k]);(p||S).appendChild(e);return e}
function T(x,y,s,a,p){const e=E('text',Object.assign({x:x,y:y,'font-size':24,fill:'#4A5361'},a),p);e.textContent=s;return e}
let sd=11;const R=()=>(sd=(sd*16807)%2147483647)/2147483647,G=()=>R()+R()+R()-1.5;
E('rect',{x:0,y:44,width:620,height:520,rx:14,fill:'#FBFAF7',stroke:'#DEDCD4','stroke-width':1.5});
T(0,30,'特徵空間（示意，k = 5）',{fill:'#646C78'});
const C=[[170,230,60],[300,420,62],[110,450,40]],P=[];
C.forEach(c=>{for(let i=0;i<22;i++)P.push([c[0]+G()*c[2]*1.6,c[1]+G()*c[2]*1.6])});
const LG=E('g',{});
P.forEach(p=>E('circle',{cx:p[0],cy:p[1],r:7,fill:'#2C5F93',opacity:.7}));
const A=[[250,280],[270,330],[350,270],[450,190],[530,130],[510,230],[400,350],[300,390]];
const D=A.map(a=>{const d=P.map(p=>[Math.hypot(p[0]-a[0],p[1]-a[1]),p]).sort((x,y)=>x[0]-y[0]).slice(0,5);return{nn:d,v:d.reduce((s,x)=>s+x[0],0)/5}});
const mx=Math.max.apply(null,D.map(d=>d.v));
const TR=E('g',{});
const pt=E('circle',{cx:A[0][0],cy:A[0][1],r:12,fill:'#B4461A',stroke:'#FBFAF7','stroke-width':3});
T(660,30,'δₜ（kNN 距離）',{fill:'#1C2430','font-weight':700});
E('line',{x1:650,x2:970,y1:520,y2:520,stroke:'#9AA1AB','stroke-width':2});
const B=[];
for(let i=0;i<8;i++){const x=660+i*38;B.push(E('rect',{x:x,y:520,width:30,height:0,rx:4,fill:'#B4461A'}));T(x+15,552,'t'+(i+1),{'text-anchor':'middle','font-size':22})}
E('circle',{cx:14,cy:598,r:8,fill:'#2C5F93'});T(30,606,'正常片段 𝓕ₙ');
E('circle',{cx:234,cy:598,r:9,fill:'#B4461A'});T(252,606,'異常影片的片段（依時間 t）');
function tw(d,f,cb){const t0=performance.now();(function s(t){const p=Math.min(1,(t-t0)/d);f(p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2);if(p<1)requestAnimationFrame(s);else if(cb)cb()})(t0)}
let cur=A[0].slice();
function stepTo(i){const a=A[i],b=cur.slice();
tw(450,p=>{pt.setAttribute('cx',b[0]+(a[0]-b[0])*p);pt.setAttribute('cy',b[1]+(a[1]-b[1])*p)},()=>{cur=a.slice();
while(LG.firstChild)LG.removeChild(LG.firstChild);
D[i].nn.forEach(n=>E('line',{x1:a[0],y1:a[1],x2:n[1][0],y2:n[1][1],stroke:'#B4461A','stroke-width':2.5,opacity:.65},LG));
E('circle',{cx:a[0],cy:a[1],r:6,fill:'none',stroke:'#B4461A','stroke-width':2},TR);
T(a[0]+12,a[1]-12,'t'+(i+1),{'font-size':22,fill:'#B4461A'},TR);
const h=D[i].v/mx*400;tw(400,p=>{B[i].setAttribute('y',520-h*p);B[i].setAttribute('height',h*p)})})}
function run(){while(TR.firstChild)TR.removeChild(TR.firstChild);while(LG.firstChild)LG.removeChild(LG.firstChild);
B.forEach(b=>{b.setAttribute('y',520);b.setAttribute('height',0)});cur=A[0].slice();
for(let i=0;i<8;i++)setTimeout(()=>stepTo(i),300+i*1250);
setTimeout(run,300+8*1250+3500)}
run();
</script></body></html></x-embed>
```

## 範例 5：累積和平滑與門檻選取（含反直覺標註）

```html
<x-embed style="position:absolute;left:128px;top:452px;width:1664px;height:460px"><!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;height:100%;background:transparent;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}svg{display:block;width:100%;height:100%}.f{transition:opacity .6s}</style></head><body><svg viewBox="0 0 1664 460"></svg><script>
const S=document.querySelector('svg'),N='http://www.w3.org/2000/svg';
function E(t,a,p){const e=document.createElementNS(N,t);for(const k in a)e.setAttribute(k,a[k]);(p||S).appendChild(e);return e}
function T(x,y,s,a,p){const e=E('text',Object.assign({x:x,y:y,'font-size':24,fill:'#4A5361'},a),p);e.textContent=s;return e}
let sd=5;const R=()=>(sd=(sd*16807)%2147483647)/2147483647;
const n=40,a0=22,a1=30,d=[];for(let t=0;t<n;t++){let v=1+(R()-.5)*.3;if(t==8)v=1.95;if(t>=a0&&t<=a1)v=1.55+.3*Math.sin((t-a0)/8*Math.PI);d.push(v)}
const m=d.reduce((a,b)=>a+b,0)/n,c=d.map(v=>v-m),D=[];let acc=0;c.forEach(v=>{acc=Math.max(0,acc+v);D.push(acc)});
const mx=Math.max.apply(null,D),Dn=D.map(v=>v/mx);
const X=t=>90+t*39,Z=140,K=110,Y=v=>420-v*190;
const BG=E('g',{class:'f'});
T(90,24,'δ̃ₜ：置中後的 kNN 距離',{fill:'#1C2430','font-weight':700});
E('line',{x1:80,x2:1650,y1:Z,y2:Z,stroke:'#9AA1AB','stroke-width':2});
T(90,214,'D̂ₜ：正規化的累積異常證據',{fill:'#1C2430','font-weight':700});
E('line',{x1:80,x2:1650,y1:420,y2:420,stroke:'#9AA1AB','stroke-width':2});
E('line',{x1:80,x2:1650,y1:Y(.8),y2:Y(.8),stroke:'#B4461A','stroke-width':2,'stroke-dasharray':'8 6'});
T(1650,Y(.8)-10,'λ = 0.8',{'text-anchor':'end',fill:'#B4461A','font-weight':700});
T(90,452,'片段 t →',{fill:'#646C78'});T(1650,452,'示意數據',{'text-anchor':'end',fill:'#646C78'});
const tr=E('g',{class:'f'});
E('path',{d:'M'+(X(a0)-13)+' 58 v-8 H'+(X(a1)+13)+' v8',fill:'none',stroke:'#2C5F93','stroke-width':3},tr);
T((X(a0)+X(a1))/2,40,'真實異常：δ̃ 最高的區段',{'text-anchor':'middle',fill:'#2C5F93','font-weight':700},tr);
const bars=c.map((v,t)=>{const h=Math.abs(v)*K;return E('rect',{x:X(t)-13,y:v>0?Z-h:Z,width:26,height:h,rx:3,fill:v>0?'#B4461A':'#9AA1AB',opacity:0})});
const line=E('polyline',{fill:'none',stroke:'#1C2430','stroke-width':4,'stroke-linejoin':'round',points:''});
const sel=[];Dn.forEach((v,t)=>{if(v>=.8)sel.push(t)});
sel.forEach(t=>E('rect',{x:X(t)-19,y:36,width:39,height:390,fill:'#F3DCCD'},BG));
S.insertBefore(BG,S.firstChild);
const lab=E('g',{class:'f'});
const cx=(X(sel[0])+X(sel[sel.length-1]))/2;
T(cx,452,'選入 I₁',{'text-anchor':'middle',fill:'#B4461A','font-weight':700},lab);
T(X(8)+24,Y(.35),'孤立雜訊：很快歸零',{fill:'#4A5361'},lab);
E('line',{x1:X(8)+20,y1:Y(.33),x2:X(8)+4,y2:Y(Dn[8])-6,stroke:'#4A5361','stroke-width':2},lab);
const lag=E('g',{class:'f'});
T(X(15),300,'證據要「累積」到異常尾端才達峰',{fill:'#1C2430','font-weight':700},lag);
T(X(15),330,'→ I₁ 偏後並溢出（拖尾）',{fill:'#1C2430'},lag);
function run(){[BG,lab,tr,lag].forEach(g=>g.style.opacity=0);bars.forEach(b=>b.setAttribute('opacity',0));line.setAttribute('points','');
let pts=[];for(let t=0;t<n;t++)setTimeout(()=>{bars[t].setAttribute('opacity',1);pts.push(X(t)+','+Y(Dn[t]));line.setAttribute('points',pts.join(' '))},300+t*110);
const e=300+n*110;
setTimeout(()=>{tr.style.opacity=1},e+300);
setTimeout(()=>{BG.style.opacity=.85;lab.style.opacity=1},e+1300);
setTimeout(()=>{lag.style.opacity=1},e+2500);
setTimeout(run,16000)}
run();
</script></body></html></x-embed>
```

## 範例 6：滑動視窗即時推論

```html
<x-embed style="position:absolute;left:128px;top:510px;width:1664px;height:400px"><!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;height:100%;background:transparent;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}svg{display:block;width:100%;height:100%}</style></head><body><svg viewBox="0 0 1664 400"></svg><script>
const S=document.querySelector('svg'),N='http://www.w3.org/2000/svg';
function E(t,a,p){const e=document.createElementNS(N,t);for(const k in a)e.setAttribute(k,a[k]);(p||S).appendChild(e);return e}
function T(x,y,s,a,p){const e=E('text',Object.assign({x:x,y:y,'font-size':24,fill:'#4A5361'},a),p);e.textContent=s;return e}
const x0=80,W=154;
E('rect',{x:x0,y:50,width:W*10,height:62,rx:8,fill:'#1C2430'});
for(let i=0;i<40;i++)E('rect',{x:x0+6+i*38.5,y:60,width:30,height:42,rx:3,fill:'#4A5361'});
['0 s','12.8','25.6','38.4','51.2','64 s'].forEach((s,i)=>T(x0+i*2*W,138,s,{'text-anchor':i==0?'start':i==5?'end':'middle'}));
T(x0,172,'每個視窗輸出一個異常分數',{fill:'#1C2430','font-weight':700});
E('line',{x1:x0,x2:x0+W*10,y1:360,y2:360,stroke:'#9AA1AB','stroke-width':2});
const th=360-.5*170;
E('line',{x1:x0,x2:x0+W*10,y1:th,y2:th,stroke:'#B4461A','stroke-width':2,'stroke-dasharray':'8 6'});
T(x0+W*10,th-10,'警報門檻（示意）',{'text-anchor':'end',fill:'#B4461A'});
const sc=[.08,.1,.13,.09,.56,.92,.95,.71,.16,.1];
const B=sc.map((v,i)=>E('rect',{x:x0+i*W+14,y:360,width:W-28,height:0,rx:4,fill:v>=.5?'#B4461A':'#9AA1AB'}));
const win=E('g',{});
E('rect',{x:0,y:40,width:W,height:82,rx:8,fill:'#F08A4B','fill-opacity':.22,stroke:'#F08A4B','stroke-width':5},win);
T(W/2,30,'32 幀 · 6.4 s',{'text-anchor':'middle',fill:'#B4461A','font-weight':700},win);
T(x0,396,'不必等影片結束：每 6.4 秒就給出一次判斷（示意）',{fill:'#4A5361'});
function tw(d,f){const t0=performance.now();(function s(t){const p=Math.min(1,(t-t0)/d);f(1-Math.pow(1-p,3));if(p<1)requestAnimationFrame(s)})(t0)}
let cx=x0;
function go(i){const a=cx,b=x0+i*W;tw(450,p=>{cx=a+(b-a)*p;win.setAttribute('transform','translate('+cx+' 0)')});
setTimeout(()=>{const h=sc[i]*170;tw(400,p=>{B[i].setAttribute('y',360-h*p);B[i].setAttribute('height',h*p)})},450)}
function run(){B.forEach(b=>{b.setAttribute('y',360);b.setAttribute('height',0)});cx=x0;win.setAttribute('transform','translate('+x0+' 0)');
for(let i=0;i<10;i++)setTimeout(()=>go(i),400+i*950);
setTimeout(run,400+10*950+3000)}
run();
</script></body></html></x-embed>
```

## 範例 7：主結果雙面板長條圖

```html
<x-embed style="position:absolute;left:128px;top:356px;width:1664px;height:560px"><!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;height:100%;background:transparent;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}svg{display:block;width:100%;height:100%}.f{transition:opacity .6s}</style></head><body><svg viewBox="0 0 1664 560"></svg><script>
const S=document.querySelector('svg'),N='http://www.w3.org/2000/svg';
function E(t,a,p){const e=document.createElementNS(N,t);for(const k in a)e.setAttribute(k,a[k]);(p||S).appendChild(e);return e}
function T(x,y,s,a,p){const e=E('text',Object.assign({x:x,y:y,'font-size':24,fill:'#4A5361'},a),p);e.textContent=s;return e}
const P=[{x:0,t:'UCF-Crime · AUC (%)',best:82.16,d:'較最佳 baseline（82.16）+4.78',r:[['S3R · I3D',81.34],['S3R · Uni',82.16],['RTFM · I3D',80.63],['RTFM · Uni',81.22],['MGFN · I3D',81.76],['MGFN · Uni',80.99],['REWARD',86.94]]},
{x:852,t:'XD-Violence · AP (%)',best:73.17,d:'較最佳 baseline（73.17）+4.54',r:[['S3R · I3D',70.14],['S3R · Uni',69.51],['RTFM · I3D',72.6],['RTFM · Uni',65.35],['MGFN · I3D',73.17],['MGFN · Uni',67.46],['REWARD',77.71]]}];
const bars=[],vals=[],dl=[];
P.forEach(p=>{const x0=p.x,bx=x0+190,bw=480,sx=v=>bx+(v-60)/30*bw;
T(x0,30,p.t,{fill:'#1C2430','font-weight':700,'font-size':28});
T(x0+812,30,'軸自 60 起',{'text-anchor':'end',fill:'#646C78'});
[60,70,80,90].forEach(v=>{E('line',{x1:sx(v),x2:sx(v),y1:56,y2:500,stroke:'#DEDCD4','stroke-width':1.5});T(sx(v),524,v,{'text-anchor':'middle','font-size':22,fill:'#646C78'})});
E('line',{x1:sx(p.best),x2:sx(p.best),y1:56,y2:500,stroke:'#646C78','stroke-width':2,'stroke-dasharray':'6 6'});
p.r.forEach((r,i)=>{const y=64+i*62,me=r[0]=='REWARD';
T(x0,y+30,r[0],{fill:me?'#B4461A':'#1C2430','font-weight':me?700:400});
const b=E('rect',{x:bx,y:y,width:0,height:42,rx:4,fill:me?'#B4461A':'#9AA1AB'});
const v=T(sx(r[1])+10,y+30,r[1].toFixed(2),{fill:me?'#B4461A':'#4A5361','font-weight':me?700:400,class:'f'});
bars.push([b,sx(r[1])-bx,me]);vals.push(v)});
dl.push(T(x0,552,p.d,{fill:'#B4461A','font-weight':700,'font-size':26,class:'f'}))});
function tw(d,f){const t0=performance.now();(function s(t){const p=Math.min(1,(t-t0)/d);f(1-Math.pow(1-p,3));if(p<1)requestAnimationFrame(s)})(t0)}
function run(){bars.forEach(b=>b[0].setAttribute('width',0));vals.concat(dl).forEach(v=>v.style.opacity=0);
let k=0;bars.forEach((b,i)=>{const delay=b[2]?1700:200+(i%7)*150;setTimeout(()=>{tw(700,p=>b[0].setAttribute('width',b[1]*p));setTimeout(()=>vals[i].style.opacity=1,600)},delay)});
setTimeout(()=>dl.forEach(d=>d.style.opacity=1),2800);
setTimeout(run,13000)}
run();
</script></body></html></x-embed>
```
