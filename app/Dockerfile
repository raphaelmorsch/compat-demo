FROM python:3.11-slim

WORKDIR /opt/app
COPY server.py .

RUN apt-get update && apt-get install -y --no-install-recommends \
      iputils-ping \
      iproute2 \
      net-tools \
      dnsutils \
      netcat-openbsd \
      traceroute \
      tcpdump \
      procps \
    && rm -rf /var/lib/apt/lists/*

ENV PORT=8080
EXPOSE 8080
CMD ["python", "server.py"]