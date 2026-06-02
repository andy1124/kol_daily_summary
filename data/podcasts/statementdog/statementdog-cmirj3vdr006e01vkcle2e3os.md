# 提及公司

- 美股：NVIDIA、Google（TPU）、AWS（Amazon）、Intel、Apple、Meta、OpenAI、Anthropic、Groq
- 台股：台積電

# 三句話總結

- **Google TPU大幅上修**：2027年TPU產量預估從300萬顆提升至500萬顆、2028年從320萬顆提升至700萬顆，Google在AI訓練與推論端持續挑戰NVIDIA地位。
- **AWS re:Invent主題—Agentic AI元年**：AWS宣稱2025年進入Agentic AI時代，企業級SaaS轉型拐點將由Agentic Workflow推動，AI訓練算力（GPU）之外，CPU與Storage需求將出現外溢增長。
- **Intel多重受惠主題**：①Agentic Flow帶動多核心CPU需求↑ ②郭明錤稱蘋果低階晶片最快2027年初交Intel代工 ③台積電CoWoS產能不足，Intel EMIB先進封裝受惠需求外溢。

# 投資觀點

- **Google TPU vs. NVIDIA**：目前尚無FP4精度的公正評比，成本優勢需等到FP4訓練完成並落地後才能確認；兩方說法均有，不能急於下結論。
  * Gemini vs. ChatGPT：細看ChatGPT回答品質仍微勝，但Gemini速度優勢明顯，使用體驗更佳。
- **規格迭代加速是硬體投資的護城河**：規格越快變化，廠商越有誘因付出溢價；散熱、光通訊、儲存均因此受惠，台灣硬體供應鏈佔比在本波AI中大幅提升。
- **台積電供不應求維持**：Intel拿到封裝單不代表台積電訂單減少，台積電現在的瓶頸是產能不足非需求不足；供應鏈投資人毋需恐慌。
- **明年消費產品注意換料風險**：記憶體漲價廠商轉嫁給下游，手機/PC可能從DDR5降規至DDR4或採購更低規格NAND，高規格消費品漲價壓力轉移至消費者或換料吸收。

# Agentic AI與CPU需求外溢

## Agentic Flow架構說明

- Agentic AI ≠ 純AI：典型Agentic Workflow由多個節點組成，部分節點由LLM處理，其餘（資料庫查詢、排名、API呼叫、貼文發布等）由CPU完成。
- **CPU用量增加邏輯**：call多個AI模型的控制邏輯、資料庫RAG的搜尋排名、後處理貼文/API整合——這些均由CPU執行，非GPU。
- 核心數增加需求：GPU/CPU比例可能從1 CPU:8 GPU演進至多CPU搭配，ARM收費邏輯（按核心數授權）因此受益。

## Intel的多重機會

- **CPU外溢**：Agentic AI帶動多核心CPU升級需求，Intel在x86伺服器CPU具有份額。
- **蘋果低階晶片**：郭明錤報告指出，蘋果低階晶片最快2027年初交Intel代工（確認度待觀察）。
- **EMIB先進封裝**：台積電CoWoS產能不足，Intel EMIB（2.5D先進封裝）承接外溢需求；AWS Graviton已有使用Intel EMIB封裝的先例。
  * 風險：Intel EMIB整體產能仍有限，擴廠態度謹慎；能承接的量相對有限。

# Google TPU與AI競爭格局

- Google TPU產量上修（2027: 300萬→500萬，2028: 320萬→700萬）。
- Google內部研發能力被認為強於Meta；Meta目前由Scalable AI負責人Alex Wang主導，組織相對激進。
- OpenAI Code Red內部信：暫停非ChatGPT核心業務，包含電商廣告優化、Pro用戶週報等；傳聞GPT-5為GPT-4o升級版，非全新模型，聚焦提速與推論優化。
- **成本爭議未解**：NVIDIA H100 vs. Google TPU v5誰更便宜，因FP4精度評比尚未出爐，無定論。

# 硬體供應鏈整體觀察

- 規格快速迭代下，散熱（水冷→微流道液冷）、光通訊（OCS）、儲存（KV Cache下放至SSD）均開拓新市場；單價從「成長20至50%」跳升至「2至5倍」。
- 台積電千金股群象：台股4位數股已達25家，硬體王國受惠顯著。
- 下游消費性電子（聯詠、手機面板IC）：記憶體漲價轉嫁至消費端，2026年消費性反彈時間點仍難言，但不應完全關閉眼光（過去每年「放羊」也有真正爆發的一天）。

# 節目金句

- 「規格如果沒有這麼快變化，那個東西就是沒有人要搞，錢砸下去大家規格不變沒得賺；規格變很快，大家就可以拿各種各樣奇奇怪怪的新規格用力幹進去。」
- 「散熱以前說算水冷大家興奮，現在有微流道水冷，更舒服、更興奮；單價SV直接用沉的，以前20至50%成長，現在是兩倍、三倍、五倍。」
- 「你以為Google用TPU比較便宜，到底是在哪一個scope？是晶片本身、還是這個rack、還是整個系統、還是最後做出一個模型？」
- 「Intel突然變成二線廠商第二圖，反過來了！台積電太滿，大家才要找Intel。」
- 「在成長的時候，整個產業都會成長，你不用那麼斤斤計較——整個大海在漲潮。」
- 「現在的這種玩法搞得像每家CSP都像新創公司一樣，好像在賽馬——哇靠隔壁的那個衝出來了，不行我們今天不能輸。」

# 疑似辨識錯誤

- 「TR3」→ 建議：「Trainium3」（AWS自研AI訓練晶片）
- 「TR4」→ 建議：「Trainium4」（AWS下一代訓練晶片）
- 「OSGS」→ 建議：「OCS」（Optical Circuit Switch，Google網路架構）
- 「Bearock」→ 建議：「Bedrock」（AWS AI平台服務名稱）
- 「Tetan」→ 建議：「Titan」（AWS或NVIDIA Switch相關名稱，待確認）
- 「Luminten」→ 建議：「Lumentum」（光通訊元件廠商）
- 「FOCI 上詮」→ 確認（台灣光纖被動元件廠商）
- 「中華資安」→ 建議：可能為「中華資安國際」（CHT Security，台灣資安廠商）
- 「馬上哇四季大陣」→ 建議：此為口語表達，非公司名稱
