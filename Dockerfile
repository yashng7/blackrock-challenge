# docker build --no-cache -t blk-hacking-ind-yashwant-gawande .
# OS: Debian Linux (python:3.12-slim) — lightweight, minimal attack surface, optimized for containerized microservices
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY test/ ./test/
COPY pytest.ini .

EXPOSE 5477

CMD ["python", "-m", "app.main"]