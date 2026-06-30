FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --default-timeout=300 --no-cache-dir -r requirements.txt

COPY . .

CMD ["python"]