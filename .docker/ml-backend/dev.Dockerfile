FROM python:3.10

WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

COPY ./ml-backend/requirements.txt .

RUN pip install -r requirements.txt

COPY ./ml-backend .

CMD uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT --reload
