# 提及公司

- 美股：Google、NVIDIA、Intel、AMD、Marvell、Apple、Kioxia（凱俠）、TI、TERADYNE
- 台股：聯發科（MediaTek）、信越化學代理（台灣 DOK）
- 其他：信越化學（Shin-Etsu，日本）、瑞薩（Renesas，日本）、MJC（日本，記憶體探針卡）、村田製作所

# 三句話總結

- **Google TPU 第八代分化訓練與 Inference**：TPU 8T（Training）與 8I（Inference）為兩個獨立晶片；8I 加入大量 SRAM、搭配 Marvell CXL，聯發科 ASIC 設計服務（Design Service）參與第八代確認，GPU 時代的雙寡頭佈局持續強化。
- **CPU 成 AI Server 新瓶頸**：Intel/AMD 伺服器 CPU 缺貨，成為 AI Server 整條供應鏈最短板；CPU 供應量決定周邊採購節奏，Intel 股價因此暴衝兩倍。
- **日本 7.7 級強震影響半導體供給**：凱俠（Kioxia）東北廠確認 NAND 產線受到波及，光阻劑（DOK、信越）停線檢查 4-8 週；本已極緊張的半導體供需雪上加霜，漲價壓力再升。

# 投資觀點

- **Inference 需求確認不可逆**：Google TPU 分成 T（訓練）與 I（推論）兩款，代表兩者需求量已大到各自需要一顆獨立優化晶片；NVIDIA 主導的 AI 正向循環（終端付費 → 算力採購 → 設備需求）未見頭。

- **CPU 瓶頸帶動 Intel 回升**：AI Server 最短板已從 GPU/HBM 轉移至 CPU，Intel/AMD 伺服器 CPU 搶不到；Intel EMIB 封裝也被納入 CPU 外溢產能選項，成為雙重利多。

- **光阻劑漲價邏輯確立**：停線 → 供給縮減 + 油價/石化成本上升 → 雙重供給壓力；DOK（台灣代理信越化學）最直接受惠，漲價時間點可能提前。

- **聯發科轉型成效可觀**：從手機晶片廠轉型為 AI ASIC Design Service 提供者；第八代 Google TPU 確認參與，未來手機（Cash Cow）＋ AI ASIC（成長）雙引擎。

# 主題分析區塊

## Google TPU 第八代重點

- **架構分化**：TPU 8T（Training） vs 8I（Inference）— 訓練與推論用途明確拆開，不再共用晶片
- **8I 設計特點**：大量內建 SRAM（減少 Time-to-First-Token）；搭配 Marvell CXL 控制器（Google 採用 CXL 傳聞驗證）；Host CPU 改用 ARM 架構（設計在台灣）
- **聯發科確認參與**：第八代 Google TPU ASIC Design Service 由聯發科承接，前幾代僅為傳聞，此代逐步確認
- **市場意涵**：Google 與 NVIDIA 合計七八成 AI 算力市占均採 SRAM 加速 Inference → SRAM 為今年產業趨勢主流

## CPU 供應瓶頸

- **Intel/AMD 伺服器 CPU 最缺**：AI Server 周邊（DRAM、GPU）雖緊，但 CPU 已成整條鏈最短板；CPU 到不了 → 周邊採購延誤
- **Intel 股價暴衝因素**：EMIB 後段封裝被 AI 晶片廠相中（Google TPU 備援），加上 CPU 缺貨，雙重利多推動股價翻倍
- **地端 CPU 需求尚未來**：Mac mini / 本地 Agent 所需 CPU 仍小眾，主要缺口在雲端 Server；但長期地端 Agent 擴大後，消費性 CPU 需求也將隨之上升

## 日本地震供應鏈衝擊

- **地點**：東北日本（7.7 級），非東京都會區，但半導體聚落集中於此
- **受影響廠商**：凱俠（Kioxia）K1 廠確認影響（K1 目前在產），NAND 全球供應約 3-4% 受波及；光阻劑廠 DOK（信越代理）、信越停線檢查 4-8 週
- **複合利多條件**：本已因 AI 需求緊俏的供應，再疊加地震停線；光阻劑同時面臨石化原料漲價壓力，雙重供給壓縮

## 半導體供應鏈觀察框架

- **類比 2021 年 MCU 缺貨**：疫情＋大雪＋廠商下單不足 → 多重巧合推動缺貨；此次 AI 需求＋地震＋停線，結構類似
- **NAND 不如 CPU 緊**：NAND 家數多（不易漲價），CPU 只有 Intel/AMD 兩家（高產業集中度，漲價能力強）
- **聽到「停線檢查」就要盯**：停線 → 供給縮 → 漲價；信越/DOK 的 4-8 週停線是具體時間節點

# 節目金句

- 「CPU 就變成一個最關鍵的品質，講不到吧？本來你不想要跟 Intel 玩，但英雄好棒，漲一漲漲兩倍，我愛 Intel 好不好。」
- 「七八成的市占告訴你就是要這樣搞，不然不夠快，Time-to-First-Token 會太慢，所以 SRAM 這件事情看起來至少在今年是個產業趨勢。」
- 「這次的循環通常都是有非常非常多的原因匯集在一起的，就像 2021 年那一次 MCU 缺貨除了疫情以外還有大雪，所以其實有很多巧合，那這一次看起來也是哇有好幾個巧合。」
- 「你問 Intel 說你封裝怎麼樣，大家都沒有產能囉可以嗎？可以介紹這個挑戰嗎？不行喔，不行，那我要買掉。」
- 「聯發科它的手機可以當個 cash cow 對不對，那再來 AI 再吃十幾年，哇大局勢都有站到。」
- 「市場的供需現在非常非常緊俏，如果有隨便弄了一個 Something，那就很精彩了，我真的這樣講。」
