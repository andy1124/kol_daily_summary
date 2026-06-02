# 提及公司

- 美股：NVIDIA、Google、Coherent、Lumentum、群聯電子（Phison）
- 台股：茂連、台光電、建策、貿聯、法人共識股（紅鏡/7769）、群聯電子（Phison）

# 三句話總結

- **市場資金輪動警訊**：法人共識Top Pick（建策、貿聯、台光電等）同日重挫，疑似主力換倉訊號，舊主流股進入橫盤或修正階段。
- **NVIDIA ICMS架構**：NVIDIA發表DPU Storage Server概念（ICMS），用Bluefield DPU搭配Pseudo-SLC SSD將KV Cache下放至儲存層，解決Agentic AI上下文記憶體爆炸問題；群聯Controller現身NVIDIA Switch Tray，為潛在受益廠商。
- **NVIDIA持續領先**：Blackwell晶片效能10x於Transistor 2x，Hooper Rack整體方案保持競爭力；ICMS延續CPX Prefill/Groq收購後的「預見痛點再推解法」戰略，硬體故事未終結。

# 投資觀點

- **市場轉換節點觀察**：當多支強勢股同日大跌，背後邏輯可能是資金偏好改變而非單純基本面惡化；舊主流不一定崩，可能進入橫盤，等待新主流浮現。
  * 「OCS鬼故事一天後就被產業人士打臉並直接拉回」，鬼故事在下跌時出現屬人之常情，要看是否有產業支撐。
- **不排除任何題材**：市場題材有時看似假貨（如過去電子紙圓泰每年放槍），卻可能數年後真正爆發；不要因被騙幾次就完全封閉眼光。
- **報告寫作建議**（給研究員）：財務數字（EPS估算）無須贅述，真正有價值的是「新應用對既有供應鏈的衝擊分析」，例如：ICMS帶動哪些SSD廠商、PCIe Gen5換代影響哪些零件。

# NVIDIA ICMS（DPU Storage Server）

## 架構概念

- **問題**：Agentic AI時代需要大量KV Cache（上下文記憶體），HBM與CPU DRAM負載爆炸，導致長對話斷片、推理成本飆升。
- **解法**：NVIDIA ICMS——由Bluefield DPU管理旁路Storage Server，將「準熱資料」下放至DPU掛載的SSD，HBM/DRAM只保留「熱資料」，透過GPU Direct Storage加速存取。
- **好處**：資料中心降低重複Token生成的算力與電力消耗；個人化AI記憶持久化；處理速度仍優於傳統CPU→RAM→Storage路徑。

## 群聯（Phison）線索

- CES現場照片顯示NVIDIA Switch Tray左下角有群聯Controller的SSD；顆粒為TLC但設定成Pseudo-SLC（犧牲三分之二容量換取耐久度與速度），實際可用容量約160至170GB（原始5.2GB單顆）。
- **核心問題**：未來SSD是否需要「NVIDIA Certified」認證？若是，類似HBM驗證機制，先取得資格者享有先發優勢；若否，全體SSD廠商受惠於整體用量成長。
- KV Cache下放從「冷儲存」升級為「準熱儲存」，大幅提升SSD在AI基礎設施中的地位與單價。

## NVIDIA戰略持續性

- **Blackwell**：Transistor數量×2，效能×10，說明Hooper Rack整體方案貢獻效能遠超純晶片密度提升（Hooper Rack=新摩爾定律）。
- **ICMS邏輯**：先看到CPX Prefill痛點→解決；再看到Decode瓶頸→收購Groq；現在看到KV Cache爆炸→推出ICMS；每次「大家才發現問題」時NVIDIA已有準備好的解法。

# 節目金句

- 「每次下跌就有很多人拿鬼故事出來嚇你，所以其實長期持有一些標的根本就不容易。」
- 「老黃真的沒有騙你——買越多省越多，然後買越新的東西你可能還要意外的又再省更多。」
- 「你不敢說什麼長期持有可能是很簡單的很無腦的，沒有，因為其實每次的壞消息你就要做出你當下的判斷。」
- 「市場就這樣，你一定要去找出那個你不知道的東西，而不是跟我說EPS估幾塊，那個我已經知道了。」
- 「老黃真的是蠻變態的，他們真的是領先別人不知道多少，就當大家發現了一個痛點，他立刻就有solution。」
- 「有些東西大家覺得是草菇股、假貨，可能只是你看不夠多，因為一開始覺得是假貨，最後面就告訴你他的生意其實每個標的那種突然間射上去都會讓你驚訝。」
- 「Gemini剛推出大家說超強，一段時間後大家覺得它變笨——其實是它的memory都是給人家佔據的。」

# 疑似辨識錯誤

- 「Backbomb」→ 建議：「Backbone」（人體工學家具品牌，廣告贊助商）
- 「VR入柄」→ 建議：「Blackwell」（NVIDIA下一代GPU架構）
- 「費半」→ 建議：「費城半導體指數」（Philadelphia Semiconductor Index，SOX）
- 「CPX Prefail」→ 建議：「CPX Prefill」（NVIDIA Blackwell架構中的KV Cache預填充機制）
- 「Anfano」→ 建議：「Amphenol」（安費諾，Cable連接器廠商）
- 「Grogg」→ 建議：「Groq」（AI推論晶片新創，NVIDIA收購）
- 「Groch」→ 建議：「Groq」（同上）
- 「廢慢」→ 建議：「Blackwell」（發音近似台語「Blackwell」簡稱）
- 「群聯 Phison」→ 確認正確（台灣SSD控制器廠商）
