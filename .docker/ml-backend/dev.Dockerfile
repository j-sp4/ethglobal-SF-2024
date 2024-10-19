FROM python:3.9

WORKDIR /app

COPY ./ml-backend/requirements.txt .
RUN pip install -r requirements.txt

COPY ./ml-backend .

CMD uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT