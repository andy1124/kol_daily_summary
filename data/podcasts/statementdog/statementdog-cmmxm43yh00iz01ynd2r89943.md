# 510.【財經時事放大鏡】EUV 一路卡到建算力 x GTC 次世代算力構築
**財報狗 Podcast｜2026-03-19**

---

# 提及公司

- 美股：NVIDIA、Anthropic（Claude）、OpenAI、Cloudflare（提及）、ASML（提及）、台積電（ADR）、Groq
- 其他：ASML（荷蘭，EUV設備商）

---

# 三句話總結

- **LPU 架構揭曉**：NVIDIA 收購 Groq 後在 GTC 推出 LPX 系統，LPU 負責 Speculative Decoding（推測性解碼），每秒可達 1000 個 token，是一般 GPU 的 20 倍，並非取代 GPU 而是協同加速。
- **EUV 是最根本的算力瓶頸**：SemiAnalysis 創辦人 Dylan Patel 指出，1 GW 的 AI 算力需要 3.5 台 EUV，EUV 長期供不應求，這解釋了為何數據中心無法快速擴產，也說明了算力資產價值為何居高不下。
- **AI Inference 需求仍在加速**：Open Claw/Claude Cowork 等 Agent 工具大幅降低使用門檻，未來只要延遲問題解決，Token 消耗將從工程師擴散至一般用戶，算力需求天花板持續上移。

---

# 投資觀點

- **算力供給受限的結構性原因**：建廠（Cleanroom）要1-2年，CoWoS產能被搶，再往上推是EUV機台本身產能不足（ASML年產量有限，非AI爆發後才開始供不應求，歷來都是拍到明後年）。
  * 任何一個環節卡住即成瓶頸，「長板效應」讓整體擴產速度受最慢的節點限制

- **算力 Pricing 邏輯**：AI 算力→可賺錢→資本支出高→設備需求大→上游設備因此受益；只要算力還稀缺、還能賺錢，算力資產估值就有支撐。

- **OpenAI vs Anthropic 的算力競爭優勢**：OpenAI 早早卡位算力長約，成本結構較低；Anthropic 算力若不足需高價外租，但融資能力強，可用資本換算力，長期影響有限。

- **Inference Scaling 才是下一個主題**：Training Scaling Law 討論已趨淡，Post-Train 和 Inference 階段才是現在的前沿；隨著 Agent 使用場景爆炸，Inference token 消耗量將大幅成長。

---

# NVIDIA LPU / LPX 技術解析

## LLM 推論的兩個階段

- **Prefill（前填充）**：理解使用者問題，拉取相關上下文（類似 RAG）；需要大量記憶體（每個 token 約 4-5 MB KV Cache），由 GPU 負責
- **Decode（解碼）**：逐字生成輸出，依賴「文字接龍」邏輯；Attention 機制仍由 GPU 負責，但 MoE 投票環節交由 LPU 做

## LPU 的角色：Speculative Decoding

- LPU 先基於小模型快速生成幾個「草稿候選字」
- GPU 負責最終從候選中選出正確答案（大模型驗證）
- 效果：每秒有效輸出 token 從一般 GPU 約 50 個提升至官方宣稱 1000 個（約 20 倍）

## 架構設計

- LPU 與 GPU 以網路連接（非同一顆晶片），有網路延遲，但整體仍大幅提升效益
- 由 8 個 Groq 3 LPU 組成的 LPX 系統，體積可觀，需水冷
- 現階段是拼裝式架構（bridge 連接），未來有望深度整合進 GPU 系統

## 對產業的意義

- SRAM 需求再添新用途（LPU 內部使用）
- 水冷需求增加（LPX 機櫃規模大）
- 整體架構靠 NVIDIA Dynamo 軟體協調，Dynamo 重要性進一步提升

---

# AI 算力瓶頸分析（Dylan Patel / SemiAnalysis）

## 最根本的瓶頸：EUV

- 1 GW AI 算力約需 3.5 台 EUV 機台（ASML 年產量有限，且製造難度高）
- EUV 自身需要特殊鏡頭、光源，良率原本就不高；並非 AI 爆發後才稀缺
- 往上推：EUV → 晶圓廠產能（Cleanroom 蓋廠 1-2 年）→ CoWoS 封裝產能 → GPU

## 第二大瓶頸：記憶體

- HBM 需求爆炸，每個 token 輸出需要大量 KV Cache 記憶體
- 記憶體廠同樣有製程升級和產能限制，並非無限擴充

## 對算力定價的影響

- 供給受限 + 算力可賺錢 = 算力資產估值長期高位支撐
- 類比：稀土/關鍵礦產，供給端有結構性約束，不是靠「多蓋一個廠」就能快速解決

---

# AI Agent 工具比較

- **Claude Cowork（Anthropic）**：Claude 版的 Open Claw，只能用 Claude 模型，但整合度高，非技術用戶友善
- **Open Claw**：可接任何 API，彈性高，但安裝仍需一定技術知識；有吃到飽方案被濫用的違規問題
- **NEMO Cloud（NVIDIA）**：GTC 現場發表，操作介面更簡單，DGX Spark 當場售罄
- **意義**：這些工具大幅降低 Inference token 的使用門檻，未來一般用戶也能成為大量 token 消費者

---

# 節目金句

- 「每個 token 大概 4 到 5 MB，一篇 1000 字的文章就要接近 5 GB 的緩存，真的很多。」
- 「LPU 先幫你縮小範圍，然後再給 GPU 猜，每秒 1000 個 token，是一般 GPU 的 20 倍。」
- 「1 GW 的 AI 晶片大概需要 3.5 台 EUV 機台，從來沒有人這樣算過，這很有意思。」
- 「ASML 的 EUV 歷來都是供不應求，不是 AI 爆發後才這樣，訂單一直都拍到明後年。」
- 「供給受限加上算力可以賺錢，那算力怎麼會不漲？這就是整個供應鏈穿在一起的邏輯。」
- 「AI 的演進能力讓我覺得，就算看到 NEMO Cloud 那個東西出來，你會覺得要擔心 AI 的資本泡沫是假的嗎？我完全不擔心。」
- 「推論的 Inference Scaling，才是現在真正的前沿——Training Scaling Law 的討論已經過了。」
- 「你手機農場每天幫你賺錢，等一下，這不就是 AI 的故事嗎？」

---

# 疑似辨識錯誤

- 「過格三」→ 建議：「Groq 3（LPU 型號）」（公司/產品名稱，發音誤轉）
- 「MVDAR」→ 建議：「NVIDIA」（重複出現的誤轉，語境明確）
- 「Open Claw」、「Open Club」→ 建議：「Open Claude / Claude Cowork」（產品名稱，多次誤轉）
- 「GCR」→ 建議：「GPU」（語境為算力硬體）
- 「預填充」的「FreeFill」→ 建議：「Prefill」（LLM 技術術語）
