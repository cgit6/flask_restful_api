## 如何在本地端運行 dockfile

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"
```

執行的指令，創建一個容器
docker build -t rest-api-flask-pytohn .
docker build -t flask-smorest-api .
這是執行 docker 的命令
docker run -p 5000:5000 rest-api-flask-pytohn
docker run -d -p 5000:5000 flask-smorest-api
能夠實時更新當前的程式碼
docker run -dp 5000:5000 -w /app -v "%cd%:/app" flask-smorest-api

## docker-compose

指定了使用 Docker Compose 檔案格式的版本

```
version: "3"
services:
  # 服務名稱
  web:
    build: . # 當前位置
    ports:
      - "5000:5000"
    volumes:
      - .:/app # 🤔這行設定了一個卷映射

# 執行命令
# docker compose up
```

### 如何在 compose 容器中執行資料庫遷移

在上一個影片中，我們使用 Docker Compose 運行我們的應用程式和資料庫。

但是我們的資料庫將為空，因為我們還沒有運行創建表的 flask db 升級命令。

要運行該命令，您應該：

- 首先使用 docker compose up -d 來執行 compose 文件

- 然後使用 docker compose exec webflask dbupgrade 執行資料庫升級指令。

在接下來的幾個講座中，我還將向您展示如何在啟動容器時自動執行此操作，因此您永遠不會在不運行資料庫遷移的情況下運行容器。

# 使用資料庫用戶端連線到 Docker Compose 資料庫

Hello!

如果您正在使用 Docker Compose，並且想要使用 DBeaver 等資料庫用戶端連線到資料庫，請依照下列步驟操作。很簡單！

在 docker-compose.yml 檔案中開啟端口
首先，在您的資料庫服務中，新增以下兩行：

"""
ports: - "5432:5432"
"""
這將使存取本機電腦中的連接埠 5432 將存取資料庫容器中的連接埠 5432。

重新建立映像
然後，使用以下命令重新建立資料庫映像：

"""
docker compose up --build --force-recreate --no-deps db
"""

與資料庫客戶端連接
最後，使用資料庫用戶端建立到以下 URL 的新連線：

postgresql://postgres:postgres@localhost:5432/myapp
Note the details used are:

Database user: postgres

Database password: postgres

Database host: localhost

Database port: 5432 (this is the port in your local machine)

Database name: myapp

如果您使用了不同的詳細信息，請相應地調整 URL。

就是這樣！現在，您將透過資料庫用戶端連接到 Docker Compose 資料庫！
