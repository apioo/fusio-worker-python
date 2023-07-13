FROM python:3.11-alpine
WORKDIR /worker
COPY . .
RUN pip install --no-cache-dir
EXPOSE 9093
VOLUME /worker/actions
CMD ["worker.py"]
ENTRYPOINT ["python3"]
