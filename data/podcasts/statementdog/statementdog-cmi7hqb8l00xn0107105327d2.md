# 486.【財經時事放大鏡】全村又被 carry 了 × Memory 考古學

**節目**：財報狗 Podcast  
**日期**：2025-11-20  
**時長**：約 44 分鐘

---

# 提及公司

- 美股：NVIDIA、Google（Alphabet / Gemini 3）、Intel（EMIB）、OpenAI、Microsoft（MAIA）、Meta、Amazon（AWS）、Apply Materials（應材）
- 台股：台積電（TSMC）、聯發科（MediaTek）、華邦電、Trendforce（集邦科技）
- 其他：Broadcom（逐字稿「Block On」）、三星、SK 海力士、YMTC（長鑫？）、Michael Burry / Scion Asset Management

---

# 三句話總結

- **Michael Burry 登出 Scion，NVIDIA CFO 直接反駁折舊短命論**：Burry 取消 Scion 的 SEC 登記後，NVIDIA 在法說會上主動揭露 A100 推出 6 年仍滿載，以「使用連線非常差」（即從不閒置）直接打臉「GPU 壽命只有 2～3 年」的放空邏輯。
- **Gemini 3 全用 TPU 訓練，但 ASIC vs GPU 仍是共存格局**：Google TPU 已走到 V7（Ironwood），表現領先，但其他 CSP（Microsoft MAIA、Meta）的 ASIC 表現不佳；通用 GPU（NVIDIA）生態系廣度與靈活性仍為優勢，AI 市場整體擴大中，無需爭論誰死誰活。
- **記憶體漲價循環開始壓抑終端需求**：DDR5 合約價持續漲，PC 品牌預期售價上漲 5～15%；歷史參照 2016～2018 年 DDR4 大循環——漲到一定程度後需求遞延，但供給缺口（2027 年前中國 DRAM/NAND 擴產產能才陸續開出）短期難以填補。

---

# 投資觀點

- **製造端視角看競爭更清晰**：在台積電等晶圓廠成為「必經之路」的情況下，與其糾結 ASIC/GPU 誰勝出，不如直接觀察 TSM 的產能擴張訊號——若 TSM 打開擴產，IC 設計鏈直接受益；若 TSM 保守，後段封裝與 Intel EMIB 成替代選項。
- **記憶體循環有歷史可循**：2016～2018 的 DDR4 漲價路徑（DDR3→DDR4 轉換不順 + 伺服器需求爆發）與現在（DDR4→DDR5 + HBM + AI CSP 需求爆發）高度相似；投資人應追蹤**合約價**而非現貨價，並留意中端（PC、網通）廠商毛利率受擠壓的時機。
- **不確定性越高，蝴蝶效應越大**：預測 2030 年以後的 AI 算力需求，一個假設改變（如 inference 成本大降）就會顛覆結論；建議持續「review」而非鎖定單一敘事。

---

# NVIDIA 法說會分析

## Michael Burry 放空邏輯（已「登出」）

- Burry 的 GPU 放空核心：AI GPU 迭代極快，真實折舊期僅 2～3 年，而市場以 5～6 年計算，帳面高估
- Burry 取消 Scion 的 SEC 登記 → 未來倉位不再公開，符合其一貫低調個性

## NVIDIA CFO 的回應（未點名但針對性強）

- GPU 的**經濟使用壽命**（economic life）≠**會計折舊期**（depreciation period）
- **A100 推出 6 年，仍滿載運行**，在算力稀缺時代無人拋棄舊 GPU
- Blackwell 新品備貨導致庫存增加、HBM 漲價拉高應收帳款——均有合理解釋，並非財報異常

---

# Google TPU 與 ASIC vs GPU 分析

## TPU 發展現況

- Gemini 3（Germany 3）**全程以 TPU 訓練**，Benchmark 表現強勁
- 目前 TPU 走至 **V7（Ironwood）**，相較其他 CSP 的 ASIC（Microsoft MAIA、Meta）在訓練端明顯領先
- 聯發科為 TPU V7 新進 IO + 後段供應商（Broadcom 仍為主晶片供應商）
- TPU V9（預估 2028～2029）可能採用 **Intel EMIB** 後段封裝

## ASIC 不等於 GPU 的終結

- NVIDIA GPU 的核心優勢：廣泛兼容所有模型與平台（GPGPU 通用性）
- 其他 CSP 的 ASIC 效果不如 TPU，且需要自建 infra team 維護
- 整體 AI 算力餅持續擴大，ASIC 搶佔部分份額不等於 GPU 需求減少

