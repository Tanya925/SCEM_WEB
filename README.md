# SCEM 網站專案

這個專案包含目前的 SCEM 網站，以及用來同步 Scopus 論文與 h-index 的自動化流程。

目前專案主要分成兩個部分：

- `網站主程式`
  - 包含前台頁面與後台管理介面
- `Scopus 同步功能`
  - 透過 Scopus / SciVal API 與 `Flask-APScheduler`，自動更新教師 h-index 與論文資料

---

## 1. 重要檔案

- `app.py`
  - Flask 應用程式主入口
- `services/scopus_sync_service.py`
  - 負責呼叫 Scopus API 並同步 h-index 與論文資料
- `services/scopus_scheduler.py`
  - 啟動 `Flask-APScheduler`，定期執行 Scopus 同步工作
- `database/`
  - 資料庫存取函式與啟動時的資料表補齊邏輯
- `routes/`
  - 前台、登入、後台與論文 API 路由
- `templates/`
  - HTML 模板檔
- `static/`
  - CSS、JavaScript、圖片、音訊、PDF 與上傳資源
- `schema.sql`
  - 初始化空資料庫用的資料表結構與預設資料
- `scem.db`
  - 目前使用中的 SQLite 資料庫
- `.env`
  - 本機環境設定，例如 `SECRET_KEY`、`SCOPUS_API_KEY` 與排程參數
- `Dockerfile`
  - 使用 `gunicorn` 啟動網站的 Docker 建置設定
- `docker-compose.yml`
  - Docker 執行設定，包含連接埠、`.env`、`scem.db` 與 `static/uploads`

---

## 2. 環境設定

### 2.1 安裝套件

```powershell
pip install -r requirements.txt
```

本專案主要使用的套件如下：

- `Flask`
- `Flask-APScheduler`
- `python-dotenv`
- `gunicorn`

### 2.2 設定 `.env`

請在專案根目錄建立 `.env` 檔案：

```env
SECRET_KEY=請替換成你自己的密鑰
SCOPUS_API_KEY=請填入你的 Scopus API 金鑰
SCOPUS_SYNC_INTERVAL_MINUTES=1440
WEB_CONCURRENCY=1
```

欄位說明：

- `SECRET_KEY`
  - Flask session 使用的密鑰
- `SCOPUS_API_KEY`
  - Scopus / SciVal API 使用的金鑰
- `SCOPUS_SYNC_INTERVAL_MINUTES`
  - 自動同步工作的執行間隔，單位為分鐘
- `WEB_CONCURRENCY`
  - 網站 worker 數量。若排程仍與網站跑在同一個 process，請維持 `1`

---

## 3. 啟動網站

### 3.1 本機啟動

```powershell
python app.py
```

預設本機網址：

```text
http://127.0.0.1:3000
```

常見啟動輸出：

```text
Scopus 排程器已啟動。
SQLite 資料庫連線成功。
目前這個程序中的 Scopus 排程器正在執行。
```

### 3.2 使用 Docker 啟動

建置映像：

```powershell
docker compose build
```

啟動容器：

```powershell
docker compose up -d
```

如果你修改了 Python、模板或 CSS，因為整個專案目錄沒有完整掛載進容器，所以建議重新建置後再啟動：

```powershell
docker compose down
docker compose build --no-cache
docker compose up -d
```

Docker 目前會保留：

- `scem.db`
- `static/uploads`

---

## 4. 網站結構

### 4.1 前台頁面

- `/`
  - 首頁
- `/staff`
  - 團隊成員頁
- `/research`
  - 研究計畫頁
- `/publications`
  - 論文頁
- `/project/<id>`
  - 單一進行中計畫的詳細頁
- `/api/publications`
  - 論文頁使用的 JSON API

### 4.2 後台頁面

目前所有後台頁面都在：

```text
/0630_SCEMadmin
```

可用的後台頁面如下：

- `/0630_SCEMadmin/login`
  - 管理員登入頁
- `/0630_SCEMadmin/dashboard`
  - 管理首頁
- `/0630_SCEMadmin/general-info`
  - 首頁文字與活動圖片管理
- `/0630_SCEMadmin/staff`
  - 團隊成員資料管理
- `/0630_SCEMadmin/projects`
  - 研究計畫管理
- `/0630_SCEMadmin/passwords`
  - 管理員帳號與密碼設定

目前系統只支援單一管理員帳號。

---

## 5. 管理員登入與帳密調整

資料庫第一次建立時，系統會先建立一組內建管理員帳號。

如果之後要修改登入帳號或密碼，可直接到：

- `/0630_SCEMadmin/passwords`

調整規則如下：

- 新帳號不得與現有帳號重複
- 儲存前必須先輸入目前密碼
- 新密碼至少要 8 個字元
- 新密碼不得與目前密碼相同

---

## 6. Scopus 同步流程

舊版的瀏覽器爬蟲、人工論文審核流程，以及手動同步頁面都已經移除。

目前同步流程如下：

1. 讀取所有有填寫 `scopus_author_id` 的教師資料
2. 呼叫 Scopus / SciVal API
3. 更新 `staff.scopus_hindex`
4. 更新 `staff.scopus_hindex_updated_at`
5. 匯入 2020 年以後的論文
6. 依 `scopus_eid` 去重
7. 將結果寫入 `publications` 資料表
8. 更新 `publications.scopus_last_updated_at`

### 6.1 排程行為

網站成功啟動後，排程器會自動啟動。

執行間隔由 `SCOPUS_SYNC_INTERVAL_MINUTES` 控制。

系統保留多 worker 防呆機制：

- 當 `WEB_CONCURRENCY > 1`
  - 預設不啟動排程器
- 這樣可以避免多個 worker 同時重複執行同步

### 6.2 論文連結選擇規則

前台顯示每篇論文時，會依照以下順序選擇連結：

1. DOI 網址
2. Scopus 網址
3. API 回傳的備援網址

如果資料庫原本已經有較好的非 Scopus 連結，同步邏輯會盡量保留。

---

## 7. 資料庫備註

目前主要使用的資料表：

- `users`
  - 管理員帳號資料
- `general_info`
  - 首頁文字內容
- `home_activity_images`
  - 首頁活動圖片
- `staff`
  - 團隊成員資料，包含 Scopus Author ID 與 h-index
- `research_projects`
  - 研究計畫資料
- `publications`
  - 由 Scopus 同步而來的公開論文資料

其他說明：

- `finished` 類型的研究計畫目前只在前台列表顯示
- 實務上 `finished` 計畫仍會保留標題與年份供前台展示與搜尋
- 目前只有 `ongoing` 類型的計畫提供前台詳細頁

重要的 Scopus 相關欄位：

- `staff.scopus_author_id`
- `staff.scopus_hindex`
- `staff.scopus_hindex_updated_at`
- `publications.scopus_eid`
- `publications.scopus_last_updated_at`

目前程式假設資料庫已使用現行結構：

- `users` 採用單一管理員模式
- `publications` 使用 `scopus_eid` 與 `scopus_last_updated_at` 作為同步識別與更新依據

---

## 8. 目前維護範圍

目前仍需在後台手動維護：

- 首頁內容
- 團隊成員資料
- 研究計畫資料
- 上傳圖片與相關靜態檔案

目前由系統自動維護：

- 教師 h-index
- 2020 年以後的論文資料

目前已不再屬於本專案的功能：

- Playwright 爬蟲
- Windows 工作排程 `.bat` 腳本
- 教師 / 研究人員分帳號登入
- 論文申請與審核流程
- 手動論文管理頁
