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
