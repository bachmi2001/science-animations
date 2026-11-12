# 國中科學互動動畫教學平台

可直接部署到 GitHub Pages 的繁體中文靜態網站。支援學科分類、即時搜尋、HTML 動畫展示、目錄自動更新。

## 1. 本機預覽

在此資料夾執行：

```powershell
python scripts/build_catalog.py
python -m http.server 8000
```

瀏覽器開啟 http://localhost:8000 。按 Ctrl+C 結束伺服器。

## 2. 發布 GitHub Pages

1. 登入 GitHub，建立 **Public** repository，例如 `science-animations`（不要勾選建立 README）。
2. 把這個資料夾**裡面的所有檔案及資料夾**上傳至儲存庫根目錄（包含 `.github` 隱藏資料夾）。可使用 GitHub 網頁上傳或 Git。
3. 在 repository 的 **Settings → Pages → Build and deployment**，選擇 **Deploy from a branch**、分支 **main**、資料夾 **/(root)**，按 Save。
4. 發布完成後網址通常是 `https://你的GitHub帳號.github.io/science-animations/`。以 GitHub Pages 顯示的實際網址為準。
5. GitHub Actions 工作流程若無權限推送，請在 **Settings → Actions → General → Workflow permissions** 設定 **Read and write permissions**，或自行在本機執行目錄生成後提交 catalog.json。

注意：GitHub Pages 的免費公開儲存庫網站可供所有人瀏覽，勿上傳學生個資、私人資料或未獲授權的內容。

## 3. 新增動畫（自動更新目錄）

**單檔 HTML**：例如 `animations/gear.html`。可加一個同名 `animations/gear.json`，內容如下：

```json
{
  "title": "腳踏車齒輪傳動",
  "category": "physics",
  "topic": "力學",
  "description": "觀察前後齒輪齒數與轉速的關係。",
  "tags": ["齒輪", "腳踏車", "力學"],
  "icon": "⚙️"
}
```

**多檔案動畫**：例如 `animations/bicycle/index.html`、`animations/bicycle/script.js`、`animations/bicycle/style.css`，將 `metadata.json` 放在同一資料夾。

分類代碼：`physics` 物理、`chemistry` 化學、`earth` 地科、`biology` 生物、`math` 數學、`other` 其他。

不提供 JSON 時，程式會從 HTML `<title>` 與路徑推測分類；這是關鍵字分類，不是 AI 語意分類。若要精準，請自行設定 JSON。

在 GitHub 上提交 `animations/` 新檔案後，GitHub Actions 會執行 `scripts/build_catalog.py` 並提交更新後的 `catalog.json`，GitHub Pages 再發布更新。若工作流程未成功，可在本機執行 `python scripts/build_catalog.py` 並提交 `catalog.json`。

**不要直接編輯 `catalog.json`**：它是自動生成的。

## 4. Google Sites 串接

最可靠：Google Sites → 插入 → 按鈕 → 名稱「科學互動動畫」→ 連結貼上 GitHub Pages 公開網址。

如要嵌入：Google Sites → 插入 → 嵌入 → 網址，貼上 GitHub Pages 網址並預覽。若瀏覽器安全政策或顯示大小導致問題，改用按鈕連結。

## 5. 注意

- 網站可直接在 GitHub Pages 執行，無需資料庫或伺服器後端。
- 外部 API、模型檔案或 CDN 依賴的動畫，需要確保資源網址能公開存取。
- 隨附的「三角形內角和」是新製作的示範動畫，不代表先前聊天中製作的原版動畫已經匯入。
