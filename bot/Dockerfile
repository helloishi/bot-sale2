FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
    build-essential \
    swig \
    libssl-dev \
    python3-dev \
    && apt-get clean
RUN pip install m2crypto
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python", "bot.py"]
