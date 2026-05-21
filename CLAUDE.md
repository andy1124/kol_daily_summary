# KOL Daily Summary

每日自動追蹤財經 Podcast 新集數，使用本地 Whisper 轉逐字稿，Claude API 生成重點摘要，發布為 GitHub Pages。

## 專案架構

```
kol_daily_summary/
├── config/sources.yaml      # Podcast / KOL 來源清單（唯一需要手動維護的設定檔）
├── data/
│   ├── processed.json       # 已處理集數 ID 記錄
│   └── podcasts/[slug]/     # 每集 JSON（元數據 + 逐字稿 + 摘要）
├── dictionary.json          # Whisper 辨識錯誤替換字典（已知錯誤詞 → 正確詞）
├── scripts/
│   ├── run_all.py           # 主要執行入口（RSS 檢查 + 轉錄）
│   ├── check_podcasts.py    # RSS 新集數檢查
│   ├── transcribe.py        # Whisper 音訊轉錄
│   ├── preprocess.py        # 逐字稿前處理：套用 dictionary.json 已知修正
│   └── detect_typos.py      # 互動式審閱 Claude 偵測到的疑似錯誤，擴充 dictionary.json
├── skills/
│   └── podcast-summarizer/
│       └── SKILL.md         # podcast-summarizer skill 原始檔（更新後用 install_skill.ps1 安裝）
├── site/                    # Astro 靜態網站
└── venv/                    # Python 虛擬環境
```

## 初次設定

1. 複製環境變數設定：
   ```powershell
   Copy-Item .env.example .env
   # 編輯 .env 填入 ANTHROPIC_API_KEY
   ```

2. 在 `config/sources.yaml` 填入 RSS URL（參考下方說明）

3. 安裝 Node 相依：
   ```powershell
   cd site && npm install
   ```

## 每日執行流程

```powershell
# 啟動虛擬環境
venv\Scripts\Activate.ps1

# Step 1: RSS 檢查 + Whisper 轉錄
python scripts/run_all.py --max-episodes 5

# Step 2: 套用已知錯誤修正（dictionary.json → 逐字稿）
python scripts/preprocess.py

# Step 3: 用 podcast-summarizer skill 整理摘要（在 Claude Cowork 中執行）
# → 摘要完成後，Claude 會在末尾輸出「# 疑似辨識錯誤」區塊

# Step 4: 建置網站並推送
cd site && npm run build && cd ..
git add data/ && git commit -m "Daily update: $(Get-Date -Format 'yyyy-MM-dd')" && git push
```

### 兩種下載模式（二擇一）

**模式一：日期區間** — 每個 Podcast 下載從指定日期（含）到今天的所有新集數

```powershell
python scripts/run_all.py --since 2026-05-01
```

**模式二：最新 N 集** — 每個 Podcast **各自**取最新 N 集（預設 5）

```powershell
python scripts/run_all.py --max-episodes 5
```

兩種模式都會自動跳過已在 `processed.json` 中記錄過的集數，不會重複處理。

### 其他常用參數

```powershell
# 只顯示待處理項目，不實際執行（可搭配任一模式）
python scripts/run_all.py --since 2026-05-01 --dry-run
python scripts/run_all.py --max-episodes 5 --dry-run

# 跳過 Whisper 轉錄（只做 RSS 檢查與記錄）
python scripts/run_all.py --max-episodes 5 --skip-transcribe
```

## 逐字稿品質修正（dictionary.json 三層防錯）

Whisper 轉錄中文時容易把公司名稱、半導體術語聽錯。專案用三層機制確保摘要準確：

### Layer 1：確定性替換（preprocess.py）

每次轉錄完成後執行，把 `dictionary.json` 裡的已知錯誤詞直接替換進逐字稿 JSON：

```powershell
python scripts/preprocess.py            # 修正所有有逐字稿的集數
python scripts/preprocess.py --dry-run  # 預覽修正內容，不實際寫入
python scripts/preprocess.py --file data/podcasts/gooaye/gooaye-xxxx.json  # 指定單檔
```

### Layer 2：Claude 語境判斷（podcast-summarizer skill）

skill 執行時會自動讀取 `dictionary.json`，並在摘要末尾輸出「# 疑似辨識錯誤」區塊，列出它在逐字稿中看到的其他疑似 Whisper 錯誤。

### Layer 3：互動式擴充字典（detect_typos.py）

累積幾集摘要後，執行此腳本批量審閱 Claude 的建議，確認後自動寫入 `dictionary.json`：

```powershell
python scripts/detect_typos.py        # 審閱新建議（未在字典中的詞）
python scripts/detect_typos.py --all  # 重新審閱所有建議（含已在字典中的）
```

操作介面會逐條顯示，輸入 `y` 確認、`n` 跳過、或直接輸入自訂修正詞。

### 更新 podcast-summarizer skill

若修改了 `skills/podcast-summarizer/SKILL.md`，需要重新安裝到 Claude：

```powershell
.\scripts\install_skill.ps1
```

### dictionary.json 格式

```json
{
    "錯誤詞": "正確詞",
    "Corex": "CoWoS",
    "歡秋金": "環球晶"
}
```

---

## 新增 Podcast 來源

編輯 `config/sources.yaml`：

```yaml
podcasts:
  - name: "節目中文名稱"
    slug: "url-friendly-name"   # 英文，用於 URL 路徑，例如 my-podcast
    rss_url: "https://..."
    language: "zh"
```

### 如何找到 RSS URL

1. 前往節目的 Apple Podcasts 頁面，通常可在原始碼或第三方工具找到 RSS
2. 使用 [Podcast Index](https://podcastindex.org/) 搜尋節目名稱
3. 許多台灣 Podcast 使用 Firstory：`https://open.firstory.me/rss/user/[id]`
4. Anchor/Spotify 格式：`https://anchor.fm/s/[id]/podcast/rss`

## 更新 Astro 網站設定

編輯 `site/astro.config.mjs`，將 `site` 和 `base` 改為你的 GitHub Pages URL：

```js
export default defineConfig({
  site: "https://YOUR_USERNAME.github.io",
  base: "/YOUR_REPO_NAME",
});
```

## GitHub Pages 部署設定

1. 在 GitHub repo Settings → Pages → Source 選擇 `Deploy from a branch`
2. Branch 選 `main`，資料夾選 `/site/dist`（或先用 `gh-pages` branch）
3. 每次推送 `site/dist/` 後自動更新

> 注意：`site/dist/` 預設在 `.gitignore` 中，需要另外設定 GitHub Actions 或移除忽略。
> 建議做法：使用 `peaceiris/actions-gh-pages` action 或改用 `docs/` 作為發布目錄。

## 未來擴充：FB KOL

當需要新增 Facebook 粉絲專頁追蹤時：

1. 在 `config/sources.yaml` 的 `kols` 區段新增來源
2. 實作 `scripts/check_kols.py`（使用 Facebook Graph API 或 Playwright）
3. 在 `scripts/run_all.py` 加入 KOL 處理步驟
4. 在 Astro 網站新增 `/kols/` 頁面

## 技術說明

- **轉錄模型**：Whisper `small`（中文辨識準確度約 90-95%）
- **摘要方式**：Claude Cowork + podcast-summarizer skill（手動互動）
- **前端**：Astro 4.x 靜態網站，深色主題
- **資料格式**：每集一個 JSON 檔，含元數據、逐字稿、摘要
- **錯誤修正**：三層防錯機制（preprocess.py → skill 語境判斷 → detect_typos.py 擴充字典）
