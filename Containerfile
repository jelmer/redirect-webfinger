FROM debian:sid-slim

RUN apt -y update && apt -y install python3-aiohttp
COPY serve.py /serve.py
CMD python3 /serve.py
