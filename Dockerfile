FROM python:3.8-alpine
WORKDIR /app
RUN pip install --no-cache-dir PyMySQL thrift
COPY . .
EXPOSE 9093
CMD ["worker.py"]
ENTRYPOINT ["python3"]
