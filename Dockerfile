FROM python:3.12-alpine

COPY requirements.txt .
RUN apt-get update
RUN apt-get install libzbar0 -y
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --user -r requirements.txt
WORKDIR /app
COPY src ./src
COPY models ./models
COPY static ./static
COPY tasks ./tasks
COPY templates ./templates
COPY main.py .
COPY celery.sh .
CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]