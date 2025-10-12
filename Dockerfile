FROM python:3.12

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
CMD ["python", "main.py"]