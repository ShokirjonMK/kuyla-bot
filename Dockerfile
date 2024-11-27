
FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY requirements.txt requirements.txt
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8048", "main:app"]
