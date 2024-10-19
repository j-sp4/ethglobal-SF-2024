FROM python:3.9

WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

COPY ./ml-backend/requirements.txt .
COPY ./ml-backend/roop/requirements.txt ./roop/

RUN pip install -r requirements.txt
RUN pip install -r roop/requirements.txt

COPY ./ml-backend .

CMD uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT
