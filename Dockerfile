FROM debian:sid-slim

COPY . .
RUN apt -y update && apt -y install --no-install-recommends python3-pip && pip3 install .
ENTRYPOINT ["python3", "-m", "redirect_webfinger"]