---

# 記憶體漲價循環分析（Memory 考古學）

## 歷史對照：2016～2018 DDR4 大循環

- **觸發點**：DDR3 → DDR4 轉換不順（良率問題），疊加伺服器 DDR4 插槽數設計變更（多通道）
- **頂點**：2018 年 Q1，合約價最高，之後需求崩塌
- **受害方**：筆電（memory 占成本 10～18%）、網通（毛利低的代工廠直接被吃掉 5%+）

## 現況與歷史比較

- 相似處：DDR4 → DDR5 轉換不順（良率下降、比特攻擊降低）+ HBM 搶佔高階產能 + CSP 成為最大買家（類比 2016 General Server CSP）
- 不同處：本次疊加 **AI HBM 需求**，需求量級更大，漲幅可能更高、更持久
- **合約價 vs 現貨價**：真正決定廠商損益的是**合約價**；現貨價波動大、代表性低

## 供需預測

- 2026 年上半年：既有庫存（低合約價買入）仍支撐一段出貨，售價壓力有限
- 2026 年下半年起：Apply Materials 法說指出記憶體先進製程產能需求開始起飛
- 2027 年：中國 YMTC 等廠擴產產能開出（需要 6～9 個月設備 lead time），屆時供給開始緩解
- **DDR5 良率問題**：DDR5 每顆 die 面積較大（含 ECC 除錯電路），良率低於 DDR4，短期壓縮 bit supply growth

## 中端產品受影響評估（Trendforce 數據）

- 機板（PC）memory 佔成本 **10～18%**
- 若記憶體持續漲價，PC 品牌售價可能上漲 **5～15%**
- 消費者觀望情緒一旦升起，終端需求遞延（歷史規律 6～9 個月）
- 網通廠毛利率薄，記憶體漲價直接吃掉 5%+ 毛利

## Vera Rubin / CBX 架構的記憶體選擇

- NVIDIA 下一代 Vera Rubin 的 CBX 模組使用 **GDDR7**（非 LPDDR），代表高頻寬記憶體需求仍在快速演進
- 未來「堆疊式 DRAM」（Stacked DRAM，SoulCam 類技術）可能改變架構，相關材料廠受益

---

# 節目金句

- 「GPU 的使用連線非常差——A100 是在六年前出貨，現在仍然是在滿載運行。」
- 「你買不到你，不然賣給我——你折完了賣給我，還是會有產值的，還是有很多人願意買。」
- 「製造商變得很單一，所以你從製造商抓到後面的競爭，反而是容易的，反而比你直接看 TPU 容易。」
- 「Anyway 就是現在就是公佈英球（布蘭特原油），大家一起成長。每個產業剛開始就是這樣子，當然沒有人在關你什麼競爭的。」
- 「你這種蝴蝶效應的這種變化很大，會造成終端你最終推論的結果變化很多，因為你推論很遠嘛——大家都推到 2030 年、2035 年。」
- 「記憶體每一次跟我講說欸靠我跟你講會長到宇宙喔，沒有到火星就可能還沒到火星我們就被擊落了，就至少到個月球好不好。」
- 「那你說這個東西漲起來他要馬上影響到需求大不大——他不會馬上，他一定會遞延，因為大家做生意還是用合約來做生意嘛。」

---

# 疑似辨識錯誤

- 「Block On」→ 建議：**Broadcom（博通）**（Google TPU 主要供應商，Whisper 音近誤識）
- 「Germany 3」/ 「Jr.mn3」/ 「gm3」→ 建議：**Gemini 3**（Google 最新大型語言模型，Whisper 誤識為德文/日文音譯）
- 「Inrec」→ 建議：**NVLink** 或 **InfiniBand**（NVIDIA 晶片互連技術）
- 「比特攻擊」→ 建議：**bit growth**（記憶體產業術語，Whisper 音近誤識）
- 「NCP」→ 建議：**MCP**（Model Context Protocol，AI 工具協定，語境為「有沒有開 MCP 支援」）
- 「Coarse S / Coarse L」→ 建議：**CoWoS-S / CoWoS-L**（台積電先進封裝，Whisper 誤識）
- 「長鑫」→ 疑為 **YMTC（長江存儲）** 或 **CXMT（長鑫存儲）**，Whisper 將兩者混用（NAND 為長江存儲；DRAM 為長鑫存儲）
