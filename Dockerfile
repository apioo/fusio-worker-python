FROM python:3.8-alpine
WORKDIR /worker
RUN pip install --no-cache-dir PyMySQL thrift
COPY . .
EXPOSE 9093
VOLUME /worker/actions
CMD ["worker.py"]
ENTRYPOINT ["python3"]
