FROM registry.access.redhat.com/ubi9/python-311:latest

WORKDIR /opt/app-root/src
COPY server.py .

ENV PORT=8080
EXPOSE 8080

CMD ["python", "server.py"]