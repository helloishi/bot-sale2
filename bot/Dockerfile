FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#RUN apt-get update
#RUN apt-get install -y build-essential
#RUN apt-get install -y python3-dev
#RUN apt-get install -y swig
#RUN pip install m2crypto
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python", "bot.py"]
