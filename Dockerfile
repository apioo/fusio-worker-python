FROM python:3.11-alpine
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev
WORKDIR /worker
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 9093
VOLUME /worker/actions
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9093"]
