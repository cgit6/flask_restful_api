# 安裝pytohn3.12
FROM python:3.12  
# port num
# EXPOSE 5000
# 
WORKDIR /app
COPY requirements.txt .
# 安裝 flask
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# copy everything
COPY . .
CMD ["gunicorn","--bind","0.0.0.0:80","app:create_app()"]


