FROM python:3.11-alpine
WORKDIR /worker
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 9093
VOLUME /worker/actions
CMD ["python", "worker.py"]
