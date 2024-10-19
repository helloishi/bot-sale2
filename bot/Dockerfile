FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
    build-essential \
    swig \
    libssl-dev \
    python3-dev \
    git \
    && apt-get clean
RUN pip install m2crypto
RUN git clone https://github.com/devartis/passbook.git /app/cards/
COPY . .
#RUN mkdir -p /app/wallet_cards
ENV PYTHONUNBUFFERED=1
CMD ["python", "bot.py"]
