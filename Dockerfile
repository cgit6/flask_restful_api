# 安裝pytohn3.12
FROM python:3.12  
# port num
EXPOSE 5000
# 
WORKDIR /app
COPY requirements.txt .
# 安裝 flask
RUN pip install -r requirements.txt
# copy everything
COPY . .
CMD ["flask","run","--host","0.0.0.0"]

# 執行的指令，創建一個容器
# docker build -t rest-api-flask-pytohn .
# docker build -t flask-smorest-api .
# 這是執行docker 的命令
# docker run -p 5000:5000 rest-api-flask-pytohn
# docker run -d -p 5000:5000 flask-smorest-api

# 能夠實時更新當前的程式碼
# docker run -dp 5000:5000 -w /app -v "%cd%:/app" flask-smorest-api

