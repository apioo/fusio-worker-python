FROM python:3.11-alpine
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /worker
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 9093
VOLUME /worker/actions
CMD ["python", "worker.py"]
